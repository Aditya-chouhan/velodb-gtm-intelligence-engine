from typing import Dict
from app.scoring.scoring import score_signals, priority_band
from app.intelligence.opportunity_mapper import map_opportunity
from app.intelligence.evidence import validate_evidence
from app.agents.strategist import build_strategy
from app.agents.personalization import generate_outreach

def analyze_account(account: Dict) -> Dict:
    scoring = score_signals(account.get("signals", []))
    opportunity = map_opportunity(account.get("signals", []))
    evidence_quality = validate_evidence(account.get("evidence", []))
    strategy = build_strategy(account, scoring, opportunity)
    outreach = generate_outreach(account, strategy)
    return {**account, "score": scoring["score"], "score_confidence": scoring["confidence"], "priority_band": priority_band(scoring["score"]), "matched_rules": scoring["matched_rules"], "opportunity": opportunity, "evidence_quality": evidence_quality, "strategy": strategy, "outreach": outreach}
