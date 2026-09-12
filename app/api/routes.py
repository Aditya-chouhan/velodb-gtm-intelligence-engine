from typing import Any, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl

from app.agents.orchestrator import analyze_account
from app.scoring.scoring import SCORING_VERSION

app = FastAPI(
    title="VeloDB Commercial Intelligence OS",
    version="0.3.0",
    description="Evidence-aware account analysis for technical GTM research and routing.",
)


class Evidence(BaseModel):
    type: Literal["observed", "hypothesis"]
    claim: str = Field(min_length=1)
    source: HttpUrl | None = None


class Account(BaseModel):
    company: str = Field(min_length=1)
    domain: str | None = None
    dataset_classification: str | None = None
    retrieved_at: str | None = None
    signals: list[str] = Field(default_factory=list)
    commercial_signals: list[str] = Field(default_factory=list)
    counter_signals: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    buying_committee: list[str] = Field(default_factory=list)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "scoring_version": SCORING_VERSION}


@app.get("/meta")
def meta() -> dict[str, Any]:
    return {
        "scoring_version": SCORING_VERSION,
        "purpose": "research_and_routing_rubric",
        "purchase_probability_model": False,
        "private_velodb_data_used": False,
    }


@app.post("/analyze")
def analyze(payload: Account) -> dict[str, Any]:
    # model_dump(mode="json") converts HttpUrl values into JSON-safe strings.
    return analyze_account(payload.model_dump(mode="json"))
