from typing import Dict

from app.scoring.scoring import priority_band, score_signals
from app.intelligence.opportunity_mapper import map_opportunity
from app.intelligence.evidence import validate_evidence
from app.intelligence.poc_planner import build_poc
from app.intelligence.commercialization import score_commercialization
from app.agents.strategist import build_strategy
from app.agents.personalization import generate_outreach


def analyze_account(account: Dict) -> Dict:
    signals = account.get("signals", [])
    commercial_signals = account.get("commercial_signals", [])
    counter_signals = account.get("counter_signals", [])
    evidence = account.get("evidence", [])

    scoring = score_signals(
        signals,
        evidence=evidence,
        commercial_signal_keys=commercial_signals,
        counter_signal_keys=counter_signals,
    )
    opportunity = map_opportunity(signals)
    evidence_quality = validate_evidence(evidence)
    strategy = build_strategy(account, scoring, opportunity)
    poc_plan = build_poc(signals, opportunity["motion"])
    commercialization = score_commercialization(commercial_signals)
    outreach = generate_outreach(account, strategy)

    return {
        **account,
        "score": scoring["score"],
        "gross_score": scoring["gross_score"],
        "counter_signal_penalty": scoring["counter_signal_penalty"],
        "score_dimensions": scoring["dimensions"],
        "scoring_version": scoring["scoring_version"],
        "score_confidence": scoring["confidence"],
        "priority_band": priority_band(scoring["score"]),
        "matched_rules": scoring["matched_rules"],
        "matched_counter_signals": scoring["matched_counter_signals"],
        "opportunity": opportunity,
        "evidence_quality": evidence_quality,
        "commercialization": commercialization,
        "strategy": strategy,
        "poc_plan": poc_plan,
        "outreach": outreach,
    }
