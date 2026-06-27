#!/usr/bin/env python3
"""Import DVREF NXDN reflector talk groups into a copy of a KPG111 DAT."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.decoder import (
    NAME_LENGTH,
    NAME_START,
    NUMERIC_LENGTH,
    NUMERIC_START,
    TALK_GROUP_TABLE_START,
    decode_table,
    xor_bytes,
)
from kpg111.imports import ImportRecord
from kpg111.planner import MergePlan, PlannedAction, plan_merge
from kpg111.writer import (
    ByteRange,
    WriteResult,
    WriterError,
    changed_byte_ranges,
    edit_record,
    load_dat,
    verify_only_ranges_changed,
    write_result,
)


DEFAULT_DECODE_KEY = 0x5B
TALK_GROUP_TABLE = "talk_groups"
TALK_GROUP_TABLE_NAME = "Talk Groups"
TG_NUMBER_COLUMNS = (
    "Reflector/TG Number",
    "TG Number",
    "TG",
    "Talkgroup",
    "Talkgroup ID",
    "id",
)
NAME_COLUMNS = (
    "Name/Description",
    "Name",
    "Description",
)


@dataclass(frozen=True)
class DvrefRow:
    tg_id: int
    name: str
    source_row: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import DVREF NXDN reflector talk groups into a patched KPG111 DAT."
    )
    parser.add_argument("--input", required=True, type=Path, help="DVREF reflector CSV")
    parser.add_argument("--baseline", required=True, type=Path, help="Baseline KPG111 DAT")
    parser.add_argument("--output", required=True, type=Path, help="Output patched DAT")
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        default=DEFAULT_DECODE_KEY,
        help="XOR byte used to decode names and numeric fields (default: 0x5b)",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=1024,
        help="Maximum decoded records to scan per table (default: 1024)",
    )
    parser.add_argument(
        "--allow-overwrite-input",
        action="store_true",
        help="Allow --output to be the same path as --baseline.",
    )
    return parser.parse_args()


def same_path(left: Path, right: Path) -> bool:
    try:
        return left.resolve() == right.resolve()
    except OSError:
        return left.absolute() == right.absolute()


def pick_column(fieldnames: list[str], candidates: tuple[str, ...]) -> str:
    by_normalized = {field.strip().casefold(): field for field in fieldnames}
    for candidate in candidates:
        found = by_normalized.get(candidate.casefold())
        if found is not None:
            return found
    raise ValueError(f"missing required column; tried: {', '.join(candidates)}")


def load_dvref_rows(path: Path) -> list[DvrefRow]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path}: missing header row")
        tg_column = pick_column(reader.fieldnames, TG_NUMBER_COLUMNS)
        name_column = pick_column(reader.fieldnames, NAME_COLUMNS)

        rows = []
        seen_ids: set[int] = set()
        for row_number, row in enumerate(reader, start=2):
            raw_tg = (row.get(tg_column) or "").strip()
            if not raw_tg:
                continue
            try:
                tg_id = int(raw_tg, 10)
            except ValueError as exc:
                raise ValueError(f"{path}:{row_number}: TG number is not an integer: {raw_tg!r}") from exc
            if tg_id in seen_ids:
                continue
            seen_ids.add(tg_id)
            raw_name = (row.get(name_column) or "").strip()
            rows.append(DvrefRow(tg_id=tg_id, name=normalize_name(tg_id, raw_name), source_row=row_number))
    return sorted(rows, key=lambda item: item.tg_id)


def normalize_name(tg_id: int, value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[^A-Za-z0-9 /_-]+", " ", ascii_text).upper()
    ascii_text = re.sub(r"\s+", " ", ascii_text).strip()
    prefix = str(tg_id)
    if ascii_text:
        name = f"{prefix} {ascii_text}"
    else:
        name = f"TG{tg_id}"
    return name[:NAME_LENGTH].rstrip() or f"TG{tg_id}"[:NAME_LENGTH]


def import_records(rows: list[DvrefRow], source: Path) -> list[ImportRecord]:
    return [
        ImportRecord(
            record_type=TALK_GROUP_TABLE,
            name=row.name,
            numeric_id=row.tg_id,
            source_file=str(source),
            source_row=row.source_row,
        )
        for row in rows
    ]


def validate_plan(plan: MergePlan) -> None:
    bad_actions = [
        action for action in plan.actions
        if action.action in {"invalid", "duplicate_name_id_diff"}
    ]
    if bad_actions:
        details = "; ".join(
            f"row {action.source_row} TG {action.numeric_id} {action.name!r}: {action.reason}"
            for action in bad_actions[:10]
        )
        raise WriterError(f"merge plan has rejected/conflicting rows: {details}")


def apply_plan(data: bytes, decode_key: int, plan: MergePlan) -> bytes:
    candidate = data
    for action in plan.actions:
        if action.table != TALK_GROUP_TABLE_NAME:
            raise WriterError(f"refusing non-talk-group action: {action.table}")
        if action.action == "duplicate_exact":
            continue
        if action.action == "possible_update":
            if action.chosen_slot is None:
                raise WriterError(f"missing slot for update row {action.source_row}")
            candidate = edit_record(
                candidate,
                decode_key,
                TALK_GROUP_TABLE,
                action.chosen_slot,
                name=action.name,
                numeric_id=action.numeric_id,
            ).data
            continue
        if action.action == "new_record":
            candidate = add_talk_group_record(candidate, decode_key, action)
            continue
        raise WriterError(f"unsupported planner action: {action.action}")
    return candidate


def add_talk_group_record(data: bytes, decode_key: int, action: PlannedAction) -> bytes:
    if action.chosen_slot is None or action.chosen_offset is None:
        raise WriterError(f"missing target slot for row {action.source_row}")
    validate_name(action.name)
    validate_numeric_id(action.numeric_id)

    record = data[action.chosen_offset : action.chosen_offset + 32]
    if len(record) != 32:
        raise WriterError(f"target slot {action.chosen_slot} is outside the DAT")
    if len(set(record)) != 1:
        raise WriterError(f"target slot {action.chosen_slot} is not an empty filler record")

    candidate = bytearray(data)
    name_offset = action.chosen_offset + NAME_START
    id_offset = action.chosen_offset + NUMERIC_START
    candidate[name_offset : name_offset + NAME_LENGTH] = encode_name(action.name, decode_key)
    candidate[id_offset : id_offset + NUMERIC_LENGTH] = encode_numeric_id(action.numeric_id, decode_key)
    return bytes(candidate)


def validate_name(name: str) -> None:
    try:
        encoded = name.encode("ascii")
    except UnicodeEncodeError as exc:
        raise WriterError("name must contain only ASCII characters") from exc
    if not encoded:
        raise WriterError("name must not be empty")
    if len(encoded) > NAME_LENGTH:
        raise WriterError(f"name must be {NAME_LENGTH} ASCII bytes or fewer")
    if any(byte < 32 or byte > 126 for byte in encoded):
        raise WriterError("name must contain only printable ASCII characters")


def validate_numeric_id(numeric_id: int) -> None:
    if numeric_id < 1 or numeric_id > 65519:
        raise WriterError("talk group numeric ID must be between 1 and 65519")


def encode_name(name: str, decode_key: int) -> bytes:
    return xor_bytes(name.encode("ascii").ljust(NAME_LENGTH, b"\x00"), decode_key)


def encode_numeric_id(numeric_id: int, decode_key: int) -> bytes:
    return xor_bytes(numeric_id.to_bytes(NUMERIC_LENGTH, "little"), decode_key)


def allowed_ranges_for_plan(plan: MergePlan) -> list[ByteRange]:
    ranges = []
    for action in plan.actions:
        if action.action not in {"new_record", "possible_update"}:
            continue
        if action.chosen_offset is None:
            continue
        ranges.append(ByteRange(action.chosen_offset + NAME_START, action.chosen_offset + NAME_START + NAME_LENGTH))
        ranges.append(
            ByteRange(action.chosen_offset + NUMERIC_START, action.chosen_offset + NUMERIC_START + NUMERIC_LENGTH)
        )
    return ranges


def verify_output(data: bytes, candidate: bytes, decode_key: int, plan: MergePlan) -> None:
    verify_only_ranges_changed(data, candidate, allowed_ranges_for_plan(plan))
    expected = {
        action.chosen_slot: (action.name, action.numeric_id)
        for action in plan.actions
        if action.action in {"new_record", "possible_update"} and action.chosen_slot is not None
    }
    records = decode_table(
        candidate,
        TALK_GROUP_TABLE,
        TALK_GROUP_TABLE_NAME,
        TALK_GROUP_TABLE_START,
        decode_key,
        include_empty=True,
        max_records=1024,
    )
    by_slot = {record.slot: record for record in records}
    for slot, (name, numeric_id) in expected.items():
        record = by_slot.get(slot)
        if record is None:
            raise WriterError(f"slot {slot} missing after write")
        if record.name != name or record.numeric_id != numeric_id:
            raise WriterError(
                f"slot {slot} verification failed: {record.name!r}/{record.numeric_id}"
            )


def action_counts(plan: MergePlan) -> Counter[str]:
    return Counter(action.action for action in plan.actions)


def render_range(changed_range: ByteRange) -> str:
    last = changed_range.end - 1
    if changed_range.length == 1:
        return f"0x{changed_range.start:08x}"
    return f"0x{changed_range.start:08x}..0x{last:08x}"


def print_summary(input_csv: Path, baseline: Path, output: Path, rows: list[DvrefRow], plan: MergePlan, ranges: list[ByteRange]) -> None:
    counts = action_counts(plan)
    print("DVREF Talk Group Import Summary")
    print(f"Input CSV: {input_csv}")
    print(f"Baseline DAT: {baseline}")
    print(f"Output DAT: {output}")
    print(f"DVREF rows after duplicate TG removal: {len(rows)}")
    print(f"New talk groups: {counts.get('new_record', 0)}")
    print(f"Updated same-ID talk groups: {counts.get('possible_update', 0)}")
    print(f"Exact duplicates ignored: {counts.get('duplicate_exact', 0)}")
    print(f"Changed byte ranges: {len(ranges)}")
    for changed_range in ranges[:20]:
        print(f"- {render_range(changed_range)} ({changed_range.length} bytes)")
    if len(ranges) > 20:
        print(f"- ... {len(ranges) - 20} more ranges")


def main() -> int:
    args = parse_args()
    try:
        if same_path(args.baseline, args.output) and not args.allow_overwrite_input:
            raise WriterError("refusing to overwrite baseline without --allow-overwrite-input")
        rows = load_dvref_rows(args.input)
        imports = import_records(rows, args.input)
        plan = plan_merge(args.baseline, args.decode_key, imports, max_records=args.max_records)
        validate_plan(plan)
        original = load_dat(args.baseline)
        candidate = apply_plan(original, args.decode_key, plan)
        verify_output(original, candidate, args.decode_key, plan)
        ranges = changed_byte_ranges(original, candidate)
        write_result(args.output, WriteResult(candidate, ranges, TALK_GROUP_TABLE, -1, -1))
        if load_dat(args.output) != candidate:
            raise WriterError("written output does not match candidate bytes")
        print_summary(args.input, args.baseline, args.output, rows, plan, ranges)
        return 0
    except (OSError, ValueError, WriterError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
