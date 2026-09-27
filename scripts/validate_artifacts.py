
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SLOTS = {"T", "O", "B", "N", "L", "S", "U"}
PRESENCE_VALUES = {0.0, 0.5, 1.0}

# Experimental design (Section 3.3 of the paper).
N_MEETINGS = 50
N_GENERATORS = 3
N_BUDGETS = 3
N_RUNS = 5
N_SUMMARIES = N_MEETINGS * N_GENERATORS * N_BUDGETS * N_RUNS  # 2,250
N_CELLS = N_SUMMARIES * len(SLOTS)  # 15,750
N_AUDIT_CELLS = 200  # second-author audit: random 100 + hard 100
N_REFERENCE_CELLS = N_MEETINGS * len(SLOTS)  # 350


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tables-only", action="store_true")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_tables() -> None:
    tables_dir = ROOT / "results" / "paper_tables"
    require(tables_dir.exists(), "missing results/paper_tables")
    for name in [
        "model_budget_results.csv",
        "slot_results.csv",
        "slot_mean_presence_ci.csv",
        "slot_recovery_ratio_by_slot.csv",
        "reference_similarity_metrics.csv",
    ]:
        require((tables_dir / name).exists(), f"missing paper table {name}")
    require((tables_dir / "appendix").exists(), "missing results/paper_tables/appendix")
    require(
        any((tables_dir / "appendix").glob("*.csv")),
        "no appendix CSV files found",
    )


def validate_core() -> None:
    manifest = pd.read_csv(ROOT / "experiment" / "sampling_manifest.csv")
    summaries = pd.read_csv(ROOT / "experiment" / "generated_summaries.csv")
    labels = pd.read_csv(ROOT / "results" / "main_experiment" / "slot_labels.csv")
    audit = pd.read_csv(
        ROOT / "results" / "second_author_audit" / "second_author_audit_labels.csv",
    )

    require(len(manifest) == N_MEETINGS, f"expected {N_MEETINGS} manifest rows, got {len(manifest)}")
    require(manifest["uid"].nunique() == N_MEETINGS, "manifest uid values must be unique")

    require(len(summaries) == N_SUMMARIES, f"expected {N_SUMMARIES} summaries, got {len(summaries)}")
    summary_keys = ["segment_id", "generator", "budget", "run_id"]
    require(
        summaries[summary_keys].drop_duplicates().shape[0] == N_SUMMARIES,
        "summary keys are not unique",
    )

    require(len(labels) == N_CELLS, f"expected {N_CELLS} slot cells, got {len(labels)}")
    label_keys = ["segment_id", "generator", "budget", "run_id", "slot"]
    require(labels[label_keys].drop_duplicates().shape[0] == N_CELLS, "label keys are not unique")
    require(set(labels["slot"]) == SLOTS, "slot set mismatch")
    presence_values = set(labels["final_presence"].dropna().astype(float))
    require(presence_values.issubset(PRESENCE_VALUES), "bad final_presence value")
    slots_per_summary = labels.groupby(summary_keys)["slot"].nunique()
    require((slots_per_summary == len(SLOTS)).all(), "not all summaries have 7 slots")

    fact_check = labels["final_fact_check"]
    require(
        fact_check[labels["final_presence"].astype(float) == 0.0].isna().all(),
        "Fact Check must be blank when Presence is 0.0",
    )
    present_fact_check = fact_check[labels["final_presence"].astype(float) > 0.0].dropna()
    require(set(present_fact_check.astype(float)).issubset({0.0, 1.0}), "bad Fact Check value")

    require(len(audit) == N_AUDIT_CELLS, f"expected {N_AUDIT_CELLS} audit rows, got {len(audit)}")
    require(set(audit["slot"]).issubset(SLOTS), "audit slot set mismatch")
    require(
        set(audit["first_presence"].astype(float)).issubset(PRESENCE_VALUES),
        "bad first_presence value",
    )
    require(
        set(audit["second_presence"].astype(float)).issubset(PRESENCE_VALUES),
        "bad second_presence value",
    )

    event_sheets = sorted((ROOT / "experiment" / "event_sheets").glob("MTG*_event_sheet.yaml"))
    rubrics = sorted(
        (ROOT / "experiment" / "slot_local_rubrics").glob("MTG*_slot_local_rubric.yaml"),
    )
    require(
        len(event_sheets) == N_MEETINGS,
        f"expected {N_MEETINGS} event sheets, got {len(event_sheets)}",
    )
    require(
        len(rubrics) == N_MEETINGS,
        f"expected {N_MEETINGS} slot-local rubrics, got {len(rubrics)}",
    )


def validate_reference_evaluation() -> None:
    ref_dir = ROOT / "results" / "reference_summary_evaluation"
    final = pd.read_csv(ref_dir / "human_final_labels.csv")
    first = pd.read_csv(ref_dir / "human_first_pass_labels.csv")
    judges = pd.read_csv(ref_dir / "llm_judge_labels.csv")

    for name, frame in [("final", final), ("first-pass", first), ("judge", judges)]:
        require(
            len(frame) == N_REFERENCE_CELLS,
            f"expected {N_REFERENCE_CELLS} {name} rows, got {len(frame)}",
        )
        require(set(frame["slot"]) == SLOTS, f"{name} slot set mismatch")
        keys = frame[["meeting_dir_name", "slot"]].drop_duplicates()
        require(len(keys) == N_REFERENCE_CELLS, f"{name} keys are not unique")

    types = pd.read_csv(ref_dir / "reference_types.csv")
    require(len(types) == N_MEETINGS, f"expected {N_MEETINGS} reference types, got {len(types)}")

    profile = pd.read_csv(ref_dir / "reference_profile_ci.csv")
    require(set(profile["slot"]) == SLOTS, "reference profile slot set mismatch")


def main() -> None:
    args = parse_args()
    if not args.tables_only:
        validate_core()
        validate_reference_evaluation()
    validate_tables()
    print("artifact validation passed")


if __name__ == "__main__":
    main()
