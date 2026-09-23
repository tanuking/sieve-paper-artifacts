# Slot-Local Rubric Validation Protocol

## Scope

This document defines how to validate a completed slot-local rubric before judge execution.

Inputs:

- the completed slot-local rubric (`MTG<nn>_slot_local_rubric.yaml`)
- the meeting's event sheet (`MTG<nn>_event_sheet.yaml`)
- `slot_semantics.json`
- rendered judge prompt / check bundle

## Check 1 — Schema

Each slot must contain:

- `slot`
- `label`
- `topic_gate`
- `quality_gate`
- `fact_check_target`
- `score_examples`
- `answer_locality`
- `marker_presence`

`fact_check_target` must contain:

- `fact_check_fields`
- `valid_items`
- optional `fact_check_notes`

## Check 2 — Gate coherence

For every gate item, verify that `match` and `not_match` follow the label meaning in `slot_semantics.json`.
Presence gates must not require source-correctness. Wrong-but-specific summaries should pass Presence and fail Fact Check.

### Check 2.1 — Presence leakage definition

Presence leakage is present when Topic Gate or Quality Gate `match` / `not_match` makes Presence depend on whether an exact stated value is source-correct.

Exact values include:

- code or classification label;
- number, amount, count, threshold, duration, or scalar value;
- vote count or unanimity;
- date, deadline, or baseline;
- procedural stage;
- actor wording;
- exact legal instrument, ordinance number, or named requirement when the gate label only needs the type of facet to be expressed.

These exact values may appear in the event sheet, `slot_local_event_sheet_excerpt`, `fact_check_target.fact_check_fields`, `valid_items`, `fact_check_notes`, and score examples. They may also appear as source context. The validation issue is only when Topic Gate or Quality Gate wording makes the exact source-correct value a condition for Presence.

This is a Presence-leakage failure:

```text
States that the policy move was to change the zoning to U-MS-2.
```

when the Presence label only needs the summary to express a zoning classification change or Main Street / two-story zoning form.

This is not a Presence-leakage failure:

```text
States that the policy move was a zoning classification change toward a Main Street / two-story zoning form.
```

with `U-MS-2` preserved in Fact Check fields, valid_items, notes, or event-sheet context.

### Check 2.2 — PASS / REVIEW / FAIL criteria

Use these criteria for the preflight result.

- `PASS`: Topic Gate and Quality Gate express the required proposition or facet without making exact source-correct values required for Presence.
- `REVIEW`: an exact value appears in `match` / `not_match` and could be read as required for Presence, but the surrounding wording may be intended as illustrative source context.
- `FAIL`: `match` requires an exact source-correct value for Presence, or `not_match` uses a wrong exact value as a Presence-fail reason.

Forbidden Presence-fail reasons include wrong number, wrong code, wrong vote count, wrong date, wrong baseline, wrong stage, wrong actor, wrong legal instrument, or wrong scalar value.

A number or named value can still help Presence when the gate label is about the existence of a value facet, especially in N. In that case, validation should require the wording to check the presence of the facet, not the correctness of the exact value.

### Check 2.3 — Required preflight reporting

Preflight must report a `presence_leakage_scan` for Check 2. The scan should list any reviewed gate item with:

```text
slot
gate
label
status: PASS / REVIEW / FAIL
detected_exact_values
reason
required_action
```

A preflight report cannot mark Check 2 as `PASS` only by saying manual review was performed. If exact values appear in gate `match` / `not_match`, the report must either explain why they are illustrative rather than Presence requirements, or mark the item as `REVIEW` / `FAIL`.

### Check 2.4 — B and L overconstraint

For B, fail validation if the rubric requires an explicit agenda-necessity or "why this came to the meeting today" statement when the summary otherwise expresses agenda-setting background or precipitating context.

For L, fail validation if the rubric requires a named place, named group, or bounded area as a Presence gate. Local anchoring may be diagnostic or a Fact Check field when explicitly stated, but it must not lower Presence by itself.

## Check 3 — Fact Check field coherence

For each slot:

- each `fact_check_field` must exist in that slot's `fact_check_structure`;
- event sheet context must support each field;
- `valid_items` must be source-consistent and not a checklist;
- `fact_check_notes` must not add hidden fields.

## Check 4 — Fact Check simplicity

Fact Check is a contradiction check, not a completeness check.
A summary does not need to reproduce every detail in the event sheet.
Omissions, abstractions, and partial but correct coverage are allowed.
Fact Check = 0 only when the summary explicitly states something that conflicts with the event-sheet context for the selected slot.


Validate that:

- omission is not treated as error;
- incomplete coverage is not treated as error;
- valid_items are not treated as mandatory;
- each Fact Check = 0 example is based on explicit contradiction.

## Check 5 — Conflict pattern coverage

Common contradiction patterns are:

1. wrong number, date, duration, amount, vote count, or threshold;
2. a correct value attached to the wrong meaning, object, condition, baseline, stage, or item;
3. wrong temporal status, such as completed vs pending, already occurred vs future effect, or existing condition vs hypothetical concern;
4. wrong decision, action, disposition, or procedural stage;
5. wrong actor, acted-on item, target, place, group, scope, jurisdiction, or legal instrument;
6. wrong condition, cause, causal direction, exception, or comparison baseline.

These are conflict patterns, not required checklists. Apply them only to explicit claims that bear on the selected slot's fact_check_fields.


The rubric does not need examples for all six patterns.
It must cover the patterns that are plausible for this slot and event sheet.

## Check 6 — Numeric/scalar consistency

When a numeric value matters to a fact_check_field, verify that the event sheet and the rubric make clear:

- the value;
- what the value is attached to;
- any relevant baseline, condition, object, or stage.

Do not validate a summary-wide number audit. Numbers outside the selected slot's `fact_check_fields` cannot make that slot Fact Check = 0.

Numeric/scalar clarity is required for Fact Check and diagnostics. It must not make exact numeric correctness part of Presence unless the gate label is explicitly about the presence of a numeric facet rather than the correctness of the value.

## Check 7 — Temporal status consistency

Verify that the event sheet records temporal status where relevant:

- already occurred;
- currently existing;
- completed in-session;
- pending future handling;
- future effect;
- hypothetical/risk;
- recurring concern.

If temporal status matters to Presence, it must appear in match/not_match.
If it matters to Fact Check, it must be represented through a fact_check_field and event-sheet context.

## Check 8 — Rendered prompt inspection

Rendered prompt inspection is mandatory before execution.
PASS is not allowed if rendered prompt inspection was not performed.

Check that:

- no slot-specific instruction from another slot appears in the prompt;
- global Fact Check rules are rendered from `slot_semantics.json`;
- Step 3 does not restate hardcoded global rules;
- event-sheet excerpt is labeled as reference source context;
- boundary rules are not rendered;
- `fact_check_fields` are visible;
- there is no summary-wide scalar audit instruction;
- Topic Gate / Quality Gate wording in the rendered bundle does not make exact source-correct values a condition for Presence.
