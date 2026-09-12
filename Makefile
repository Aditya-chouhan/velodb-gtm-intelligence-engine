PYTHON ?= python

.PHONY: install test demo public dashboard api evidence check

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q

demo:
	$(PYTHON) -m app.main --dataset demo

public:
	$(PYTHON) -m app.main --dataset public

dashboard:
	streamlit run app/dashboard.py

api:
	uvicorn app.api.routes:app --reload

evidence:
	$(PYTHON) scripts/refresh_public_evidence.py --check

check: test public
