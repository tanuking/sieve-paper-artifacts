# Slot-U source-absence adjudication (2026-09-24)

Section 5 of the paper reports that mean U Presence over the generated
summaries moves only from 0.530 to 0.562 when the segments where a
faithful summary cannot earn U credit are excluded, and that U remains
the lowest slot (S is 0.593). This note records which segments those
are and how the classification was decided.

## Criterion

A segment counts as U-unearnable when (a) its event sheet records that
no source-supported pending handling path remained after the segment,
and (b) its slot-local rubric requires a positive pendingness claim for
the U Topic Gate, so a faithful summary cannot pass it.

## Classification of the four candidate segments

Four event sheets record that the primary item did not remain pending.
Three of them are U-unearnable; one is not:

| Segment | Event sheet record | Rubric U gate | Verdict |
|---|---|---|---|
| MTG06 | "No unresolved Council handling remained" (Proclamation 1060 adopted in-session; retirement remarks explicitly noted as not a pending path) | ordinary positive pendingness gate | unearnable |
| MTG11 | "No source-supported unresolved tail remained" (Council Bill 1034 passed; future redevelopment noted as outcome, not pending action) | ordinary positive pendingness gate | unearnable |
| MTG47 | "does not leave a source-supported pending return path" (final motion failed 4-5; petition not granted) | gate itself declares "no source-supported positive pendingness match for this sample" | unearnable |
| MTG15 | main permit did not remain pending (both motions failed, Planning Board denial stood), but conditional future paths were discussed | gate explicitly credits "a correct summary may state that the main permit was not pending" | **earnable** — U here is answerable as a correct no-pending status, so the segment stays in |

## Recomputation

From `../main_experiment/slot_labels.csv`, U rows (final_presence):

- all 50 segments (n = 2,250): mean 0.530
- excluding MTG06 / MTG11 / MTG47 (n = 2,115): mean 0.562
- the three excluded segments' own U means: 0.011 / 0.000 / 0.089

Per-slot means over all 50 segments: T 0.946, O 0.911, N 0.902,
L 0.661, B 0.634, S 0.593, U 0.530 — so U remains the lowest slot
after the exclusion.

## Note on an earlier count

An earlier draft of the paper stated that only one of the 50 segments
records source-side U absence. That count matched only the rubric-level
absence declaration (MTG47); at the event-sheet level the record shows
four segments, and under the earnability criterion above the correct
count is three. The sentence was corrected on 2026-09-24.
