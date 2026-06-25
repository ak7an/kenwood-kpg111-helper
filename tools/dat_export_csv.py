#!/usr/bin/env python3
"""Export decoded KPG111 ID and Talk Group tables to CSV files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.decoder import decode_program_tables
from kpg111.export import export_tables, rows_for_export


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


def main() -> int:
    args = parse_args()
    tables = decode_program_tables(
        args.dat_file,
        args.decode_key,
        include_empty=args.include_empty,
    )
    outputs = export_tables(
        tables,
        args.out_dir,
        prefix=args.prefix,
        include_empty=args.include_empty,
    )
    counts = {
        "individual_ids": len(rows_for_export(tables.individual_ids, args.include_empty)),
        "talk_groups": len(rows_for_export(tables.talk_groups, args.include_empty)),
    }
    for table_id, path in outputs.items():
        print(f"wrote {path} ({counts[table_id]} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
