from typing import Dict

def build_strategy(account: Dict, scoring: Dict, opportunity: Dict) -> Dict:
    observed = [e["claim"] for e in account.get("evidence", []) if e.get("type") == "observed"]
    hypotheses = [e["claim"] for e in account.get("evidence", []) if e.get("type") == "hypothesis"]
    pain = hypotheses[0] if hypotheses else "Analytical latency, concurrency, cost, or stack complexity deserves validation."
    return {"why_now": observed[:4], "technical_pain_hypothesis": pain, "recommended_motion": opportunity["motion"], "talk_track": opportunity["angle"], "priority": scoring["score"]}
