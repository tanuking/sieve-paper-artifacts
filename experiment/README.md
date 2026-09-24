# experiment/ — instruments and inputs of the paper's run

This folder holds the instantiation of the SIEVE definition (`../method/`)
for the 50 sampled MeetingBank meetings, and the inputs used to produce
the evaluated summaries.

- `sampling_manifest.csv` — the 50 sampled segments with their
  MeetingBank identifiers, strata, and selection evidence.
- `event_sheets/` — 50 per-meeting event sheets (source-grounded slot
  content, authored from the transcript only).
- `slot_local_rubrics/` — 50 per-meeting evaluation instruments
  (gates, fact-check targets, score examples).
- `generation_prompt.txt` — the prompt used to generate all evaluated
  summaries (identical to the version quoted in the paper's Appendix A).
- `second_author_audit_instructions.md` — instructions given to the
  second author for the blind Presence-only audit.

## Sampling procedure (summary)

Eligible segments (2,500-20,000 transcript words, reference summary of
at least 15 words, one representative segment per meeting = the longest
eligible one) were stratified into decision-bearing / non-decision by
whether the reference summary mentions a motion, resolution, or
ordinance. Within each stratum, candidates were ordered by a random key
drawn with fixed seed 20260322 and selected top-down under a per-body
cap, incremented only when a pass yielded no admissible candidate,
until 25 segments per stratum were fixed (the cap in effect at each
admission is recorded per row). The
`random_key`, `candidate_rank_within_stratum`,
`selection_order_within_stratum`, and `selection_body_cap` columns of
`sampling_manifest.csv` let this selection be re-checked. One meeting
was replaced on 2026-05-19 after a duplicate-meeting check (main_order
3), using the same body-balanced rule.
