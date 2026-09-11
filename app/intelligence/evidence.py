from typing import List, Dict

def validate_evidence(evidence: List[Dict]) -> dict:
    observed = [e for e in evidence if e.get("type") == "observed"]
    hypotheses = [e for e in evidence if e.get("type") == "hypothesis"]
    sourced = [e for e in observed if e.get("source")]
    coverage = round(len(sourced) / max(1, len(observed)), 2)
    return {"observed_count": len(observed), "hypothesis_count": len(hypotheses), "source_coverage": coverage, "ready_for_outreach": len(observed) >= 2 and coverage >= 0.8}
