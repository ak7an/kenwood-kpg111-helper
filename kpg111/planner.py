"""Read-only merge planning for decoded KPG111 tables."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .decoder import RECORD_SIZE, decode_program_tables
from .imports import ImportRecord
from .model import DecodedRecord


TABLE_LABELS = {
    "individual_ids": "Individual IDs",
    "talk_groups": "Talk Groups",
}


@dataclass(frozen=True)
class PlannedAction:
    table: str
    action: str
    recommended_action: str
    source_file: str
    source_row: int
    name: str
    numeric_id: int
    chosen_slot: int | None
    chosen_offset: int | None
    reason: str


@dataclass(frozen=True)
class MergePlan:
    actions: list[PlannedAction]
    empty_slots_available: dict[str, int]
    append_slots_needed: dict[str, int]


def occupied(record: DecodedRecord) -> bool:
    return bool(record.name) and not record.empty


def table_records_by_type(
    program_path: Path | str,
    decode_key: int,
    max_records: int,
) -> dict[str, list[DecodedRecord]]:
    tables = decode_program_tables(
        program_path,
        decode_key,
        include_empty=True,
        max_records=max_records,
    )
    return {
        "individual_ids": trim_after_table(tables.individual_ids),
        "talk_groups": trim_after_table(tables.talk_groups),
    }


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


def find_existing(
    records: list[DecodedRecord],
    name: str,
    numeric_id: int,
) -> tuple[DecodedRecord | None, DecodedRecord | None, DecodedRecord | None]:
    exact = None
    same_id = None
    same_name = None
    for record in records:
        if not occupied(record):
            continue
        if record.name == name and record.numeric_id == numeric_id:
            exact = record
        if record.numeric_id == numeric_id and record.name != name:
            same_id = record
        if record.name == name and record.numeric_id != numeric_id:
            same_name = record
    return exact, same_id, same_name


def first_empty_slot(records: list[DecodedRecord], reserved_slots: set[int]) -> DecodedRecord | None:
    for record in records:
        if record.empty and record.slot not in reserved_slots:
            return record
    return None


def append_slot(records: list[DecodedRecord], reserved_slots: set[int]) -> DecodedRecord | None:
    occupied_records = [record for record in records if occupied(record) or record.slot in reserved_slots]
    if occupied_records:
        next_slot = max(record.slot for record in occupied_records) + 1
    else:
        next_slot = 0
    for record in records:
        if record.slot == next_slot and record.empty and record.slot not in reserved_slots:
            return record
    return None


def plan_merge(
    program_path: Path | str,
    decode_key: int,
    imports: list[ImportRecord],
    max_records: int = 1024,
    include_existing: bool = False,
) -> MergePlan:
    tables = table_records_by_type(program_path, decode_key, max_records)
    reserved_slots: dict[str, set[int]] = {
        "individual_ids": set(),
        "talk_groups": set(),
    }
    append_needed = {
        "individual_ids": 0,
        "talk_groups": 0,
    }
    actions: list[PlannedAction] = []

    for item in imports:
        records = tables[item.record_type]
        table_name = TABLE_LABELS[item.record_type]
        exact, same_id, same_name = find_existing(records, item.name, item.numeric_id)

        if exact:
            actions.append(
                PlannedAction(
                    table=table_name,
                    action="duplicate_exact",
                    recommended_action="ignore",
                    source_file=item.source_file,
                    source_row=item.source_row,
                    name=item.name,
                    numeric_id=item.numeric_id,
                    chosen_slot=exact.slot if include_existing else None,
                    chosen_offset=exact.offset if include_existing else None,
                    reason=f"same name and numeric ID already exist at slot {exact.slot}",
                )
            )
            continue
        if same_id:
            actions.append(
                PlannedAction(
                    table=table_name,
                    action="possible_update",
                    recommended_action="review_update",
                    source_file=item.source_file,
                    source_row=item.source_row,
                    name=item.name,
                    numeric_id=item.numeric_id,
                    chosen_slot=same_id.slot,
                    chosen_offset=same_id.offset,
                    reason="numeric ID exists with different name; may be rename/update",
                )
            )
            continue
        if same_name:
            actions.append(
                PlannedAction(
                    table=table_name,
                    action="duplicate_name_id_diff",
                    recommended_action="review_name_conflict",
                    source_file=item.source_file,
                    source_row=item.source_row,
                    name=item.name,
                    numeric_id=item.numeric_id,
                    chosen_slot=same_name.slot,
                    chosen_offset=same_name.offset,
                    reason=f"name already exists with numeric ID {same_name.numeric_id}",
                )
            )
            continue
        if item.numeric_id < 0 or item.numeric_id > 0xFFFF:
            actions.append(
                PlannedAction(
                    table=table_name,
                    action="invalid",
                    recommended_action="reject",
                    source_file=item.source_file,
                    source_row=item.source_row,
                    name=item.name,
                    numeric_id=item.numeric_id,
                    chosen_slot=None,
                    chosen_offset=None,
                    reason="numeric ID outside uint16 range",
                )
            )
            continue

        chosen = first_empty_slot(records, reserved_slots[item.record_type])
        reason = "candidate first empty slot"
        if chosen is None:
            chosen = append_slot(records, reserved_slots[item.record_type])
            reason = "candidate append slot after last occupied record"
            append_needed[item.record_type] += 1

        if chosen is None:
            actions.append(
                PlannedAction(
                    table=table_name,
                    action="invalid",
                    recommended_action="reject",
                    source_file=item.source_file,
                    source_row=item.source_row,
                    name=item.name,
                    numeric_id=item.numeric_id,
                    chosen_slot=None,
                    chosen_offset=None,
                    reason="no empty slot available within scanned table capacity",
                )
            )
            continue

        reserved_slots[item.record_type].add(chosen.slot)
        actions.append(
            PlannedAction(
                table=table_name,
                action="new_record",
                recommended_action="candidate_add",
                source_file=item.source_file,
                source_row=item.source_row,
                name=item.name,
                numeric_id=item.numeric_id,
                chosen_slot=chosen.slot,
                chosen_offset=chosen.offset,
                reason=reason,
            )
        )

    empty_available = {
        table_id: sum(1 for record in records if record.empty and record.slot not in reserved_slots[table_id])
        for table_id, records in tables.items()
    }
    return MergePlan(
        actions=actions,
        empty_slots_available=empty_available,
        append_slots_needed=append_needed,
    )
