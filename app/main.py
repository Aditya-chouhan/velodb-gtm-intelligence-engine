from __future__ import annotations
import json
from pathlib import Path
from app.agents.orchestrator import analyze_account

def load_demo_accounts():
    path = Path(__file__).resolve().parents[1] / "data" / "demo_accounts.json"
    return json.loads(path.read_text())

def run():
    results = [analyze_account(a) for a in load_demo_accounts()]
    for item in sorted(results, key=lambda x: x["score"], reverse=True):
        print(f"{item['company']}: {item['score']}/100 — {item['priority_band']}")
        print(f"  Motion: {item['opportunity']['motion']}")
        print(f"  Outreach-ready: {item['evidence_quality']['ready_for_outreach']}")

if __name__ == "__main__":
    run()
