# Single responsibility: reproduce core model-budget and slot tables from released labels.

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "derived" / "paper_tables"


def fact_error_rate(series: pd.Series) -> float:
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return float("nan")
    return float(numeric.mean())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    labels = pd.read_csv(ROOT / "data" / "final_slot_labels.csv")
    labels["presence"] = labels["presence"].astype(float)
    labels["fact_error_numeric"] = pd.to_numeric(labels["fact_error"], errors="coerce")

    summary_cols = ["segment_id", "generator", "budget", "run_id"]
    summary_scores = (
        labels.groupby(summary_cols, dropna=False)
        .agg(
            mean_presence=("presence", "mean"),
            total_presence=("presence", "sum"),
            fact_error_rate=("fact_error_numeric", fact_error_rate),
            n_slots=("slot", "count"),
        )
        .reset_index()
    )
    summary_scores.to_csv(OUT / "summary_scores_reproduced.csv", index=False)

    model_budget = (
        summary_scores.groupby(["generator", "budget"], dropna=False)
        .agg(
            n_segments=("segment_id", "nunique"),
            n_summaries=("run_id", "count"),
            mean_cell_presence_0_1=("mean_presence", "mean"),
            mean_total_presence_0_7=("total_presence", "mean"),
            fact_error_rate=("fact_error_rate", "mean"),
        )
        .reset_index()
    )
    model_budget.to_csv(OUT / "model_budget_results_reproduced.csv", index=False)

    slot_results = (
        labels.groupby(["generator", "budget", "slot"], dropna=False)
        .agg(
            n_cells=("slot", "count"),
            mean_slot_presence_0_1=("presence", "mean"),
            strict_presence_rate=("presence", lambda s: float((s == 1.0).mean())),
            partial_presence_rate=("presence", lambda s: float((s == 0.5).mean())),
            zero_presence_rate=("presence", lambda s: float((s == 0.0).mean())),
            fact_error_rate=("fact_error_numeric", fact_error_rate),
        )
        .reset_index()
    )
    slot_results.to_csv(OUT / "slot_results_reproduced.csv", index=False)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
