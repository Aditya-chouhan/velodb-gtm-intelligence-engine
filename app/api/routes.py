from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.agents.orchestrator import analyze_account
app=FastAPI(title="VeloDB GTM Intelligence Engine",version="0.1.0")
class Evidence(BaseModel):
    type:str=Field(pattern="^(observed|hypothesis)$"); claim:str; source:str|None=None
class Account(BaseModel):
    company:str; domain:str|None=None; signals:List[str]=[]; evidence:List[Evidence]=[]; buying_committee:List[str]=[]
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/analyze")
def analyze(payload:Account)->Dict[str,Any]: return analyze_account(payload.model_dump())
