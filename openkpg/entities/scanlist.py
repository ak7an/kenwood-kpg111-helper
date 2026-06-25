"""Scan list domain data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScanList:
    name: str
    channel_slots: tuple[int, ...] = ()
    source_offset: int | None = None
    confidence: str = "UNKNOWN"
