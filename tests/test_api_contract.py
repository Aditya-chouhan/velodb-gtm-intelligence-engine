import pytest
from pydantic import ValidationError

from app.api.routes import Account, Evidence, health, meta


def test_health_exposes_scoring_version():
    payload = health()
    assert payload["status"] == "ok"
    assert payload["scoring_version"] == "2.0.0"


def test_meta_keeps_research_boundary_explicit():
    payload = meta()
    assert payload["purchase_probability_model"] is False
    assert payload["private_velodb_data_used"] is False


def test_account_defaults_are_isolated_and_counter_signals_supported():
    first = Account(company="A")
    second = Account(company="B")
    first.signals.append("clickhouse")
    assert second.signals == []

    account = Account(company="C", counter_signals=["no_observed_pain"])
    assert account.counter_signals == ["no_observed_pain"]


def test_observed_source_must_be_valid_url_when_present():
    with pytest.raises(ValidationError):
        Evidence(type="observed", claim="Uses ClickHouse", source="not-a-url")
