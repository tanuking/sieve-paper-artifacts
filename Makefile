PYTHON ?= python

.PHONY: validate tables appendix all

validate:
	$(PYTHON) scripts/validate_artifacts.py

tables:
	$(PYTHON) scripts/reproduce_tables.py
	$(PYTHON) scripts/bootstrap_ci.py
	$(PYTHON) scripts/metrics_reference_similarity.py

appendix:
	$(PYTHON) scripts/validate_artifacts.py --appendix-only

all: validate tables appendix
