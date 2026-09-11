import json
from pathlib import Path

import streamlit as st

from app.agents.orchestrator import analyze_account

st.set_page_config(page_title="VeloDB Commercial Intelligence OS", page_icon="⚡", layout="wide")

DATA = Path(__file__).resolve().parents[1] / "data" / "demo_accounts.json"
accounts = json.loads(DATA.read_text())
results = sorted([analyze_account(a) for a in accounts], key=lambda x: x["score"], reverse=True)

st.title("VeloDB Commercial Intelligence OS")
st.caption("Evidence-aware account intelligence → motion routing → technical POC strategy → commercialization")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Accounts", len(results))
c2.metric("P1 accounts", sum(r["score"] >= 80 for r in results))
c3.metric("Avg. score", round(sum(r["score"] for r in results) / len(results)))
c4.metric("Outreach-ready", sum(r["evidence_quality"]["ready_for_outreach"] for r in results))
c5.metric("Sales-ready PQL", sum(r["commercialization"]["stage"] == "sales-ready PQL" for r in results))

st.divider()
labels = [f"{r['company']} — {r['score']}/100" for r in results]
selected = st.selectbox("Inspect account", labels)
r = results[labels.index(selected)]

left, right = st.columns([1.05, 1])

with left:
    st.subheader(r["company"])
    st.progress(r["score"] / 100, text=f"Opportunity score: {r['score']}/100")
    st.write(f"**Priority:** {r['priority_band']}")
    st.write(f"**Recommended motion:** {r['opportunity']['motion']}")
    st.write(f"**Score confidence:** {int(r['score_confidence'] * 100)}%")
    st.write(f"**Commercialization stage:** {r['commercialization']['stage']} ({r['commercialization']['score']}/100)")

    st.markdown("### Why now — observed evidence")
    for e in r["evidence"]:
        if e["type"] == "observed":
            st.markdown(f"- {e['claim']}  \n  Source: {e.get('source', 'missing')}")

    st.markdown("### Hypotheses — validate in discovery")
    for e in r["evidence"]:
        if e["type"] == "hypothesis":
            st.warning(e["claim"])

    st.markdown("### Buying committee")
    for role in r.get("buying_committee", []):
        st.markdown(f"- {role}")

with right:
    st.markdown("### Matched GTM signals")
    for rule in r["matched_rules"]:
        st.markdown(f"**+{rule['points']} — {rule['label']}**  \n{rule['rationale']}")

    st.markdown("### Commercial intent signals")
    if r["commercialization"]["matched_signals"]:
        for signal in r["commercialization"]["matched_signals"]:
            st.markdown(f"**+{signal['points']} — {signal['key']}**  \n{signal['meaning']}")
    else:
        st.caption("No modeled commercial/product-intent signals for this demo account.")

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
    st.markdown("## Activation")
    st.markdown("**Talk track**")
    st.info(r["strategy"]["talk_track"])
    st.markdown("**Suggested LinkedIn opener**")
    st.code(r["outreach"]["linkedin"], language=None)
    st.markdown("**Evidence gate**")
    st.json(r["evidence_quality"])

st.caption("Demo accounts are fictional. Observed vs. inferred claims are intentionally separated; internal product telemetry is never claimed.")
