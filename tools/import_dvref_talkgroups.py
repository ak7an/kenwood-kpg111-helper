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
    RECORD_SIZE,
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
TABLE_FULL_REASON = "no empty slot available within scanned table capacity"
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


@dataclass(frozen=True)
class ImportSummary:
    mode: str
    imported: int
    updated: int
    exact_duplicates: int
    skipped_ids: list[int]
    existing_talk_groups: int
    empty_slots: int


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
        "--talk-group-capacity",
        type=int,
        help="Explicit scanned/allowed talk group table capacity, e.g. 400",
    )
    parser.add_argument(
        "--talk-group-start",
        type=lambda value: int(value, 0),
        default=TALK_GROUP_TABLE_START,
        help="Explicit Talk Group table start offset, e.g. 0x14940 or 0x14f80",
    )
    parser.add_argument(
        "--mode",
        choices=("merge", "replace"),
        default="merge",
        help="Import mode: merge into empty slots or replace the Talk Group list (default: merge)",
    )
    parser.add_argument(
        "--allow-overwrite-input",
        action="store_true",
        help="Allow --output to be the same path as --baseline.",
    )
    return parser.parse_args()


def effective_talk_group_capacity(args: argparse.Namespace) -> int:
    capacity = (
        args.talk_group_capacity
        if args.talk_group_capacity is not None
        else args.max_records
    )
    if capacity <= 0:
        raise WriterError("--talk-group-capacity must be > 0")
    return capacity


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
    if ascii_text:
        name = ascii_text
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


def validate_plan(plan: MergePlan, talk_group_capacity: int) -> None:
    bad_actions = [
        action for action in plan.actions
        if action.action in {"invalid", "duplicate_name_id_diff"}
        and not is_table_full_skip(action)
    ]
    if bad_actions:
        details = "; ".join(
            f"row {action.source_row} TG {action.numeric_id} {action.name!r}: {action.reason}"
            for action in bad_actions[:10]
        )
        raise WriterError(f"merge plan has rejected/conflicting rows: {details}")
    out_of_capacity = [
        action for action in plan.actions
        if action.chosen_slot is not None and action.chosen_slot >= talk_group_capacity
    ]
    if out_of_capacity:
        details = "; ".join(
            f"row {action.source_row} TG {action.numeric_id} slot {action.chosen_slot}"
            for action in out_of_capacity[:10]
        )
        raise WriterError(
            f"merge plan exceeds talk group capacity {talk_group_capacity}: {details}"
        )


def apply_plan(
    data: bytes,
    decode_key: int,
    plan: MergePlan,
    talk_group_start: int = TALK_GROUP_TABLE_START,
) -> bytes:
    candidate = data
    template = first_occupied_talk_group_record(data, decode_key, talk_group_start)
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
            candidate = add_talk_group_record(candidate, decode_key, action, template)
            continue
        if is_table_full_skip(action):
            continue
        raise WriterError(f"unsupported planner action: {action.action}")
    return candidate


def add_talk_group_record(
    data: bytes,
    decode_key: int,
    action: PlannedAction,
    template: bytes,
) -> bytes:
    if action.chosen_slot is None or action.chosen_offset is None:
        raise WriterError(f"missing target slot for row {action.source_row}")
    validate_name(action.name)
    validate_numeric_id(action.numeric_id)

    record = data[action.chosen_offset : action.chosen_offset + RECORD_SIZE]
    if len(record) != RECORD_SIZE:
        raise WriterError(f"target slot {action.chosen_slot} is outside the DAT")
    if len(set(record)) != 1:
        raise WriterError(f"target slot {action.chosen_slot} is not an empty filler record")

    initialized = build_talk_group_record(template, action.name, action.numeric_id, decode_key)
    candidate = bytearray(data)
    candidate[action.chosen_offset : action.chosen_offset + RECORD_SIZE] = initialized
    return bytes(candidate)


def build_talk_group_record(template: bytes, name: str, numeric_id: int, decode_key: int) -> bytes:
    if len(template) != RECORD_SIZE:
        raise WriterError("template talk group record has invalid length")
    validate_name(name)
    validate_numeric_id(numeric_id)

    record = bytearray(template)
    record[NAME_START : NAME_START + NAME_LENGTH] = encode_name(name, decode_key)
    record[NUMERIC_START : NUMERIC_START + NUMERIC_LENGTH] = encode_numeric_id(numeric_id, decode_key)
    return bytes(record)


def first_occupied_talk_group_record(
    data: bytes,
    decode_key: int,
    talk_group_start: int = TALK_GROUP_TABLE_START,
) -> bytes:
    records = decode_table(
        data,
        TALK_GROUP_TABLE,
        TALK_GROUP_TABLE_NAME,
        talk_group_start,
        decode_key,
        include_empty=False,
        max_records=max_talk_group_records(data, talk_group_start),
    )
    for record in records:
        if record.name and not record.empty:
            raw = data[record.offset : record.offset + RECORD_SIZE]
            if len(raw) == RECORD_SIZE:
                return raw
    raise WriterError("no occupied Talk Group record available for template")


