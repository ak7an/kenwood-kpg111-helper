"""Experimental byte-preserving writer for known KPG111 TG/ID records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .decoder import (
    NAME_LENGTH,
    NAME_START,
    NUMERIC_LENGTH,
    NUMERIC_START,
    RECORD_SIZE,
    TABLE_DEFINITIONS,
    decode_table,
    xor_bytes,
)
from .model import DecodedRecord


SUPPORTED_TABLES = {table_id: (table_name, start) for table_id, table_name, start in TABLE_DEFINITIONS}
MIN_NUMERIC_ID = 1
MAX_NUMERIC_ID = 65519


class WriterError(ValueError):
    """Raised when an experimental write would be unsafe or unsupported."""


@dataclass(frozen=True)
class ByteRange:
    """A half-open byte range changed by the writer."""

    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start


@dataclass(frozen=True)
class WriteResult:
    """Candidate DAT bytes plus the exact byte ranges changed."""

    data: bytes
    changed_ranges: list[ByteRange]
    table: str
    slot: int
    record_offset: int


def load_dat(path: Path | str) -> bytes:
    return Path(path).read_bytes()


def rename_record(
    data: bytes,
    decode_key: int,
    table: str,
    slot: int,
    name: str,
) -> WriteResult:
    """Rename one already-decoded occupied Talk Group or Individual ID record."""

    return edit_record(data, decode_key, table, slot, name=name)


def edit_record(
    data: bytes,
    decode_key: int,
    table: str,
    slot: int,
    name: str | None = None,
    numeric_id: int | None = None,
) -> WriteResult:
    """Edit supported fields on one occupied Talk Group or Individual ID record."""

    table_name, table_start = _table_definition(table)
    _validate_slot(slot)
    if name is None and numeric_id is None:
        raise WriterError("at least one supported field change is required")
    if name is not None:
        _validate_name(name)
    if numeric_id is not None:
        _validate_numeric_id(table, numeric_id)

    records = decode_table(
        data,
        table,
        table_name,
        table_start,
        decode_key,
        include_empty=False,
        max_records=_table_max_records(table, len(data)),
    )
    target = next((record for record in records if record.slot == slot), None)
    if target is None:
        raise WriterError(f"slot {slot} is not an occupied decoded record in {table}")

    candidate = bytearray(data)
    allowed_ranges: list[ByteRange] = []

    if name is not None:
        encoded_name = _encode_name(name, decode_key)
        name_offset = target.offset + NAME_START
        candidate[name_offset : name_offset + NAME_LENGTH] = encoded_name
        allowed_ranges.append(ByteRange(name_offset, name_offset + NAME_LENGTH))

    if numeric_id is not None:
        encoded_id = _encode_numeric_id(numeric_id, decode_key)
        numeric_offset = target.offset + NUMERIC_START
        candidate[numeric_offset : numeric_offset + NUMERIC_LENGTH] = encoded_id
        allowed_ranges.append(ByteRange(numeric_offset, numeric_offset + NUMERIC_LENGTH))

    output = bytes(candidate)

    changed_ranges = changed_byte_ranges(data, output)
    verify_only_ranges_changed(data, output, allowed_ranges)
    _verify_edit_decodes(data, output, decode_key, table, slot, name, numeric_id)

    return WriteResult(
        data=output,
        changed_ranges=changed_ranges,
        table=table,
        slot=slot,
        record_offset=target.offset,
    )


def write_result(path: Path | str, result: WriteResult) -> Path:
    output = Path(path)
    output.write_bytes(result.data)
    return output


def changed_byte_ranges(original: bytes, candidate: bytes) -> list[ByteRange]:
    """Return contiguous half-open ranges for all byte differences."""

    if len(original) != len(candidate):
        raise WriterError("candidate size differs from source size")

    ranges: list[ByteRange] = []
    current_start: int | None = None
    for offset, (left, right) in enumerate(zip(original, candidate)):
        if left != right and current_start is None:
            current_start = offset
        elif left == right and current_start is not None:
            ranges.append(ByteRange(current_start, offset))
            current_start = None

    if current_start is not None:
        ranges.append(ByteRange(current_start, len(original)))
    return ranges


def verify_only_ranges_changed(
    original: bytes,
    candidate: bytes,
    allowed_ranges: list[ByteRange],
) -> None:
    """Fail unless every changed byte is inside the supplied ranges."""

    if len(original) != len(candidate):
        raise WriterError("candidate size differs from source size")

    allowed_offsets = {
        offset
        for changed_range in allowed_ranges
        for offset in range(changed_range.start, changed_range.end)
    }
    for offset, (left, right) in enumerate(zip(original, candidate)):
        if left != right and offset not in allowed_offsets:
            raise WriterError(f"unexpected byte change at 0x{offset:08x}")


def _table_definition(table: str) -> tuple[str, int]:
    if table not in SUPPORTED_TABLES:
        raise WriterError(f"unsupported table: {table}")
    return SUPPORTED_TABLES[table]


def _table_max_records(table: str, data_size: int) -> int:
    _table_name, table_start = _table_definition(table)
    if table == "individual_ids":
        talk_group_start = SUPPORTED_TABLES["talk_groups"][1]
        return max(0, (talk_group_start - table_start) // RECORD_SIZE)
    return max(0, (data_size - table_start) // RECORD_SIZE)


def _validate_slot(slot: int) -> None:
    if slot < 0:
        raise WriterError("slot must be non-negative")


def _validate_name(name: str) -> None:
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


def _validate_numeric_id(table: str, numeric_id: int) -> None:
    _table_definition(table)
    if numeric_id < MIN_NUMERIC_ID or numeric_id > MAX_NUMERIC_ID:
        raise WriterError(
            f"{table} numeric ID must be between {MIN_NUMERIC_ID} and {MAX_NUMERIC_ID}"
        )


def _encode_name(name: str, decode_key: int) -> bytes:
    decoded = name.encode("ascii").ljust(NAME_LENGTH, b"\x00")
    return xor_bytes(decoded, decode_key)


def _encode_numeric_id(numeric_id: int, decode_key: int) -> bytes:
    decoded = numeric_id.to_bytes(NUMERIC_LENGTH, "little")
    return xor_bytes(decoded, decode_key)


def _verify_edit_decodes(
    original: bytes,
    candidate: bytes,
    decode_key: int,
    table: str,
    slot: int,
    name: str | None,
    numeric_id: int | None,
) -> None:
    original_records = _decode_known_records(original, decode_key)
    candidate_records = _decode_known_records(candidate, decode_key)

    if original_records.keys() != candidate_records.keys():
        raise WriterError("decoded record set changed unexpectedly")

    for key, original_record in original_records.items():
        candidate_record = candidate_records[key]
        is_target = key == (table, slot)
        expected_name = name if is_target and name is not None else original_record.name
        expected_numeric_id = (
            numeric_id if is_target and numeric_id is not None else original_record.numeric_id
        )
        if candidate_record.name != expected_name:
            raise WriterError(
                f"decoded name mismatch for {key[0]} slot {key[1]}: {candidate_record.name!r}"
            )
        if candidate_record.numeric_id != expected_numeric_id:
            raise WriterError(
                f"decoded numeric ID mismatch for {key[0]} slot {key[1]}: "
                f"{candidate_record.numeric_id}"
            )
        if candidate_record.empty != original_record.empty:
            raise WriterError(f"empty-state changed unexpectedly for {key[0]} slot {key[1]}")


def _decode_known_records(data: bytes, decode_key: int) -> dict[tuple[str, int], DecodedRecord]:
    records_by_key: dict[tuple[str, int], DecodedRecord] = {}
    for table, (table_name, table_start) in SUPPORTED_TABLES.items():
        records = decode_table(
            data,
            table,
            table_name,
            table_start,
            decode_key,
            include_empty=False,
            max_records=_table_max_records(table, len(data)),
        )
        for record in records:
            records_by_key[(table, record.slot)] = record
    return records_by_key
