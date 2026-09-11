from app.intelligence.commercialization import score_commercialization
from app.intelligence.feedback_loop import summarize_outcomes
from app.intelligence.poc_planner import build_poc


def test_clickhouse_poc_is_routed():
    plan = build_poc(["clickhouse", "kafka_flink"], "ClickHouse competitive / migration")
    assert plan["trigger"] == "clickhouse"
    assert "concurrent" in " ".join(plan["tests"]).lower()


def test_commercialization_stage():
    result = score_commercialization(["oss_activity", "trial_started", "data_loaded", "multi_user", "technical_fit", "enterprise_domain"])
    assert result["score"] >= 75
    assert result["stage"] == "sales-ready PQL"


def test_feedback_does_not_autorewrite_weights():
    result = summarize_outcomes([
        {"signals": ["clickhouse"], "outcome": "poc"},
        {"signals": ["clickhouse"], "outcome": "opportunity"},
        {"signals": ["recent_growth"], "outcome": "no_reply"},
    ])
    assert result["signal_performance"][0]["signal"] == "clickhouse"
    assert "does not automatically rewrite" in result["guardrail"]
