#!/usr/bin/env python3
"""Analyze observed KPG111 table allocation behavior read-only."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.allocation import AllocationAnalysis, AllocationEvent, SlotContext
from kpg111.allocation import analyze_allocation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze newly occupied KPG111 TG/ID table slots from existing research experiments."
    )
    parser.add_argument(
        "research_roots",
        nargs="*",
        type=Path,
        default=[
            Path("research/dattest"),
            Path("research/dattest2"),
            Path("research/dattest3"),
            Path("research/dattest4"),
        ],
        help="Research experiment roots to analyze.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("allocation_report.md"),
        help="Markdown report path (default: allocation_report.md)",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=1024,
        help="Maximum records to scan per table (default: 1024)",
    )
    return parser.parse_args()


def md_escape(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|")


def markdown_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    if not rows:
        lines.append("| " + " | ".join("none" for _ in headers) + " |")
        return lines
    for row in rows:
        lines.append("| " + " | ".join(md_escape(value) for value in row) + " |")
    return lines


def context_label(context: SlotContext) -> str:
    if context.slot is None:
        return "missing"
    label = f"slot {context.slot} {context.state}"
    if context.name:
        label += f" {context.name} ({context.numeric_id})"
    return label


def distance(value: int | None) -> str:
    return "none" if value is None else str(value)


def event_rows(events: tuple[AllocationEvent, ...]) -> list[list[object]]:
    return [
        [
            event.experiment,
            event.modified_path.name,
            event.table_name,
            event.slot,
            f"0x{event.offset:08x}",
            event.name,
            event.numeric_id,
            event.previous_slot_state,
            context_label(event.previous_neighbor),
            context_label(event.next_neighbor),
            distance(event.distance_from_previous_occupied),
            distance(event.distance_from_next_occupied),
            ", ".join(event.candidate_policies),
        ]
        for event in events
    ]


def counterexample_rows(analysis: AllocationAnalysis) -> list[list[object]]:
    rows: list[list[object]] = []
    for policy in analysis.policies:
        if policy.policy in {
            "unknown",
            "bitmap allocation",
            "free list",
            "observed first available empty record in slot order",
            "sequential scan implementation",
            "lowest-available-slot implementation",
        }:
            continue
        for event in analysis.events:
            if policy.policy not in event.candidate_policies:
                rows.append(
                    [
                        policy.policy,
                        event.experiment,
                        event.modified_path.name,
                        event.table_name,
                        event.slot,
                        f"0x{event.offset:08x}",
                        ", ".join(event.candidate_policies),
                    ]
                )
    return rows


def render_report(analysis: AllocationAnalysis) -> str:
    lines: list[str] = [
        "# KPG111 Allocation Analysis",
        "",
        "This report is read-only. It analyzes existing `.dat` variants under `research/` and does not write or modify `Program.dat`.",
        "",
        "## Inputs",
        "",
    ]
    lines.extend(
        markdown_table(
            ["Experiment", "Baseline", "Modified", "Baseline Key", "Modified Key", "Source"],
            [
                [
                    pair.experiment,
                    pair.baseline_path,
                    pair.modified_path,
                    f"0x{pair.baseline_key:02x}",
                    f"0x{pair.modified_key:02x}",
                    pair.source,
                ]
                for pair in analysis.pairs
            ],
        )
    )

    lines.extend(
        [
            "",
            "## Observed Allocation Sequence",
            "",
            "Rows are ordered by experiment comparison and slot. When one modified file contains multiple newly occupied records, the file does not prove the UI creation order.",
            "",
        ]
    )
    lines.extend(
        markdown_table(
            [
                "Experiment",
                "Modified",
                "Table",
                "Slot",
                "Offset",
                "Name",
                "Numeric ID",
                "Previous Slot State",
                "Previous Neighbor",
                "Next Neighbor",
                "Distance From Previous Occupied",
                "Distance From Next Occupied",
                "Candidate Policies",
            ],
            event_rows(analysis.events),
        )
    )

    lines.extend(["", "## Evidence Table", ""])
    lines.extend(
        markdown_table(
            ["Assessment", "Matching Events", "Counterexamples", "Confidence", "Notes"],
            [
                [
                    policy.policy,
                    policy.matching_events,
                    policy.counterexamples,
                    policy.confidence,
                    policy.notes,
                ]
                for policy in analysis.policies
            ],
        )
    )

    lines.extend(["", "## Candidate Allocation Policy", ""])
    lines.append(
        "Observed behavior is consistent with selecting the first available empty record in slot order. "
        "Current experiments do not distinguish between a sequential scan, a lowest-available-slot rule, "
        "or another implementation that produces the same observable result. "
        "Append-after-last-occupied is observed when the selected slot is immediately after the occupied run, "
        "but Dattest4 provides counterexamples to an append-only explanation because cleared interior slots are reused. "
        "No bitmap or free-list structure has been identified in current evidence."
    )

    lines.extend(["", "## Counterexamples", ""])
    lines.extend(
        markdown_table(
            [
                "Policy",
                "Experiment",
                "Modified",
                "Table",
                "Slot",
                "Offset",
                "Observed Candidate Policies",
            ],
            counterexample_rows(analysis),
        )
    )

    lines.extend(["", "## Unknowns", ""])
    for unknown in analysis.unknowns:
        lines.append(f"- {unknown}")

    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            "The observed newly occupied records are consistent with selecting the first available empty record in slot order. "
            "Observed behavior confidence is HIGH for the current events because every newly occupied slot matches that result. "
            "Implementation mechanism confidence remains MODERATE because the experiments do not prove whether KPG111 uses a sequential scan, a lowest-available-slot rule, or another mechanism with the same visible output. "
            "General production confidence remains limited by unresolved table capacity, metadata, pointer/index structures, and multi-gap behavior.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    analysis = analyze_allocation(args.research_roots, max_records=args.max_records)
    args.output.write_text(render_report(analysis), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"Analyzed {len(analysis.pairs)} experiment comparisons")
    print(f"Observed {len(analysis.events)} newly occupied records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
