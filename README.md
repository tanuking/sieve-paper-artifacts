# SIEVE paper artifacts

This repository contains the public artifact package for the SIEVE paper.

## What is included

- 50-segment manifest with MeetingBank identifiers and sampling metadata
- Generated summaries for the 50-segment evaluation set
- Human-final slot-level Presence / Fact Check labels
- V1 pre-discussion second-author Presence audit
- SIEVE rubric, prompts, event sheets, and slot-local rubrics
- Paper and appendix analysis tables
- Scripts to validate artifacts and reproduce core paper tables

## What is not included

- Raw MeetingBank transcripts
- API keys or provider request logs
- Non-canonical internal diagnostics and review materials
- Non-public peer-review information

## Reproducing the paper tables

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make validate
make tables
make appendix
```

Generated outputs are written under `derived/` and can be compared with `results/`.

## Data schema

See `data/data_dictionary.md`.

## Citation

See `CITATION.cff`.
