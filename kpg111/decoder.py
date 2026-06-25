"""Read-only decoder for known KPG111 Program.dat table records."""

from __future__ import annotations

from pathlib import Path

from .model import DecodedRecord, ProgramTables


PAYLOAD_START = 0x40
RECORD_SIZE = 32
NAME_START = 1
NAME_LENGTH = 14
NUMERIC_START = 19
NUMERIC_LENGTH = 2

INDIVIDUAL_ID_TABLE_START = 0x10480
TALK_GROUP_TABLE_START = 0x14F80

TABLE_DEFINITIONS = (
    ("individual_ids", "Individual IDs", INDIVIDUAL_ID_TABLE_START),
    ("talk_groups", "Talk Groups", TALK_GROUP_TABLE_START),
)


def xor_bytes(data: bytes, key: int) -> bytes:
    return bytes(byte ^ key for byte in data)


def decode_name(record: bytes, decode_key: int) -> str:
    decoded = xor_bytes(record[NAME_START : NAME_START + NAME_LENGTH], decode_key)
    name_bytes = decoded.split(b"\x00", 1)[0]
    if name_bytes and all(32 <= byte <= 126 for byte in name_bytes):
        return name_bytes.decode("ascii")
    return ""


def decode_numeric_id(record: bytes, decode_key: int) -> int:
    decoded = xor_bytes(
        record[NUMERIC_START : NUMERIC_START + NUMERIC_LENGTH],
        decode_key,
    )
    return int.from_bytes(decoded, "little")


def is_empty_record(record: bytes) -> bool:
    return bool(record) and len(set(record)) == 1


def decode_record(
    record: bytes,
    table_id: str,
    table_name: str,
    slot: int,
    offset: int,
    decode_key: int,
) -> DecodedRecord:
    return DecodedRecord(
        table_id=table_id,
        table_name=table_name,
        slot=slot,
        offset=offset,
        name=decode_name(record, decode_key),
        numeric_id=decode_numeric_id(record, decode_key),
        raw_record_hex=record.hex(" "),
        empty=is_empty_record(record),
    )


def is_occupied(record: DecodedRecord) -> bool:
    return bool(record.name) and not record.empty


def decode_table(
    data: bytes,
    table_id: str,
    table_name: str,
    start: int,
    decode_key: int,
    include_empty: bool = False,
    max_records: int = 1024,
) -> list[DecodedRecord]:
    records: list[DecodedRecord] = []
    consecutive_empty = 0
    for slot in range(max_records):
        offset = start + slot * RECORD_SIZE
        if offset + RECORD_SIZE > len(data):
            break

        record_bytes = data[offset : offset + RECORD_SIZE]
        record = decode_record(record_bytes, table_id, table_name, slot, offset, decode_key)
        if is_occupied(record):
            consecutive_empty = 0
            records.append(record)
            continue

        if record.empty:
            consecutive_empty += 1
            if include_empty:
                records.append(record)
            if consecutive_empty >= 2 and not include_empty:
                break
            continue

        consecutive_empty = 0
        if include_empty:
            records.append(record)
    return records


def decode_program_tables(
    path: Path | str,
    decode_key: int,
    include_empty: bool = False,
    max_records: int = 1024,
) -> ProgramTables:
    data = Path(path).read_bytes()
    tables: dict[str, list[DecodedRecord]] = {}
    for table_id, table_name, start in TABLE_DEFINITIONS:
        table_max_records = max_records
        if table_id == "individual_ids":
            table_max_records = min(
                max_records,
                (TALK_GROUP_TABLE_START - INDIVIDUAL_ID_TABLE_START) // RECORD_SIZE,
            )
        tables[table_id] = decode_table(
            data,
            table_id,
            table_name,
            start,
            decode_key,
            include_empty=include_empty,
            max_records=table_max_records,
        )
    return ProgramTables(
        individual_ids=tables["individual_ids"],
        talk_groups=tables["talk_groups"],
    )
