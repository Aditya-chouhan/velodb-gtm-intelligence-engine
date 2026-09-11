import json
from pathlib import Path

import streamlit as st

from app.agents.orchestrator import analyze_account

st.set_page_config(page_title="VeloDB Commercial Intelligence OS", page_icon="⚡", layout="wide")
ROOT = Path(__file__).resolve().parents[1]

st.title("VeloDB Commercial Intelligence OS")
st.caption("Evidence-aware account intelligence → motion routing → technical POC strategy → commercialization")

mode = st.radio(
    "Dataset",
    ["Fictional demo", "Public observed accounts"],
    horizontal=True,
    help="Public observed accounts use cited public technical evidence. They are not claimed opportunities or buying-intent leads.",
)
path = ROOT / "data" / ("demo_accounts.json" if mode == "Fictional demo" else "real_target_accounts.json")
accounts = json.loads(path.read_text())
results = sorted([analyze_account(a) for a in accounts], key=lambda x: x["score"], reverse=True)

if mode == "Public observed accounts":
    st.warning("Boundary: a public technology/workload signal can justify research or discovery; it does not prove pain, purchase intent, evaluation status, or willingness to migrate.")
else:
    st.info("Fictional demo mode is safe for testing workflow behavior without making claims about real companies.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Accounts", len(results))
c2.metric("P1 by rubric", sum(r["score"] >= 80 for r in results))
c3.metric("Avg. technical-fit score", round(sum(r["score"] for r in results) / len(results)))
c4.metric("Evidence gate passed", sum(r["evidence_quality"]["ready_for_outreach"] for r in results))

st.divider()
labels = [f"{r['company']} — {r['score']}/100" for r in results]
r = results[labels.index(st.selectbox("Inspect account", labels))]

left, right = st.columns([1.05, 1])
with left:
    st.subheader(r["company"])
    st.progress(r["score"] / 100, text=f"Technical/commercial relevance score: {r['score']}/100")
    st.write(f"**Priority band:** {r['priority_band']}")
    st.write(f"**Recommended motion:** {r['opportunity']['motion']}")
    st.write(f"**Score confidence:** {int(r['score_confidence'] * 100)}%")
    if r.get("dataset_classification"):
        st.write(f"**Dataset classification:** {r['dataset_classification']}")
    st.write(f"**Commercialization model:** {r['commercialization']['stage']} ({r['commercialization']['score']}/100)")

    st.markdown("### Observed evidence")
    for e in r["evidence"]:
        if e["type"] == "observed":
            st.markdown(f"- {e['claim']}  \n  Source: {e.get('source', 'missing')}")

    st.markdown("### Hypotheses — discovery required")
    for e in r["evidence"]:
        if e["type"] == "hypothesis":
            st.warning(e["claim"])

    st.markdown("### Likely buying committee — role model, not identified people")
    for role in r.get("buying_committee", []):
        st.markdown(f"- {role}")

with right:
    st.markdown("### Matched GTM signals")
    for rule in r["matched_rules"]:
        st.markdown(f"**+{rule['points']} — {rule['label']}**  \n{rule['rationale']}")

    st.markdown("### Commercial signal model")
    for signal in r["commercialization"]["matched_signals"]:
        st.markdown(f"**+{signal['points']} — {signal['key']}**  \n{signal['meaning']}")
    st.caption(r["commercialization"]["note"])

st.divider()
poc, activation = st.columns([1.2, 1])
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

st.caption("Independent portfolio prototype. No private VeloDB telemetry, customer data, pipeline, or revenue outcomes are claimed.")
