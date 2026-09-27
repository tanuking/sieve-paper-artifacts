# Third-Party Licenses and Redistribution Notes

- **MeetingBank** (Hu et al., 2023) is distributed under
  **CC BY-NC-SA 4.0**. This repository redistributes MeetingBank-derived
  content — the dataset-provided reference summaries, and transcript
  quotations inside the event sheets and slot-local rubrics — and
  therefore releases all data files under CC BY-NC-SA 4.0 as well
  (see `LICENSE`). Raw transcripts are not redistributed; obtain them
  from the original MeetingBank release and verify its license terms
  before redistributing additional source content.
- **LLM provider outputs**: the generated summaries are redistributed
  as research artifacts for reproducibility. No API keys, request IDs,
  or private provider logs are included.
- **Metric libraries**: the repository ships computed ROUGE-L,
  BERTScore (`roberta-large`), and sentence-embedding
  (`all-mpnet-base-v2`) values as tables. Users who install the metric
  libraries to recompute them should follow those projects' licenses.
- **Code**: the scripts in `scripts/` are released under the MIT
  License (see `LICENSE`).
