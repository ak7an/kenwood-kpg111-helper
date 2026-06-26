#!/usr/bin/env python3
"""Compare verified frequency samples with basic BCD storage hypotheses.

This read-only helper uses hard-coded samples and does not read or write DAT
files. A reported match is an observation about one tested representation, not
evidence of a complete frequency-encoding formula.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


SAMPLES = (
    ("146.12000", bytes.fromhex("01 dc f4")),
    ("146.51000", bytes.fromhex("f1 d1 fa")),
    ("146.52000", bytes.fromhex("81 f6 fa")),
    ("146.53000", bytes.fromhex("91 9f fa")),
    ("146.72000", bytes.fromhex("41 84 ff")),
    ("147.00000", bytes.fromhex("81 4b 82")),
)


@dataclass(frozen=True)
class Candidate:
    name: str
    value: bytes


def frequency_to_hz(frequency_mhz: str) -> int:
    """Convert the decimal-MHz sample notation to an integral Hz value."""
    return int(Decimal(frequency_mhz) * 1_000_000)


def bcd_byte(value: int) -> int:
    if not 0 <= value <= 99:
        raise ValueError(f"BCD byte value is out of range: {value}")
    return ((value // 10) << 4) | (value % 10)


def lbcd4(value: int) -> bytes:
    """Return four bytes of little-endian packed BCD."""
    return bytes(bcd_byte((value // (100 ** index)) % 100) for index in range(4))


def bbcd4(value: int) -> bytes:
    """Return four bytes of big-endian packed BCD."""
    return lbcd4(value)[::-1]


def reverse_bits(byte: int) -> int:
    return int(f"{byte:08b}"[::-1], 2)


def bit_reversed(value: bytes) -> bytes:
    return bytes(reverse_bits(byte) for byte in value)


def variants(name: str, value: bytes) -> tuple[Candidate, ...]:
    return (
        Candidate(name, value),
        Candidate(f"{name}, XOR ff", bytes(byte ^ 0xFF for byte in value)),
        Candidate(f"{name}, bit-reversed", bit_reversed(value)),
    )


def candidates(lbcd: bytes, bbcd: bytes) -> tuple[Candidate, ...]:
    bases = (
        ("first 3 bytes of lbcd", lbcd[:3]),
        ("last 3 bytes of lbcd", lbcd[-3:]),
        ("first 3 bytes of bbcd", bbcd[:3]),
        ("last 3 bytes of bbcd", bbcd[-3:]),
    )
    return tuple(candidate for name, value in bases for candidate in variants(name, value))


def matching_byte_count(left: bytes, right: bytes) -> int:
    return sum(left_byte == right_byte for left_byte, right_byte in zip(left, right))


def report_sample(frequency_mhz: str, observed: bytes) -> bool:
    frequency_hz = frequency_to_hz(frequency_mhz)
    divided_by_ten = frequency_hz // 10
    lbcd = lbcd4(divided_by_ten)
    bbcd = bbcd4(divided_by_ten)
    results = [
        (candidate, matching_byte_count(observed, candidate.value))
        for candidate in candidates(lbcd, bbcd)
    ]
    matches = [(candidate, count) for candidate, count in results if count == 3]
    near_matches = [(candidate, count) for candidate, count in results if count == 2]

    print(f"## {frequency_mhz} MHz")
    print(f"- Decimal Hz: `{frequency_hz}`")
    print(f"- Frequency / 10: `{divided_by_ten}`")
    print(f"- 4-byte little-endian BCD: `{lbcd.hex(' ')}`")
    print(f"- 4-byte big-endian BCD: `{bbcd.hex(' ')}`")
    print(f"- Observed 3 bytes: `{observed.hex(' ')}`")

    if matches:
        print("- Matches:")
        for candidate, _ in matches:
            print(f"  - `{candidate.name}`: `{candidate.value.hex(' ')}`")
    if near_matches:
        print("- Near-matches (2 of 3 bytes at the same positions):")
        for candidate, count in near_matches:
            print(f"  - `{candidate.name}`: `{candidate.value.hex(' ')}` ({count}/3)")
    if not matches and not near_matches:
        print("- No matches or near-matches among the tested BCD representations.")
    print()
    return bool(matches)


def main() -> int:
    print("# Frequency Encoding Hypotheses")
    print()
    print("Read-only exploratory comparison of hard-coded verified samples.")
    print("A formula is not inferred unless every sample has an exact match.")
    print()

    all_exact = True
    for frequency_mhz, observed in SAMPLES:
        all_exact = report_sample(frequency_mhz, observed) and all_exact

    if all_exact:
        print("All samples have at least one exact tested representation match.")
    else:
        print("No frequency-encoding formula is claimed: not all samples have an exact tested representation match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
