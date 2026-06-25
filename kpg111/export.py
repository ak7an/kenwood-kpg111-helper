"""CSV export helpers for decoded KPG111 tables."""

from __future__ import annotations

import csv
from pathlib import Path

from .model import DecodedRecord, ProgramTables


def occupied(record: DecodedRecord) -> bool:
    return bool(record.name) and not record.empty


def output_name(base: str, prefix: str | None) -> str:
    return f"{prefix}_{base}" if prefix else base


def rows_for_export(records: list[DecodedRecord], include_empty: bool) -> list[DecodedRecord]:
    if include_empty:
        return records
    return [record for record in records if occupied(record)]


def write_table_csv(path: Path, records: list[DecodedRecord], include_empty: bool) -> int:
    rows = rows_for_export(records, include_empty)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "table_id",
                "slot",
                "offset_hex",
                "name",
                "numeric_id",
                "empty",
            ],
        )
        writer.writeheader()
        for record in rows:
            writer.writerow(
                {
                    "table_id": record.table_id,
                    "slot": record.slot,
                    "offset_hex": f"0x{record.offset:08x}",
                    "name": record.name,
                    "numeric_id": record.numeric_id,
                    "empty": record.empty,
                }
            )
    return len(rows)


def export_tables(
    tables: ProgramTables,
    out_dir: Path | str,
    prefix: str | None = None,
    include_empty: bool = False,
) -> dict[str, Path]:
    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "individual_ids": output_dir / output_name("individual_ids.csv", prefix),
        "talk_groups": output_dir / output_name("talk_groups.csv", prefix),
    }
    write_table_csv(outputs["individual_ids"], tables.individual_ids, include_empty)
    write_table_csv(outputs["talk_groups"], tables.talk_groups, include_empty)
    return outputs
