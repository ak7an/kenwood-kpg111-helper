#!/usr/bin/env python3
"""Plan a read-only merge of CSV records into decoded KPG111 tables."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.imports import load_import_csvs
from kpg111.planner import MergePlan, PlannedAction, plan_merge


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan a CSV merge into KPG111 tables without modifying Program.dat."
    )
    parser.add_argument("dat_file", type=Path, help="Path to Program.dat")
    parser.add_argument("imports", nargs="+", type=Path, help="CSV import file(s)")
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        required=True,
        help="XOR byte used to decode Program.dat tables",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "csv"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--include-existing",
        action="store_true",
        help="Include exact duplicates in the action list.",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=1024,
        help="Maximum records to scan per table (default: 1024)",
    )
    return parser.parse_args()


def markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(row) + " |")


def summary_counts(plan: MergePlan) -> Counter[str]:
    return Counter(action.action for action in plan.actions)


def render_markdown(dat_file: Path, decode_key: int, import_paths: list[Path], plan: MergePlan) -> None:
    counts = summary_counts(plan)
    print("# KPG111 Merge Plan")
    print()
    print("This is a read-only planning report. Candidate slots are suggestions based on observed table behavior and must be validated by KPG111 before any generated file is used.")
    print()
    print("No Program.dat bytes were generated or modified.")
    print()
    print(f"- Program.dat: `{dat_file}`")
    print(f"- Decode key: `0x{decode_key:02x}`")
    print(f"- Imports: {', '.join(f'`{path}`' for path in import_paths)}")
    print()

    print("## Summary")
    rows = [
        ["Exact duplicates", str(counts.get("duplicate_exact", 0))],
        ["Possible updates", str(counts.get("possible_update", 0))],
        ["Name conflicts", str(counts.get("duplicate_name_id_diff", 0))],
        ["Candidate new records", str(counts.get("new_record", 0))],
        ["Invalid rows", str(counts.get("invalid", 0))],
    ]
    markdown_table(["Metric", "Count"], rows)
    print()

    render_action_section("Existing / Ignored", plan, {"duplicate_exact"})
    render_action_section("Candidate New Records", plan, {"new_record"})
    render_action_section("Possible Updates", plan, {"possible_update"})
    render_action_section("Conflicts", plan, {"duplicate_name_id_diff"})
    render_action_section("Invalid Rows", plan, {"invalid"})

    print("## Capacity / Slot Utilization")
    rows = [
        ["Individual ID empty slots available", str(plan.empty_slots_available["individual_ids"])],
        ["Talk Group empty slots available", str(plan.empty_slots_available["talk_groups"])],
        ["Individual ID candidate append slots needed", str(plan.append_slots_needed["individual_ids"])],
        ["Talk Group candidate append slots needed", str(plan.append_slots_needed["talk_groups"])],
    ]
    markdown_table(["Metric", "Count"], rows)


def render_action_section(title: str, plan: MergePlan, actions: set[str]) -> None:
    print(f"## {title}")
    markdown_table(
        [
            "Table",
            "Action",
            "Recommended Action",
            "Source Row",
            "Name",
            "Numeric ID",
            "Candidate Slot",
            "Candidate Offset",
            "Reason",
        ],
        [
            [
                action.table,
                action.action,
                action.recommended_action,
                f"{action.source_file}:{action.source_row}",
                action.name,
                str(action.numeric_id),
                "" if action.chosen_slot is None else str(action.chosen_slot),
                "" if action.chosen_offset is None else f"0x{action.chosen_offset:08x}",
                action.reason,
            ]
            for action in plan.actions
            if action.action in actions
        ],
    )
    print()


def render_csv(plan: MergePlan) -> None:
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "table",
            "action",
            "recommended_action",
            "source_file",
            "source_row",
            "name",
            "numeric_id",
            "candidate_slot",
            "candidate_offset_hex",
            "reason",
        ],
    )
    writer.writeheader()
    for action in plan.actions:
        writer.writerow(
            {
                "table": action.table,
                "action": action.action,
                "recommended_action": action.recommended_action,
                "source_file": action.source_file,
                "source_row": action.source_row,
                "name": action.name,
                "numeric_id": action.numeric_id,
                "candidate_slot": "" if action.chosen_slot is None else action.chosen_slot,
                "candidate_offset_hex": "" if action.chosen_offset is None else f"0x{action.chosen_offset:08x}",
                "reason": action.reason,
            }
        )


def main() -> int:
    args = parse_args()
    imports = load_import_csvs(args.imports)
    plan = plan_merge(
        args.dat_file,
        args.decode_key,
        imports,
        max_records=args.max_records,
        include_existing=args.include_existing,
    )
    if args.format == "csv":
        render_csv(plan)
    else:
        render_markdown(args.dat_file, args.decode_key, args.imports, plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
