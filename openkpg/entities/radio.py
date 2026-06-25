"""Radio-level domain data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Radio:
    model: str = "UNKNOWN"
    software_version: str | None = None
    source_file: str | None = None
    raw_size: int | None = None
