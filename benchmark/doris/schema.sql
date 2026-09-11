CREATE DATABASE IF NOT EXISTS velodb_portfolio;
USE velodb_portfolio;

DROP TABLE IF EXISTS agent_events;

CREATE TABLE agent_events (
    event_time DATETIME NOT NULL,
    trace_id VARCHAR(64) NOT NULL,
    session_id VARCHAR(64) NOT NULL,
    tenant_id INT NOT NULL,
    model VARCHAR(64) NOT NULL,
    event_type VARCHAR(32) NOT NULL,
    latency_ms INT NOT NULL,
    input_tokens INT NOT NULL,
    output_tokens INT NOT NULL,
    cost_usd DECIMAL(12,6) NOT NULL,
    success BOOLEAN NOT NULL,
    message STRING NULL
)
DUPLICATE KEY(event_time, trace_id)
DISTRIBUTED BY HASH(trace_id) BUCKETS 8
PROPERTIES (
    "replication_num" = "1"
);
