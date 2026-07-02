"""Talk Group Manager built on immutable Codeplug instances."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .decoder import (
    NAME_LENGTH,
    NAME_START,
    NUMERIC_LENGTH,
    NUMERIC_START,
    RECORD_SIZE,
    TALK_GROUP_TABLE_START,
    decode_table,
)
from .model import DecodedRecord
from .project import Codeplug
from .writer import (
    ByteRange,
    WriterError,
    changed_byte_ranges,
    encode_name,
    encode_numeric_id,
    validate_name,
    validate_numeric_id,
    verify_only_ranges_changed,
)

TALK_GROUP_TABLE = "talk_groups"
TALK_GROUP_TABLE_NAME = "Talk Groups"
DEFAULT_TALK_GROUP_CAPACITY = 400
SAFE_TALK_GROUP_SLOTS = tuple(
    list(range(200, 300))
    + list(range(343, 351))
    + list(range(354, 400))
)


@dataclass(frozen=True)
class TalkGroupChange:
    name: str
    numeric_id: int


class TalkGroupManager:
    """Apply proven Talk Group changes without mutating the source Codeplug."""

    def __init__(
        self,
        codeplug: Codeplug,
        *,
        table_start: int = TALK_GROUP_TABLE_START,
        capacity: int = DEFAULT_TALK_GROUP_CAPACITY,
    ) -> None:
        self.codeplug = codeplug
        self.table_start = table_start
        self.capacity = capacity

    def records(self, *, include_empty: bool = False) -> list[DecodedRecord]:
        return decode_table(
            self.codeplug.to_bytes(),
            TALK_GROUP_TABLE,
            TALK_GROUP_TABLE_NAME,
            self.table_start,
            self.codeplug.decode_key,
            include_empty=include_empty,
            max_records=self.capacity,
        )

    def add(self, name: str, numeric_id: int) -> Codeplug:
        validate_name(name)
        validate_numeric_id(TALK_GROUP_TABLE, numeric_id)
        self._reject_duplicate(name, numeric_id)
        target = self._first_safe_empty_slot()
        if target is None:
            raise WriterError("no safe empty Talk Group slot is available")
        return self._write_known_fields(target.slot, name, numeric_id)

    def update(
        self,
        slot: int,
        *,
        name: str | None = None,
        numeric_id: int | None = None,
    ) -> Codeplug:
        return self.codeplug.edit_record(
            TALK_GROUP_TABLE,
            slot,
            name=name,
            numeric_id=numeric_id,
        )

    def delete(self, slot: int) -> Codeplug:
        self._require_occupied_slot(slot)
        raise WriterError(
            "Talk Group delete is not write-supported yet because safe clearing "
            "would require modifying unverified record bytes"
        )

    def merge(self, records: Iterable[TalkGroupChange]) -> Codeplug:
        codeplug = self.codeplug
        for record in records:
            manager = TalkGroupManager(
                codeplug,
                table_start=self.table_start,
                capacity=self.capacity,
            )
            existing = manager._find_by_numeric_id(record.numeric_id)
            if existing is None:
                codeplug = manager.add(record.name, record.numeric_id)
                continue
            if existing.name != record.name:
                codeplug = manager.update(existing.slot, name=record.name)
        return codeplug

    def replace(self, records: Iterable[TalkGroupChange]) -> Codeplug:
        desired = list(records)
        desired_ids = {record.numeric_id for record in desired}
        existing_ids = {
            record.numeric_id
            for record in self.records()
            if _occupied(record)
        }
        removed = existing_ids - desired_ids
        if removed:
            raise WriterError(
                "Talk Group replace would require delete support for existing IDs: "
                + ", ".join(str(value) for value in sorted(removed))
            )
        return self.merge(desired)

    def sort(self, *, key: str = "numeric_id") -> Codeplug:
        if key not in {"numeric_id", "name"}:
            raise WriterError(f"unsupported Talk Group sort key: {key}")
        records = [record for record in self.records() if _occupied(record)]
        key_fn = (lambda record: record.numeric_id) if key == "numeric_id" else (lambda record: record.name)
        if records == sorted(records, key=key_fn):
            return self.codeplug
        raise WriterError(
            "Talk Group physical sort is not write-supported yet because safe "
            "reordering would require unverified record movement"
        )

    def _write_known_fields(self, slot: int, name: str, numeric_id: int) -> Codeplug:
        data = self.codeplug.to_bytes()
        offset = self.table_start + slot * RECORD_SIZE
        record = data[offset : offset + RECORD_SIZE]
        if len(record) != RECORD_SIZE:
            raise WriterError(f"target slot {slot} is outside the DAT")
        if len(set(record)) != 1:
            raise WriterError(f"target slot {slot} is not an empty filler record")

        candidate = bytearray(data)
        candidate[offset + NAME_START : offset + NAME_START + NAME_LENGTH] = encode_name(
            name,
            self.codeplug.decode_key,
        )
        candidate[offset + NUMERIC_START : offset + NUMERIC_START + NUMERIC_LENGTH] = encode_numeric_id(
            numeric_id,
            self.codeplug.decode_key,
        )
        output = bytes(candidate)
        allowed = [
            ByteRange(offset + NAME_START, offset + NAME_START + NAME_LENGTH),
            ByteRange(offset + NUMERIC_START, offset + NUMERIC_START + NUMERIC_LENGTH),
        ]
        verify_only_ranges_changed(data, output, allowed)
        self._verify_slot_decodes(output, slot, name, numeric_id)
        return Codeplug(
            output,
            source_path=self.codeplug.source_path,
            decode_key=self.codeplug.decode_key,
            changed_ranges=tuple(changed_byte_ranges(data, output)),
        )

    def _verify_slot_decodes(self, data: bytes, slot: int, name: str, numeric_id: int) -> None:
        records = decode_table(
            data,
            TALK_GROUP_TABLE,
            TALK_GROUP_TABLE_NAME,
            self.table_start,
            self.codeplug.decode_key,
            include_empty=True,
            max_records=self.capacity,
        )
        target = next((record for record in records if record.slot == slot), None)
        if target is None:
            raise WriterError(f"target slot {slot} did not decode after write")
        if target.name != name or target.numeric_id != numeric_id:
            raise WriterError(f"target slot {slot} did not decode to requested Talk Group")

    def _first_safe_empty_slot(self) -> DecodedRecord | None:
        by_slot = {record.slot: record for record in self.records(include_empty=True)}
        data = self.codeplug.to_bytes()
        for slot in SAFE_TALK_GROUP_SLOTS:
            if slot >= self.capacity:
                continue
            record = by_slot.get(slot)
            if record is None or not record.empty:
                continue
            offset = self.table_start + slot * RECORD_SIZE
            raw = data[offset : offset + RECORD_SIZE]
            if len(raw) == RECORD_SIZE and len(set(raw)) == 1:
                return record
        return None

    def _find_by_numeric_id(self, numeric_id: int) -> DecodedRecord | None:
        for record in self.records():
            if _occupied(record) and record.numeric_id == numeric_id:
                return record
        return None

    def _find_by_name(self, name: str) -> DecodedRecord | None:
        for record in self.records():
            if _occupied(record) and record.name == name:
                return record
        return None

    def _reject_duplicate(self, name: str, numeric_id: int) -> None:
        same_id = self._find_by_numeric_id(numeric_id)
        if same_id is not None:
            raise WriterError(f"Talk Group numeric ID already exists at slot {same_id.slot}")
        same_name = self._find_by_name(name)
        if same_name is not None:
            raise WriterError(f"Talk Group name already exists at slot {same_name.slot}")

    def _require_occupied_slot(self, slot: int) -> DecodedRecord:
        for record in self.records():
            if record.slot == slot and _occupied(record):
                return record
        raise WriterError(f"slot {slot} is not an occupied Talk Group record")


def _occupied(record: DecodedRecord) -> bool:
    return bool(record.name) and not record.empty
