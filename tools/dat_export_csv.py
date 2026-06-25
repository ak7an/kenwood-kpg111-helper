#!/usr/bin/env python3
"""Export decoded KPG111 ID and Talk Group tables to CSV files."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.decoder import decode_program_tables
from kpg111.model import DecodedRecord, ProgramTables


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export decoded KPG111 tables to CSV without modifying Program.dat."
    )
    parser.add_argument("dat_file", type=Path, help="Path to Program.dat")
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        required=True,
        help="XOR byte used to decode table fields, e.g. 0x5b",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Directory where CSV files will be written",
    )
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Include empty slots in exported CSV files.",
    )
    parser.add_argument(
        "--prefix",
        help="Optional filename prefix, e.g. ak7an",
    )
    return parser.parse_args()


def occupied(record: DecodedRecord) -> bool:
    return bool(record.name) and not record.empty


def output_name(base: str, prefix: str | None) -> str:
    return f"{prefix}_{base}" if prefix else base


def rows_for_export(records: list[DecodedRecord], include_empty: bool) -> list[DecodedRecord]:
    if include_empty:
        return records
    return [record for record in records if occupied(record)]


def write_table_csv(path: Path, records: list[DecodedRecord], include_empty: bool) -> int:
    rows = rows_for_export(records, include_empty)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "table_id",
                "slot",
                "offset_hex",
                "name",
                "numeric_id",
                "empty",
            ],
        )
        writer.writeheader()
        for record in rows:
            writer.writerow(
                {
                    "table_id": record.table_id,
                    "slot": record.slot,
                    "offset_hex": f"0x{record.offset:08x}",
                    "name": record.name,
                    "numeric_id": record.numeric_id,
                    "empty": record.empty,
                }
            )
    return len(rows)


def export_tables(
    tables: ProgramTables,
    out_dir: Path,
    include_empty: bool,
    prefix: str | None,
) -> list[tuple[Path, int]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        (
            out_dir / output_name("individual_ids.csv", prefix),
            tables.individual_ids,
        ),
        (
            out_dir / output_name("talk_groups.csv", prefix),
            tables.talk_groups,
        ),
    ]
    written = []
    for path, records in outputs:
        count = write_table_csv(path, records, include_empty)
        written.append((path, count))
    return written


def main() -> int:
    args = parse_args()
    tables = decode_program_tables(
        args.dat_file,
        args.decode_key,
        include_empty=args.include_empty,
    )
    written = export_tables(tables, args.out_dir, args.include_empty, args.prefix)
    for path, count in written:
        print(f"wrote {path} ({count} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
