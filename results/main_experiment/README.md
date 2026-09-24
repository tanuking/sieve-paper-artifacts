# Main experiment results

`slot_labels.csv` — one row per summary x slot (15,750 cells: 2,250
summaries x 7 slots). `final_presence` and `final_fact_check` are the
adjudicated labels used in all main analyses; the file also carries
both judges' raw labels and `adjudication_source` (12,763
judge-agreement cells, 2,987 human-adjudicated cells).

Rows join to `../../experiment/generated_summaries.csv` on
(segment_id, generator, budget, run_id), and to the instruments in
`../../experiment/` via segment_id / uid. Summary-level aggregates
(mean Presence per summary, fact-error rates) are derived from this
file by the analysis scripts rather than shipped separately.
