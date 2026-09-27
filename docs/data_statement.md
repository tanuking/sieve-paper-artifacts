# Data Statement

This repository releases the evaluation instruments, labels, and
analysis tables of the SIEVE paper. It includes MeetingBank segment
identifiers, the dataset-provided reference summaries of the 50
sampled meetings, the 2,250 generated summaries, all SIEVE labels
(machine and human), the per-meeting event sheets and slot-local
rubrics, and the analysis scripts.

Raw MeetingBank transcripts are **not** redistributed. To obtain the
source transcripts, download MeetingBank from its original source and
locate the sampled segments via `experiment/sampling_manifest.csv`
(the `dataset_split`, `dataset_id`, and `uid` columns identify each
MeetingBank row).

The source material consists of public municipal and county council
proceedings in the United States. Speakers are public officials and
members of the public speaking on the record in open government
meetings. The release adds no personal information beyond what the
public dataset already contains.

Licensing: see `LICENSE` (two-tier: data under CC BY-NC-SA 4.0,
code under MIT) and `docs/third_party_licenses.md`.
