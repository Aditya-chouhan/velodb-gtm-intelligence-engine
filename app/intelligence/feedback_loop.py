from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Dict


OUTCOME_VALUES = {
    "no_reply": 0.0,
    "reply": 0.15,
    "meeting": 0.35,
    "poc": 0.60,
    "opportunity": 0.80,
    "won": 1.00,
    "lost": 0.05,
}


def summarize_outcomes(events: Iterable[dict]) -> dict:
    by_signal: Dict[str, list[float]] = defaultdict(list)
    counts = defaultdict(int)
    for event in events:
        outcome = event.get("outcome", "no_reply")
        value = OUTCOME_VALUES.get(outcome, 0.0)
        counts[outcome] += 1
        for signal in event.get("signals", []):
            by_signal[signal].append(value)

    signal_performance = []
    for signal, values in by_signal.items():
        signal_performance.append({
            "signal": signal,
            "samples": len(values),
            "mean_outcome_value": round(sum(values) / len(values), 3),
        })
    signal_performance.sort(key=lambda row: (row["mean_outcome_value"], row["samples"]), reverse=True)

    return {
        "outcome_counts": dict(counts),
        "signal_performance": signal_performance,
        "guardrail": "This diagnostic does not automatically rewrite production scoring weights. Re-weighting requires sufficient samples, holdout evaluation, and human approval.",
    }
