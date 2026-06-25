"""Read-only record specification discovery for known KPG111 tables."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .allocation import BASELINE_DECODE_KEYS, discover_experiment_pairs
from .decoder import NAME_LENGTH, NAME_START, NUMERIC_LENGTH, NUMERIC_START, RECORD_SIZE
from .decoder import decode_program_tables
from .model import DecodedRecord, ProgramTables


DEFAULT_RESEARCH_ROOTS = (
    Path("research/dattest"),
    Path("research/dattest2"),
    Path("research/dattest3"),
    Path("research/dattest4"),
)


@dataclass(frozen=True)
class FileDecodeProfile:
    path: Path
    decode_key: int
    source: str


@dataclass(frozen=True)
class ByteSpec:
    offset: int
    meaning: str
    encoding: str
    observed_raw_values: tuple[str, ...]
    observed_decoded_values: tuple[str, ...]
    files_observed: tuple[str, ...]
    constant_raw: bool
    constant_decoded: bool
    variable: bool
    reserved: bool
    changes_with_record_edits: str
    confidence: str
    notes: str


@dataclass(frozen=True)
class FieldSpec:
    offset: int
    length: int
    meaning: str
    encoding: str
    observed_values: tuple[str, ...]
    observed_raw_values: tuple[str, ...]
    confidence: str
    notes: str


@dataclass(frozen=True)
class TableRecordSpec:
    table_id: str
    table_name: str
    record_size: int
    record_count_observed: int
    files_observed: tuple[str, ...]
    fields: tuple[FieldSpec, ...]
    bytes: tuple[ByteSpec, ...]
    known_bytes: int
    unknown_bytes: int
    reserved_bytes: int
    known_percentage: float


@dataclass(frozen=True)
class RecordSpecification:
    file_profiles: tuple[FileDecodeProfile, ...]
    shared_fields: tuple[FieldSpec, ...]
    talk_group: TableRecordSpec
    individual_id: TableRecordSpec

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def occupied(record: DecodedRecord) -> bool:
    return bool(record.name) and not record.empty


def table_rows(tables: ProgramTables) -> tuple[tuple[str, str, list[DecodedRecord]], ...]:
    return (
        ("individual_ids", "Individual IDs", tables.individual_ids),
        ("talk_groups", "Talk Groups", tables.talk_groups),
    )


def discover_file_profiles(research_roots: list[Path] | None = None) -> tuple[FileDecodeProfile, ...]:
    roots = research_roots or list(DEFAULT_RESEARCH_ROOTS)
    profiles: dict[Path, FileDecodeProfile] = {}

    for root in roots:
        key = BASELINE_DECODE_KEYS.get(root.name)
        report = root / "reports" / "xor_analysis.json"
        if key is None or not report.exists():
            continue
        data = json.loads(report.read_text(encoding="utf-8"))
        baseline = Path(data["baseline"]["path"])
        profiles[baseline] = FileDecodeProfile(baseline, key, str(report))

    for pair in discover_experiment_pairs(roots):
        profiles[pair.baseline_path] = FileDecodeProfile(
            pair.baseline_path,
            pair.baseline_key,
            pair.source,
        )
        profiles[pair.modified_path] = FileDecodeProfile(
            pair.modified_path,
            pair.modified_key,
            pair.source,
        )

    return tuple(profiles[path] for path in sorted(profiles))


def decoded_byte(raw_hex: str, offset: int, decode_key: int) -> int:
    raw = bytes.fromhex(raw_hex)
    return raw[offset] ^ decode_key


def raw_byte(raw_hex: str, offset: int) -> int:
    return bytes.fromhex(raw_hex)[offset]


def hex_values(values: set[int]) -> tuple[str, ...]:
    return tuple(f"0x{value:02x}" for value in sorted(values))


def ascii_values(values: set[int]) -> tuple[str, ...]:
    rendered = []
    for value in sorted(values):
        if 32 <= value <= 126:
            rendered.append(f"0x{value:02x} '{chr(value)}'")
        elif value == 0:
            rendered.append("0x00 NUL")
        elif value == 0xFF:
            rendered.append("0xff")
        else:
            rendered.append(f"0x{value:02x}")
    return tuple(rendered)


def byte_meaning(offset: int) -> tuple[str, str, bool, str, str]:
    if NAME_START <= offset < NAME_START + NAME_LENGTH:
        return (
            "name byte",
            "raw byte XOR active decode key; ASCII text with NUL padding after decode",
            False,
            "known text field; changes when record name changes",
            "HIGH",
        )
    if NUMERIC_START <= offset < NUMERIC_START + NUMERIC_LENGTH:
        return (
            "numeric ID byte",
            "raw byte XOR active decode key; little-endian uint16 across bytes +19/+20",
            False,
            "known numeric field; changes when record numeric ID changes",
            "HIGH",
        )
    return (
        "UNKNOWN / candidate reserved or padding",
        "observed as raw byte XOR active decode key; decoded values are tracked, but meaning is not proven",
        True,
        "not observed changing independently with record edits in current experiments",
        "MODERATE",
    )


def collect_records(
    profiles: tuple[FileDecodeProfile, ...],
    max_records: int,
) -> dict[str, list[tuple[FileDecodeProfile, DecodedRecord]]]:
    collected: dict[str, list[tuple[FileDecodeProfile, DecodedRecord]]] = {
        "individual_ids": [],
        "talk_groups": [],
    }
    for profile in profiles:
        tables = decode_program_tables(
            profile.path,
            profile.decode_key,
            include_empty=True,
            max_records=max_records,
        )
        for table_id, _table_name, records in table_rows(tables):
            for record in records:
                if occupied(record):
                    collected[table_id].append((profile, record))
    return collected


def build_byte_specs(records: list[tuple[FileDecodeProfile, DecodedRecord]]) -> tuple[ByteSpec, ...]:
    specs = []
    for offset in range(RECORD_SIZE):
        raw_values = {raw_byte(record.raw_record_hex, offset) for _profile, record in records}
        decoded_values = {
            decoded_byte(record.raw_record_hex, offset, profile.decode_key)
            for profile, record in records
        }
        files = {str(profile.path) for profile, _record in records}
        meaning, encoding, reserved, edit_note, confidence = byte_meaning(offset)
        specs.append(
            ByteSpec(
                offset=offset,
                meaning=meaning,
                encoding=encoding,
                observed_raw_values=hex_values(raw_values),
                observed_decoded_values=ascii_values(decoded_values),
                files_observed=tuple(sorted(files)),
                constant_raw=len(raw_values) == 1,
                constant_decoded=len(decoded_values) == 1,
                variable=len(decoded_values) > 1,
                reserved=reserved,
                changes_with_record_edits="yes" if not reserved else "not observed",
                confidence=confidence,
                notes=edit_note,
            )
        )
    return tuple(specs)


def field_raw_values(
    records: list[tuple[FileDecodeProfile, DecodedRecord]],
    offset: int,
    length: int,
) -> tuple[str, ...]:
    values = {
        bytes.fromhex(record.raw_record_hex)[offset : offset + length].hex(" ")
        for _profile, record in records
    }
    return tuple(sorted(values))


def field_decoded_values(
    records: list[tuple[FileDecodeProfile, DecodedRecord]],
    offset: int,
    length: int,
) -> tuple[str, ...]:
    values = set()
    for profile, record in records:
        raw = bytes.fromhex(record.raw_record_hex)[offset : offset + length]
        decoded = bytes(byte ^ profile.decode_key for byte in raw)
        if offset == NAME_START:
            values.add(decoded.split(b"\x00", 1)[0].decode("ascii", errors="replace"))
        elif offset == NUMERIC_START:
            values.add(str(int.from_bytes(decoded, "little")))
        else:
            values.add(decoded.hex(" "))
    return tuple(sorted(values))


def build_field_specs(records: list[tuple[FileDecodeProfile, DecodedRecord]]) -> tuple[FieldSpec, ...]:
    field_defs = (
        (
            0,
            1,
            "UNKNOWN / candidate record marker or reserved byte",
            "raw byte XOR active decode key; decoded value observed but meaning unknown",
            "MODERATE",
            "Decoded value is constant in observed occupied records; semantic role is not proven.",
        ),
        (
            NAME_START,
            NAME_LENGTH,
            "name",
            "14 bytes; raw bytes XOR active decode key; ASCII text terminated/padded with decoded NUL",
            "HIGH",
            "Controlled rename/add experiments change this field.",
        ),
        (
            15,
            4,
            "UNKNOWN / candidate reserved or padding",
            "raw bytes XOR active decode key; decoded values observed but meaning unknown",
            "MODERATE",
            "Not observed changing independently with record edits.",
        ),
        (
            NUMERIC_START,
            NUMERIC_LENGTH,
            "numeric ID",
            "2 bytes; raw bytes XOR active decode key; little-endian uint16",
            "HIGH",
            "Controlled numeric experiments support little-endian decoding.",
        ),
        (
            21,
            11,
            "UNKNOWN / candidate reserved or padding",
            "raw bytes XOR active decode key; decoded values observed but meaning unknown",
            "MODERATE",
            "Not observed changing independently with record edits.",
        ),
    )
    return tuple(
        FieldSpec(
            offset=offset,
            length=length,
            meaning=meaning,
            encoding=encoding,
            observed_values=field_decoded_values(records, offset, length),
            observed_raw_values=field_raw_values(records, offset, length),
            confidence=confidence,
            notes=notes,
        )
        for offset, length, meaning, encoding, confidence, notes in field_defs
    )


def table_spec(
    table_id: str,
    table_name: str,
    records: list[tuple[FileDecodeProfile, DecodedRecord]],
) -> TableRecordSpec:
    byte_specs = build_byte_specs(records)
    field_specs = build_field_specs(records)
    known = sum(1 for spec in byte_specs if spec.confidence == "HIGH")
    reserved = sum(1 for spec in byte_specs if spec.reserved)
    unknown = RECORD_SIZE - known
    files = {str(profile.path) for profile, _record in records}
    return TableRecordSpec(
        table_id=table_id,
        table_name=table_name,
        record_size=RECORD_SIZE,
        record_count_observed=len(records),
        files_observed=tuple(sorted(files)),
        fields=field_specs,
        bytes=byte_specs,
        known_bytes=known,
        unknown_bytes=unknown,
        reserved_bytes=reserved,
        known_percentage=round((known / RECORD_SIZE) * 100, 1),
    )


def record_spec(
    research_roots: list[Path | str] | None = None,
    max_records: int = 1024,
) -> RecordSpecification:
    roots = [Path(root) for root in research_roots] if research_roots else list(DEFAULT_RESEARCH_ROOTS)
    profiles = discover_file_profiles(roots)
    records = collect_records(profiles, max_records)
    shared = build_field_specs(records["individual_ids"] + records["talk_groups"])
    return RecordSpecification(
        file_profiles=profiles,
        shared_fields=shared,
        individual_id=table_spec("individual_ids", "Individual ID record", records["individual_ids"]),
        talk_group=table_spec("talk_groups", "Talk Group record", records["talk_groups"]),
    )
