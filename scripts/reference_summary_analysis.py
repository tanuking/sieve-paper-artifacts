# numbers from the released files.
#
# Covers: (1) first-pass vs LLM-judge Presence agreement and the flag count
# (Section 3.8); (2) the reference role-retention profile with meeting-level
# bootstrap CIs (Section 4.4; seed 20260521); (3) the lenient-reading
# sensitivity for O and B; (4) the slot-U source-absence exclusion
# (Section 5, 0.530 -> 0.562); (5) the per-segment-type diagnostics of
# Appendix E.4 (U recovery and within-stratum correlations).

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "results" / "reference_summary_evaluation"
OUT = ROOT / "derived" / "reference_summary"
SLOTS = ["T", "O", "B", "N", "L", "S", "U"]
KEYS = ["segment_id", "generator", "budget", "run_id"]
U_UNEARNABLE = {"MTG6", "MTG11", "MTG47"}  # see u_absence_adjudication.md


def presence_from_gates(tg: object, qg: object) -> float:
    if str(tg) in {"0", "0.0"}:
        return 0.0
    return 1.0 if str(qg) in {"1", "1.0"} else 0.5


def agreement() -> pd.DataFrame:
    first = pd.read_csv(REF / "human_first_pass_labels.csv")
    judges = pd.read_csv(REF / "llm_judge_labels.csv")
    merged = first.merge(judges, on=["meeting_dir_name", "slot"], validate="one_to_one")
    merged["v1_presence"] = [
        presence_from_gates(t, q)
        for t, q in zip(merged["v1_topic_gate"], merged["v1_quality_gate"])
    ]
    n = len(merged)
    vs_gpt = int((merged["v1_presence"] == merged["gpt_5_presence"]).sum())
    vs_claude = int((merged["v1_presence"] == merged["claude_presence"]).sum())
    vs_both = int(
        (
            (merged["v1_presence"] == merged["gpt_5_presence"])
            & (merged["v1_presence"] == merged["claude_presence"])
        ).sum(),
    )
    flags = int((merged["flagged_for_reread"] == 1).sum())
    return pd.DataFrame(
        [
            {"quantity": "v1_vs_gpt5_exact", "count": vs_gpt, "n": n, "rate": vs_gpt / n},
            {"quantity": "v1_vs_claude_exact", "count": vs_claude, "n": n, "rate": vs_claude / n},
            {"quantity": "v1_vs_both_exact", "count": vs_both, "n": n, "rate": vs_both / n},
            {"quantity": "flagged_for_reread", "count": flags, "n": n, "rate": flags / n},
        ],
    )


def reference_profile(b: int = 10000, seed: int = 20260521) -> pd.DataFrame:
    final = pd.read_csv(REF / "human_final_labels.csv")
    final["presence"] = [
        presence_from_gates(t, q)
        for t, q in zip(final["topic_gate"], final["quality_gate"])
    ]
    rng = np.random.default_rng(seed)
    rows = []
    for slot in SLOTS:
        values = final.loc[final["slot"] == slot, "presence"].to_numpy()
        idx = rng.integers(0, len(values), size=(b, len(values)))
        means = values[idx].mean(axis=1)
        low, high = np.percentile(means, [2.5, 97.5])
        fc = final.loc[final["slot"] == slot, "fact_check"]
        fc_num = pd.to_numeric(fc, errors="coerce").dropna()
        rows.append(
            {
                "slot": slot,
                "mean_presence": round(float(values.mean()), 3),
                "ci_low": round(float(low), 3),
                "ci_high": round(float(high), 3),
                "fact_error_rate": round(float((fc_num == 0).mean()) if len(fc_num) else 0.0, 3),
                "n_fact_checked": int(len(fc_num)),
                "n_meetings": len(values),
                "bootstrap_B": b,
                "bootstrap_unit": "meeting_id",
                "seed": seed,
            },
        )
    return pd.DataFrame(rows)


def sensitivity() -> pd.DataFrame:
    final = pd.read_csv(REF / "human_final_labels.csv")
    final["presence"] = [
        presence_from_gates(t, q)
        for t, q in zip(final["topic_gate"], final["quality_gate"])
    ]
    cells = pd.read_csv(REF / "sensitivity_cells.csv")
    rows = []
    for slot in ["O", "B"]:
        base = final.loc[final["slot"] == slot, "presence"].mean()
        credited = set(cells.loc[cells["slot"] == slot, "meeting_dir_name"])
        adj = final[final["slot"] == slot].copy()
        adj.loc[adj["meeting_dir_name"].isin(credited), "presence"] = 0.5
        rows.append(
            {
                "slot": slot,
                "final_mean": round(float(base), 3),
                "lenient_mean": round(float(adj["presence"].mean()), 3),
                "n_credited": len(credited),
            },
        )
    return pd.DataFrame(rows)


def u_absence() -> pd.DataFrame:
    labels = pd.read_csv(ROOT / "results" / "main_experiment" / "slot_labels.csv")
    u = labels[labels["slot"] == "U"].copy()
    u["presence"] = u["final_presence"].astype(float)
    kept = u[~u["segment_id"].isin(U_UNEARNABLE)]
    per_slot = labels.copy()
    per_slot["presence"] = per_slot["final_presence"].astype(float)
    slot_means = per_slot.groupby("slot")["presence"].mean()
    return pd.DataFrame(
        [
            {
                "quantity": "u_mean_all_segments",
                "value": round(float(u["presence"].mean()), 3),
                "n_cells": len(u),
            },
            {
                "quantity": "u_mean_excluding_unearnable",
                "value": round(float(kept["presence"].mean()), 3),
                "n_cells": len(kept),
            },
            {
                "quantity": "next_lowest_slot_mean (S)",
                "value": round(float(slot_means["S"]), 3),
                "n_cells": int((per_slot["slot"] == "S").sum()),
            },
        ],
    )


def stratified() -> pd.DataFrame:
    labels = pd.read_csv(ROOT / "results" / "main_experiment" / "slot_labels.csv")
    labels["presence"] = labels["final_presence"].astype(float)
    metrics = pd.read_csv(ROOT / "results" / "paper_tables" / "reference_similarity_metrics.csv")
    rows = []
    for stratum, group in labels.groupby("segment_type"):
        u = group[group["slot"] == "U"]
        cond = u.groupby(["segment_id", "generator", "budget"])["presence"]
        mean_p = cond.mean()
        best5 = cond.max()
        missing = float((1.0 - mean_p).mean())
        recovered = float((best5 - mean_p).mean())
        rows.append(
            {
                "segment_type": stratum,
                "quantity": "u_best_of_5_recovery_ratio",
                "value": round(recovered / missing, 3),
            },
        )
        agg = (
            group.groupby(KEYS)["presence"].mean().reset_index(name="MeanPresence")
        )
        joined = metrics.merge(agg, on=KEYS)
        for metric in ["rougeL_f1", "bertscore_f1", "embedding_cosine"]:
            rows.append(
                {
                    "segment_type": stratum,
                    "quantity": f"pearson_{metric}_vs_mean_presence",
                    "value": round(float(joined[metric].corr(joined["MeanPresence"])), 3),
                },
            )
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    agreement().to_csv(OUT / "first_pass_agreement.csv", index=False)
    reference_profile().to_csv(OUT / "reference_profile_ci_reproduced.csv", index=False)
    sensitivity().to_csv(OUT / "lenient_reading_sensitivity.csv", index=False)
    u_absence().to_csv(OUT / "u_absence_exclusion.csv", index=False)
    stratified().to_csv(OUT / "segment_type_diagnostics.csv", index=False)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
