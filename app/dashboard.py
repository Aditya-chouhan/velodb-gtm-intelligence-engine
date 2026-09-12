import json
from pathlib import Path

import streamlit as st

from app.agents.orchestrator import analyze_account

st.set_page_config(page_title="VeloDB Commercial Intelligence OS", page_icon="⚡", layout="wide")
ROOT = Path(__file__).resolve().parents[1]

st.title("VeloDB Commercial Intelligence OS")
st.caption("Public technical evidence → commercial motion → technical POC → revenue learning")

mode = st.radio(
    "Dataset",
    ["Public observed accounts", "Fictional demo"],
    horizontal=True,
    help="Public accounts are research examples, not claimed opportunities or buying-intent leads.",
)
path = ROOT / "data" / ("real_target_accounts.json" if mode == "Public observed accounts" else "demo_accounts.json")
accounts = json.loads(path.read_text())
results = sorted([analyze_account(a) for a in accounts], key=lambda x: x["score"], reverse=True)

if mode == "Public observed accounts":
    st.warning("Research boundary: technical relevance can justify discovery. It does not prove pain, active evaluation, budget, or willingness to migrate.")
else:
    st.info("Fictional mode demonstrates workflow behavior without making claims about real companies.")

# Executive overview
st.subheader("Executive market view")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Accounts", len(results))
col2.metric("P1", sum(r["score"] >= 75 for r in results))
col3.metric("P2", sum(55 <= r["score"] < 75 for r in results))
col4.metric("Avg. priority", round(sum(r["score"] for r in results) / max(1, len(results)), 1))
col5.metric("Evidence-gated", sum(r["evidence_quality"]["ready_for_outreach"] for r in results))

market_rows = []
for r in results:
    dims = r["score_dimensions"]
    market_rows.append(
        {
            "Account": r["company"],
            "Priority": r["score"],
            "Technical fit": dims["technical_fit"],
            "Pain evidence": dims["pain_evidence"],
            "Timing": dims["timing"],
            "Intent": dims["intent"],
            "Evidence": dims["evidence_quality"],
            "Counter penalty": r["counter_signal_penalty"],
            "Motion": r["opportunity"]["motion"],
        }
    )
st.dataframe(market_rows, use_container_width=True, hide_index=True)

st.divider()
labels = [f"{r['company']} — {r['score']}/100" for r in results]
r = results[labels.index(st.selectbox("Account deep dive", labels))]

header1, header2, header3, header4 = st.columns(4)
header1.metric("Priority score", f"{r['score']}/100")
header2.metric("Confidence", f"{int(r['score_confidence'] * 100)}%")
header3.metric("Counter penalty", f"-{r['counter_signal_penalty']}")
header4.metric("Scoring model", r["scoring_version"])

left, right = st.columns([1.05, 1])
with left:
    st.subheader(r["company"])
    st.write(f"**Priority band:** {r['priority_band']}")
    st.write(f"**Recommended motion:** {r['opportunity']['motion']}")
    if r.get("dataset_classification"):
        st.write(f"**Dataset classification:** {r['dataset_classification']}")

    st.markdown("### Score decomposition")
    for name, value in r["score_dimensions"].items():
        st.write(f"**{name.replace('_', ' ').title()}:** {value}")
        st.progress(min(float(value) / 40.0, 1.0))

    if r.get("matched_counter_signals"):
        st.markdown("### Counter-signals")
        st.caption("These reduce current sales priority without erasing technical relevance.")
        for signal in r["matched_counter_signals"]:
            st.markdown(f"- {signal.replace('_', ' ')}")

    st.markdown("### Observed evidence")
    for e in r["evidence"]:
        if e["type"] == "observed":
            st.markdown(f"- {e['claim']}  \n  Source: {e.get('source', 'missing')}")

    st.markdown("### Hypotheses — discovery required")
    for e in r["evidence"]:
        if e["type"] == "hypothesis":
            st.warning(e["claim"])

with right:
    st.markdown("### Matched technical / timing signals")
    for rule in r["matched_rules"]:
        st.markdown(f"**{rule['dimension'].upper()} · +{rule['points']} · {rule['label']}**  \n{rule['rationale']}")

    st.markdown("### Likely buying committee")
    st.caption("Role model only; no individuals are inferred from this dataset.")
    for role in r.get("buying_committee", []):
        st.markdown(f"- {role}")

    st.markdown("### Commercialization model")
    st.write(f"**{r['commercialization']['stage']} — {r['commercialization']['score']}/100**")
    st.caption(r["commercialization"]["note"])

st.divider()
poc, activation = st.columns([1.15, 1])
with poc:
    st.markdown("## Technical POC blueprint")
    plan = r["poc_plan"]
    st.write(f"**{plan['name']}**")
    st.info(plan["hypothesis"])
    st.write(f"**Dataset guidance:** {plan['dataset']}")
    st.markdown("**Tests**")
    for test in plan["tests"]:
        st.markdown(f"- {test}")
    st.markdown("**Success metrics**")
    for metric in plan["success_metrics"]:
        st.markdown(f"- {metric}")

with activation:
    st.markdown("## Discovery / activation")
    st.markdown("**Talk track**")
    st.info(r["strategy"]["talk_track"])
    st.markdown("**Evidence-grounded opener**")
    st.code(r["outreach"]["linkedin"], language=None)
    st.markdown("**Evidence gate**")
    st.json(r["evidence_quality"])

st.divider()
st.markdown("## What changes with internal VeloDB access")
st.markdown(
    """
- resolve Apache Doris community activity to known accounts with consent and governance;
- add VeloDB Cloud trial activation, data-loaded, repeat-query and multi-user PQL signals;
- join CRM stages, seller activity and partner/co-sell context;
- capture POC benchmarks, technical blockers and competitive outcomes;
- evaluate signal lift against meetings, POCs, pipeline and wins using controls/holdouts;
- recalibrate scoring only after sufficient sample size and human review.
"""
)

st.caption("Independent portfolio system. No private VeloDB telemetry, customer data, pipeline, or revenue outcomes are claimed.")
