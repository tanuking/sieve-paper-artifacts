# Paper tables

Source data for the tables and reported statistics in the paper.
Files join to `../main_experiment/slot_labels.csv` and
`../../experiment/generated_summaries.csv` on
(segment_id, generator, budget, run_id) where applicable.

- `model_budget_results.csv` — Presence by generator x sentence budget
  (Section 4.1).
- `slot_results.csv` — per-slot Presence by generator x budget
  (Section 4.2).
- `slot_mean_presence_ci.csv` — slot mean Presence with meeting-level
  bootstrap 95% CIs (Section 4.2).
- `slot_mean_presence_contrast_ci.csv` — slot contrasts (e.g. T - U)
  with bootstrap CIs (Section 4.2).
- `jaccard_strict_vs_loose.csv` — across-run slot-set stability
  (Section 4.4).
- `external_similarity_correlations.csv` — global correlations between
  reference-similarity metrics and SIEVE scores (Section 4.5).
- `external_similarity_within_meeting_spearman.csv` — within-meeting
  rank correlations for the same metric pairs (Section 4.5).
- `reference_similarity_metrics.csv` — per-summary ROUGE-L, BERTScore,
  and embedding-cosine values for all 2,250 summaries. These are the
  precomputed metric values behind Section 4.5; shipping them avoids
  requiring the heavyweight metric models for recomputation.
- `heterogeneity_results.csv` — Presence and diagnostics cut by public
  body, decision type, length bin, and segment type (robustness
  reporting in Sections 4.2 and 5).

## appendix/

Source data for the appendix tables and worked examples:
inter-annotator agreement breakdowns from the second-author audit
(`iaa_*.csv`), the BERTScore mechanism check
(`bertscore_mechanism_check.csv`), and the full texts behind the
worked examples (`b_severe_disagreement_cases_full.csv`,
`d_b_background_examples.csv`, `external_similarity_case_studies.csv`).
