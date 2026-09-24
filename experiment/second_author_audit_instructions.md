# Second-Author Presence Audit Instructions

You are performing a blind reliability audit for SIEVE Presence labels.
Your task is Presence-only.
Do not judge overall summary quality.
Do not judge factual correctness.
Do not use the summary's factual errors to lower Presence unless the slot
information itself is not expressed.

For each case, read:
1. the summary under review,
2. the selected slot definition,
3. the Topic Gate,
4. the Quality Gate,
5. the slot-local source context.

Presence labels:
- 0.0: Topic Gate fails.
- 0.5: Topic Gate passes, but Quality Gate fails.
- 1.0: Topic Gate and Quality Gate both pass.

Please fill:
- second_topic_gate_passed: true / false
- second_quality_gate_satisfied: true / false
- second_presence: 0.0 / 0.5 / 1.0
- second_rationale: one or two English sentences
- second_notes: optional

Important:
Presence and Fact Check are separate.
A summary can receive Presence = 1.0 even if a number, date, procedural stage,
actor, code, or value is factually wrong.
Factual correctness is handled separately and should not lower Presence by itself.
If the case feels ambiguous, choose the best label under the provided gates and
write the ambiguity in second_notes.
Do not revise the rubric during adjudication.
