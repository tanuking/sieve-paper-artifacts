# Single responsibility: compute meeting-level bootstrap CIs for released SIEVE labels.

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "derived" / "bootstrap"
SLOTS = ["T", "O", "B", "N", "L", "S", "U"]
CONTRASTS = {
    "T_minus_U": (["T"], ["U"]),
    "O_minus_U": (["O"], ["U"]),
    "N_minus_U": (["N"], ["U"]),
    "mean_T_O_minus_U": (["T", "O"], ["U"]),
    "mean_T_O_N_minus_mean_B_L_S_U": (["T", "O", "N"], ["B", "L", "S", "U"]),
    "mean_T_O_N_minus_U": (["T", "O", "N"], ["U"]),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap-b", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260524)
    return parser.parse_args()


def percentile_ci(values: list[float]) -> tuple[float, float]:
    return tuple(np.percentile(values, [2.5, 97.5]).tolist())


def contrast_value(df: pd.DataFrame, left_slots: list[str], right_slots: list[str]) -> float:
    left = df[df["slot"].isin(left_slots)]["presence"].mean()
    right = df[df["slot"].isin(right_slots)]["presence"].mean()
    return float(left - right)


def main() -> None:
    args = parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    labels = pd.read_csv(ROOT / "data" / "final_slot_labels.csv")
    labels["presence"] = labels["presence"].astype(float)
    rng = np.random.default_rng(args.seed)
    meetings = labels["segment_id"].drop_duplicates().to_numpy()
    by_meeting = {meeting: labels[labels["segment_id"] == meeting] for meeting in meetings}

    slot_rows = []
    for slot in SLOTS:
        sub = labels[labels["slot"] == slot]
        boot = []
        for _ in range(args.bootstrap_b):
            sampled = rng.choice(meetings, size=len(meetings), replace=True)
            boot_df = pd.concat([by_meeting[m] for m in sampled], ignore_index=True)
            boot.append(float(boot_df[boot_df["slot"] == slot]["presence"].mean()))
        low, high = percentile_ci(boot)
        slot_rows.append(
            {
                "slot": slot,
                "mean_presence": sub["presence"].mean(),
                "ci_low": low,
                "ci_high": high,
                "n_segments": sub["segment_id"].nunique(),
                "n_cells": len(sub),
                "bootstrap_b": args.bootstrap_b,
                "seed": args.seed,
                "unit": "segment_id",
            },
        )
    pd.DataFrame(slot_rows).to_csv(OUT / "slot_mean_presence_ci.csv", index=False)

    contrast_rows = []
    for name, (left, right) in CONTRASTS.items():
        observed = contrast_value(labels, left, right)
        boot = []
        for _ in range(args.bootstrap_b):
            sampled = rng.choice(meetings, size=len(meetings), replace=True)
            boot_df = pd.concat([by_meeting[m] for m in sampled], ignore_index=True)
            boot.append(contrast_value(boot_df, left, right))
        low, high = percentile_ci(boot)
        contrast_rows.append(
            {
                "contrast": name,
                "estimate": observed,
                "ci_low": low,
                "ci_high": high,
                "bootstrap_b": args.bootstrap_b,
                "seed": args.seed,
                "unit": "segment_id",
            },
        )
    pd.DataFrame(contrast_rows).to_csv(OUT / "slot_mean_presence_contrast_ci.csv", index=False)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
