# Event Sheet Protocol v29 — Temporal Status and Slot-Local Source Context

## Scope

This document defines how to build `event_sheet_<meeting_order>.md` from one sampled segment transcript.

The event sheet records source-grounded slot content. It is used by QA authoring and by judge-bundle construction as the source context for the selected slot.

The event sheet does not define scoring rules. It does not write judge instructions.

## Inputs

- sampled segment transcript
- `slot_semantics.json`

`slots.md` is retired as a source document.

## Required output per slot

Each slot entry must include:

- `label`
- `summary`
- `evidence`
- `source_vocabulary`
- `temporal_status`
- `source_context_for_fact_check`
- `answer_locality`
- `marker_presence`

## temporal_status

For each slot, state the time/status of the slot content when it matters.
Use one or more of:

- `already_occurred`
- `currently_existing`
- `completed_in_session`
- `pending_future_handling`
- `future_effect`
- `hypothetical_or_risk`
- `recurring_concern`

This is not a scoring field by itself. It is source context. QA authors decide whether temporal status matters for Presence, Fact Check, or neither.

Example:

```yaml
temporal_status:
  primary: completed_in_session
  notes:
    - S1 was adopted during the committee segment.
    - Full Council action remained pending.
```

## source_context_for_fact_check

For each slot, record source-side facts needed to decide whether a summary contradicts the event sheet.
Do not list every possible wrong summary. Record what the event sheet supports.

Example for O:

```yaml
source_context_for_fact_check:
  actor: committee/body conducting the segment
  procedural_stage: committee-stage recommendation and later handling, not final Council passage
  disposition_result:
    - S1 was adopted.
    - Proposed Ordinance 2021-0185 as amended received a do-pass recommendation.
  acted_on_item:
    - S1
    - Proposed Ordinance 2021-0185 as amended
  vote_result:
    value: 8-0
    attached_to: committee motion / do-pass recommendation
  temporal_status:
    - completed_in_session for committee action
    - pending_future_handling for full Council action
```

Example for N:

```yaml
source_context_for_fact_check:
  payload_content:
    - default ballot placement unless Council specifies an earlier time
    - S1 changes effective-date timing after a valid referendum petition
  numeric_values:
    - value: 90 days
      meaning: ordinance effective-date period after enactment when a valid referendum petition is submitted
    - value: 60 days
      meaning: baseline in the underlying ordinance
    - value: 45 days
      meaning: signed referendum petition filing deadline
  temporal_status:
    - future_effect
```

## Authoring rule

Write event-sheet source context so a later reader can tell:

- what happened;
- what was pending;
- what was future effect;
- what was hypothetical concern;
- what values were attached to what objects or conditions.

Do not optimize the event sheet for a particular judge prompt.
