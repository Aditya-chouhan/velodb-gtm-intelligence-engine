from typing import Iterable, Dict
MOTIONS = [
("clickhouse","ClickHouse competitive / migration","Lead with concurrency, complex JOINs, operational simplicity, and consolidation."),
("elasticsearch","Observability / search consolidation","Lead with unified analytics, cost efficiency, and reducing stack fragmentation."),
("loki","PB-scale log analytics","Lead with log-search economics, performance at scale, and fewer moving parts."),
("trino_hive","Lakehouse / warehouse acceleration","Lead with faster interactive analytics and simplifying query-serving layers."),
("ai_context","AI context / agent analytics","Lead with fresh, queryable context and reducing separate analytical/search/vector infrastructure."),
("realtime_product","Real-time product analytics","Lead with freshness, high concurrency, and user-facing analytical latency.")]

def map_opportunity(signal_keys: Iterable[str]) -> Dict[str,str]:
    keys=set(signal_keys)
    for key,motion,angle in MOTIONS:
        if key in keys: return {"motion":motion,"angle":angle}
    return {"motion":"Discovery-led analytics infrastructure","angle":"Validate workload, concurrency, freshness, cost, and stack-complexity pain before positioning a solution."}
