from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence

SCORING_VERSION = "2.0.0"


@dataclass(frozen=True)
class SignalRule:
    key: str
    label: str
    points: int
    dimension: str
    rationale: str


RULES: Dict[str, SignalRule] = {
    "clickhouse": SignalRule("clickhouse", "ClickHouse detected", 18, "fit", "Strong competitive/workload relevance; not proof of pain."),
    "elasticsearch": SignalRule("elasticsearch", "Elasticsearch/OpenSearch detected", 16, "fit", "Relevant observability/search workload."),
    "loki": SignalRule("loki", "Loki detected", 15, "fit", "Relevant log-analytics workload."),
    "trino_hive": SignalRule("trino_hive", "Trino/Presto/Hive detected", 14, "fit", "Relevant lakehouse/serving workload."),
    "kafka_flink": SignalRule("kafka_flink", "Kafka/Flink detected", 9, "fit", "Real-time pipeline relevance."),
    "realtime_product": SignalRule("realtime_product", "Real-time analytics product", 14, "fit", "Direct workload fit for low-latency analytics."),
    "customer_dashboards": SignalRule("customer_dashboards", "Customer-facing dashboards", 10, "fit", "Potential concurrency/latency sensitivity."),
    "ai_context": SignalRule("ai_context", "AI/RAG/agent infrastructure", 14, "fit", "Potential context/agent-observability motion."),
    "large_scale": SignalRule("large_scale", "Large / fast-growing data scale", 9, "fit", "Scale increases technical relevance."),
    "fragmented_stack": SignalRule("fragmented_stack", "Multiple analytical systems", 12, "pain", "Potential consolidation complexity, subject to discovery."),
    "data_platform_hiring": SignalRule("data_platform_hiring", "Data-platform hiring", 12, "timing", "Active infrastructure investment signal."),
    "clickhouse_hiring": SignalRule("clickhouse_hiring", "Hiring for ClickHouse experience", 15, "timing", "Strong stack + timing evidence."),
    "recent_growth": SignalRule("recent_growth", "Recent funding / rapid growth", 8, "timing", "Possible budget/timing signal."),
}

COMMERCIAL_SIGNAL_POINTS = {
    "enterprise_domain": 6,
    "technical_fit": 8,
    "oss_activity": 4,
    "docs_interest": 5,
    "trial_started": 12,
    "data_loaded": 14,
    "repeat_queries": 12,
    "multi_user": 10,
    "integration_connected": 10,
}

COUNTER_SIGNAL_POINTS = {
    "incumbent_meeting_requirements": 14,
    "recent_successful_migration_to_incumbent": 16,
    "deep_incumbent_investment": 10,
    "no_observed_pain": 8,
    "stale_evidence": 8,
}

DIMENSION_CAPS = {"fit": 40, "pain": 20, "timing": 15, "intent": 15, "evidence": 10}


def _bounded(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def evidence_score(evidence: Sequence[Mapping]) -> dict:
    observed = [e for e in evidence if e.get("type") == "observed"]
    hypotheses = [e for e in evidence if e.get("type") == "hypothesis"]
    sourced = [e for e in observed if e.get("source")]
    source_coverage = len(sourced) / max(1, len(observed))
    corroboration = min(1.0, len({e.get("source") for e in sourced if e.get("source")}) / 3)
    score = round(10 * (0.65 * source_coverage + 0.35 * corroboration), 1) if observed else 0.0
    return {
        "score": score,
        "observed_count": len(observed),
        "hypothesis_count": len(hypotheses),
        "source_coverage": round(source_coverage, 2),
        "independent_source_factor": round(corroboration, 2),
    }


def score_signals(
    signal_keys: Iterable[str],
    *,
    evidence: Sequence[Mapping] | None = None,
    commercial_signal_keys: Iterable[str] | None = None,
    counter_signal_keys: Iterable[str] | None = None,
) -> dict:
    keys = list(dict.fromkeys(signal_keys))
    matched: List[SignalRule] = [RULES[k] for k in keys if k in RULES]

    fit_raw = sum(r.points for r in matched if r.dimension == "fit")
    pain_raw = sum(r.points for r in matched if r.dimension == "pain")
    timing_raw = sum(r.points for r in matched if r.dimension == "timing")

    commercial_keys = list(dict.fromkeys(commercial_signal_keys or []))
    intent_raw = sum(COMMERCIAL_SIGNAL_POINTS.get(k, 0) for k in commercial_keys)

    evidence_meta = evidence_score(evidence or [])
    counter_keys = list(dict.fromkeys(counter_signal_keys or []))
    counter_penalty = sum(COUNTER_SIGNAL_POINTS.get(k, 0) for k in counter_keys)

    dimensions = {
        "technical_fit": min(fit_raw, DIMENSION_CAPS["fit"]),
        "pain_evidence": min(pain_raw, DIMENSION_CAPS["pain"]),
        "timing": min(timing_raw, DIMENSION_CAPS["timing"]),
        "intent": min(intent_raw, DIMENSION_CAPS["intent"]),
        "evidence_quality": min(evidence_meta["score"], DIMENSION_CAPS["evidence"]),
    }

    gross = sum(dimensions.values())
    score = round(_bounded(gross - counter_penalty), 1)

    # Confidence reflects evidence quality and independent corroboration, not signal count.
    confidence = round(
        _bounded(
            0.2
            + 0.45 * evidence_meta["source_coverage"]
            + 0.25 * evidence_meta["independent_source_factor"]
            + (0.1 if evidence_meta["observed_count"] >= 2 else 0),
            0,
            0.95,
        ),
        2,
    )

    return {
        "scoring_version": SCORING_VERSION,
        "score": score,
        "gross_score": round(gross, 1),
        "counter_signal_penalty": counter_penalty,
        "confidence": confidence,
        "dimensions": dimensions,
        "evidence_meta": evidence_meta,
        "matched_rules": [r.__dict__ for r in matched],
        "matched_commercial_signals": [k for k in commercial_keys if k in COMMERCIAL_SIGNAL_POINTS],
        "matched_counter_signals": [k for k in counter_keys if k in COUNTER_SIGNAL_POINTS],
    }


def priority_band(score: float) -> str:
    if score >= 75:
        return "P1 - investigate now"
    if score >= 55:
        return "P2 - qualified research"
    if score >= 35:
        return "P3 - monitor / educate"
    return "P4 - low current priority"
