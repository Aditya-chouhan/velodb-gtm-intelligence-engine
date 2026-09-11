from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.collectors.public_web import fetch_public_page

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "real_target_accounts.json"
OUTPUT = ROOT / "data" / "public_signal_receipt.json"
KEYWORDS = [
    "ClickHouse", "Kafka", "Flink", "Trino", "Hive", "Hudi", "real-time",
    "analytics", "data platform", "Metabase", "Superset", "events", "scale",
]


def unique_sources(accounts: list[dict]) -> list[str]:
    return sorted({
        item["source"]
        for account in accounts
        for item in account.get("evidence", [])
        if item.get("type") == "observed" and item.get("source")
    })


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh public-source reachability and keyword receipts.")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if fewer than half of sources are reachable.")
    args = parser.parse_args()

    accounts = json.loads(INPUT.read_text())
    sources = unique_sources(accounts)
    receipts = [fetch_public_page(url, KEYWORDS) for url in sources]
    ok = [row for row in receipts if row["error"] is None and row["status"] and row["status"] < 400]
    payload = {
        "classification": "live_public_web_receipt",
        "what_it_proves": "Configured public evidence URLs were reachable and disclosed keywords appeared at refresh time.",
        "what_it_does_not_prove": "Production usage beyond the cited text, purchase intent, current pain, evaluation status, pipeline, or revenue.",
        "source_count": len(sources),
        "reachable_count": len(ok),
        "sources": receipts,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"source_count": len(sources), "reachable_count": len(ok), "output": str(OUTPUT)}, indent=2))

    if args.check and len(ok) < max(1, (len(sources) + 1) // 2):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
