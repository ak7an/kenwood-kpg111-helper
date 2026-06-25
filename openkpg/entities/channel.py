"""Channel domain data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Channel:
    slot: int
    name: str
    rx_frequency: str | None = None
    tx_frequency: str | None = None
    bandwidth: str | None = None
    power: str | None = None
    mode: str | None = None
    tone: str | None = None
    ran: int | None = None
    zone_names: tuple[str, ...] = ()
    source_offset: int | None = None
    confidence: str = "UNKNOWN"
