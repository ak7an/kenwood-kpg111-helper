#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

PAYLOAD_START = 0x40

INTERESTING_VALUES = {
    0x14940: "blank/ladder TG start",
    0x14F80: "travel old TG start",
    0x14600: "travel first 397-window candidate",
    0x018D: "397 decimal",
    0x0190: "400 decimal",
    0x0154: "340 decimal",
    0x3200: "400 * 32 bytes",
    0x2A80: "340 * 32 bytes",
}


def normalize_to_reference(reference: bytes, candidate: bytes) -> bytes:
    if len(reference) != len(candidate):
        raise SystemExit(f"size mismatch: {len(reference)} != {len(candidate)}")

    out = bytearray(candidate)
    mask = reference[PAYLOAD_START] ^ candidate[PAYLOAD_START]
    for i in range(PAYLOAD_START, len(out)):
        out[i] ^= mask
    return bytes(out)


def find_u16(data: bytes, value: int, limit: int) -> list[int]:
    needle = value.to_bytes(2, "little")
    out = []
    start = 0
    while True:
        pos = data[:limit].find(needle, start)
        if pos < 0:
            break
        out.append(pos)
        start = pos + 1
    return out


def find_u24(data: bytes, value: int, limit: int) -> list[int]:
    needle = value.to_bytes(3, "little")
    out = []
    start = 0
    while True:
        pos = data[:limit].find(needle, start)
        if pos < 0:
            break
        out.append(pos)
        start = pos + 1
    return out


def find_u32(data: bytes, value: int, limit: int) -> list[int]:
    needle = value.to_bytes(4, "little")
    out = []
    start = 0
    while True:
        pos = data[:limit].find(needle, start)
        if pos < 0:
            break
        out.append(pos)
        start = pos + 1
    return out


def preview(data: bytes, pos: int, context: int) -> str:
    lo = max(0, pos - context)
    hi = min(len(data), pos + context + 4)
    return data[lo:hi].hex(" ")


def print_hits(label: str, data: bytes, limit: int, context: int) -> None:
    print()
    print("=" * 72)
    print(label)
    print(f"search limit: 0x{limit:05x}")

    for value, meaning in INTERESTING_VALUES.items():
        print()
        print(f"value 0x{value:04x} ({value}) - {meaning}")

        hits = []
        if value <= 0xFFFF:
            hits.extend(("u16", p) for p in find_u16(data, value, limit))
        if value <= 0xFFFFFF:
            hits.extend(("u24", p) for p in find_u24(data, value, limit))
        hits.extend(("u32", p) for p in find_u32(data, value, limit))

        if not hits:
            print("  no hits")
            continue

        for kind, pos in hits[:40]:
            print(f"  {kind} @ 0x{pos:05x}: {preview(data, pos, context)}")
        if len(hits) > 40:
            print(f"  ... {len(hits) - 40} more")


def main() -> None:
    ap = argparse.ArgumentParser(description="Search DAT metadata for table offset/capacity hints")
    ap.add_argument("reference", type=Path)
    ap.add_argument("candidate", type=Path)
    ap.add_argument("--limit", type=lambda x: int(x, 0), default=0x14940)
    ap.add_argument("--context", type=int, default=12)
    args = ap.parse_args()

    ref = args.reference.read_bytes()
    cand = normalize_to_reference(ref, args.candidate.read_bytes())

    print_hits(f"reference: {args.reference}", ref, args.limit, args.context)
    print_hits(f"candidate normalized to reference: {args.candidate}", cand, args.limit, args.context)


if __name__ == "__main__":
    main()
