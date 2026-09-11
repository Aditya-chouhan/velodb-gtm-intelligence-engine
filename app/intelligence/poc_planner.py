from __future__ import annotations

from typing import Dict, Iterable


POC_PLAYBOOKS: Dict[str, dict] = {
    "clickhouse": {
        "name": "ClickHouse competitive evaluation",
        "hypothesis": "Concurrency, complex joins, freshness, or operational complexity may justify an Apache Doris / VeloDB evaluation.",
        "dataset": "Use the prospect's representative analytical schema and production-like data distribution.",
        "tests": [
            "P50/P95/P99 latency for representative queries",
            "10/30/50+ concurrent analytical users",
            "join-heavy and aggregation-heavy workloads",
            "streaming ingestion while queries are running",
            "resource consumption normalized to comparable hardware",
        ],
        "success_metrics": [
            "query latency",
            "concurrency throughput",
            "freshness / ingestion lag",
            "infrastructure cost per workload unit",
            "operational complexity",
        ],
    },
    "elasticsearch": {
        "name": "Observability / search consolidation evaluation",
        "hypothesis": "Search-heavy observability workloads may benefit from consolidating analytical and search infrastructure.",
        "dataset": "Representative logs/events with structured fields, free text, and JSON payloads.",
        "tests": [
            "high-cardinality filters",
            "full-text + structured predicates",
            "aggregation latency",
            "fresh-ingest queryability",
            "retention-cost projection",
        ],
        "success_metrics": ["search latency", "aggregation latency", "storage cost", "freshness", "systems eliminated"],
    },
    "loki": {
        "name": "Large-scale log analytics evaluation",
        "hypothesis": "Fast-growing log volumes may create a cost/performance opportunity for a unified analytical engine.",
        "dataset": "Time-partitioned application and infrastructure logs with realistic label/cardinality distribution.",
        "tests": ["recent-window search", "wide-window scan", "high-cardinality group-by", "burst ingestion", "retention-cost model"],
        "success_metrics": ["P95 search latency", "ingest throughput", "storage footprint", "cost per retained TB"],
    },
    "trino_hive": {
        "name": "Lakehouse serving-layer evaluation",
        "hypothesis": "Interactive analytical workloads may benefit from a lower-latency serving layer while preserving lakehouse interoperability.",
        "dataset": "Representative fact/dimension tables and lakehouse files.",
        "tests": ["interactive BI queries", "multi-table joins", "high-concurrency dashboards", "incremental refresh", "cold vs warm runs"],
        "success_metrics": ["P95 dashboard latency", "concurrent users", "refresh time", "compute efficiency"],
    },
    "ai_context": {
        "name": "AI context / agent observability evaluation",
        "hypothesis": "Agentic workloads may benefit from one engine supporting fresh structured, JSON, search, and analytical context.",
        "dataset": "Agent traces, tool calls, events, structured metadata, JSON payloads, and searchable text.",
        "tests": ["trace lookup", "JSON filtering", "text + structured retrieval", "session aggregation", "fresh event visibility"],
        "success_metrics": ["retrieval latency", "freshness", "query flexibility", "systems consolidated", "cost per million events"],
    },
    "realtime_product": {
        "name": "Real-time customer analytics evaluation",
        "hypothesis": "Customer-facing analytics may require predictable low latency under concurrent interactive workloads.",
        "dataset": "Representative product events and dashboard queries.",
        "tests": ["live ingestion", "dashboard concurrency", "join-heavy product queries", "tenant isolation patterns", "peak-load simulation"],
        "success_metrics": ["P95 user-facing latency", "concurrent sessions", "ingestion lag", "cost per tenant/workload"],
    },
}


def build_poc(signal_keys: Iterable[str], motion: str) -> dict:
    keys = list(signal_keys)
    for key in ("clickhouse", "elasticsearch", "loki", "trino_hive", "ai_context", "realtime_product"):
        if key in keys:
            return {"trigger": key, "motion": motion, **POC_PLAYBOOKS[key]}
    return {
        "trigger": "discovery",
        "motion": motion,
        "name": "Discovery-first technical evaluation",
        "hypothesis": "A POC should only be scoped after validating workload, scale, latency, freshness, cost, and operational pain.",
        "dataset": "Prospect-provided representative data after discovery.",
        "tests": ["baseline current system", "representative query set", "representative ingestion", "concurrency profile"],
        "success_metrics": ["latency", "throughput", "freshness", "cost", "operational complexity"],
    }
