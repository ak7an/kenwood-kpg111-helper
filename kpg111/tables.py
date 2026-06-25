"""Shared table helpers for decoded KPG111 records."""

from __future__ import annotations

from .model import DecodedRecord


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
