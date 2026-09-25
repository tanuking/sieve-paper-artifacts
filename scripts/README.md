# Scripts

All scripts read only the released files in this repository and write
their outputs under `derived/` (gitignored). Requirements: Python 3.11+,
pandas, numpy.

- `validate_artifacts.py` — structural checks on every released data
  file (row counts, key uniqueness, label domains, gate/Fact-Check
  consistency, 50 event sheets and rubrics present).
- `reproduce_tables.py` — derives summary-level aggregates from
  `results/main_experiment/slot_labels.csv` and reproduces the
  model x budget and per-slot tables (verified identical to
  `results/paper_tables/model_budget_results.csv` and
  `slot_results.csv`).
- `bootstrap_ci.py` — meeting-level bootstrap (B=10,000, seed 20260524)
  for slot means and slot contrasts. Reproduces
  `results/paper_tables/slot_mean_presence_ci.csv` and
  `slot_mean_presence_contrast_ci.csv` exactly, including the CI
  endpoints: one resampling draw per iteration is shared across all
  seven slots, meetings are ordered lexicographically by segment_id,
  and the contrasts reuse the same draws.
- `metrics_reference_similarity.py` — joins
  `results/paper_tables/reference_similarity_metrics.csv` with derived
  summary-level aggregates and reproduces the Section 4.3 correlations
  (overall and per budget). It does not recompute ROUGE / BERTScore /
  embedding values themselves; those are shipped precomputed.
- `reference_summary_analysis.py` — recomputes the reference-summary
  evaluation numbers from `results/reference_summary_evaluation/`:
  first-pass vs judge agreement (299/304/294 of 350; 46 flags), the
  Section 4.4 profile with bootstrap CIs (seed 20260521), the
  lenient-reading sensitivity (O 0.040 -> 0.230, B 0.100 -> 0.160),
  the slot-U source-absence exclusion (0.530 -> 0.562), and the
  Appendix E.4 per-segment-type diagnostics.
