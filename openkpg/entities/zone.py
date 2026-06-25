"""Zone domain data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Zone:
    name: str
    channel_slots: tuple[int, ...] = ()
    source_offset: int | None = None
    confidence: str = "UNKNOWN"
