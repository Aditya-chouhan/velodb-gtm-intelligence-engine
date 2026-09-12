from app.scoring.scoring import SCORING_VERSION, priority_band, score_signals


def observed(claim: str, source: str) -> dict:
    return {"type": "observed", "claim": claim, "source": source}


def test_scoring_is_multidimensional_and_versioned():
    result = score_signals(
        ["clickhouse", "realtime_product", "large_scale", "data_platform_hiring"],
        evidence=[
            observed("Uses ClickHouse", "https://example.com/a"),
            observed("Runs real-time analytics", "https://example.com/b"),
        ],
        commercial_signal_keys=["enterprise_domain", "technical_fit"],
    )
    assert result["scoring_version"] == SCORING_VERSION
    assert set(result["dimensions"]) == {
        "technical_fit",
        "pain_evidence",
        "timing",
        "intent",
        "evidence_quality",
    }
    assert 0 <= result["score"] <= 100


def test_counter_signals_reduce_priority_without_erasing_fit():
    kwargs = dict(
        signal_keys=["clickhouse", "realtime_product", "large_scale"],
        evidence=[
            observed("ClickHouse is used", "https://example.com/a"),
            observed("The workload is real time", "https://example.com/b"),
        ],
        commercial_signal_keys=["enterprise_domain", "technical_fit"],
    )
    baseline = score_signals(**kwargs)
    countered = score_signals(
        **kwargs,
        counter_signal_keys=["incumbent_meeting_requirements", "no_observed_pain"],
    )
    assert countered["dimensions"]["technical_fit"] == baseline["dimensions"]["technical_fit"]
    assert countered["score"] < baseline["score"]
    assert countered["counter_signal_penalty"] > 0


def test_confidence_depends_on_evidence_quality_not_signal_count():
    many_unsourced = score_signals(["clickhouse", "kafka_flink", "large_scale"], evidence=[])
    sourced = score_signals(
        ["clickhouse"],
        evidence=[
            observed("Uses ClickHouse", "https://example.com/a"),
            observed("Independent corroboration", "https://example.com/b"),
            observed("Third corroboration", "https://example.com/c"),
        ],
    )
    assert sourced["confidence"] > many_unsourced["confidence"]


def test_duplicate_signals_do_not_double_count():
    once = score_signals(["clickhouse"])
    duplicate = score_signals(["clickhouse", "clickhouse", "clickhouse"])
    assert duplicate["score"] == once["score"]


def test_priority_band_boundaries():
    assert priority_band(75).startswith("P1")
    assert priority_band(55).startswith("P2")
    assert priority_band(35).startswith("P3")
    assert priority_band(34.9).startswith("P4")
