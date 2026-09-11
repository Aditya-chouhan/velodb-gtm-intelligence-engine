# ⚡ VeloDB GTM Intelligence Engine

An evidence-aware GTM engineering system for identifying accounts entering a high-value real-time analytics infrastructure buying window.

> Portfolio project demonstrating how technical market signals become account prioritization, opportunity hypotheses, buying-committee context, and responsible personalized outreach.

## Why this exists

Developer-infrastructure GTM is not just list building. The hard problem is timing: **which companies have a technical workload, architecture, or growth signal that makes a conversation relevant now?**

The engine models VeloDB / Apache Doris-style motions: ClickHouse migration, Elasticsearch/observability consolidation, Loki/log analytics, Trino/Hive acceleration, real-time customer analytics, AI/agent context infrastructure, and multi-database consolidation.

It deliberately separates **observed evidence** from **hypotheses** so weak public signals never become fake certainty.

## Pipeline

```text
Public market signals → Signal normalization → Weighted scoring
→ Evidence quality gate → GTM motion routing → Strategy brief
→ Buying committee → Evidence-backed personalization
```

For each account it returns: opportunity score, confidence, P1–P4 band, matched signals, recommended GTM motion, evidence quality, buying committee, talk track, and outreach.

## Signal model

| Signal | Weight | Interpretation |
|---|---:|---|
| ClickHouse detected | +20 | Migration / competitive |
| ClickHouse hiring | +18 | Stack + timing |
| Elasticsearch / OpenSearch | +15 | Search / observability consolidation |
| Loki | +15 | Log analytics scale |
| Multiple analytical DBs | +15 | Consolidation |
| Real-time analytics product | +15 | Core workload fit |
| Trino / Hive | +12 | Lakehouse acceleration |
| Data-platform hiring | +12 | Infrastructure investment |
| Customer dashboards | +12 | Concurrency / latency |
| AI / RAG / agents | +12 | Context infrastructure |
| Kafka / Flink | +10 | Streaming workload |
| Large data scale | +10 | Scale pressure |
| Recent growth | +8 | Timing / budget |

## Evidence integrity

**Observed** = publicly verifiable claim with a source. **Hypothesis** = interpretation requiring discovery validation.

`ready_for_outreach=true` requires at least two observed signals and ≥80% source coverage.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
streamlit run app/dashboard.py
uvicorn app.api.routes:app --reload
pytest -q
```

## Architecture

```text
app/
├── agents/          # orchestration, strategy, personalization
├── intelligence/    # evidence gate + opportunity routing
├── scoring/         # transparent weighted scoring
├── api/             # FastAPI
├── dashboard.py     # Streamlit GTM console
└── main.py          # CLI demo
```

## Demo-data policy

The repository ships with fictional `.example` accounts. Production collectors should retain source URL, retrieval date, and provenance for every factual signal.

## Author

**Aditya Chouhan** — GTM Engineering · AI Revenue Systems · GTM Strategy  
Portfolio: https://aditya-chouhan.github.io/  
GitHub: https://github.com/Aditya-chouhan

### Disclaimer

Independent portfolio project; not an official VeloDB product or endorsement. Demo prospect data is fictional.
