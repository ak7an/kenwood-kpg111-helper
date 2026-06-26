"""KPG111 channel frequency field helpers.

Channel frequency fields observed so far store only the low 24 bits of the
frequency integer. Full MHz reconstruction requires band/context because those
three bytes do not carry the high bits.
"""

from __future__ import annotations


FREQUENCY_FIELD_SIZE = 3
FREQUENCY_XOR_MASK = 0x41
FREQUENCY_LOW24_MASK = 0xFFFFFF


def encode_frequency_hz(hz: int) -> bytes:
    """Encode the low 24 bits of a non-negative frequency integer."""
    if not isinstance(hz, int):
        raise TypeError("hz must be an int")
    if hz < 0:
        raise ValueError("hz must be >= 0")
    low24 = hz & FREQUENCY_LOW24_MASK
    return bytes(byte ^ FREQUENCY_XOR_MASK for byte in low24.to_bytes(FREQUENCY_FIELD_SIZE, "little"))


def decode_frequency_low24(raw: bytes) -> int:
    """Decode a channel field to its stored low-24-bit integer value.

    This returns only the low 24 bits. Full MHz reconstruction requires
    band/context because the three-byte field does not store the high bits.
    """
    if len(raw) != FREQUENCY_FIELD_SIZE:
        raise ValueError("frequency field must be exactly 3 bytes")
    decoded = bytes(byte ^ FREQUENCY_XOR_MASK for byte in raw)
    return int.from_bytes(decoded, "little")


def format_frequency_mhz(hz: int) -> str:
    """Format an integer Hz value as MHz with up to six decimal places."""
    if not isinstance(hz, int):
        raise TypeError("hz must be an int")
    if hz < 0:
        raise ValueError("hz must be >= 0")
    whole = hz // 1_000_000
    fractional = hz % 1_000_000
    if fractional == 0:
        return f"{whole}.000"
    return f"{whole}.{fractional:06d}".rstrip("0")
