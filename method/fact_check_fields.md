# Fact Check Fields

Fact Check is a contradiction-only slot-local check and is applied only when Presence > 0.

## T: Topic/Framing

- `subject`: Compare the substantive subject stated by the summary with the source-supported subject. Fail condition: Fact Check = 0 if the summary explicitly states a different policy area, issue, or matter as the subject.
- `policy_direction`: Compare the policy direction stated by the summary with the source-supported direction. Fail condition: Fact Check = 0 if the summary explicitly states a direction that reverses or replaces the source-supported policy move.
- `target`: Compare the target stated by the summary with the source-supported target. Fail condition: Fact Check = 0 if the summary explicitly states a different entity, group, area, process, jurisdiction, or scope as the target.

## O: Outcome/Position

- `actor`: If the summary explicitly states an acting body or actor, compare that actor with the source-supported actor. Actor is separate from procedural stage. A broad institutional label alone is not a stage replacement when surrounding context preserves the source-supported stage. Omitting the actor alone is not a Fact Check error. Fail condition: Fact Check = 0 if the summary explicitly attributes the disposition to a different actor or body than the source supports.
- `procedural_stage`: If the summary states or clearly implies where the acted-on item stands in the institutional processing path, compare that procedural stage with the source-supported stage. Stage is separate from actor and disposition result. Examples of stages include committee recommendation, referral, first reading, final body passage, enactment, ballot placement, voter approval, and later scheduled handling. Fail condition: Fact Check = 0 if the summary explicitly states or clearly implies that the acted-on item reached a procedural stage different from the source-supported stage. This includes stating that a body completed a later legal, electoral, or administrative effect when the source supports only recommendation, referral, advancement, or another earlier-stage action.
- `disposition_result`: Compare the result the summary says occurred at the stated or implied stage with the source-supported result. Result is separate from procedural stage: recommended, adopted, referred, rejected, deferred, passed, enacted, and similar verbs can describe different results depending on stage. Fail condition: Fact Check = 0 if the summary explicitly states a result different from the source-supported result for the same acted-on item and stage.
- `acted_on_item`: Compare the acted-on item stated by the summary with the source-supported acted-on item. Fail condition: Fact Check = 0 if the summary explicitly states a different ordinance, motion, amendment, appointment, resolution, agenda item, or other acted-on item than the source supports.
- `vote_result`: If the summary states a vote count, unanimity, passed/failed vote result, or attaches a vote result to a disposition, compare both the value and the disposition/stage it is attached to against the event-sheet source context. Fail condition: Fact Check = 0 if the summary states a different vote result, attaches a source-supported vote result to the wrong disposition or procedural stage, or states the vote result with materially ambiguous attachment to the acted-on action.

## B: Agenda-Setting Background / Precipitating Context

- `trigger_condition`: Compare the prior event, condition, process, problem, opposition, mediation, revision, failure, deadline, or other background stated by the summary with the source-supported background for the item. Fail condition: Fact Check = 0 if the summary explicitly states a different prior event, condition, process, problem, opposition, mediation, revision, failure, deadline, affected process, or triggering background than the source supports.
- `agenda_connection`: If the summary states the relation between the background context and the current item, compare that relation with the source-supported relation. Fail condition: Fact Check = 0 if the summary reverses the relation or explicitly states a different reason or background relation for why the current item took its form or came forward.

## N: Outcome-Near Condition / Operative Payload

- `payload_carrier`: Compare which action, ordinance, motion, amendment, resolution, or acted-on item the summary attaches the payload to with the source-supported carrier. Fail condition: Fact Check = 0 if the summary attaches the payload to a different action or item than the source supports.
- `payload_content`: Compare the requirement, condition, restriction, permission, rule, or operative content stated by the summary with the source-supported payload content. Fail condition: Fact Check = 0 if the summary explicitly states different operative payload content than the source supports.
- `payload_scope`: If the summary states the payload's applicable scope, category, population, geography, process, or target, compare it with the source-supported scope. Fail condition: Fact Check = 0 if the summary explicitly states a different scope or target for the payload than the source supports.
- `payload_scalar_or_baseline`: If the summary states a number, date, duration, threshold, amount, deadline, or baseline comparison attached to the payload, compare both value and role binding. Fail condition: Fact Check = 0 if the summary states a wrong value, attaches a correct value to the wrong payload role, states an unsupported baseline, or makes the scalar role binding materially ambiguous.

## L: Concrete Concern

- `obstacle_content`: Compare the concern, harm, obstacle, difficulty, loss, risk, tradeoff, constraint, or problem stated by the summary with the source-supported concern content. Fail condition: Fact Check = 0 if the summary explicitly states a different concern, harm, obstacle, difficulty, loss, risk, tradeoff, or constraint than the source supports.
- `local_anchor`: If the summary explicitly ties the concern to a named place, named group, bounded area, or other local anchor, compare that anchor with the source-supported local anchor. Local anchor is not required for Presence. Fail condition: Fact Check = 0 if the summary explicitly states a different named place, named group, bounded area, or local anchor for the concern than the source supports.

## S: Shared Concern Synthesis

- `concern_theme`: Compare the recurring concern theme stated by the summary with the source-supported concern theme. Fail condition: Fact Check = 0 if the summary explicitly states a different concern theme than the source supports.
- `concern_content`: If the summary states the concern's object, contrast, mechanism, tension, tradeoff, risk, consequence, affected group, or scope, compare it with the source-supported concern content. Fail condition: Fact Check = 0 if the summary explicitly states different concern content, such as a different object, contrast, mechanism, risk, affected group, or scope, than the source supports.

## U: Unresolved Tail / Future Return Path

- `pending_status`: Compare the unfinished, pending, or resolved status stated by the summary with the source-supported status. Fail condition: Fact Check = 0 if the summary explicitly states a resolved or completed status for a source-supported pending item, or a pending status for a source-supported completed item.
- `pending_item`: Compare what the summary says is pending with the source-supported pending item. Fail condition: Fact Check = 0 if the summary explicitly states a different item, issue, workstream, ordinance, motion, or follow-up object as pending.
- `handling_path`: If the summary states a future meeting, body, committee, process, report-back, review, drafting, or custody path, compare it with the source-supported handling path. Fail condition: Fact Check = 0 if the summary explicitly states a handling path, body, process, date, destination, or custody path different from the source-supported path.
