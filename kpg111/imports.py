"""CSV import parsing for read-only KPG111 merge planning."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


VALID_TYPES = {
    "TG": "talk_groups",
    "TALKGROUP": "talk_groups",
    "INDIVIDUAL": "individual_ids",
    "ID": "individual_ids",
}


@dataclass(frozen=True)
class ImportRecord:
    record_type: str
    name: str
    numeric_id: int
    source_file: str
    source_row: int


def normalize_type(value: str) -> str:
    key = value.strip().upper()
    if key not in VALID_TYPES:
        raise ValueError(f"invalid type {value!r}")
    return VALID_TYPES[key]


def load_import_csv(path: Path | str) -> list[ImportRecord]:
    source = Path(path)
    records: list[ImportRecord] = []
    with source.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{source}: missing header row")
        required = {"type", "name", "id"}
        fieldnames = {field.strip() for field in reader.fieldnames}
        missing = sorted(required - fieldnames)
        if missing:
            raise ValueError(f"{source}: missing required columns: {', '.join(missing)}")

        for row_number, row in enumerate(reader, start=2):
            raw_type = (row.get("type") or "").strip()
            raw_name = (row.get("name") or "").strip()
            raw_id = (row.get("id") or "").strip()

            if not raw_name:
                raise ValueError(f"{source}:{row_number}: name is blank")
            try:
                record_type = normalize_type(raw_type)
            except ValueError as exc:
                raise ValueError(f"{source}:{row_number}: {exc}") from exc
            try:
                numeric_id = int(raw_id, 10)
            except ValueError as exc:
                raise ValueError(f"{source}:{row_number}: id is not an integer: {raw_id!r}") from exc

            records.append(
                ImportRecord(
                    record_type=record_type,
                    name=raw_name,
                    numeric_id=numeric_id,
                    source_file=str(source),
                    source_row=row_number,
                )
            )
    return records


def load_import_csvs(paths: list[Path] | list[str]) -> list[ImportRecord]:
    records: list[ImportRecord] = []
    for path in paths:
        records.extend(load_import_csv(path))
    return records
