from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.agents.orchestrator import analyze_account

ROOT = Path(__file__).resolve().parents[1]
DATASETS = {
    "demo": ROOT / "data" / "demo_accounts.json",
    "public": ROOT / "data" / "real_target_accounts.json",
}


def load_accounts(dataset: str = "demo") -> list[dict]:
    return json.loads(DATASETS[dataset].read_text())


def run(dataset: str = "demo") -> None:
    results = [analyze_account(a) for a in load_accounts(dataset)]
    print(f"dataset={dataset} accounts={len(results)}")
    if dataset == "public":
        print("boundary: public technical evidence is not buying intent or proof of pain")
    for item in sorted(results, key=lambda x: x["score"], reverse=True):
        print(f"{item['company']}: {item['score']}/100 — {item['priority_band']}")
        print(f"  Motion: {item['opportunity']['motion']}")
        print(f"  Outreach-ready evidence gate: {item['evidence_quality']['ready_for_outreach']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=DATASETS, default="demo")
    args = parser.parse_args()
    run(args.dataset)


if __name__ == "__main__":
    main()
