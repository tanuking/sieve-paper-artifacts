# Single responsibility: compute meeting-level bootstrap CIs for released SIEVE labels.
#
# Reproduces results/paper_tables/slot_mean_presence_ci.csv and
# slot_mean_presence_contrast_ci.csv exactly: one resampling draw per
# bootstrap iteration is shared across all seven slots (meetings ordered
# lexicographically by segment_id: MTG1, MTG10, ...), and the slot
# contrasts reuse the same bootstrap draws.

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "derived" / "bootstrap"
SLOTS = ["T", "O", "B", "N", "L", "S", "U"]
CONTRASTS = [
    "T - U",
    "O - U",
    "N - U",
    "mean(T,O) - U",
    "mean(T,O,N) - mean(B,L,S,U)",
    "mean(T,O,N) - U",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap-b", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260524)
    return parser.parse_args()


def percentile_ci(values: list[float]) -> tuple[float, float]:
    return tuple(np.percentile(values, [2.5, 97.5]).tolist())


def contrast_value(slot_values: dict[str, float], contrast: str) -> float:
    v = slot_values
    if contrast == "T - U":
        return v["T"] - v["U"]
    if contrast == "O - U":
        return v["O"] - v["U"]
    if contrast == "N - U":
        return v["N"] - v["U"]
    if contrast == "mean(T,O) - U":
        return float(np.mean([v["T"], v["O"]]) - v["U"])
    if contrast == "mean(T,O,N) - mean(B,L,S,U)":
        return float(np.mean([v["T"], v["O"], v["N"]]) - np.mean([v["B"], v["L"], v["S"], v["U"]]))
    if contrast == "mean(T,O,N) - U":
        return float(np.mean([v["T"], v["O"], v["N"]]) - v["U"])
    raise ValueError(f"Unknown contrast: {contrast}")


def main() -> None:
    args = parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    labels = pd.read_csv(ROOT / "results" / "main_experiment" / "slot_labels.csv")
    labels["presence"] = labels["final_presence"].astype(float)

    rng = np.random.default_rng(args.seed)
    meeting_slot = (
        labels.groupby(["segment_id", "slot"], as_index=False)
        .agg(presence_sum=("presence", "sum"), n_cells=("presence", "size"))
        .pivot(index="segment_id", columns="slot", values=["presence_sum", "n_cells"])
    )
    meetings = meeting_slot.index.to_numpy()
    presence_sum = {s: meeting_slot[("presence_sum", s)] for s in SLOTS}
    n_cells = {s: meeting_slot[("n_cells", s)] for s in SLOTS}

    boot_values: dict[str, list[float]] = {slot: [] for slot in SLOTS}
    for _ in range(args.bootstrap_b):
        sampled = rng.choice(meetings, size=len(meetings), replace=True)
        for slot in SLOTS:
            numerator = presence_sum[slot].loc[sampled].sum()
            denominator = n_cells[slot].loc[sampled].sum()
            boot_values[slot].append(float(numerator / denominator))

    summary_keys = ["segment_id", "generator", "budget", "run_id"]
    slot_rows = []
    for slot in SLOTS:
        sub = labels[labels["slot"] == slot]
        low, high = percentile_ci(boot_values[slot])
        slot_rows.append(
            {
                "slot": slot,
                "mean_presence": float(sub["presence"].mean()),
                "ci_low": low,
                "ci_high": high,
                "n_meetings": int(sub["meeting_id"].nunique()),
                "n_summaries": int(sub[summary_keys].drop_duplicates().shape[0]),
                "n_cells": int(len(sub)),
                "bootstrap_B": args.bootstrap_b,
                "bootstrap_unit": "meeting_id",
                "seed": args.seed,
            },
        )
    pd.DataFrame(slot_rows).to_csv(OUT / "slot_mean_presence_ci.csv", index=False)

    point_values = {s: float(labels.loc[labels["slot"] == s, "presence"].mean()) for s in SLOTS}
    contrast_rows = []
    for contrast in CONTRASTS:
        boot = [
            contrast_value({s: boot_values[s][i] for s in SLOTS}, contrast)
            for i in range(args.bootstrap_b)
        ]
        low, high = percentile_ci(boot)
        contrast_rows.append(
            {
                "contrast": contrast,
                "estimate": contrast_value(point_values, contrast),
                "ci_low": low,
                "ci_high": high,
                "bootstrap_B": args.bootstrap_b,
                "bootstrap_unit": "meeting_id",
                "seed": args.seed,
                "note": (
                    "Human-final operationalization; do not interpret as "
                    "annotator-independent for B-sensitive contrasts."
                ),
            },
        )
    pd.DataFrame(contrast_rows).to_csv(OUT / "slot_mean_presence_contrast_ci.csv", index=False)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