def empty_talk_group_record(
    data: bytes,
    decode_key: int,
    talk_group_capacity: int,
    talk_group_start: int = TALK_GROUP_TABLE_START,
) -> bytes:
    for slot in range(talk_group_capacity):
        offset = talk_group_start + slot * RECORD_SIZE
        record = data[offset : offset + RECORD_SIZE]
        if len(record) != RECORD_SIZE:
            break
        if len(set(record)) == 1:
            return record
    template = first_occupied_talk_group_record(data, decode_key, talk_group_start)
    return bytes([template[0]]) * RECORD_SIZE


def max_talk_group_records(data: bytes, talk_group_start: int = TALK_GROUP_TABLE_START) -> int:
    return max(0, (len(data) - talk_group_start) // RECORD_SIZE)


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
        if action.action == "new_record":
            ranges.append(ByteRange(action.chosen_offset, action.chosen_offset + RECORD_SIZE))
            continue
        ranges.append(ByteRange(action.chosen_offset + NAME_START, action.chosen_offset + NAME_START + NAME_LENGTH))
        ranges.append(
            ByteRange(action.chosen_offset + NUMERIC_START, action.chosen_offset + NUMERIC_START + NUMERIC_LENGTH)
        )
    return ranges


def allowed_talk_group_capacity_ranges(
    talk_group_capacity: int,
    talk_group_start: int = TALK_GROUP_TABLE_START,
) -> list[ByteRange]:
    return [
        ByteRange(
            talk_group_start,
            talk_group_start + talk_group_capacity * RECORD_SIZE,
        )
    ]


def verify_output(
    data: bytes,
    candidate: bytes,
    decode_key: int,
    plan: MergePlan,
    talk_group_capacity: int,
    talk_group_start: int = TALK_GROUP_TABLE_START,
) -> None:
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
        talk_group_start,
        decode_key,
        include_empty=True,
        max_records=talk_group_capacity,
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


def apply_replace(
    data: bytes,
    decode_key: int,
    rows: list[DvrefRow],
    talk_group_capacity: int,
    talk_group_start: int = TALK_GROUP_TABLE_START,
) -> bytes:
    if talk_group_capacity > max_talk_group_records(data, talk_group_start):
        raise WriterError("talk group capacity extends beyond DAT size")

    template = first_occupied_talk_group_record(data, decode_key, talk_group_start)
    empty_record = empty_talk_group_record(
        data,
        decode_key,
        talk_group_capacity,
        talk_group_start,
    )
    candidate = bytearray(data)

    for slot in range(talk_group_capacity):
        offset = TALK_GROUP_TABLE_START + slot * RECORD_SIZE
        if slot < len(rows):
            row = rows[slot]
            record = build_talk_group_record(template, row.name, row.tg_id, decode_key)
        else:
            record = empty_record
        candidate[offset : offset + RECORD_SIZE] = record

    return bytes(candidate)


def verify_replace_output(
    data: bytes,
    candidate: bytes,
    decode_key: int,
    rows: list[DvrefRow],
    talk_group_capacity: int,
    talk_group_start: int = TALK_GROUP_TABLE_START,
) -> None:
    verify_only_ranges_changed(
        data,
        candidate,
        allowed_talk_group_capacity_ranges(talk_group_capacity, talk_group_start),
    )
    expected_rows = rows[:talk_group_capacity]
    records = decode_table(
        candidate,
        TALK_GROUP_TABLE,
        TALK_GROUP_TABLE_NAME,
        talk_group_start,
        decode_key,
        include_empty=True,
        max_records=talk_group_capacity,
    )
    by_slot = {record.slot: record for record in records}
    for slot, row in enumerate(expected_rows):
        record = by_slot.get(slot)
        if record is None:
            raise WriterError(f"slot {slot} missing after replace")
        if record.name != row.name or record.numeric_id != row.tg_id:
            raise WriterError(
                f"slot {slot} verification failed: {record.name!r}/{record.numeric_id}"
            )
    for slot in range(len(expected_rows), talk_group_capacity):
        record = by_slot.get(slot)
        if record is not None and not record.empty:
            raise WriterError(f"slot {slot} was not cleared during replace")


def action_counts(plan: MergePlan) -> Counter[str]:
    return Counter(action.action for action in plan.actions)


def is_table_full_skip(action: PlannedAction) -> bool:
    return action.action == "invalid" and action.reason == TABLE_FULL_REASON


def table_full_skips(plan: MergePlan) -> list[PlannedAction]:
    return [action for action in plan.actions if is_table_full_skip(action)]


def existing_talk_group_count(
    data: bytes,
    decode_key: int,
    talk_group_capacity: int,
    talk_group_start: int = TALK_GROUP_TABLE_START,
) -> int:
    records = decode_table(
        data,
        TALK_GROUP_TABLE,
        TALK_GROUP_TABLE_NAME,
        talk_group_start,
        decode_key,
        include_empty=True,
        max_records=talk_group_capacity,
    )
    return sum(1 for record in records if record.name and not record.empty)


def empty_talk_group_count(
    data: bytes,
    decode_key: int,
    talk_group_capacity: int,
    talk_group_start: int = TALK_GROUP_TABLE_START,
) -> int:
    records = decode_table(
        data,
        TALK_GROUP_TABLE,
        TALK_GROUP_TABLE_NAME,
        talk_group_start,
        decode_key,
        include_empty=True,
        max_records=talk_group_capacity,
    )
    return sum(1 for record in records if record.empty)


def render_range(changed_range: ByteRange) -> str:
    last = changed_range.end - 1
    if changed_range.length == 1:
        return f"0x{changed_range.start:08x}"
    return f"0x{changed_range.start:08x}..0x{last:08x}"


def print_summary(
    input_csv: Path,
    baseline: Path,
    output: Path,
    rows: list[DvrefRow],
    ranges: list[ByteRange],
    talk_group_capacity: int,
    summary: ImportSummary,
) -> None:
    print("DVREF Talk Group Import Summary")
    print(f"Mode: {summary.mode}")
    print(f"Input CSV: {input_csv}")
    print(f"Baseline DAT: {baseline}")
    print(f"Output DAT: {output}")
    print(f"Talk group capacity: {talk_group_capacity}")
    print(f"DVREF rows after duplicate TG removal: {len(rows)}")
    print(f"Existing TGs: {summary.existing_talk_groups}")
    print(f"Empty slots: {summary.empty_slots}")
    print(f"Imported: {summary.imported}")
    print(f"Updated: {summary.updated}")
    print(f"Skipped (table full): {len(summary.skipped_ids)}")
    if summary.skipped_ids:
        skipped_ids = ", ".join(str(tg_id) for tg_id in summary.skipped_ids)
        print(f"TG IDs skipped (table full): {skipped_ids}")
    print(f"New talk groups: {summary.imported}")
    print(f"Updated same-ID talk groups: {summary.updated}")
    print(f"Exact duplicates ignored: {summary.exact_duplicates}")
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
        talk_group_capacity = effective_talk_group_capacity(args)
        rows = load_dvref_rows(args.input)
        original = load_dat(args.baseline)
        if talk_group_capacity > max_talk_group_records(original, args.talk_group_start):
            raise WriterError("talk group capacity extends beyond DAT size")
        existing_talk_groups = existing_talk_group_count(
            original,
            args.decode_key,
            talk_group_capacity,
            args.talk_group_start,
        )
        empty_slots = empty_talk_group_count(
            original,
            args.decode_key,
            talk_group_capacity,
            args.talk_group_start,
        )

        if args.mode == "merge":
            imports = import_records(rows, args.input)
            plan = plan_merge(args.baseline, args.decode_key, imports, max_records=talk_group_capacity)
            validate_plan(plan, talk_group_capacity)
            candidate = apply_plan(original, args.decode_key, plan, args.talk_group_start)
            verify_output(
                original,
                candidate,
                args.decode_key,
                plan,
                talk_group_capacity,
                args.talk_group_start,
            )
            counts = action_counts(plan)
            skipped_ids = [action.numeric_id for action in table_full_skips(plan)]
            summary = ImportSummary(
                mode=args.mode,
                imported=counts.get("new_record", 0),
                updated=counts.get("possible_update", 0),
                exact_duplicates=counts.get("duplicate_exact", 0),
                skipped_ids=skipped_ids,
                existing_talk_groups=existing_talk_groups,
                empty_slots=empty_slots,
            )
        else:
            candidate = apply_replace(
                original,
                args.decode_key,
                rows,
                talk_group_capacity,
                args.talk_group_start,
            )
            verify_replace_output(
                original,
                candidate,
                args.decode_key,
                rows,
                talk_group_capacity,
                args.talk_group_start,
            )
            skipped_ids = [row.tg_id for row in rows[talk_group_capacity:]]
            summary = ImportSummary(
                mode=args.mode,
                imported=min(len(rows), talk_group_capacity),
                updated=0,
                exact_duplicates=0,
                skipped_ids=skipped_ids,
                existing_talk_groups=existing_talk_groups,
                empty_slots=empty_slots,
            )

        ranges = changed_byte_ranges(original, candidate)
        write_result(args.output, WriteResult(candidate, ranges, TALK_GROUP_TABLE, -1, -1))
        if load_dat(args.output) != candidate:
            raise WriterError("written output does not match candidate bytes")
        print_summary(
            args.input,
            args.baseline,
            args.output,
            rows,
            ranges,
            talk_group_capacity,
            summary,
        )
        return 0
    except (OSError, ValueError, WriterError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
