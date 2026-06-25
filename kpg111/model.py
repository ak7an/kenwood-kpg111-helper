"""Application model objects for decoded KPG111 tables."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecodedRecord:
    table_id: str
    table_name: str
    slot: int
    offset: int
    name: str
    numeric_id: int
    raw_record_hex: str
    empty: bool


@dataclass(frozen=True)
class ProgramTables:
    individual_ids: list[DecodedRecord]
    talk_groups: list[DecodedRecord]
