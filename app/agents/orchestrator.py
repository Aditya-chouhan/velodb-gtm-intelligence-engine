from typing import Dict

from app.scoring.scoring import score_signals, priority_band
from app.intelligence.opportunity_mapper import map_opportunity
from app.intelligence.evidence import validate_evidence
from app.intelligence.poc_planner import build_poc
from app.intelligence.commercialization import score_commercialization
from app.agents.strategist import build_strategy
from app.agents.personalization import generate_outreach


def analyze_account(account: Dict) -> Dict:
    signals = account.get("signals", [])
    scoring = score_signals(signals)
    opportunity = map_opportunity(signals)
    evidence_quality = validate_evidence(account.get("evidence", []))
    strategy = build_strategy(account, scoring, opportunity)
    poc_plan = build_poc(signals, opportunity["motion"])
    commercialization = score_commercialization(account.get("commercial_signals", []))
    outreach = generate_outreach(account, strategy)

    return {
        **account,
        "score": scoring["score"],
        "score_confidence": scoring["confidence"],
        "priority_band": priority_band(scoring["score"]),
        "matched_rules": scoring["matched_rules"],
        "opportunity": opportunity,
        "evidence_quality": evidence_quality,
        "commercialization": commercialization,
        "strategy": strategy,
        "poc_plan": poc_plan,
        "outreach": outreach,
    }
