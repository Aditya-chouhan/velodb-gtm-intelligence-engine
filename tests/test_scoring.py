from app.scoring.scoring import score_signals, priority_band

def test_score_is_capped():
    result=score_signals(["clickhouse","elasticsearch","loki","trino_hive","kafka_flink","data_platform_hiring","clickhouse_hiring","realtime_product","customer_dashboards","ai_context","large_scale","recent_growth","fragmented_stack"])
    assert result["score"]==100

def test_priority_band():
    assert priority_band(85).startswith("P1"); assert priority_band(61).startswith("P2"); assert priority_band(45).startswith("P3"); assert priority_band(20).startswith("P4")
