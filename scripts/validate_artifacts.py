# Single responsibility: validate released SIEVE paper artifact schemas and counts.

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SLOTS = {"T", "O", "B", "N", "L", "S", "U"}
PRESENCE_VALUES = {0.0, 0.5, 1.0}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--appendix-only", action="store_true")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_appendix() -> None:
    appendix_dir = ROOT / "results" / "appendix_tables"
    require(appendix_dir.exists(), "missing results/appendix_tables")
    require(any(appendix_dir.glob("appendix_*.csv")), "no appendix CSV files found")
    require(any(appendix_dir.glob("appendix_*.md")), "no appendix Markdown files found")


def validate_core() -> None:
    manifest = pd.read_csv(ROOT / "experiment" / "sampling_manifest.csv")
    summaries = pd.read_csv(ROOT / "data" / "generated_summaries.csv")
    labels = pd.read_csv(ROOT / "data" / "final_slot_labels.csv")
    iaa = pd.read_csv(ROOT / "data" / "iaa_v1_presence_audit.csv")

    require(len(manifest) == 50, f"expected 50 manifest rows, got {len(manifest)}")
    require(manifest["uid"].nunique() == 50, "manifest uid values must be unique")

    require(len(summaries) == 2250, f"expected 2,250 summaries, got {len(summaries)}")
    summary_keys = ["segment_id", "generator", "budget", "run_id"]
    require(
        summaries[summary_keys].drop_duplicates().shape[0] == 2250,
        "summary keys are not unique",
    )

    require(len(labels) == 15750, f"expected 15,750 slot cells, got {len(labels)}")
    label_keys = ["segment_id", "generator", "budget", "run_id", "slot"]
    require(labels[label_keys].drop_duplicates().shape[0] == 15750, "label keys are not unique")
    require(set(labels["slot"]) == SLOTS, "slot set mismatch")
    presence_values = set(labels["presence"].dropna().astype(float))
    require(presence_values.issubset(PRESENCE_VALUES), "bad presence value")
    slots_per_summary = labels.groupby(summary_keys)["slot"].nunique()
    require((slots_per_summary == 7).all(), "not all summaries have 7 slots")

    fact_check = labels["fact_check"]
    require(
        fact_check[labels["presence"].astype(float) == 0.0].isna().all(),
        "Fact Check must be blank when Presence is 0.0",
    )
    present_fact_check = fact_check[labels["presence"].astype(float) > 0.0].dropna()
    require(set(present_fact_check.astype(float)).issubset({0.0, 1.0}), "bad Fact Check value")

    require(len(iaa) == 200, f"expected 200 IAA rows, got {len(iaa)}")
    require(set(iaa["slot"]).issubset(SLOTS), "IAA slot set mismatch")
    require(
        set(iaa["first_presence"].astype(float)).issubset(PRESENCE_VALUES),
        "bad first_presence value",
    )
    require(
        set(iaa["second_presence"].astype(float)).issubset(PRESENCE_VALUES),
        "bad second_presence value",
    )

    event_sheets = sorted((ROOT / "experiment" / "event_sheets").glob("MTG*_event_sheet.yaml"))
    rubrics = sorted(
        (ROOT / "experiment" / "slot_local_rubrics").glob("MTG*_slot_local_rubric.yaml"),
    )
    require(len(event_sheets) == 50, f"expected 50 event sheets, got {len(event_sheets)}")
    require(len(rubrics) == 50, f"expected 50 slot-local rubrics, got {len(rubrics)}")


def main() -> None:
    args = parse_args()
    if not args.appendix_only:
        validate_core()
    validate_appendix()
    print("artifact validation passed")


if __name__ == "__main__":
    main()
