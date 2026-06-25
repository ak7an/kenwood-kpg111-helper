"""Unknown decoded or raw record evidence."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UnknownRecord:
    source: str
    offset: int
    length: int
    description: str = "UNKNOWN"
    confidence: str = "UNKNOWN"
