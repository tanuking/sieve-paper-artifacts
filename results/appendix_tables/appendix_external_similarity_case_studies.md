# External Similarity Case Studies

These cases illustrate why reference similarity is not a substitute for SIEVE.

## low_external_high_sieve: MTG31 / deepseek_reasoning / budget_03 / run_03

- ROUGE-L F1: `0.102`
- BERTScore F1: `0.822`
- Embedding cosine: `0.380`
- MeanPresence: `1.000`
- FactErrorRate: `0.000`

Candidate summary:

> City manager recommended rejecting all bids for a 30-day independent review after auditor raised concerns.   Council approved a compromise motion for a third-party review selected by the city attorney, avoiding contract extension.   The review will examine written protests, verbal allegations, and RFP steps, reporting by June 14th.

Reference summary:

> Recommendation to adopt Specifications No. RFP PW 15-091 and award a contract to USA Waste of California, dba Waste Management, of Long Beach, for recyclable collection services, in an annual amount not to exceed $3,500,000, plus an annual Consumer Price Index adjustment; and authorize City Manager, or designee, to execute all documents necessary to enter into the agreement for the term of July 1, 2016 to June 30, 2026 (ten years), including any necessary amendments thereto regarding the term and/or scope of services.  (Citywide)

Interpretation:

Preserves deliberative role structure despite lexical distance from the reference. Reference similarity under-scores paraphrased role retention.

## high_external_low_sieve: MTG41 / gemini_2_5_flash_lite / budget_02 / run_04

- ROUGE-L F1: `0.364`
- BERTScore F1: `0.911`
- Embedding cosine: `0.753`
- MeanPresence: `0.286`
- FactErrorRate: `0.000`

Candidate summary:

> Council members debated and voted on the proposed 2017-2018 budget and capital program. The committee recommended the budget pass with amendments, and the resolution was adopted.

Reference summary:

> City Council Changes to the 2017-2018 Proposed Budget and the 2017-2022 Proposed Capital Improvement Program.

Interpretation:

Mimics agenda-title or docket wording while omitting role-bearing content. Reference similarity over-scores title-like summaries that drop SIEVE slots.
