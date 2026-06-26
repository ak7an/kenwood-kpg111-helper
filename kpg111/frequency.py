"""Compatibility imports for KPG111 channel frequency field helpers."""

from __future__ import annotations

from openkpg.dat.frequency import (
    FREQUENCY_FIELD_SIZE,
    FREQUENCY_LOW24_MASK,
    FREQUENCY_XOR_MASK,
    decode_frequency_low24,
    encode_frequency_hz,
    format_frequency_mhz,
)


def decode_frequency_bytes(raw: bytes) -> int:
    """Compatibility alias for decode_frequency_low24."""
    return decode_frequency_low24(raw)


__all__ = [
    "FREQUENCY_FIELD_SIZE",
    "FREQUENCY_LOW24_MASK",
    "FREQUENCY_XOR_MASK",
    "decode_frequency_bytes",
    "decode_frequency_low24",
    "encode_frequency_hz",
    "format_frequency_mhz",
]
