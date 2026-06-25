#!/usr/bin/env python3
"""Read-only validation report for known KPG111 Program.dat tables."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.decoder import INDIVIDUAL_ID_TABLE_START, PAYLOAD_START, RECORD_SIZE
from kpg111.decoder import TABLE_DEFINITIONS, TALK_GROUP_TABLE_START, decode_table
from kpg111.model import DecodedRecord, ProgramTables


HEADER_SIGNATURE = b"KPG111D"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate decoded KPG111 Program.dat tables without writing files."
    )
    parser.add_argument("dat_file", type=Path, help="Path to Program.dat")
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        required=True,
        help="XOR byte used to decode names and numeric fields, e.g. 0x5b",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=1024,
        help="Maximum records to scan per table for validation (default: 1024)",
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


def table_records(tables: ProgramTables) -> list[tuple[str, list[DecodedRecord]]]:
    return [
        ("Individual IDs", tables.individual_ids),
        ("Talk Groups", tables.talk_groups),
    ]


def trim_after_table(records: list[DecodedRecord]) -> list[DecodedRecord]:
    trimmed: list[DecodedRecord] = []
    saw_empty = False
    for record in records:
        if record.empty:
            saw_empty = True
            trimmed.append(record)
            continue
        if not record.name and saw_empty:
            break
        if record.name:
            saw_empty = False
        trimmed.append(record)
    return trimmed


def occupied(records: list[DecodedRecord]) -> list[DecodedRecord]:
    return [record for record in records if record.name and not record.empty]


def empty(records: list[DecodedRecord]) -> list[DecodedRecord]:
    return [record for record in records if record.empty]


def invalid(records: list[DecodedRecord]) -> list[DecodedRecord]:
    return [
        record
        for record in records
        if not record.empty and not record.name
    ]


def duplicates(records: list[DecodedRecord], attr: str) -> list[tuple[str, list[DecodedRecord]]]:
    grouped: dict[str, list[DecodedRecord]] = {}
    for record in occupied(records):
        value = str(getattr(record, attr))
        grouped.setdefault(value, []).append(record)
    return sorted(
        ((value, rows) for value, rows in grouped.items() if len(rows) > 1),
        key=lambda item: item[0],
    )


def first_empty(records: list[DecodedRecord]) -> DecodedRecord | None:
    for record in records:
        if record.empty:
            return record
    return None


def format_offsets(records: list[DecodedRecord], limit: int = 12) -> str:
    offsets = [f"0x{record.offset:08x}" for record in records[:limit]]
    if len(records) > limit:
        offsets.append(f"... {len(records) - limit} more")
    return ", ".join(offsets) if offsets else "none"


def render_validation(path: Path, decode_key: int, max_records: int) -> int:
    exists = path.exists()
    data = path.read_bytes() if exists else b""
    id_max_records = min(
        max_records,
        (TALK_GROUP_TABLE_START - INDIVIDUAL_ID_TABLE_START) // RECORD_SIZE,
    )
    tables = (
        ProgramTables(
            individual_ids=trim_after_table(
                decode_table(
                    data,
                    "individual_ids",
                    "Individual IDs",
                    INDIVIDUAL_ID_TABLE_START,
                    decode_key,
                    include_empty=True,
                    max_records=id_max_records,
                )
            ),
            talk_groups=trim_after_table(
                decode_table(
                    data,
                    "talk_groups",
                    "Talk Groups",
                    TALK_GROUP_TABLE_START,
                    decode_key,
                    include_empty=True,
                    max_records=max_records,
                )
            ),
        )
        if exists
        else ProgramTables(individual_ids=[], talk_groups=[])
    )

    print("# KPG111 Program.dat Validation")
    print()
    print("Read-only validation of known Individual ID and Talk Group table records.")
    print()
    print("## File")
    print()
    print(f"- Path: `{path}`")
    print(f"- Exists: {'yes' if exists else 'no'}")
    print(f"- Size: {len(data)} bytes")
    print(f"- Header signature visible: {'yes' if data.startswith(HEADER_SIGNATURE) else 'no'}")
    print(f"- Payload start: `0x{PAYLOAD_START:x}`")
    print(f"- Decode key: `0x{decode_key:02x}`")
    print()

    print("## Table Summary")
    rows = []
    for table_id, table_name, start in TABLE_DEFINITIONS:
        records = getattr(tables, table_id)
        occupied_records = occupied(records)
        empty_records = empty(records)
        invalid_records = invalid(records)
        first = first_empty(records)
        numeric_ffff = [
            record for record in occupied_records if record.numeric_id == 65535
        ]
        rows.append(
            [
                table_name,
                f"0x{start:08x}",
                str(len(records)),
                str(len(occupied_records)),
                str(len(empty_records)),
                str(len(invalid_records)),
                f"0x{first.offset:08x}" if first else "none",
                str(len(empty_records)),
                str(len(numeric_ffff)),
            ]
        )
    markdown_table(
        [
            "Table",
            "Start",
            "Records Scanned",
            "Occupied",
            "Empty",
            "Invalid Names",
            "First Empty Slot",
            "Capacity Estimate",
            "Occupied Numeric 65535",
        ],
        rows,
    )
    print()

    for table_name, records in table_records(tables):
        print(f"## {table_name} Details")
        occupied_records = occupied(records)
        invalid_records = invalid(records)
        numeric_ffff = [
            record for record in occupied_records if record.numeric_id == 65535
        ]
        print()
        print(f"- Occupied records decoded: {len(occupied_records)}")
        print(f"- Empty records scanned: {len(empty(records))}")
        print(f"- Invalid names: {len(invalid_records)}")
        print(f"- Invalid name offsets: {format_offsets(invalid_records)}")
        print(f"- Numeric IDs equal to 65535: {format_offsets(numeric_ffff)}")
        first = first_empty(records)
        print(f"- First empty slot: {f'0x{first.offset:08x}' if first else 'none'}")
        print()

        print("### Duplicate Names")
        name_rows = [
            [value, str(len(rows)), format_offsets(rows)]
            for value, rows in duplicates(records, "name")
        ]
        markdown_table(["Name", "Count", "Offsets"], name_rows)
        print()

        print("### Duplicate Numeric IDs")
        numeric_rows = [
            [value, str(len(rows)), format_offsets(rows)]
            for value, rows in duplicates(records, "numeric_id")
        ]
        markdown_table(["Numeric ID", "Count", "Offsets"], numeric_rows)
        print()

    return 0 if exists else 1


def main() -> int:
    args = parse_args()
    return render_validation(args.dat_file, args.decode_key, args.max_records)


if __name__ == "__main__":
    raise SystemExit(main())
