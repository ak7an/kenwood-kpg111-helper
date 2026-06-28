#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

PAYLOAD_START = 0x40
TG_START = 0x14F80
TG_RECORD_SIZE = 32
TG_COUNT = 400
TG_END = TG_START + TG_RECORD_SIZE * TG_COUNT


def normalize_to_reference(reference: bytes, candidate: bytes) -> bytes:
    if len(reference) != len(candidate):
        raise SystemExit(f"file sizes differ: {len(reference)} != {len(candidate)}")

    out = bytearray(candidate)
    mask = reference[PAYLOAD_START] ^ candidate[PAYLOAD_START]

    for i in range(PAYLOAD_START, len(out)):
        out[i] ^= mask

    return bytes(out)


def changed_ranges(a: bytes, b: bytes) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start: int | None = None

    for i, (x, y) in enumerate(zip(a, b)):
        if x != y and start is None:
            start = i
        elif x == y and start is not None:
            ranges.append((start, i))
            start = None

    if start is not None:
        ranges.append((start, len(a)))

    return ranges


def tg_slot_for_offset(offset: int) -> int | None:
    if TG_START <= offset < TG_END:
        return (offset - TG_START) // TG_RECORD_SIZE
    return None


def hex_preview(data: bytes, start: int, end: int, context: int) -> str:
    lo = max(0, start - context)
    hi = min(len(data), end + context)
    return data[lo:hi].hex(" ")


def main() -> None:
    ap = argparse.ArgumentParser(description="Normalize KPG111 DAT payload mask and diff")
    ap.add_argument("before", type=Path)
    ap.add_argument("after", type=Path)
    ap.add_argument("--context", type=int, default=16)
    ap.add_argument("--tg-only", action="store_true")
    args = ap.parse_args()

    before = args.before.read_bytes()
    raw_after = args.after.read_bytes()
    after = normalize_to_reference(before, raw_after)

    ranges = changed_ranges(before, after)

    if args.tg_only:
        ranges = [
            (s, e) for s, e in ranges
            if not (e <= TG_START or s >= TG_END)
        ]

    print(f"before: {args.before}")
    print(f"after:  {args.after}")
    print(f"payload mask applied to after: 0x{before[PAYLOAD_START] ^ raw_after[PAYLOAD_START]:02x}")
    print(f"changed ranges: {len(ranges)}")

    for s, e in ranges:
        slot_s = tg_slot_for_offset(s)
        slot_e = tg_slot_for_offset(e - 1)

        slot_text = ""
        if slot_s is not None:
            slot_text = f" tg_slot={slot_s}" if slot_s == slot_e else f" tg_slots={slot_s}-{slot_e}"

        print()
        print(f"0x{s:05x}..0x{e-1:05x} len={e-s}{slot_text}")
        print("before:")
        print(hex_preview(before, s, e, args.context))
        print("after:")
        print(hex_preview(after, s, e, args.context))

        print("byte changes:")
        for off in range(s, e):
            print(f"  0x{off:05x}: {before[off]:02x} -> {after[off]:02x}")


if __name__ == "__main__":
    main()
