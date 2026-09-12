# Reviewer Guide

This repository is designed to be reviewable in three passes.

## 1. Five-minute executive review

Read `README.md`, then open `app/dashboard.py` and run:

```bash
streamlit run app/dashboard.py
```

Start with **Public observed accounts**. The market view separates technical fit, pain evidence, timing, intent, evidence quality, and counter-signal penalties. A high technical-fit account can remain low priority when there is no observed pain or when the incumbent appears to be working well.

## 2. Fifteen-minute GTM systems review

Inspect:

- `app/scoring/scoring.py` — transparent, versioned multidimensional scoring;
- `app/intelligence/evidence.py` — provenance and outreach-readiness gate;
- `app/intelligence/opportunity_mapper.py` — competitive/use-case routing;
- `app/intelligence/poc_planner.py` — technical evaluation plans;
- `app/intelligence/commercialization.py` — OSS/product-commercialization model;
- `app/intelligence/feedback_loop.py` — downstream outcome analysis;
- `data/real_target_accounts.json` — public research examples with counter-signals.

The central design choice is to keep **fit, pain, timing, intent, confidence, and counter-evidence separate** instead of collapsing them into a single opaque AI score.

## 3. Technical credibility review

Run:

```bash
python -m pytest -q
python -m app.main --dataset public
python scripts/refresh_public_evidence.py --check
```

For Apache Doris, inspect `benchmark/doris/`. It includes deterministic event generation, schema, representative queries, Stream Load, and a disclosed fair-benchmark protocol. No unmeasured performance result is claimed.

## What is real vs modeled

### Implemented with public/reproducible evidence

- sourced public account research;
- public-page evidence checks;
- multidimensional scoring and counter-signals;
- commercial-motion routing;
- POC planning;
- Streamlit review interface;
- FastAPI analysis endpoint;
- GitHub Actions CI and public-source smoke checks;
- reproducible Apache Doris workload harness.

### Modeled because internal access is unavailable

- VeloDB Cloud trial/PQL telemetry;
- CRM opportunity and seller activity;
- partner/co-sell activity;
- real POC results;
- pipeline, win/loss, and revenue outcomes.

Those signals are represented as interfaces/architecture only and are never presented as observed VeloDB data.

## Productionization path

With internal authorization, the next production steps would be:

1. identity resolution across OSS/community, product, CRM, and enrichment data;
2. event contracts with provenance, timestamps, consent/governance, and scoring-version metadata;
3. real PQL and lifecycle signals;
4. seller-facing routing with SLA/feedback capture;
5. technical POC result ingestion;
6. holdout/control measurement for prioritization lift;
7. model recalibration only after adequate sample sizes and human approval.

## Design principles

- public technology usage is not intent;
- inferred pain is never stored as observed fact;
- independent sources increase confidence;
- negative evidence is first-class;
- scoring is transparent and versioned;
- benchmark claims require reproducible measurements;
- automation must remain auditable and reversible.
