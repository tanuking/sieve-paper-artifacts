# Presence Gates

Presence uses 0.0 / 0.5 / 1.0 ordinal labels.

- 0.0: Topic Gate fails.
- 0.5: Topic Gate passes, Quality Gate fails.
- 1.0: Topic Gate and Quality Gate pass.

## T: Topic/Framing

T captures the substantive framing of the sampled segment's discussion: the subject of the discussion, the policy direction being pursued, and the target to which that policy direction applies. T is about substantive framing, not procedural disposition.

### topic_gate

Operator: `all_of`

- `subject_identified`: The summary names the substantive subject as a noun or noun phrase identifying the policy area, issue, or matter being discussed. Procedural form, bare agenda labels, motion numbers, or bill identifiers without the substantive subject do not satisfy this label.

### quality_gate

Operator: `all_of`

- `policy_direction`: The summary shows what policy move was being pursued for the subject. This may be a direction-bearing verb such as update, revise, clarify, expand, restrict, launch, phase out, or consolidate. It may also be a concrete rule effect showing how the target would change, such as defaulting, extending, narrowing, broadening, adding, removing, changing a threshold, or changing a deadline. Procedural disposition, such as approved, adopted, recommended, or passed, is not policy direction.
- `target`: The summary identifies the target to which the policy direction applies: the entity, group, area, process, rule set, or scope the direction is aimed at. A bare direction without a target does not satisfy this label.

## O: Outcome/Position

O captures the body's in-session disposition shell: what the body did to an acted-on item during the sampled segment. O asks what the body did and which acted-on item the disposition was tied to. The action's operative payload belongs to N. Unresolved handling after the action belongs to U.

### topic_gate

Operator: `all_of`

- `disposition_verb_tied_to_acted_on_item`: The summary states that the body took a disposition on an acted-on item. Discussion, questioning, support, or hearing activity alone does not satisfy this label. This label does not decide whether the disposition is at the source-supported procedural stage. If a recognizable disposition is tied to an acted-on item, Presence may pass even when the stage is wrong. Stage accuracy is evaluated in Fact Check.

### quality_gate

Operator: `all_of`

- `acted_on_item_specific`: The acted-on item is identified specifically enough that the reader can tell which item was acted on. Formal numbers or labels are sufficient but not required. A substantive description also satisfies this label when it distinguishes the item within the sampled segment. A generic referent alone is not enough.

## B: Agenda-Setting Background / Precipitating Context

B captures prior event, condition, process, problem, opposition, mediation, revision, failure, deadline, or other background that shaped the current item or the form in which it was discussed. B does not require an explicit agenda-necessity statement, and it is not the action itself.

### topic_gate

Operator: `all_of`

- `precipitating_context_visible`: The summary states a prior event, condition, process, problem, opposition, mediation, revision, failure, deadline, or similar background connected to the current item. The context must be stated as its own proposition; it need not include an explicit agenda-necessity statement.

### quality_gate

Operator: `all_of`

- `connected_to_current_item_or_form`: The prior event, condition, process, problem, opposition, mediation, revision, failure, deadline, or similar background is visibly connected to the current item, the form of the proposal, a revision, the discussion frame, or how the item was handled. An explicit “why now” or agenda-necessity statement is not required.

## N: Outcome-Near Condition / Operative Payload

N captures the operative payload carried by the body's action: conditions, requirements, restrictions, scope, numbers, dates, thresholds, or similar content attached to the action beyond the bare fact that the body acted.

### topic_gate

Operator: `all_of`

- `payload_attached_to_action`: The summary expresses a condition, requirement, scope, restriction, number, date, or other payload as attached to the action or acted-on item. Single-sentence attachment and anaphora-linked adjacent sentences count. A free-standing background description that requires the reader to reconstruct the action-payload link does not satisfy this label. A recognizable payload assigned to the wrong actor or stage can pass Presence; the replacement error belongs to Fact Check.

### quality_gate

Operator: `any_of`

- `number`: The attached payload includes an identifiable numeric quantity, such as a count, amount, percentage, duration, height, vote threshold, or other measured value.
- `named_requirement`: The attached payload includes an identifiable named requirement, restriction, condition, or carve-out.
- `scope_boundary`: The attached payload includes an identifiable scope boundary, such as a geographic boundary, categorical boundary, population-specific boundary, or other boundary defining what the payload applies to.
- `date_cutoff`: The attached payload includes an identifiable date cutoff or time boundary, such as an effective date, expiration date, sunset clause, or deadline.

## L: Concrete Concern

L captures a concrete concern, harm, obstacle, difficulty, loss, risk, or tradeoff. A local anchor is not required for Presence. Local anchoring may be recorded as diagnostic context or checked in Fact Check when explicitly stated, but it must not be used to lower Presence by itself.

### topic_gate

Operator: `all_of`

- `concrete_concern_language`: The summary states a concern, harm, obstacle, difficulty, loss, risk, tradeoff, deficiency, shortage, gap, barrier, failure, or similar problem-side condition. The concern must be asserted on the problem/concern side, not merely appear as the object of a solution-side verb. A named place, named group, or bounded area is not required for Presence.

### quality_gate

Operator: `all_of`

- `specific_concern_content`: The concern content is specific enough that the reader can tell what the concern, harm, obstacle, difficulty, loss, risk, or tradeoff is about. A generic statement that concerns were raised, without saying what the concern was, does not satisfy this label. A named place, named group, or bounded area is not required for Presence.

## S: Shared Concern Synthesis

S captures a recurring problem-side concern theme in the discussion. The recurrence is grounded in the event sheet from the transcript. The summary does not need to state recurrence explicitly, but it must name the concern theme in problem-side language.

### topic_gate

Operator: `all_of`

- `problem_side_concern`: The summary names the concern theme in problem-side language: problem, difficulty, deficiency, gap, fragmentation, dissatisfaction, negative state, or similar language. Problem vocabulary that appears only as the object or modifier of a solution-side verb does not satisfy this label. Generic debate language alone does not satisfy it.

### quality_gate

Operator: `all_of`

- `specific_content`: The named concern theme has identifiable concern content. The reader can tell what the concern is about: object of concern, contrast at issue, criticized mechanism, specific tension/tradeoff, or problem content itself. A generic concern label alone does not satisfy this label. The summary does not need to reproduce every downstream risk or evidentiary detail. The judge must not require downstream risk, consequence, or evidence detail beyond what the semantic rule, label meaning, and QA match require.

## U: Unresolved Tail / Future Return Path

U captures what remained unfinished after the body's action: pending handling, later review, future process, unresolved implementation steps, or an explicit return path. U's core is unfinishedness.

### topic_gate

Operator: `all_of`

- `pendingness_marker`: The summary explicitly includes an unfinished, pending, or still-open state marker, such as remained pending, still to be decided, unresolved, remained in committee, held over, or final action remained pending. If the item is identifiable and the summary says it will proceed to a later full-body meeting, final action, final passage, or final consideration, that can satisfy pendingness. A bare directive without an explicit pendingness marker does not satisfy this label.

### quality_gate

Operator: `all_of`

- `pending_item_identifiable`: What specifically remains pending is identifiable. The reader can tell which item, workstream, or issue is unfinished, not merely that something is unfinished.
- `handling_path_visible`: A concrete handling path is visible. This can be a future event path, process path, or institutional custody path. A path to a later full-body meeting, final action, final passage, or final consideration can satisfy this label if the item is identifiable. Bare future orientation does not satisfy it unless tied to an identifiable body, item, custody, review, hearing, or process path. An unrelated future item, post-adjournment announcement, or future hearing for a different item does not satisfy U.
