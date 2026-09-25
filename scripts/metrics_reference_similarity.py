# Single responsibility: recompute reference-similarity correlation tables.
#
# Joins the released per-summary similarity metrics with summary-level
# SIEVE aggregates derived from slot_labels.csv, and reproduces the
# correlations reported in Section 4.3 and Appendix E.2.

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "derived" / "reference_similarity"
KEYS = ["segment_id", "generator", "budget", "run_id"]
METRICS = ["rougeL_f1", "bertscore_f1", "embedding_cosine"]
TARGETS = ["MeanPresence", "FactErrorRate"]


def corr_pair(df: pd.DataFrame, metric: str, target: str) -> dict[str, float | int]:
    clean = df[[metric, target]].dropna()
    if len(clean) < 3 or clean[metric].nunique() < 2 or clean[target].nunique() < 2:
        return {"n": len(clean), "pearson_r": float("nan"), "spearman_r": float("nan")}
    return {
        "n": len(clean),
        "pearson_r": float(clean[metric].corr(clean[target], method="pearson")),
        "spearman_r": float(clean[metric].corr(clean[target], method="spearman")),
    }


def summary_aggregates() -> pd.DataFrame:
    labels = pd.read_csv(ROOT / "results" / "main_experiment" / "slot_labels.csv")
    labels["presence"] = labels["final_presence"].astype(float)
    labels["fact_error_numeric"] = pd.to_numeric(labels["fact_error"], errors="coerce")
    return (
        labels.groupby(KEYS, dropna=False)
        .agg(
            MeanPresence=("presence", "mean"),
            FactErrorRate=("fact_error_numeric", lambda s: float(s.dropna().mean())),
        )
        .reset_index()
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    metrics = pd.read_csv(ROOT / "results" / "paper_tables" / "reference_similarity_metrics.csv")
    joined = metrics.merge(summary_aggregates(), on=KEYS, validate="one_to_one")

    rows = []
    for metric in METRICS:
        for target in TARGETS:
            rows.append({"metric": metric, "target": target, **corr_pair(joined, metric, target)})
    pd.DataFrame(rows).to_csv(OUT / "external_similarity_correlations_reproduced.csv", index=False)

    per_budget_rows = []
    for budget, sub in joined.groupby("budget"):
        for metric in METRICS:
            for target in TARGETS:
                per_budget_rows.append(
                    {
                        "budget": budget,
                        "metric": metric,
                        "target": target,
                        **corr_pair(sub, metric, target),
                    },
                )
    pd.DataFrame(per_budget_rows).to_csv(
        OUT / "external_similarity_correlations_by_budget_reproduced.csv",
        index=False,
    )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
