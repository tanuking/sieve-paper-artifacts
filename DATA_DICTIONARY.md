# Data Dictionary

Column-level definitions for every released data file. Paths are
relative to the repository root.

## experiment/sampling_manifest.csv (50 rows, one per sampled meeting)

- `main_order`: paper-internal segment number, 1–50 (`MTG<main_order>`
  is the `segment_id` used by every other file).
- `meeting_id`: reconstructed MeetingBank meeting key (body + date),
  used for the one-segment-per-meeting constraint.
- `uid`: MeetingBank segment identifier.
- `dataset_split`, `dataset_id`: the MeetingBank split and row that
  hold the sampled segment.
- `body_code`: public body (six bodies; used by the selection body cap).
- `decision_type`: deterministic sampling metadata derived from the
  dataset-provided summary (`Motion` / `Resolution` / `Ordinance` /
  `Other`).
- `segment_type`: sampling stratum, `decision-bearing` or
  `non-decision`.
- `segment_word_count`, `summary_word_count`: word counts of the
  segment transcript and of the dataset-provided reference summary
  (eligibility: 2,500–20,000 and >= 15).
- `length_bin`: transcript length bin (`2.5k-5k` / `5k-10k` /
  `10k-20k`).
- `random_key`: the fixed-seed random draw (seed 20260322) that
  ordered candidates within each stratum.
- `candidate_rank_within_stratum`, `selection_order_within_stratum`:
  the candidate's position in that ordering and its admission order.
- `selection_body_cap`: the per-stratum body cap in effect when the
  row was admitted (the cap starts low and is raised only when a
  selection pass yields no admissible candidate).

One meeting (main_order 3) was replaced on 2026-05-19 after a
duplicate-meeting check: the original draw contained a second segment
from an already-sampled meeting, and the replacement was selected by
the same body-balanced rule.

## experiment/generated_summaries.csv (2,250 rows, one per summary)

- `segment_id`, `segment_dir`, `meeting_id`, `uid`: segment
  identification (as in the manifest; `segment_dir` is the numbered
  folder name used by the event sheets).
- `generator`: generation profile (`deepseek_reasoning`,
  `deepseek_temp1_chat`, `gemini_2_5_flash_lite`).
- `model_family`, `variant`: generator family and variant labels.
- `budget`: sentence budget (`budget_02` / `budget_03` / `budget_06`).
- `run_id`: run within the condition (`run_01`–`run_05`).
- `sentence_count`, `word_count`: measured length of the generated
  summary.
- `valid_budget_flag`: 1 when `sentence_count` equals the requested
  budget (2,228 of 2,250; the compliance figure in Appendix A).
- `generated_summary`: the summary under evaluation.
- `meetingbank_reference_summary`: the dataset-provided reference
  summary of the meeting (used only for reference-similarity
  diagnostics).

## results/main_experiment/slot_labels.csv (15,750 rows, one per summary x slot)

- `segment_id` … `run_id`: keys as above, plus `segment_type`,
  `decision_type`, `length_bin`, `generation_mode`, `sentence_count`
  copied for convenience.
- `slot`: one of `T O B N L S U`.
- `final_presence`: the adjudicated Presence label in
  `{0.0, 0.5, 1.0}` used in all main analyses.
- `final_fact_check`: the adjudicated Fact Check label; `1` no
  contradiction, `0` contradiction, blank when Presence = 0.0.
- `fact_error`: derived indicator (`1` iff `final_fact_check = 0`).
- `adjudication_source`: `judge_agreement` (12,763 cells) or
  `human_adjudication` (2,987 cells; the 19.0% reported in
  Section 3.8).
- `gpt_5_presence`, `claude_presence`, `gpt_5_fact_check`,
  `claude_fact_check`: the two LLM judges' raw labels.
- `presence_agreement`, `fact_check_agreement`, `tuple_agreement`:
  judge-agreement indicators derived from the raw labels.
- `source_event_sheet_id`: event sheet used (equals `segment_id`).
- `reference_summary_id`: MeetingBank `uid`.

## results/second_author_audit/second_author_audit_labels.csv (200 rows)

- `case_id`: audit case identifier.
- `sample_set`: `random` (slot-stratified, 100) or `hard` (purposive
  diagnostic, 100).
- `sample_reason`: how the cell was selected —
  `slot_stratified_random`, `human_vs_both` (50), `gpt_claude_gap_human_matched`
  (30), or a `boundary:*` heuristic tag (20); this documents the hard-subset
  composition described in Section 3.8.
- `meeting_id`, `meeting_dir_name`, `generator`, `budget`, `run`,
  `slot`, `slot_label`, `source_row_id`: cell identification.
- `first_presence`, `first_fact_check`, `adjudication_source`: the
  first author's final label for the cell and its provenance.
- `gpt_presence`, `claude_presence`: the LLM judges' labels.
- `second_topic_gate_passed`, `second_quality_gate_satisfied`,
  `second_presence`, `second_rationale`, `second_notes`: the second
  author's blind audit entries.
- `presence_distance`, `disagreement_type`: |first − second| and its
  class (`agreement` / `adjacent_disagreement` / `severe_disagreement`).

## results/reference_summary_evaluation/

- `human_first_pass_labels.csv` (350 rows): `batch` (entry batch
  1–13), `meeting_dir_name`, `slot`, `v1_topic_gate`,
  `v1_quality_gate` (1/0/NA), `v1_fact_check` (1/0/NA),
  `flagged_for_reread` (1 for the 46 cells where the first pass
  disagreed with both judges on Presence or both on Fact Check).
- `human_final_labels.csv` (350 rows): `topic_gate`, `quality_gate`,
  `fact_check` as above; `adjudication_status` (`first_pass` when the
  first-pass label stood, `revised_after_reread` when the flagged
  re-read changed it).
- `llm_judge_labels.csv` (350 rows): both judges' Presence and Fact
  Check labels, plus `presence_gap` and `fact_check_disagreement`.
- `reference_types.csv` (50 rows): `reference_type` per meeting
  (`pre_session_text_only`, 45 / `includes_action_line`, 5).
- `sensitivity_cells.csv` (25 rows): the cells credited at 0.5 in the
  lenient-reading sensitivity, with the caption `pattern` that
  triggered crediting.
- `reference_profile_ci.csv` (7 rows): the Section 4.4 table (per-slot
  mean Presence, bootstrap CI, fact-error rate).

## results/paper_tables/reference_similarity_metrics.csv (2,250 rows)

- Keys as in `generated_summaries.csv`.
- `rougeL_precision/recall/f1`: ROUGE-L against the reference summary.
- `bertscore_precision/recall/f1`: BERTScore (`roberta-large`,
  no baseline rescaling).
- `embedding_model`, `embedding_cosine`: sentence-embedding cosine
  (`sentence-transformers/all-mpnet-base-v2`).

The remaining files under `results/paper_tables/` are aggregate tables
whose columns are described in `results/paper_tables/README.md` and
reproduced by the scripts in `scripts/`.
