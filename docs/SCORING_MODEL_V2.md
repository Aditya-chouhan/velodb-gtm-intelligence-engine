# Scoring Model v2.0.0

The priority score is a **research and routing rubric**, not a purchase-probability model.

Its purpose is to keep five different questions separate:

1. **Technical fit** — is the workload relevant to a VeloDB / Apache Doris motion?
2. **Pain evidence** — is there public evidence of architecture complexity or a problem worth validating?
3. **Timing** — is there a credible reason to investigate now?
4. **Intent** — is there authorized engagement/product evidence? Public technology usage alone is not intent.
5. **Evidence quality** — how well sourced and independently corroborated are the observed facts?

A sixth component, **counter-signal penalty**, reduces current sales priority when public evidence suggests the incumbent is working well or there is no observed pain.

## Formula

```text
priority_score =
    technical_fit        (0–40)
  + pain_evidence         (0–20)
  + timing                (0–15)
  + intent                (0–15)
  + evidence_quality      (0–10)
  - counter_signal_penalty
```

The result is bounded to `0–100`.

## Why this is better than a flat additive score

A company can be an excellent technical fit while still being a poor near-term sales target.

Example:

```text
Technical fit:       38/40
Pain evidence:        0/20
Timing:               0/15
Intent:               8/15
Evidence quality:    10/10
Counter penalty:    -24

Priority:            32/100
```

That result says: **study the account because the workload is highly relevant; do not pretend there is a displacement opportunity yet.**

## Confidence

Confidence is not derived from the number of detected signals.

It increases with:

- source coverage across observed claims;
- independent source corroboration;
- at least two observed pieces of evidence.

This avoids a common failure mode where many weak or duplicated signals create false certainty.

## Counter-signals

Current supported counter-signals include:

| Counter-signal | Meaning |
|---|---|
| `incumbent_meeting_requirements` | public evidence says the current system is satisfying important requirements |
| `recent_successful_migration_to_incumbent` | the company recently chose/migrated to the incumbent |
| `deep_incumbent_investment` | architecture shows meaningful investment around the current platform |
| `no_observed_pain` | no public evidence supports a pain claim |
| `stale_evidence` | evidence is old enough to reduce current-priority confidence |

Counter-signals reduce **priority**, not **technical fit**.

## Governance

Weights are intentionally transparent and versioned.

A production deployment should not tune them by intuition indefinitely. Recalibration should require:

1. sufficient downstream sample size;
2. a stable outcome definition (meeting, POC, opportunity, win, etc.);
3. holdout/control evaluation;
4. false-positive analysis and seller feedback;
5. documented before/after model versions;
6. human approval before production routing changes.

## What v2 still does not claim

- calibrated purchase probability;
- causal relationship between a signal and revenue;
- private VeloDB product intent;
- current dissatisfaction with an incumbent;
- statistical validity from the small public research sample.

Those boundaries are deliberate.
