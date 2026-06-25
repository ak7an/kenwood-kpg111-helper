#!/usr/bin/env python3
"""Experimentally edit one decoded KPG111 Talk Group or Individual ID record."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.writer import (
    ByteRange,
    WriterError,
    edit_record,
    load_dat,
    verify_only_ranges_changed,
    write_result,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experimentally edit one known decoded TG/ID record in a copy of a DAT file."
    )
    parser.add_argument("input_dat", type=Path, help="Input KPG111 .dat file")
    parser.add_argument("output_dat", type=Path, help="Output KPG111 .dat file")
    parser.add_argument(
        "--table",
        required=True,
        choices=("talk_groups", "individual_ids"),
        help="Decoded table containing the target record",
    )
    parser.add_argument("--slot", type=int, help="Zero-based decoded internal slot to edit")
    parser.add_argument("--row", type=int, help="One-based KPG-111D displayed row number to edit")
    parser.add_argument("--name", help="New record name, 14 ASCII bytes or fewer")
    parser.add_argument("--id", type=int, help="New numeric ID, 1 through 65519")
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


def resolve_slot(slot: int | None, row: int | None) -> tuple[int, int]:
    if slot is not None and row is not None:
        raise WriterError("provide exactly one of --slot or --row, not both")
    if slot is None and row is None:
        raise WriterError("provide exactly one of --slot or --row")
    if slot is not None:
        if slot < 0:
            raise WriterError("--slot must be >= 0")
        return slot, slot + 1
    if row is None:
        raise WriterError("provide exactly one of --slot or --row")
    if row < 1:
        raise WriterError("--row must be >= 1")
    return row - 1, row


def main() -> int:
    args = parse_args()
    try:
        if same_path(args.input_dat, args.output_dat) and not args.allow_overwrite_input:
            raise WriterError("refusing to overwrite input file without --allow-overwrite-input")

        original = load_dat(args.input_dat)
        if args.name is None and args.id is None:
            raise WriterError("at least one of --name or --id is required")
        slot, row = resolve_slot(args.slot, args.row)

        result = edit_record(
            original,
            args.decode_key,
            args.table,
            slot,
            name=args.name,
            numeric_id=args.id,
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
        print(f"Row: {row}")
        print(f"Slot: {slot}")
        print(f"Record offset: 0x{result.record_offset:08x}")
        print_changed_ranges(result.changed_ranges)
        return 0
    except (OSError, WriterError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
