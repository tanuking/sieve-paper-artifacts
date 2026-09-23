# Slot-Local Rubric Authoring Protocol

## Scope

This document defines how to author a per-meeting slot-local rubric (published as `MTG<nn>_slot_local_rubric.yaml` under `../experiment/slot_local_rubrics/`) for all seven slots from a completed event sheet (`MTG<nn>_event_sheet.yaml` under `../experiment/event_sheets/`).

Use only:

- the completed event sheet;
- `slot_semantics.json`.

## Core concept

Presence is decided by Topic Gate and Quality Gate.
Fact Check is decided by contradiction against the event sheet.

Fact Check is a contradiction check, not a completeness check.
A summary does not need to reproduce every detail in the event sheet.
Omissions, abstractions, and partial but correct coverage are allowed.
Fact Check = 0 only when the summary explicitly states something that conflicts with the event-sheet context for the selected slot.

Presence gates evaluate whether the required gate labels are expressed in the summary. They do not evaluate whether stated values are source-correct. Wrong numbers, codes, vote counts, dates, baselines, stages, actors, or scalar values are Fact Check issues, not Presence issues.

Do not give Presence = 0.5 an independent semantic definition. It remains the mechanical result of Topic Gate pass + Quality Gate fail.


## fact_check_target schema

Use this shape:

```json
{
  "fact_check_fields": ["<field>", "..."],
  "valid_items": ["<source-consistent statement>", "..."],
  "fact_check_notes": ["<optional note>", "..."]
}
```

### fact_check_fields

`fact_check_fields` are the only fields this slot checks in Fact Check.
If a summary says nothing about a field, that is omission, not error.
If a summary explicitly says something about a field, compare it with the event sheet.

### valid_items

`valid_items` are representative correct statements. They are not required checklists.

### fact_check_notes

`fact_check_notes` are explanatory notes only. They do not add fields.
If something should be checked, put it in `fact_check_fields`.

## Fact Check error patterns

Common contradiction patterns are:

1. wrong number, date, duration, amount, vote count, or threshold;
2. a correct value attached to the wrong meaning, object, condition, baseline, stage, or item;
3. wrong temporal status, such as completed vs pending, already occurred vs future effect, or existing condition vs hypothetical concern;
4. wrong decision, action, disposition, or procedural stage;
5. wrong actor, acted-on item, target, place, group, scope, jurisdiction, or legal instrument;
6. wrong condition, cause, causal direction, exception, or comparison baseline.

These are conflict patterns, not required checklists. Apply them only to explicit claims that bear on the selected slot's fact_check_fields.


## Numeric and scalar authoring

A number can help Presence when the existence of a numeric, scalar, threshold, amount, date, or duration facet is a Quality Gate discriminator, especially in N. Fact Check is separate.

Do not use the source-correctness of the stated value as a Presence criterion. For example, a wrong number, wrong zoning code, wrong vote count, wrong baseline, or wrong date must not be used as a Topic Gate or Quality Gate failure by itself.

When a number, date, duration, vote count, threshold, amount, or baseline matters to a `fact_check_field`, make the event-sheet meaning explicit.

Example:

```json
"fact_check_fields": ["payload_content", "payload_scalar_or_baseline"]
```

Then make `valid_items` / `fact_check_notes` or event-sheet context clear enough to distinguish:

- the value;
- what the value is attached to;
- the baseline or condition, if any.

Do not make Fact Check require every number in the event sheet to be mentioned.

## B and L authoring notes

For B, author match / not_match around agenda-setting background or precipitating context: prior event, condition, process, problem, opposition, mediation, revision, failure, deadline, or similar background that shaped the current item or the form in which it was discussed. Do not require an explicit agenda-necessity statement.

For L, author match / not_match around concrete concern content: concern, harm, obstacle, difficulty, loss, risk, or tradeoff. Do not require a named place, named group, or bounded area for Presence. If local anchoring matters, record it as diagnostic context or a Fact Check field when explicitly stated; do not use it to lower Presence.

## Temporal status authoring

For each slot, read the event sheet's `temporal_status`.
If temporal status affects Presence, materialize it in `match` / `not_match`.
If temporal status affects Fact Check, include the relevant field in `fact_check_fields` and explain the source status in `valid_items` or `fact_check_notes`.

Examples:

- L may require an already-occurred, currently-existing, hypothetical/risk, or recurring concrete concern depending on how the event sheet grounds the concern.
- U usually requires pending or unresolved future handling.
- O often checks completed in-session action and may also distinguish later pending handling.
- N may describe future legal or procedural effect.

## Score examples

Use score examples for criteria application only. They do not add rules.
They should include at least:

- Topic fail;
- Topic pass / Quality fail;
- Full correct;
- Wrong-but-specific Fact Check failure.
