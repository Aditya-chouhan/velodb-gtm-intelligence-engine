# ⚡ VeloDB Commercial Intelligence OS

**An outside-in prototype for turning open-source activity, competitive technology signals, account timing, product evaluation, and sales outcomes into repeatable enterprise GTM actions.**

> Independent portfolio project by Aditya Chouhan. Not an official VeloDB product, endorsement, customer system, or claim of access to VeloDB internal data.

## The commercial problem

For a developer-infrastructure company, the hard problem is not generating more contacts. It is answering:

1. **Who** is entering a relevant technical buying window?
2. **Why now?**
3. **Which VeloDB / Apache Doris motion fits?**
4. **What evidence supports that conclusion?**
5. **What technical POC would actually validate the hypothesis?**
6. **How should OSS / product intent change prioritization?**
7. **What happened afterward, and what should the GTM system learn?**

This project models that revenue-intelligence layer.

## Architecture

```text
PUBLIC / AUTHORIZED SIGNALS
│
├─ OSS / ecosystem activity
├─ competitive technology
├─ engineering hiring
├─ growth / timing
├─ workload evidence
└─ authorized product telemetry*
        ↓
ENTITY + EVIDENCE LAYER
        ↓
FIT / INTENT / TIMING
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

`*` Product/trial signals are modeled only with fictional demo inputs unless the company explicitly authorizes access.

## Commercial motions

| Observed signal | Routed motion | What to validate |
|---|---|---|
| ClickHouse | Competitive / migration | concurrency, joins, freshness, operational complexity, cost |
| Elasticsearch / OpenSearch | Observability/search consolidation | search + analytics performance, retention economics, stack fragmentation |
| Loki | Large-scale log analytics | log-search latency, cardinality, storage cost, scale |
| Trino / Hive | Lakehouse acceleration | interactive latency, concurrency, serving-layer efficiency |
| AI / RAG / agents | Context / agent observability | JSON/search/analytics convergence, freshness, trace volume |
| Customer-facing analytics | Real-time product analytics | P95 latency, peak concurrency, ingestion lag, workload cost |

The system does **not** claim that detecting a technology proves pain. Each pain statement is stored as a hypothesis requiring discovery validation.

## 1. Evidence-aware account scoring

The deterministic scorer weighs technical fit and commercial timing signals such as:

- ClickHouse / Elasticsearch / Loki / Trino-Hive presence
- Kafka / Flink
- customer-facing real-time analytics
- AI / agent infrastructure
- data-platform hiring
- large or fast-growing data scale
- multiple analytical databases
- recent growth

Every account gets a score, confidence, priority band, matched rules, and source-coverage status.

### Evidence integrity

**Observed** = a publicly verifiable claim with a source.  
**Hypothesis** = an interpretation that must be validated.

`ready_for_outreach=true` requires at least two observed signals and ≥80% source coverage.

## 2. Competitive / use-case motion routing

A high score is not enough. The engine routes an account into a commercial motion so sales does not use the same pitch everywhere.

```text
ClickHouse   → migration / competitive evaluation
Elasticsearch→ observability / search consolidation
Loki         → log analytics economics
Trino/Hive   → lakehouse serving acceleration
AI agents    → context / agent observability
Real-time app→ user-facing analytics
```

## 3. Technical POC planner

This is the biggest upgrade over a normal “AI SDR” demo.

For each routed motion, the engine generates:

- the technical hypothesis to validate;
- representative dataset guidance;
- benchmark workload;
- concurrency / ingestion tests;
- measurable success criteria;
- a discovery-first fallback when evidence is insufficient.

Example ClickHouse evaluation:

```text
Current signal: ClickHouse + Kafka + customer-facing analytics

Hypothesis:
Concurrency, joins, freshness, or operational complexity may justify
an Apache Doris / VeloDB evaluation.

Test:
• representative production schema
• 10 / 30 / 50+ concurrent users
• join + aggregation workloads
• streaming ingestion during queries
• normalized infrastructure comparison

