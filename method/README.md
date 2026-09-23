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
