# Apache Doris agent-observability workload harness

This directory is a **reproducible technical evaluation harness**, not a benchmark claim.

It models an agent-observability workload with event time, trace/session identity, tenant, model, tool/agent event type, latency, token volume, estimated cost, success state and searchable message text. The query set exercises recent-window analytics, tenant/model economics, error investigation, point trace lookup and high-cardinality grouped analytics.

## Evidence status

| Artifact | Status | What it proves |
|---|---|---|
| `schema.sql` | implemented | reviewable Doris table design |
| `generate_events.py` | implemented | deterministic synthetic workload generation |
| `queries.sql` | implemented | representative analytical query set |
| `run.sh` | implemented | reproducible load/query procedure for a running Doris instance |
| latency / throughput results | **not measured here** | no performance claim is made |

The ChatGPT build environment used to create this portfolio artifact did not expose a Docker daemon or running Apache Doris cluster, so publishing invented timings would be misleading.

## Run against Apache Doris

Start a local Apache Doris deployment using the official quick-start instructions, then install a MySQL-compatible CLI and run:

```bash
bash benchmark/doris/run.sh
```

Optional configuration:

```bash
ROWS=1000000 \
DORIS_HOST=127.0.0.1 \
DORIS_QUERY_PORT=9030 \
DORIS_HTTP_PORT=8030 \
DORIS_USER=root \
DORIS_PASSWORD='' \
bash benchmark/doris/run.sh
```

`run.sh` creates the table, uses Doris Stream Load for the generated CSV, verifies row count, and executes the disclosed query suite.

## Fair benchmark protocol

If this is extended into a competitive POC, record rather than cherry-pick:

1. software versions and exact configuration;
2. machine/cloud instance shape and storage;
3. row count and data distribution;
4. cold/warm run policy;
5. concurrency level;
6. ingestion running or paused during reads;
7. P50/P95/P99 latency across repeated runs;
8. throughput and resource utilization;
9. failures/timeouts;
10. cost assumptions.

A competitive result should use equivalent datasets, query semantics and infrastructure budgets. This repository intentionally contains **no claim that Apache Doris is faster than another engine** until that experiment is actually run.
