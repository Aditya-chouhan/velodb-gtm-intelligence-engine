# ⚡ VeloDB Commercial Intelligence OS

**An outside-in, evidence-aware prototype for turning public technical signals into account prioritization, commercial-motion routing, technical POC plans, and eventually closed-loop revenue learning.**

> Independent portfolio project by Aditya Chouhan. Not an official VeloDB product, endorsement, customer system, or claim of access to VeloDB internal data.

## What changed from a normal GTM demo

This repository is deliberately not a “scrape leads → generate emails” project. It tries to answer the higher-value questions a developer-infrastructure GTM team faces:

1. Who has a technically relevant workload?
2. What is **observed** versus merely **inferred**?
3. Which VeloDB / Apache Doris commercial motion fits the evidence?
4. What would a fair technical POC need to prove?
5. How could OSS/product signals change prioritization if the company later authorized them?
6. How should downstream meetings, POCs, opportunities, wins and losses feed back into the system?

```text
PUBLIC / AUTHORIZED SIGNALS
        ↓
ENTITY + EVIDENCE LAYER
        ↓
TECHNICAL FIT / TIMING
        ↓
OPPORTUNITY SCORE
        ↓
MOTION ROUTER
        ↓
ACCOUNT INTELLIGENCE
        ↓
TECHNICAL POC BLUEPRINT
        ↓
CRM / SALES / PARTNER ACTIVATION
        ↓
MEETING → POC → OPPORTUNITY → WON / LOST
        ↓
OUTCOME ANALYSIS → FUTURE SCORING REVIEW
```

## Current evidence status

| Layer | Status | Honest boundary |
|---|---|---|
| Fictional workflow dataset | implemented | proves software behavior only |
| Public observed account universe | **implemented with source URLs** | proves cited public technical evidence, **not buying intent** |
| Public web collector | **implemented** | verifies page reachability + disclosed keyword presence |
| Weekly public-source smoke test | **implemented in GitHub Actions** | source health only; no intent claim |
| Competitive/use-case routing | implemented | deterministic hypothesis routing |
| Technical POC planner | implemented | plan generation, not benchmark performance |
| Apache Doris workload harness | **implemented** | runnable schema/data/query procedure; no timings claimed yet |
| Internal VeloDB trial/product telemetry | unavailable / not claimed | would require authorization |
| Real campaign, pipeline or revenue outcomes | unavailable / not claimed | closed-loop module is architectural until real outcomes exist |
| Apache Doris upstream contribution | planned, **not claimed** | contribution must solve a real upstream need |

## Real public account universe

`data/real_target_accounts.json` currently contains a small, intentionally inspectable set of companies selected because public engineering/ecosystem material documents VeloDB-relevant workloads:

- **Contentsquare** — ClickHouse, Kafka/Flink and near-real-time customer analytics;
- **QuestionPro** — ClickHouse + Kafka pipeline for real-time BI over billions of rows;
- **Razorpay** — Trino with Spark/Hudi/S3/Hive Metastore;
- **Rapido** — Trino for large-scale analytics, KPI/system metrics and BI visualization;
- **Vimeo** — ClickHouse-based real-time video analytics at very large event volume.

Every real account is marked `dataset_classification=publicly_observed`, carries source URLs, and includes a discovery hypothesis. None is labeled a “lead,” “buyer,” or “migration opportunity” merely because a technology was detected.

Run the public set:

```bash
python -m app.main --dataset public
```

The Streamlit dashboard also lets a reviewer switch between **Fictional demo** and **Public observed accounts**.

## Live public-source collector

`app/collectors/public_web.py` uses only the Python standard library to retrieve configured public pages, strip markup, and record disclosed keyword hits. `scripts/refresh_public_evidence.py` creates a receipt containing:

- URL;
- retrieval timestamp;
- HTTP status;
- matched disclosed keywords;
- visible failure state.

A keyword hit means exactly that: **the term appeared on the retrieved page**. It is not silently promoted into production usage, pain or intent.

```bash
python scripts/refresh_public_evidence.py --check
```

`.github/workflows/public-signal-smoke.yml` runs this weekly and uploads the receipt as a 30-day workflow artifact.

## Commercial motions

