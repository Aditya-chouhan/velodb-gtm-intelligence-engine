# Apache Doris open-source contribution plan

The goal is to contribute something genuinely useful to Apache Doris, not manufacture a contributor badge for a portfolio.

## Acceptable first-contribution paths

1. **Documentation correction or clarification** discovered while running the workload harness.
2. **Reproducible example improvement** where official steps are correct but an edge case, prerequisite, or error path is undocumented.
3. **Small test / good-first-issue fix** only after reproducing the issue locally and understanding the expected behavior.
4. **Technical content** that teaches a real Doris workload without unverifiable performance claims.

## Process

- run the official quick start and this repository's `benchmark/doris` harness;
- record every setup ambiguity or reproducible failure;
- search existing Apache Doris issues and documentation before opening anything new;
- reproduce against the current supported version;
- prepare the smallest useful patch;
- include evidence and exact reproduction steps;
- follow Apache Doris contribution and documentation conventions;
- never submit a cosmetic/noise PR merely to show contribution activity.

## Portfolio boundary

Until an upstream patch is accepted or otherwise publicly visible, this repository will describe this as a **contribution plan**, not as an Apache Doris contribution.