Measure:
• P50 / P95 / P99 latency
• concurrency throughput
• ingestion lag
• cost per workload unit
• operational complexity
```

This helps bridge account intelligence to the work a seller / solution architect would need to progress a technical deal.

## 4. Open-source → revenue commercialization model

Open-source activity is **not purchase intent**. The project therefore models commercialization as a combination of independent signals:

```text
OSS activity
   +
known company identity
   +
technical fit
   +
commercial timing
   +
authorized trial/product intent
   ↓
commercial stage
```

Supported modeled signals include OSS activity, docs interest, trial start, meaningful data load, repeat querying, multi-user adoption, integration connection, enterprise domain, and technical fit.

Stages:

- community / low commercial intent
- nurture / technical education
- high-intent evaluation
- sales-ready PQL

The public project does **not** claim access to VeloDB telemetry or private Apache Doris user data.

## 5. Closed-loop revenue learning

The feedback layer tracks outcomes such as:

```text
no reply → reply → meeting → POC → opportunity → won / lost
```

It summarizes which signal families are associated with stronger downstream outcomes.

Crucially, it **does not automatically rewrite production weights**. A real deployment should require minimum sample sizes, a holdout set, statistical evaluation, and human approval before changing routing logic.

## What this demonstrates

This repo is designed to show how several GTM-engineering disciplines combine into one commercial system:

- market / technical signal intelligence
- deterministic scoring
- evidence provenance
- competitive positioning
- technical discovery
- POC strategy
- product-led / OSS commercialization
- sales activation
- outcome measurement
- revenue learning

That is a materially different problem from “scrape leads and write emails.”

## Repository structure

```text
app/
├── agents/
│   ├── orchestrator.py
│   ├── strategist.py
│   └── personalization.py
├── intelligence/
│   ├── evidence.py
│   ├── opportunity_mapper.py
│   ├── poc_planner.py
│   ├── commercialization.py
│   └── feedback_loop.py
├── scoring/
│   └── scoring.py
├── api/
│   └── routes.py
├── dashboard.py
└── main.py

data/
└── demo_accounts.json

docs/
├── architecture.md
├── gtm-strategy.md
├── scoring-methodology.md
└── COMMERCIAL_INTELLIGENCE_OS.md

tests/
├── test_scoring.py
├── test_orchestrator.py
└── test_commercial_os.py
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m app.main
streamlit run app/dashboard.py
uvicorn app.api.routes:app --reload
pytest -q
```

API docs are available at `http://localhost:8000/docs` when FastAPI is running.

## Demo-data policy

The committed account dataset uses fictional `.example` companies. This makes the software reproducible without publishing unsupported claims about real prospects.

A production implementation should preserve, at minimum:

- source URL;
- retrieval timestamp;
- signal type;
- entity-resolution confidence;
- observed vs inferred classification;
- scoring version;
- activation decision;
- downstream commercial outcome.

## What a real deployment would measure

A real company deployment should be evaluated against business outcomes, including:

- OSS/community → known-account conversion;
- known-account → opportunity conversion;
- PQL → meeting / POC conversion;
- signal-based prioritization lift versus control;
- POC win rate by technical motion;
- time from meaningful signal to seller action;
- pipeline / revenue influenced by signal family;
- false-positive rate and seller trust.

None of those business results are claimed by this portfolio repository.

## Relationship to my broader GTM engineering portfolio

This project combines patterns I have separately implemented across signal intelligence, AI revenue agents, CRM control planes, workflow orchestration, GTM data quality, revenue warehousing, evaluation, and closed-loop learning.

The goal here is to show how those capabilities can be assembled around one developer-infrastructure company's commercialization problem rather than presented as disconnected demos.

## Author

**Aditya Chouhan**  
GTM / Revenue Systems Engineering · GTM Strategy · AI Revenue Infrastructure

Portfolio: https://aditya-chouhan.github.io/  
GitHub: https://github.com/Aditya-chouhan

## Disclaimer

This is an independent portfolio case study and software prototype. It is not affiliated with or endorsed by VeloDB or the Apache Software Foundation. It does not use private VeloDB customer, product, CRM, trial, partner, or pipeline data. Apache Doris and other product names are referenced only to model public technical GTM scenarios.
