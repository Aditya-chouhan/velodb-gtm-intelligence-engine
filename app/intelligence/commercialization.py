from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Dict


@dataclass(frozen=True)
class CommercialSignal:
    key: str
    points: int
    meaning: str


COMMERCIAL_SIGNALS: Dict[str, CommercialSignal] = {
    "oss_activity": CommercialSignal("oss_activity", 10, "Public Apache Doris / related ecosystem activity"),
    "docs_interest": CommercialSignal("docs_interest", 8, "Technical education or documentation engagement"),
    "trial_started": CommercialSignal("trial_started", 15, "Product evaluation has begun"),
    "data_loaded": CommercialSignal("data_loaded", 15, "Trial reached meaningful workload setup"),
    "repeat_queries": CommercialSignal("repeat_queries", 12, "Sustained product usage rather than one-off exploration"),
    "multi_user": CommercialSignal("multi_user", 10, "Evaluation is spreading beyond one individual"),
    "integration_connected": CommercialSignal("integration_connected", 10, "User connected surrounding data infrastructure"),
    "enterprise_domain": CommercialSignal("enterprise_domain", 10, "Account has plausible commercial capacity"),
    "technical_fit": CommercialSignal("technical_fit", 15, "Observed workload aligns with a VeloDB motion"),
}


def score_commercialization(signal_keys: Iterable[str]) -> dict:
    matched = [COMMERCIAL_SIGNALS[k] for k in signal_keys if k in COMMERCIAL_SIGNALS]
    raw = sum(item.points for item in matched)
    score = min(raw, 100)
    if score >= 75:
        stage = "sales-ready PQL"
    elif score >= 50:
        stage = "high-intent evaluation"
    elif score >= 25:
        stage = "nurture / technical education"
    else:
        stage = "community / low commercial intent"
    return {
        "score": score,
        "stage": stage,
        "matched_signals": [item.__dict__ for item in matched],
        "note": "Internal product/engagement signals must only be used with authorization. Public demo inputs should remain fictional or explicitly public.",
    }
