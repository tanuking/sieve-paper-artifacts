# Reference summary evaluation

Human evaluation of the 50 MeetingBank reference summaries against the
same event sheets and gate definitions as the generated summaries
(350 cells = 50 meetings x 7 slots; paper Sections 3.8 and 4.6).

- `human_final_labels.csv` — the adjudicated final labels (topic gate,
  quality gate, fact check) per cell, with adjudication status and
  working notes.
- `human_first_pass_labels.csv` — the first author's blind first-pass labels
  (V1, judge outputs undisclosed) with the re-read flag. Agreement is
  reported against V1 only: recomputing Presence from these gates
  against `llm_judge_labels.csv` gives 299/350 (85.4%) vs GPT-5, 304/350
  (86.9%) vs Claude, 294/350 (84.0%) vs both, and 46 flagged cells
  (13.1%) — the figures in Section 3.8. One cell (meeting 47, slot U)
  was left blank at entry with a question note and resolved to
  0 / NA / NA under the entry-time question rule.
- `llm_judge_labels.csv` — both LLM judges' Presence and Fact Check labels
  for the same 350 cells.
- `reference_profile_ci.csv` — the per-slot reference profile with
  meeting-level bootstrap 95% CIs (the Section 4.6 table).
- `reference_types.csv` — per-meeting classification of the reference
  summary (45 pre-session text only / 5 include an action line;
  Section 5).
- `sensitivity_cells.csv` — the 25 cells behind the lenient-reading
  sensitivity numbers (crediting boilerplate wording at Presence 0.5
  moves O 0.040 -> 0.230 and B 0.100 -> 0.160): 7 prior-stage filing
  cells, 12 recommendation-wording cells, 6 prior-stage background
  mentions.
- `adjudication_precedents.md` — the precedent ledger used to
  adjudicate boundary cells during the review.
- `u_absence_adjudication.md` — which segments leave no earnable slot-U
  credit on the source side, and the recomputation behind the
  Section 5 robustness sentence (0.530 -> 0.562).
