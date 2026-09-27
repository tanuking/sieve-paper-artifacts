# Known issues

## O-gate stage-leniency clause and pre-session boilerplate

The Outcome (O) Topic Gate deliberately does not require the exact
procedural stage to be correct: a recognizable disposition tied to an
acted-on item passes Presence even when the stage is wrong, and stage
accuracy is evaluated in Fact Check (`method/presence_gates.md`). The
design intent of this leniency is tolerance for stage-description
drift in **generated summaries of the sampled session**.

When the same gates are applied to text drafted **before** the session
— such as MeetingBank's dataset-provided reference summaries, which
for 45 of the 50 sampled meetings are pre-session agenda captions
(`results/reference_summary_evaluation/reference_types.csv`) — the
leniency can over-credit prior-stage boilerplate: committee
filing-approval lines ("approved filing ... at its meeting on ...")
and clerk-drafted recommendation wording ("Recommendation to declare
... adopted") can read as in-session dispositions. In the released
reference evaluation this shows up as the LLM judges crediting O and B
on such captions where the human labels do not (compare
`llm_judge_labels.csv` with `human_final_labels.csv`; the
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
