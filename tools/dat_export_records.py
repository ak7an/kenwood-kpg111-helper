#!/usr/bin/env python3
"""Export decoded KPG111 Talk Group or Individual ID records for experimental editing."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.decoder import decode_program_tables
from kpg111.export import occupied
from kpg111.model import DecodedRecord


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export decoded KPG111 TG/ID records to a row-based CSV."
    )
    parser.add_argument("dat_file", type=Path, help="Input KPG111 .dat file")
    parser.add_argument(
        "--table",
        required=True,
        choices=("talk_groups", "individual_ids"),
        help="Decoded table to export",
    )
    parser.add_argument("--output", required=True, type=Path, help="Output CSV path")
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        default=0x5B,
        help="XOR byte used to decode names and numeric fields (default: 0x5b)",
    )
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Include empty decoded slots exposed by the current decoder.",
    )
    return parser.parse_args()


def records_for_table(path: Path, table: str, decode_key: int, include_empty: bool) -> list[DecodedRecord]:
    tables = decode_program_tables(path, decode_key, include_empty=include_empty)
    if table == "talk_groups":
        records = tables.talk_groups
    else:
        records = tables.individual_ids
    if include_empty:
        return records
    return [record for record in records if occupied(record)]


def write_records_csv(path: Path, records: list[DecodedRecord]) -> int:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["row", "slot", "id", "name"])
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "row": record.slot + 1,
                    "slot": record.slot,
                    "id": record.numeric_id,
                    "name": record.name,
                }
            )
    return len(records)


def main() -> int:
    args = parse_args()
    try:
        records = records_for_table(args.dat_file, args.table, args.decode_key, args.include_empty)
        count = write_records_csv(args.output, records)
        print(f"wrote {args.output} ({count} rows)")
        return 0
    except OSError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
