"""Experimental KPG111 channel frequency field helpers.

Channel frequency fields observed so far store only the low 24 bits of the
frequency integer. Full MHz reconstruction requires band/context because those
three bytes do not carry the high bits. These helpers are research utilities and
are intentionally unused by the default GUI frequency display.
"""

from __future__ import annotations


FREQUENCY_FIELD_SIZE = 3
FREQUENCY_XOR_MASK = 0x41
FREQUENCY_LOW24_MASK = 0xFFFFFF
FREQUENCY_LOW24_MODULUS = FREQUENCY_LOW24_MASK + 1

VHF_BAND = (136_000_000, 174_000_000)
UHF_BAND = (400_000_000, 520_000_000)
DEFAULT_FREQUENCY_CANDIDATES = (VHF_BAND, UHF_BAND)


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


def reconstruct_frequency(
    low24: int,
    candidates: tuple[tuple[int, int], ...] | list[tuple[int, int]],
) -> int | None:
    """Reconstruct a full frequency from a low-24 value and candidate ranges.

    Candidate ranges are inclusive ``(start_hz, end_hz)`` pairs. The function
    returns the unique frequency in those ranges whose low 24 bits match
    ``low24``. It returns ``None`` when there are no matches or when multiple
    frequencies match. Broad bands can be ambiguous because only low 24 bits are
    stored in the channel field.
    """
    if not isinstance(low24, int):
        raise TypeError("low24 must be an int")
    if low24 < 0 or low24 > FREQUENCY_LOW24_MASK:
        raise ValueError("low24 must be between 0x000000 and 0xffffff")

    matches: list[int] = []
    for start_hz, end_hz in candidates:
        if start_hz < 0 or end_hz < start_hz:
            raise ValueError("candidate ranges must be non-negative start/end pairs")
        first = low24
        if first < start_hz:
            steps = (start_hz - first + FREQUENCY_LOW24_MODULUS - 1) // FREQUENCY_LOW24_MODULUS
            first += steps * FREQUENCY_LOW24_MODULUS
        while first <= end_hz:
            matches.append(first)
            if len(set(matches)) > 1:
                return None
            first += FREQUENCY_LOW24_MODULUS

    unique = set(matches)
    if len(unique) != 1:
        return None
    return unique.pop()


def format_frequency_mhz(hz: int) -> str:
    """Format an integer Hz value as MHz with at least three decimal places."""
    if not isinstance(hz, int):
        raise TypeError("hz must be an int")
    if hz < 0:
        raise ValueError("hz must be >= 0")
    whole = hz // 1_000_000
    fractional = hz % 1_000_000
    if fractional == 0:
        return f"{whole}.000"
    text = f"{fractional:06d}".rstrip("0")
    if len(text) < 3:
        text = text.ljust(3, "0")
    return f"{whole}.{text}"
