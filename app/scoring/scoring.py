from dataclasses import dataclass
from typing import Iterable, List, Dict
@dataclass(frozen=True)
class SignalRule:
    key:str; label:str; points:int; category:str; rationale:str
RULES: Dict[str,SignalRule]={
"clickhouse":SignalRule("clickhouse","ClickHouse detected",20,"competitive","Potential migration / concurrency / JOIN opportunity"),
"elasticsearch":SignalRule("elasticsearch","Elasticsearch/OpenSearch detected",15,"competitive","Potential observability or search-stack consolidation"),
"loki":SignalRule("loki","Loki detected",15,"competitive","Potential log analytics cost / scale motion"),
"trino_hive":SignalRule("trino_hive","Trino/Presto/Hive detected",12,"warehouse","Potential warehouse or lakehouse acceleration"),
"kafka_flink":SignalRule("kafka_flink","Kafka/Flink detected",10,"realtime","Strong real-time data pipeline signal"),
"data_platform_hiring":SignalRule("data_platform_hiring","Hiring data platform engineers",12,"timing","Active infrastructure investment"),
"clickhouse_hiring":SignalRule("clickhouse_hiring","Hiring for ClickHouse experience",18,"timing","Very strong workload and stack evidence"),
"realtime_product":SignalRule("realtime_product","Real-time analytics product",15,"workload","Direct fit with low-latency analytical workloads"),
"customer_dashboards":SignalRule("customer_dashboards","Customer-facing dashboards",12,"workload","Concurrency and response-time sensitivity likely matters"),
"ai_context":SignalRule("ai_context","AI/RAG/agent infrastructure",12,"ai","Potential unified analytical + context workload"),
"large_scale":SignalRule("large_scale","Large / fast-growing data scale",10,"scale","Data volume increases urgency for efficient analytics"),
"recent_growth":SignalRule("recent_growth","Recent funding or rapid growth",8,"timing","Budget and timing signal"),
"fragmented_stack":SignalRule("fragmented_stack","Multiple analytical databases",15,"consolidation","Potential stack consolidation motion")}
def score_signals(signal_keys: Iterable[str], cap:int=100)->dict:
    matched:List[SignalRule]=[RULES[k] for k in signal_keys if k in RULES]
    raw=sum(r.points for r in matched); score=min(raw,cap)
    confidence=min(0.95,0.45+0.07*len(matched)) if matched else 0.2
    return {"score":score,"raw_score":raw,"confidence":round(confidence,2),"matched_rules":[r.__dict__ for r in matched]}
def priority_band(score:int)->str:
    if score>=80:return "P1 - high priority"
    if score>=60:return "P2 - qualified"
    if score>=40:return "P3 - monitor"
    return "P4 - low priority"