| Observed signal | Routed motion | What the POC should validate |
|---|---|---|
| ClickHouse | competitive / migration evaluation | concurrency, joins, freshness, operational complexity, cost |
| Elasticsearch / OpenSearch | observability/search consolidation | search + analytics performance, retention economics, fragmentation |
| Loki | large-scale log analytics | search latency, cardinality, storage economics, scale |
| Trino / Hive | lakehouse / serving acceleration | interactive latency, concurrency, serving-layer efficiency |
| AI / RAG / agents | context / agent observability | structured + event analytics, freshness, operational simplification |
| customer-facing analytics | real-time product analytics | P95 latency, peak concurrency, ingestion lag, cost |

The system never treats detected technology as proof of dissatisfaction.

## Apache Doris technical workload harness

`benchmark/doris/` adds a reproducible **agent-observability analytical workload**:

```text
schema.sql             Doris table design
generate_events.py     deterministic synthetic event generator
queries.sql            recent-window, tenant/model, error, trace and aggregation queries
run.sh                 Stream Load + query execution procedure
README.md              fair benchmark protocol + evidence boundaries
```

Run it against a real Apache Doris instance:

```bash
bash benchmark/doris/run.sh
```

### Important benchmark boundary

The environment used to build this portfolio artifact did not expose a Docker daemon or a running Doris cluster. Therefore this repository currently claims **zero Doris latency/throughput benchmark results**. The harness exists so a result can be produced reproducibly on real infrastructure instead of invented.

Any later competitive benchmark should disclose software versions, hardware, data distribution, concurrency, ingestion state, repeated-run policy, P50/P95/P99 latency, throughput, failures and cost assumptions.

## Open-source → revenue model

Open-source activity alone is not purchase intent. The model therefore separates public/community signals from authorized internal product signals.

```text
OSS activity
  + company identity
  + technical fit
  + timing / scale
  + authorized product intent (only if VeloDB supplies it)
  ↓
commercial stage
```

The public project can model `oss_activity`, `enterprise_domain` and `technical_fit`; signals such as trial start, data loaded, repeat queries, multi-user adoption and integrations must come from an authorized system and are never fabricated here.

## Closed-loop revenue learning

The feedback module can summarize:

```text
no reply → reply → meeting → POC → opportunity → won / lost
```

It deliberately does **not** auto-rewrite production scoring weights. Real reweighting should require adequate samples, a control/holdout design, statistical evaluation and human approval.

## Repository structure

```text
app/
├── agents/                 account strategy + activation
├── collectors/             public evidence retrieval
├── intelligence/           evidence, motion, POC, commercialization, feedback
├── scoring/                deterministic scoring
├── api/                    FastAPI
├── dashboard.py            reviewer-facing Streamlit console
└── main.py                 CLI for demo/public datasets

benchmark/doris/             runnable Apache Doris workload harness
data/
├── demo_accounts.json       fictional software-behavior fixture
└── real_target_accounts.json public observed account evidence
scripts/
└── refresh_public_evidence.py
tests/
.github/workflows/
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

pytest -q
python -m app.main --dataset demo
python -m app.main --dataset public
streamlit run app/dashboard.py
uvicorn app.api.routes:app --reload
```

## Open-source contribution policy

See `docs/OPEN_SOURCE_CONTRIBUTION_PLAN.md`. The rule is simple: no meaningless upstream PR for a portfolio badge. A Doris contribution should come from a reproduced issue, documentation gap, example problem, test gap or other concrete upstream need.

## What this could become inside VeloDB

With explicit internal authorization, the same architecture could add:

- Apache Doris community/account resolution;
- VeloDB Cloud trial/PQL telemetry;
- CRM opportunity stages and seller actions;
- partner/co-sell signals;
- technical POC results;
- loss reasons and competitive outcomes;
- signal-to-pipeline and signal-to-win evaluation.

That is the path from an outside-in portfolio prototype to an actual **open-source-to-enterprise revenue intelligence layer**.

## Author

**Aditya Chouhan**  
GTM / Revenue Systems Engineering · GTM Strategy · AI Revenue Infrastructure

Portfolio: https://aditya-chouhan.github.io/  
GitHub: https://github.com/Aditya-chouhan

## Disclaimer

This is an independent portfolio case study and software prototype. It is not affiliated with or endorsed by VeloDB or the Apache Software Foundation. It does not use private VeloDB customer, product, CRM, trial, partner, pipeline or revenue data. Public-account scoring is a research/prioritization rubric, not a claim that any named company is a VeloDB prospect or is dissatisfied with its current technology.
