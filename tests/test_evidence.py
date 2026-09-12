from app.intelligence.evidence import validate_evidence


def test_two_independent_sourced_observations_pass_gate():
    result = validate_evidence([
        {"type": "observed", "claim": "A", "source": "https://example.com/a"},
        {"type": "observed", "claim": "B", "source": "https://example.com/b"},
        {"type": "hypothesis", "claim": "Possible pain"},
    ])
    assert result["ready_for_outreach"] is True
    assert result["source_coverage"] == 1.0
    assert result["unique_source_count"] == 2


def test_duplicate_source_does_not_count_as_independent_corroboration():
    result = validate_evidence([
        {"type": "observed", "claim": "A", "source": "https://example.com/a"},
        {"type": "observed", "claim": "B", "source": "https://example.com/a"},
    ])
    assert result["ready_for_outreach"] is False
    assert "independent-source diversity" in " ".join(result["issues"])


def test_unsourced_observation_fails_gate():
    result = validate_evidence([
        {"type": "observed", "claim": "A", "source": "https://example.com/a"},
        {"type": "observed", "claim": "B"},
    ])
    assert result["ready_for_outreach"] is False
    assert result["missing_source_count"] == 1


def test_unsupported_evidence_type_is_visible():
    result = validate_evidence([
        {"type": "fact", "claim": "A", "source": "https://example.com/a"},
        {"type": "observed", "claim": "B", "source": "https://example.com/b"},
    ])
    assert result["invalid_count"] == 1
    assert result["ready_for_outreach"] is False
