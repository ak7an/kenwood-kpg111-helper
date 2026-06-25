#!/usr/bin/env python3
"""Experimentally rename one decoded KPG111 Talk Group or Individual ID record."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.writer import (
    ByteRange,
    WriterError,
    load_dat,
    rename_record,
    verify_only_ranges_changed,
    write_result,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experimentally rename one known decoded TG/ID record in a copy of a DAT file."
    )
    parser.add_argument("input_dat", type=Path, help="Input KPG111 .dat file")
    parser.add_argument("output_dat", type=Path, help="Output KPG111 .dat file")
    parser.add_argument(
        "--table",
        required=True,
        choices=("talk_groups", "individual_ids"),
        help="Decoded table containing the target record",
    )
    parser.add_argument("--slot", required=True, type=int, help="Decoded table slot to rename")
    parser.add_argument("--name", required=True, help="New record name, 14 ASCII bytes or fewer")
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        default=0x5B,
        help="XOR byte used to decode names and numeric fields (default: 0x5b)",
    )
    parser.add_argument(
        "--allow-overwrite-input",
        action="store_true",
        help="Allow output path to be the same file as the input path.",
    )
    return parser.parse_args()


def same_path(left: Path, right: Path) -> bool:
    try:
        return left.resolve() == right.resolve()
    except OSError:
        return left.absolute() == right.absolute()


def render_range(changed_range: ByteRange) -> str:
    last = changed_range.end - 1
    if changed_range.length == 1:
        return f"0x{changed_range.start:08x}"
    return f"0x{changed_range.start:08x}..0x{last:08x}"


def print_changed_ranges(ranges: list[ByteRange]) -> None:
    if not ranges:
        print("Changed byte ranges: none")
        return
    print("Changed byte ranges:")
    for changed_range in ranges:
        print(f"- {render_range(changed_range)} ({changed_range.length} bytes)")


def main() -> int:
    args = parse_args()
    try:
        if same_path(args.input_dat, args.output_dat) and not args.allow_overwrite_input:
            raise WriterError("refusing to overwrite input file without --allow-overwrite-input")

        original = load_dat(args.input_dat)
        result = rename_record(
            original,
            args.decode_key,
            args.table,
            args.slot,
            args.name,
        )

        verify_only_ranges_changed(original, result.data, result.changed_ranges)
        write_result(args.output_dat, result)

        written = load_dat(args.output_dat)
        verify_only_ranges_changed(original, written, result.changed_ranges)
        if written != result.data:
            raise WriterError("written output does not match validated candidate bytes")

        print("PASS")
        print(f"Input: {args.input_dat}")
        print(f"Output: {args.output_dat}")
        print(f"Table: {args.table}")
        print(f"Slot: {args.slot}")
        print(f"Record offset: 0x{result.record_offset:08x}")
        print_changed_ranges(result.changed_ranges)
        return 0
    except (OSError, WriterError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
