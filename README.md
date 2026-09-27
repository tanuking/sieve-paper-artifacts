# SIEVE paper artifacts

Evaluation instruments, labels, tables, and analysis code for:

> **SIEVE: Slot-wise Evaluation of Information-Role Retention in
> Fixed-Length Meeting Summarization.**
> Jumpei Nagasawa and Seiya Shibayama.
> *Findings of AACL-IJCNLP 2026.*

Paper: to appear in the ACL Anthology (link will be added on
publication).

SIEVE evaluates meeting summaries role by role: for each of seven
information roles (Topic, Outcome, Operative Payload, Background,
Concrete Concern, Shared Concern, Unresolved Tail) it measures whether
the role is retained (Presence) and whether the retained content
contradicts the source (Fact Check).

## Repository layout

- `method/` — the SIEVE definition, independent of any experiment:
  slot semantics, Presence gates, Fact Check fields, slot boundaries,
  the authoring and validation protocols, and the judge prompt
  template.
- `experiment/` — the instantiation for the paper's run: the sampling
  manifest, 50 event sheets, 50 slot-local rubrics, the generation
  prompt, the 2,250 generated summaries, and the second-author audit
  instructions.
- `results/` — SIEVE's outputs: the 15,750 adjudicated slot labels,
  the 200-cell second-author audit, the 350-cell reference-summary
  evaluation, and the source tables behind every number in the paper
  (`results/paper_tables/`).
- `scripts/` — analysis code that recomputes the paper's numbers from
  the released files alone (see `scripts/README.md`).
- `DATA_DICTIONARY.md` — column-level definitions for every data file.

Before applying the gates to text drafted before the evaluated
session, read the caveat at the end of `method/README.md`.

## What is included, and what is not

The release contains MeetingBank segment identifiers, the
dataset-provided reference summaries of the 50 sampled meetings,
transcript quotations inside the event sheets and rubrics, the
generated summaries, and all SIEVE labels (LLM-judge and human). Raw
MeetingBank transcripts are **not** redistributed: obtain MeetingBank
from its original source and locate the sampled segments via the
`dataset_split` / `dataset_id` / `uid` columns of
`experiment/sampling_manifest.csv`.

The source material consists of public municipal and county council
proceedings in the United States; speakers are public officials and
members of the public speaking on the record. The release adds no
personal information beyond what the public dataset already contains.

## Reproducing the paper's numbers

Requirements: Python 3.11+, `pip install -r requirements.txt`.

```
make validate    # structural checks on every released data file
make tables      # Sections 4.1-4.3 tables and bootstrap CIs
make reference   # Sections 3.8, 4.4, 5 and Appendix E.4 numbers
```

`bootstrap_ci.py` reproduces the released CI tables exactly, endpoints
included; `scripts/README.md` states what each script reproduces and
at what precision. Outputs are written under `derived/` (untracked).
Generation and machine judging are not rerun: they require provider
credentials, and the API model IDs are version pointers whose backends
change over time (see the paper's Appendix A). File integrity can be
checked against `SHA256SUMS`.

## Licensing

Two-tier (see `LICENSE`):

- **Data** (everything outside `scripts/`) is released under
  **CC BY-NC-SA 4.0**, because it includes content derived from
  MeetingBank (Hu et al., 2023), which is distributed under
  CC BY-NC-SA 4.0 — the dataset-provided reference summaries and
  transcript quotations in the event sheets and rubrics.
- **Code** (`scripts/`) is released under the **MIT License**.

Shipped metric values (ROUGE-L; BERTScore, `roberta-large`;
sentence-embedding cosine, `all-mpnet-base-v2`) are plain numbers;
users who install the metric libraries to recompute them should follow
those projects' licenses.

## Citation

See `CITATION.cff`.
