# Event Sheets

One YAML file per sampled meeting (MTG01-MTG50). Each file carries the
segment identification keys (segment_id, meeting_id, uid, decision_type,
segment_type) and the authored event sheet as markdown: per-slot
source-grounded content (summary, evidence, source_vocabulary,
temporal_status, source context for Fact Check).

Event sheets were authored from the sampled segment transcript only,
following `../../method/event_sheet_authoring_protocol.md`. Raw
MeetingBank transcripts are not redistributed; see the sampling manifest
(`../sampling_manifest.csv`) for the MeetingBank row of each meeting.
