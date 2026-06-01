# Data Dictionary

## `manifest_50.csv`

- `main_order`: paper-internal segment order, 1--50.
- `meeting_id`: reconstructed MeetingBank meeting key used for one-segment-per-meeting sampling.
- `uid`: MeetingBank segment identifier.
- `decision_type`: deterministic sampling metadata from the dataset-provided summary.
- `segment_type`: `decision-bearing` or `non-decision`.
- `segment_word_count`: word count of the selected segment transcript.
- `length_bin`: sampling length bin.

## `generated_summaries.csv`

- `segment_id`: paper segment ID (`MTG1`--`MTG50`).
- `meeting_id`: reconstructed MeetingBank meeting key.
- `uid`: MeetingBank segment identifier.
- `generator`: generation profile.
- `budget`: sentence budget label (`budget_02`, `budget_03`, `budget_06`).
- `sentence_budget`: numeric sentence budget.
- `run_id`: stochastic run identifier.
- `generated_summary`: generated candidate summary.
- `meetingbank_reference_summary`: dataset-provided reference summary used only for external-similarity diagnostics.

## `final_slot_labels.csv`

- `segment_id`: paper segment ID.
- `generator`: generation profile.
- `budget`: sentence budget.
- `run_id`: run identifier.
- `slot`: one of `T`, `O`, `B`, `N`, `L`, `S`, `U`.
- `presence`: SIEVE Presence label in `{0.0, 0.5, 1.0}`.
- `fact_check`: slot-local contradiction check. `1` means no contradiction; `0` means contradiction; blank means not applicable (`presence = 0.0`) or unavailable in a small number of adjudicated cells.
- `fact_error`: derived indicator where `1` means `fact_check = 0`; blank when Fact Check is not applicable or unavailable.
- `source_event_sheet_id`: event sheet identifier.
- `reference_summary_id`: MeetingBank `uid`.

## `summary_scores.csv`

- `mean_presence`: mean Presence over seven slots.
- `total_presence`: sum of Presence over seven slots, range 0--7.
- `fact_error_rate`: mean `fact_error` over fact-checked cells.

## `iaa_v1_presence_audit.csv`

V1 pre-discussion blind second-author Presence audit. These labels are used for IAA diagnostics and do not overwrite `final_slot_labels.csv`.
