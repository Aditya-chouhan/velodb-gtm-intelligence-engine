from app.agents.orchestrator import analyze_account


def test_analysis_has_required_sections():
    account = {
        "company": "Acme",
        "signals": ["clickhouse", "realtime_product"],
        "commercial_signals": ["enterprise_domain", "technical_fit"],
        "counter_signals": ["no_observed_pain"],
        "evidence": [
            {"type": "observed", "claim": "Uses ClickHouse", "source": "https://example.com/a"},
            {"type": "observed", "claim": "Runs real-time dashboards", "source": "https://example.com/b"},
            {"type": "hypothesis", "claim": "Concurrency may become a bottleneck"},
        ],
    }
    result = analyze_account(account)
    assert result["score"] >= 0
    assert result["scoring_version"] == "2.0.0"
    assert "score_dimensions" in result
    assert result["counter_signal_penalty"] > 0
    assert "opportunity" in result
    assert "strategy" in result
    assert "poc_plan" in result
    assert "outreach" in result
