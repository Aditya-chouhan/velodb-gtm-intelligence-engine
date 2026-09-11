from app.agents.orchestrator import analyze_account

def test_analysis_has_required_sections():
    account={"company":"Acme","signals":["clickhouse","realtime_product"],"evidence":[{"type":"observed","claim":"Uses ClickHouse","source":"https://example.com"},{"type":"observed","claim":"Runs real-time dashboards","source":"https://example.com/2"},{"type":"hypothesis","claim":"Concurrency may become a bottleneck"}]}
    result=analyze_account(account)
    assert result["score"]>0; assert "opportunity" in result; assert "strategy" in result; assert "outreach" in result
