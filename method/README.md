# method/ — SIEVE definition

This folder contains the fixed definition of SIEVE: what the seven
information roles (slots) mean, how Presence and Fact Check are scored,
and how the per-meeting evaluation instruments are authored. Everything
here is experiment-independent; the instruments actually authored for
the 50 meetings in this paper are under `../experiment/`.

## Files, in reading order

1. `slot_semantics.json` — canonical semantic definition of the seven
   slots (T, O, B, N, L, S, U), plus the global judging rules
   (gate/value separation, slot-local contradiction-only Fact Check).
   Other documents in this folder refer to this file by name.
2. `presence_gates.md` — the Presence scale (0.0 / 0.5 / 1.0) and the
   Topic Gate / Quality Gate criteria per slot.
3. `fact_check_fields.md` — per-slot fields that Fact Check compares,
   with explicit fail conditions. Fact Check is contradiction-only,
   applied only when Presence > 0.
4. `slot_boundaries.md` — pairwise boundary rules between slots
   ("this slot when / other slot when"). Used for authoring and
   interpretation; the judge does not reclassify content across slots.
5. `event_sheet_authoring_protocol.md` — how a per-meeting event sheet
   is built from the sampled segment transcript. The event sheet is
   the source context that slot-local rubrics and judge bundles are
   built from.
6. `slot_local_rubric_authoring_protocol.md` — how a per-meeting
   slot-local rubric is authored from the completed event sheet and
   `slot_semantics.json`: the fact_check_target schema, numeric and
   temporal-status authoring rules, and the required score examples.
7. `slot_local_rubric_validation_protocol.md` — the checks applied to
   each authored rubric before judge execution, including the
   Presence-leakage scan (Presence gates must not require exact
   source-correct values) and mandatory rendered-prompt inspection.
8. `judge_prompt_template.txt` — the common prompt given to an LLM
   judge for evaluating one summary on one slot. Slot-specific content
   (gates, fact-check target, event-sheet excerpt) is inserted into
   this template from the per-meeting instruments.

## Relation to the experiment folders

- `../experiment/` holds the instantiation of this definition for the
  50 sampled meetings (event sheets, slot-local rubrics) and the
  experimental protocol of the paper's run.
- `../results/` holds the labels and scores produced by applying this
  definition.

## Caveat: the O gate's stage leniency on pre-session text

The Outcome (O) Topic Gate deliberately does not require the exact
procedural stage to be correct: a recognizable disposition tied to an
acted-on item passes Presence even when the stage is wrong, and stage
accuracy is evaluated in Fact Check (`presence_gates.md`). The
design intent of this leniency is tolerance for stage-description
drift in **generated summaries of the sampled session**.

When the same gates are applied to text drafted **before** the session
— such as MeetingBank's dataset-provided reference summaries, which
for 45 of the 50 sampled meetings are pre-session agenda captions
(`../results/reference_summary_evaluation/reference_types.csv`) — the
leniency can over-credit prior-stage boilerplate: committee
filing-approval lines ("approved filing ... at its meeting on ...")
and clerk-drafted recommendation wording ("Recommendation to declare
... adopted") can read as in-session dispositions. In the released
reference evaluation this shows up as the LLM judges crediting O and B
on such captions where the human labels do not (compare
`../results/reference_summary_evaluation/llm_judge_labels.csv` with
`human_final_labels.csv` in the same folder; the
lenient-reading sensitivity in `sensitivity_cells.csv` quantifies the
effect: O 0.040 -> 0.230, B 0.100 -> 0.160).

Scope: this issue is specific to pre-session-drafted input text. A
scan of all generated summaries in the released experiment found zero
occurrences of the prior-stage boilerplate phrasings, so the main
experiment's numbers are unaffected. The paper's reference-summary
results use the human labels, not the judge labels.

Recommendation for reuse: when applying the SIEVE gates to text that
may have been drafted before the evaluated session, restrict the O
gate's stage leniency with a session-locality condition (credit only
dispositions attributable to the evaluated session), as the
adjudication rules used for the released human labels do.
