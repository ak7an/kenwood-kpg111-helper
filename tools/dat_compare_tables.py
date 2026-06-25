#!/usr/bin/env python3
"""Compare decoded KPG111 tables between two Program.dat files read-only."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.decoder import decode_program_tables
from kpg111.model import DecodedRecord, ProgramTables


@dataclass(frozen=True)
class SlotChange:
    table_name: str
    slot: int
    offset: int
    baseline: DecodedRecord | None
    modified: DecodedRecord | None
    kind: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare decoded KPG111 table records between two .dat files."
    )
    parser.add_argument("baseline", type=Path, help="Baseline Program.dat")
    parser.add_argument("modified", type=Path, help="Modified Program.dat")
    parser.add_argument(
        "--baseline-key",
        type=lambda value: int(value, 0),
        required=True,
        help="Decode key for baseline file",
    )
    parser.add_argument(
        "--modified-key",
        type=lambda value: int(value, 0),
        required=True,
        help="Decode key for modified file",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "csv"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=1024,
        help="Maximum records to scan per table (default: 1024)",
    )
    return parser.parse_args()


def occupied(record: DecodedRecord) -> bool:
    return bool(record.name) and not record.empty


def material(record: DecodedRecord) -> tuple[str, int, bool]:
    return record.name, record.numeric_id, record.empty


def table_pairs(
    baseline: ProgramTables,
    modified: ProgramTables,
) -> list[tuple[str, list[DecodedRecord], list[DecodedRecord]]]:
    return [
        ("Individual IDs", baseline.individual_ids, modified.individual_ids),
        ("Talk Groups", baseline.talk_groups, modified.talk_groups),
    ]


def by_slot(records: list[DecodedRecord]) -> dict[int, DecodedRecord]:
    return {record.slot: record for record in records}


def compare_slots(
    table_name: str,
    baseline_records: list[DecodedRecord],
    modified_records: list[DecodedRecord],
) -> list[SlotChange]:
    baseline_slots = by_slot(baseline_records)
    modified_slots = by_slot(modified_records)
    changes: list[SlotChange] = []
    for slot in sorted(set(baseline_slots) | set(modified_slots)):
        before = baseline_slots.get(slot)
        after = modified_slots.get(slot)
        offset = (after or before).offset if (after or before) else 0
        if before and after and material(before) == material(after):
            kind = "unchanged"
        elif (not before or not occupied(before)) and after and occupied(after):
            kind = "added"
        elif before and occupied(before) and (not after or not occupied(after)):
            kind = "removed"
        else:
            kind = "modified"
        changes.append(SlotChange(table_name, slot, offset, before, after, kind))
    return changes


def record_label(record: DecodedRecord | None) -> str:
    if record is None:
        return "<missing>"
    if record.empty:
        return "<empty>"
    name = record.name or "<invalid>"
    return f"{name} ({record.numeric_id})"


def duplicate_values(records: list[DecodedRecord], attr: str) -> dict[str, list[DecodedRecord]]:
    grouped: dict[str, list[DecodedRecord]] = defaultdict(list)
    for record in records:
        if not occupied(record):
            continue
        value = getattr(record, attr)
        if attr == "name" and not value:
            continue
        grouped[str(value)].append(record)
    return {
        value: rows
        for value, rows in sorted(grouped.items())
        if len(rows) > 1
    }


def same_numeric_renamed(
    baseline_records: list[DecodedRecord],
    modified_records: list[DecodedRecord],
) -> list[tuple[int, DecodedRecord, DecodedRecord]]:
    before_by_id = {record.numeric_id: record for record in baseline_records if occupied(record)}
    after_by_id = {record.numeric_id: record for record in modified_records if occupied(record)}
    rows = []
    for numeric_id in sorted(set(before_by_id) & set(after_by_id)):
        before = before_by_id[numeric_id]
        after = after_by_id[numeric_id]
        if before.name != after.name:
            rows.append((numeric_id, before, after))
    return rows


def same_name_numeric_changed(
    baseline_records: list[DecodedRecord],
    modified_records: list[DecodedRecord],
) -> list[tuple[str, DecodedRecord, DecodedRecord]]:
    before_by_name = {record.name: record for record in baseline_records if occupied(record)}
    after_by_name = {record.name: record for record in modified_records if occupied(record)}
    rows = []
    for name in sorted(set(before_by_name) & set(after_by_name)):
        before = before_by_name[name]
        after = after_by_name[name]
        if before.numeric_id != after.numeric_id:
            rows.append((name, before, after))
    return rows


def markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(row) + " |")


def offsets(records: list[DecodedRecord]) -> str:
    return ", ".join(f"0x{record.offset:08x}" for record in records)


def render_markdown(
    baseline_path: Path,
    modified_path: Path,
    baseline_key: int,
    modified_key: int,
    baseline_tables: ProgramTables,
    modified_tables: ProgramTables,
) -> None:
    print("# KPG111 Table Comparison")
    print()
    print("Read-only comparison of decoded Individual ID and Talk Group records.")
    print()
    print(f"- Baseline: `{baseline_path}` (`0x{baseline_key:02x}`)")
    print(f"- Modified: `{modified_path}` (`0x{modified_key:02x}`)")
    print()

    for table_name, before_records, after_records in table_pairs(baseline_tables, modified_tables):
        changes = compare_slots(table_name, before_records, after_records)
        counts = {kind: sum(1 for change in changes if change.kind == kind) for kind in ("unchanged", "added", "removed", "modified")}
        print(f"## {table_name}")
        print()
        print(
            f"- Unchanged: {counts['unchanged']}; Added: {counts['added']}; "
            f"Removed: {counts['removed']}; Modified: {counts['modified']}"
        )
        print()

        rows = [
            [
                change.kind,
                str(change.slot),
                f"0x{change.offset:08x}",
                record_label(change.baseline),
                record_label(change.modified),
            ]
            for change in changes
            if change.kind != "unchanged"
        ]
        markdown_table(["Kind", "Slot", "Offset", "Baseline", "Modified"], rows)
        print()

        renamed = same_numeric_renamed(before_records, after_records)
        print("### Same Numeric ID But Renamed")
        markdown_table(
            ["Numeric ID", "Baseline Slot", "Baseline Name", "Modified Slot", "Modified Name"],
            [
                [
                    str(numeric_id),
                    str(before.slot),
                    before.name,
                    str(after.slot),
                    after.name,
                ]
                for numeric_id, before, after in renamed
            ],
        )
        print()

        numeric_changed = same_name_numeric_changed(before_records, after_records)
        print("### Same Name But Numeric ID Changed")
        markdown_table(
            ["Name", "Baseline Slot", "Baseline ID", "Modified Slot", "Modified ID"],
            [
                [
                    name,
                    str(before.slot),
                    str(before.numeric_id),
                    str(after.slot),
                    str(after.numeric_id),
                ]
                for name, before, after in numeric_changed
            ],
        )
        print()

        print("### Duplicate Numeric IDs")
        duplicate_id_rows = []
        for label, records in (("baseline", before_records), ("modified", after_records)):
            for value, rows_for_value in duplicate_values(records, "numeric_id").items():
                duplicate_id_rows.append([label, value, str(len(rows_for_value)), offsets(rows_for_value)])
        markdown_table(["File", "Numeric ID", "Count", "Offsets"], duplicate_id_rows)
        print()

        print("### Duplicate Names")
        duplicate_name_rows = []
        for label, records in (("baseline", before_records), ("modified", after_records)):
            for value, rows_for_value in duplicate_values(records, "name").items():
                duplicate_name_rows.append([label, value, str(len(rows_for_value)), offsets(rows_for_value)])
        markdown_table(["File", "Name", "Count", "Offsets"], duplicate_name_rows)
        print()


def render_csv(
    baseline_tables: ProgramTables,
    modified_tables: ProgramTables,
) -> None:
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "section",
            "table",
            "kind",
            "slot",
            "offset_hex",
            "baseline_name",
            "baseline_numeric_id",
            "baseline_empty",
            "modified_name",
            "modified_numeric_id",
            "modified_empty",
            "value",
            "count",
            "offsets",
        ],
    )
    writer.writeheader()
    for table_name, before_records, after_records in table_pairs(baseline_tables, modified_tables):
        for change in compare_slots(table_name, before_records, after_records):
            if change.kind == "unchanged":
                continue
            before = change.baseline
            after = change.modified
            writer.writerow(
                {
                    "section": "slot_change",
                    "table": table_name,
                    "kind": change.kind,
                    "slot": change.slot,
                    "offset_hex": f"0x{change.offset:08x}",
                    "baseline_name": "" if before is None else before.name,
                    "baseline_numeric_id": "" if before is None else before.numeric_id,
                    "baseline_empty": "" if before is None else before.empty,
                    "modified_name": "" if after is None else after.name,
                    "modified_numeric_id": "" if after is None else after.numeric_id,
                    "modified_empty": "" if after is None else after.empty,
                    "value": "",
                    "count": "",
                    "offsets": "",
                }
            )
        for numeric_id, before, after in same_numeric_renamed(before_records, after_records):
            writer.writerow(
                {
                    "section": "same_numeric_id_renamed",
                    "table": table_name,
                    "kind": "",
                    "slot": "",
                    "offset_hex": "",
                    "baseline_name": before.name,
                    "baseline_numeric_id": before.numeric_id,
                    "baseline_empty": before.empty,
                    "modified_name": after.name,
                    "modified_numeric_id": after.numeric_id,
                    "modified_empty": after.empty,
                    "value": numeric_id,
                    "count": "",
                    "offsets": "",
                }
            )
        for name, before, after in same_name_numeric_changed(before_records, after_records):
            writer.writerow(
                {
                    "section": "same_name_numeric_changed",
                    "table": table_name,
                    "kind": "",
                    "slot": "",
                    "offset_hex": "",
                    "baseline_name": before.name,
                    "baseline_numeric_id": before.numeric_id,
                    "baseline_empty": before.empty,
                    "modified_name": after.name,
                    "modified_numeric_id": after.numeric_id,
                    "modified_empty": after.empty,
                    "value": name,
                    "count": "",
                    "offsets": "",
                }
            )
        for label, records in (("baseline", before_records), ("modified", after_records)):
            for value, rows_for_value in duplicate_values(records, "numeric_id").items():
                writer.writerow(
                    {
                        "section": "duplicate_numeric_ids",
                        "table": table_name,
                        "kind": label,
                        "slot": "",
                        "offset_hex": "",
                        "baseline_name": "",
                        "baseline_numeric_id": "",
                        "baseline_empty": "",
                        "modified_name": "",
                        "modified_numeric_id": "",
                        "modified_empty": "",
                        "value": value,
                        "count": len(rows_for_value),
                        "offsets": offsets(rows_for_value),
                    }
                )
            for value, rows_for_value in duplicate_values(records, "name").items():
                writer.writerow(
                    {
                        "section": "duplicate_names",
                        "table": table_name,
                        "kind": label,
                        "slot": "",
                        "offset_hex": "",
                        "baseline_name": "",
                        "baseline_numeric_id": "",
                        "baseline_empty": "",
                        "modified_name": "",
                        "modified_numeric_id": "",
                        "modified_empty": "",
                        "value": value,
                        "count": len(rows_for_value),
                        "offsets": offsets(rows_for_value),
                    }
                )


def main() -> int:
    args = parse_args()
    baseline_tables = decode_program_tables(
        args.baseline,
        args.baseline_key,
        include_empty=True,
        max_records=args.max_records,
    )
    modified_tables = decode_program_tables(
        args.modified,
        args.modified_key,
        include_empty=True,
        max_records=args.max_records,
    )

    if args.format == "csv":
        render_csv(baseline_tables, modified_tables)
    else:
        render_markdown(
            args.baseline,
            args.modified,
            args.baseline_key,
            args.modified_key,
            baseline_tables,
            modified_tables,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
