PYTHON ?= python3

.PHONY: validate tables reference all

validate:
	$(PYTHON) scripts/validate_artifacts.py

tables:
	$(PYTHON) scripts/reproduce_tables.py
	$(PYTHON) scripts/bootstrap_ci.py
	$(PYTHON) scripts/metrics_reference_similarity.py

reference:
	$(PYTHON) scripts/reference_summary_analysis.py

all: validate tables reference
