from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "scoring_v2.json"
_CONFIG = json.loads(CONFIG_PATH.read_text())
SCORING_VERSION = _CONFIG["version"]


@dataclass(frozen=True)
class SignalRule:
    key: str
    label: str
    points: int
    dimension: str
    rationale: str


RULES: Dict[str, SignalRule] = {
    key: SignalRule(
        key=key,
        label=value["label"],
        points=value["points"],
        dimension=value["dimension"],
        rationale=value["rationale"],
    )
    for key, value in _CONFIG["signal_rules"].items()
}

COMMERCIAL_SIGNAL_POINTS = _CONFIG["commercial_signal_points"]
COUNTER_SIGNAL_POINTS = _CONFIG["counter_signal_points"]
DIMENSION_CAPS = _CONFIG["dimension_caps"]


def _bounded(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def evidence_score(evidence: Sequence[Mapping]) -> dict:
    observed = [e for e in evidence if e.get("type") == "observed"]
    hypotheses = [e for e in evidence if e.get("type") == "hypothesis"]
    sourced = [e for e in observed if e.get("source")]
    source_coverage = len(sourced) / max(1, len(observed))
    unique_sources = {e.get("source") for e in sourced if e.get("source")}
    corroboration = min(1.0, len(unique_sources) / 3)
    score = round(10 * (0.65 * source_coverage + 0.35 * corroboration), 1) if observed else 0.0
    return {
        "score": score,
        "observed_count": len(observed),
        "hypothesis_count": len(hypotheses),
        "source_coverage": round(source_coverage, 2),
        "independent_source_factor": round(corroboration, 2),
        "unique_source_count": len(unique_sources),
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

    # Confidence reflects evidence quality and corroboration, not signal volume.
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
        "unknown_signals": [k for k in keys if k not in RULES],
    }


def priority_band(score: float) -> str:
    if score >= 75:
        return "P1 - investigate now"
    if score >= 55:
        return "P2 - qualified research"
    if score >= 35:
        return "P3 - monitor / educate"
    return "P4 - low current priority"
