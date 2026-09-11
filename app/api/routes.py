from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.agents.orchestrator import analyze_account

app = FastAPI(title="VeloDB Commercial Intelligence OS", version="0.2.0")


class Evidence(BaseModel):
    type: str = Field(pattern="^(observed|hypothesis)$")
    claim: str
    source: str | None = None


class Account(BaseModel):
    company: str
    domain: str | None = None
    dataset_classification: str | None = None
    retrieved_at: str | None = None
    signals: list[str] = []
    commercial_signals: list[str] = []
    evidence: list[Evidence] = []
    buying_committee: list[str] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(payload: Account) -> dict[str, Any]:
    return analyze_account(payload.model_dump())
