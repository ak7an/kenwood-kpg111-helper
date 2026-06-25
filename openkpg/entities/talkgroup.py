"""Talkgroup domain data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TalkGroup:
    slot: int
    name: str
    numeric_id: int
    source_offset: int | None = None
    empty: bool = False
    confidence: str = "HIGH"
