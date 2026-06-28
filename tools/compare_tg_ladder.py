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
        raise SystemExit(f"size mismatch: {len(reference)} != {len(candidate)}")

    out = bytearray(candidate)
    mask = reference[PAYLOAD_START] ^ candidate[PAYLOAD_START]
    for i in range(PAYLOAD_START, len(out)):
        out[i] ^= mask
    return bytes(out)


def changed_offsets(a: bytes, b: bytes) -> set[int]:
    return {i for i, (x, y) in enumerate(zip(a, b)) if x != y}


def ranges(offsets: set[int]) -> list[tuple[int, int]]:
    if not offsets:
        return []
    ordered = sorted(offsets)
    out = []
    start = prev = ordered[0]
    for off in ordered[1:]:
        if off == prev + 1:
            prev = off
            continue
        out.append((start, prev + 1))
        start = prev = off
    out.append((start, prev + 1))
    return out


def region_name(start: int, end: int) -> str:
    if not (end <= TG_START or start >= TG_END):
        return "TG_TABLE"
    return "outside"


def main() -> None:
    ap = argparse.ArgumentParser(description="Compare KPG111 TG count ladder files against blank DAT")
    ap.add_argument("blank", type=Path)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--show-outside", action="store_true")
    ap.add_argument("--context", type=int, default=8)
    args = ap.parse_args()

    blank = args.blank.read_bytes()

    previous_offsets: set[int] | None = None

    for path in args.files:
        raw = path.read_bytes()
        data = normalize_to_reference(blank, raw)
        changed = changed_offsets(blank, data)

        outside = {o for o in changed if not (TG_START <= o < TG_END)}
        inside = changed - outside

        print()
        print("=" * 72)
        print(path)
        print(f"changed bytes total: {len(changed)}")
        print(f"changed bytes in TG table: {len(inside)}")
        print(f"changed bytes outside TG table: {len(outside)}")

        if previous_offsets is not None:
            added = changed - previous_offsets
            removed = previous_offsets - changed
            outside_added = {o for o in added if not (TG_START <= o < TG_END)}
            outside_removed = {o for o in removed if not (TG_START <= o < TG_END)}
            print(f"new changed bytes vs previous: {len(added)}")
            print(f"removed changed bytes vs previous: {len(removed)}")
            print(f"outside new changed bytes vs previous: {len(outside_added)}")
            print(f"outside removed changed bytes vs previous: {len(outside_removed)}")

        print()
        print("changed ranges summary:")
        for s, e in ranges(changed):
            print(f"  0x{s:05x}..0x{e-1:05x} len={e-s} {region_name(s,e)}")

        if args.show_outside and outside:
            print()
            print("outside ranges with previews:")
            for s, e in ranges(outside):
                lo = max(0, s - args.context)
                hi = min(len(data), e + args.context)
                print(f"  0x{s:05x}..0x{e-1:05x} len={e-s}")
                print(f"    blank: {blank[lo:hi].hex(' ')}")
                print(f"    file:  {data[lo:hi].hex(' ')}")

        previous_offsets = changed


if __name__ == "__main__":
    main()
