USE velodb_portfolio;

-- Q1: recent-window workload health
SELECT
    event_type,
    COUNT(*) AS events,
    AVG(latency_ms) AS avg_latency_ms,
    SUM(CASE WHEN success = FALSE THEN 1 ELSE 0 END) AS failures
FROM agent_events
WHERE event_time >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
GROUP BY event_type
ORDER BY events DESC;

-- Q2: tenant/model economics
SELECT
    tenant_id,
    model,
    COUNT(*) AS events,
    SUM(input_tokens + output_tokens) AS total_tokens,
    SUM(cost_usd) AS estimated_cost_usd,
    AVG(latency_ms) AS avg_latency_ms
FROM agent_events
GROUP BY tenant_id, model
ORDER BY estimated_cost_usd DESC
LIMIT 50;

-- Q3: error investigation
SELECT
    event_time,
    trace_id,
    session_id,
    tenant_id,
    model,
    event_type,
    latency_ms,
    message
FROM agent_events
WHERE success = FALSE
ORDER BY event_time DESC
LIMIT 100;

-- Q4: trace lookup
SELECT *
FROM agent_events
WHERE trace_id = 'trace-00000042'
ORDER BY event_time;

-- Q5: high-cardinality aggregation representative of dashboard traffic
SELECT
    tenant_id,
    event_type,
    model,
    COUNT(*) AS events,
    AVG(latency_ms) AS avg_latency_ms,
    MAX(latency_ms) AS max_latency_ms
FROM agent_events
WHERE event_time >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY tenant_id, event_type, model
ORDER BY events DESC
LIMIT 200;
