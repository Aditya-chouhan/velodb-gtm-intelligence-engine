import json
from pathlib import Path
import streamlit as st
from app.agents.orchestrator import analyze_account
st.set_page_config(page_title="VeloDB GTM Intelligence",page_icon="⚡",layout="wide")
DATA=Path(__file__).resolve().parents[1]/"data"/"demo_accounts.json"
accounts=json.loads(DATA.read_text()); results=sorted([analyze_account(a) for a in accounts],key=lambda x:x["score"],reverse=True)
st.title("VeloDB GTM Intelligence Engine"); st.caption("Evidence-aware account prioritization for real-time analytics infrastructure GTM")
c1,c2,c3,c4=st.columns(4); c1.metric("Accounts",len(results)); c2.metric("P1 accounts",sum(r["score"]>=80 for r in results)); c3.metric("Avg. score",round(sum(r["score"] for r in results)/len(results))); c4.metric("Outreach-ready",sum(r["evidence_quality"]["ready_for_outreach"] for r in results))
st.divider(); labels=[f"{r['company']} — {r['score']}/100" for r in results]; selected=st.selectbox("Inspect account",labels); r=results[labels.index(selected)]
left,right=st.columns([1.1,1])
with left:
 st.subheader(r["company"]); st.progress(r["score"]/100,text=f"Opportunity score: {r['score']}/100"); st.write(f"**Priority:** {r['priority_band']}"); st.write(f"**Recommended motion:** {r['opportunity']['motion']}"); st.write(f"**Confidence:** {int(r['score_confidence']*100)}%"); st.markdown("### Why now — observed")
 for e in r["evidence"]:
  if e["type"]=="observed": st.markdown(f"- {e['claim']}  \n  Source: {e.get('source','missing')}")
 st.markdown("### Hypotheses — validate before outreach")
 for e in r["evidence"]:
  if e["type"]=="hypothesis": st.markdown(f"- {e['claim']}")
with right:
 st.markdown("### Matched GTM signals")
 for rule in r["matched_rules"]: st.markdown(f"**+{rule['points']} — {rule['label']}**  \n{rule['rationale']}")
 st.markdown("### Buying committee")
 for role in r.get("buying_committee",[]): st.markdown(f"- {role}")
 st.markdown("### Suggested LinkedIn opener"); st.code(r["outreach"]["linkedin"],language=None); st.markdown("### Talk track"); st.info(r["strategy"]["talk_track"])
