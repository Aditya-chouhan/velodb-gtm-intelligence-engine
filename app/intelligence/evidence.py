from __future__ import annotations

from typing import Dict, List

ALLOWED_TYPES = {"observed", "hypothesis"}


def validate_evidence(evidence: List[Dict]) -> dict:
    """Validate evidence quality without promoting inference into fact.

    Outreach readiness is intentionally conservative: at least two observed claims,
    every observed claim sourced, and at least two distinct source URLs.
    """
    invalid = [e for e in evidence if e.get("type") not in ALLOWED_TYPES]
    observed = [e for e in evidence if e.get("type") == "observed"]
    hypotheses = [e for e in evidence if e.get("type") == "hypothesis"]
    sourced = [e for e in observed if e.get("source")]
    unique_sources = {e.get("source") for e in sourced if e.get("source")}
    missing_source_count = len(observed) - len(sourced)
    source_coverage = len(sourced) / max(1, len(observed))

    issues: list[str] = []
    if invalid:
        issues.append("unsupported evidence type present")
    if missing_source_count:
        issues.append(f"{missing_source_count} observed claim(s) missing a source")
    if observed and len(unique_sources) < min(2, len(observed)):
        issues.append("observed claims lack independent-source diversity")
    if len(observed) < 2:
        issues.append("fewer than two observed claims")

    ready = (
        not invalid
        and len(observed) >= 2
        and source_coverage == 1.0
        and len(unique_sources) >= 2
    )

    return {
        "observed_count": len(observed),
        "hypothesis_count": len(hypotheses),
        "invalid_count": len(invalid),
        "missing_source_count": missing_source_count,
        "unique_source_count": len(unique_sources),
        "source_coverage": round(source_coverage, 2),
        "issues": issues,
        "ready_for_outreach": ready,
    }
