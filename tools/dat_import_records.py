#!/usr/bin/env python3
"""Import row-based CSV edits into an existing KPG111 DAT file experimentally."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.writer import (
    ByteRange,
    WriteResult,
    WriterError,
    changed_byte_ranges,
    edit_record,
    load_dat,
    write_result,
)


@dataclass(frozen=True)
class CsvEdit:
    csv_row: int
    slot: int
    display_row: int
    name: str | None
    numeric_id: int | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply row-based TG/ID CSV edits to a copy of an existing DAT file."
    )
    parser.add_argument("input_dat", type=Path, help="Input KPG111 .dat file")
    parser.add_argument("output_dat", type=Path, help="Output KPG111 .dat file")
    parser.add_argument(
        "--table",
        required=True,
        choices=("talk_groups", "individual_ids"),
        help="Decoded table to edit",
    )
    parser.add_argument("--csv", required=True, type=Path, help="CSV file containing record edits")
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


def load_csv_edits(path: Path) -> list[CsvEdit]:
    edits: list[CsvEdit] = []
    seen_slots: dict[int, int] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise WriterError(f"{path}: missing header row")

        fieldnames = {field.strip() for field in reader.fieldnames}
        if "row" not in fieldnames and "slot" not in fieldnames:
            raise WriterError(f"{path}: missing required row or slot column")

        for csv_row, row in enumerate(reader, start=2):
            edit = parse_csv_edit(path, csv_row, row)
            if edit.slot in seen_slots:
                raise WriterError(
                    f"{path}:{csv_row}: duplicate target also used on CSV row {seen_slots[edit.slot]}"
                )
            seen_slots[edit.slot] = csv_row
            edits.append(edit)
    return edits


def parse_csv_edit(path: Path, csv_row: int, row: dict[str, str]) -> CsvEdit:
    raw_row = (row.get("row") or "").strip()
    raw_slot = (row.get("slot") or "").strip()
    if raw_row:
        try:
            display_row = int(raw_row, 10)
        except ValueError as exc:
            raise WriterError(f"{path}:{csv_row}: row is not an integer: {raw_row!r}") from exc
        if display_row < 1:
            raise WriterError(f"{path}:{csv_row}: row must be >= 1")
        slot = display_row - 1
    elif raw_slot:
        try:
            slot = int(raw_slot, 10)
        except ValueError as exc:
            raise WriterError(f"{path}:{csv_row}: slot is not an integer: {raw_slot!r}") from exc
        if slot < 0:
            raise WriterError(f"{path}:{csv_row}: slot must be >= 0")
        display_row = slot + 1
    else:
        raise WriterError(f"{path}:{csv_row}: missing row and slot")

    name = parse_optional_text(row, "name")
    numeric_id = parse_optional_id(path, csv_row, row)
    if name is None and numeric_id is None:
        raise WriterError(f"{path}:{csv_row}: missing editable name or id")

    return CsvEdit(
        csv_row=csv_row,
        slot=slot,
        display_row=display_row,
        name=name,
        numeric_id=numeric_id,
    )


def parse_optional_text(row: dict[str, str], field: str) -> str | None:
    if field not in row or row[field] is None:
        return None
    value = row[field].strip()
    if not value:
        return None
    return value


def parse_optional_id(path: Path, csv_row: int, row: dict[str, str]) -> int | None:
    if "id" not in row or row["id"] is None:
        return None
    raw_id = row["id"].strip()
    if not raw_id:
        return None
    try:
        return int(raw_id, 10)
    except ValueError as exc:
        raise WriterError(f"{path}:{csv_row}: id is not an integer: {raw_id!r}") from exc


def apply_edits(data: bytes, decode_key: int, table: str, edits: list[CsvEdit]) -> bytes:
    candidate = data
    for edit in edits:
        result = edit_record(
            candidate,
            decode_key,
            table,
            edit.slot,
            name=edit.name,
            numeric_id=edit.numeric_id,
        )
        candidate = result.data
    return candidate


def main() -> int:
    args = parse_args()
    try:
        if same_path(args.input_dat, args.output_dat) and not args.allow_overwrite_input:
            raise WriterError("refusing to overwrite input file without --allow-overwrite-input")

        edits = load_csv_edits(args.csv)
        original = load_dat(args.input_dat)
        candidate = apply_edits(original, args.decode_key, args.table, edits)
        changed_ranges = changed_byte_ranges(original, candidate)
        write_result(
            args.output_dat,
            WriteResult(candidate, changed_ranges, args.table, -1, -1),
        )

        written = load_dat(args.output_dat)
        if written != candidate:
            raise WriterError("written output does not match validated candidate bytes")

        print("PASS")
        print(f"Input: {args.input_dat}")
        print(f"Output: {args.output_dat}")
        print(f"Table: {args.table}")
        print(f"CSV: {args.csv}")
        print(f"Rows applied: {len(edits)}")
        print_changed_ranges(changed_ranges)
        return 0
    except (OSError, WriterError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
