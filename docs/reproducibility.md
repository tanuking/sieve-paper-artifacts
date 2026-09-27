# Reproducibility

The repository is designed so that the paper's reported numbers can be
recomputed from the released files alone. It does not rerun LLM
generation or machine judging: that would require provider credentials,
and the API model IDs are version pointers whose backends change over
time (see the paper's Appendix A for the generation window and model
notes).

- `python3 scripts/validate_artifacts.py` — structural integrity of
  every released data file.
- `python3 scripts/reproduce_tables.py` — the model x budget and
  per-slot tables (Section 4.1).
- `python3 scripts/bootstrap_ci.py` — the slot-mean and slot-contrast
  bootstrap CIs, reproducing the released tables exactly, endpoints
  included (B=10,000, seed 20260524).
- `python3 scripts/metrics_reference_similarity.py` — the
  reference-similarity correlations (Section 4.3), from the shipped
  per-summary metric values.
- `python3 scripts/reference_summary_analysis.py` — the
  reference-summary evaluation numbers (Sections 3.8, 4.4, 5 and
  Appendix E.4).

Outputs are written under `derived/` (not tracked). File integrity can
be checked against `SHA256SUMS` at the repository root. Column-level
definitions for every data file are in `docs/data_dictionary.md`.
