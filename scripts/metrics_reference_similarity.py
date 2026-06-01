# Single responsibility: recompute external-reference similarity correlation tables.

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "derived" / "reference_similarity"
JOINED_NAME = (
    "meeting01_50_budget02_03_06_deepseek_gemini_human_final_"
    "external_reference_similarity_joined.csv"
)
METRICS = ["rougeL_f1", "bertscore_f1", "embedding_cosine"]
TARGETS = ["MeanPresence", "OraclePresence", "FactErrorRate"]


def corr_pair(df: pd.DataFrame, metric: str, target: str) -> dict[str, float | int]:
    clean = df[[metric, target]].dropna()
    if len(clean) < 3 or clean[metric].nunique() < 2 or clean[target].nunique() < 2:
        return {"n": len(clean), "pearson_r": float("nan"), "spearman_r": float("nan")}
    return {
        "n": len(clean),
        "pearson_r": float(clean[metric].corr(clean[target], method="pearson")),
        "spearman_r": float(clean[metric].corr(clean[target], method="spearman")),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    joined = pd.read_csv(ROOT / "results" / "paper_tables" / JOINED_NAME)
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
