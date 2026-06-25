#!/usr/bin/env python3
"""Probe candidate fixed-width records after dominant-XOR normalization."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print candidate records from baseline and normalized modified .dat files."
    )
    parser.add_argument("baseline", type=Path)
    parser.add_argument("modified", type=Path)
    parser.add_argument(
        "--payload-start",
        type=lambda value: int(value, 0),
        default=0x40,
        help="Offset where payload starts (default: 0x40)",
    )
    parser.add_argument(
        "--record-base",
        action="append",
        type=lambda value: int(value, 0),
        required=True,
        help="Record base offset to print. May be repeated.",
    )
    parser.add_argument("--record-size", type=int, default=32)
    parser.add_argument(
        "--text-xor",
        type=lambda value: int(value, 0),
        default=0x5B,
        help="XOR byte used to decode record-name bytes +1..+14 (default: 0x5b)",
    )
    parser.add_argument(
        "--numeric-xor",
        type=lambda value: int(value, 0),
        help="Optional XOR byte used to decode numeric bytes +19..+20",
    )
    return parser.parse_args()


def hex_bytes(data: bytes) -> str:
    return " ".join(f"{byte:02x}" for byte in data)


def printable(data: bytes) -> str:
    return "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in data)


def dominant_xor(baseline: bytes, modified: bytes, start: int) -> int:
    shared = min(len(baseline), len(modified))
    counts = Counter(baseline[offset] ^ modified[offset] for offset in range(start, shared))
    return counts.most_common(1)[0][0]


def normalize_modified(baseline: bytes, modified: bytes, start: int) -> tuple[int, bytes]:
    xor_value = dominant_xor(baseline, modified, start)
    normalized = bytearray(modified)
    for offset in range(start, min(len(baseline), len(modified))):
        normalized[offset] ^= xor_value
    return xor_value, bytes(normalized)


def text_xor(record: bytes, key: int) -> str:
    field = record[1:15]
    decoded = bytes(byte ^ key for byte in field)
    decoded = decoded.split(b"\x00", 1)[0]
    return decoded.decode("ascii", errors="replace")


def print_record(label: str, base: int, record: bytes, text_key: int, numeric_key: int | None) -> None:
    print(f"- {label} `0x{base:08x}`")
    print(f"  - hex: `{hex_bytes(record)}`")
    print(f"  - raw printable: `{printable(record)}`")
    print(f"  - bytes `+1..+14` XOR `0x{text_key:02x}`: `{text_xor(record, text_key)}`")
    print(f"  - bytes `+19..+20`: `{hex_bytes(record[19:21])}`")
    if numeric_key is not None:
        decoded = bytes(byte ^ numeric_key for byte in record[19:21])
        little = int.from_bytes(decoded, "little")
        big = int.from_bytes(decoded, "big")
        print(
            f"  - bytes `+19..+20` XOR `0x{numeric_key:02x}`: "
            f"`{hex_bytes(decoded)}` LE={little} BE={big}"
        )


def main() -> int:
    args = parse_args()
    baseline = args.baseline.read_bytes()
    modified = args.modified.read_bytes()
    xor_value, normalized = normalize_modified(baseline, modified, args.payload_start)

    print(f"# Candidate Record Probe: {args.modified.name}")
    print()
    print(f"- Dominant payload XOR to normalize modified file: `0x{xor_value:02x}`")
    print(f"- Record size shown: {args.record_size} bytes")
    print()

    for base in args.record_base:
        before = baseline[base : base + args.record_size]
        after = normalized[base : base + args.record_size]
        print_record("baseline", base, before, args.text_xor, args.numeric_xor)
        print_record("normalized modified", base, after, args.text_xor, args.numeric_xor)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
