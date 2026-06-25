#!/usr/bin/env python3
"""Decode known KPG111 Individual ID and Talk Group table records read-only."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.decoder import NUMERIC_LENGTH, NUMERIC_START, RECORD_SIZE
from kpg111.decoder import decode_program_tables, xor_bytes
from kpg111.model import DecodedRecord, ProgramTables


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only decoder for known KPG111 ID and Talk Group table records."
    )
    parser.add_argument("dat_file", type=Path, help="Path to Program.dat")
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        required=True,
        help="XOR byte used to decode names and numeric fields, e.g. 0x5b",
    )
    parser.add_argument(
        "--record-size",
        type=int,
        default=RECORD_SIZE,
        help="Record size in bytes (default: 32)",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=1024,
        help="Maximum records to scan per table (default: 1024)",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "csv"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Include empty records after the occupied run.",
    )
    return parser.parse_args()


def numeric_raw_hex(record: DecodedRecord) -> str:
    raw = bytes.fromhex(record.raw_record_hex)
    return raw[NUMERIC_START : NUMERIC_START + NUMERIC_LENGTH].hex(" ")


def numeric_decoded_hex(record: DecodedRecord, decode_key: int) -> str:
    raw = bytes.fromhex(record.raw_record_hex)
    decoded = xor_bytes(raw[NUMERIC_START : NUMERIC_START + NUMERIC_LENGTH], decode_key)
    return decoded.hex(" ")


def table_rows(tables: ProgramTables) -> list[tuple[str, list[DecodedRecord]]]:
    return [
        ("Individual IDs", tables.individual_ids),
        ("Talk Groups", tables.talk_groups),
    ]


def markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(row) + " |")


def render_markdown(path: Path, key: int, tables: ProgramTables) -> None:
    print("# KPG111 Decoded Tables")
    print()
    print("Read-only decode of known Individual ID and Talk Group table offsets.")
    print()
    print(f"- File: `{path}`")
    print(f"- Decode key: `0x{key:02x}`")
    print()
    for table_name, rows in table_rows(tables):
        print(f"## {table_name}")
        markdown_table(
            [
                "Index",
                "Offset",
                "Name",
                "Raw +19/+20",
                "Decoded +19/+20",
                "LE Value",
                "Empty",
            ],
            [
                [
                    str(record.slot),
                    f"0x{record.offset:08x}",
                    record.name,
                    numeric_raw_hex(record),
                    numeric_decoded_hex(record, key),
                    str(record.numeric_id),
                    "yes" if record.empty else "no",
                ]
                for record in rows
            ],
        )
        print()


def render_csv(tables: ProgramTables, decode_key: int) -> None:
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "table_id",
            "table_name",
            "index",
            "offset_hex",
            "name",
            "numeric_raw_hex",
            "numeric_decoded_hex",
            "numeric_little_endian",
            "empty",
        ],
    )
    writer.writeheader()
    for _table_name, records in table_rows(tables):
        for record in records:
            writer.writerow(
                {
                    "table_id": record.table_id,
                    "table_name": record.table_name,
                    "index": record.slot,
                    "offset_hex": f"0x{record.offset:08x}",
                    "name": record.name,
                    "numeric_raw_hex": numeric_raw_hex(record),
                    "numeric_decoded_hex": numeric_decoded_hex(record, decode_key),
                    "numeric_little_endian": record.numeric_id,
                    "empty": record.empty,
                }
            )


def main() -> int:
    args = parse_args()
    if args.record_size != RECORD_SIZE:
        raise SystemExit("only 32-byte records are supported by the current decoder")
    tables = decode_program_tables(
        args.dat_file,
        args.decode_key,
        include_empty=args.include_empty,
        max_records=args.max_records,
    )

    if args.format == "csv":
        render_csv(tables, args.decode_key)
    else:
        render_markdown(args.dat_file, args.decode_key, tables)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
