#!/usr/bin/env python3
"""Byte-by-byte diff helper for KPG111 Program.dat research."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two binary .dat files without modifying either file."
    )
    parser.add_argument("before", type=Path, help="Original Program.dat")
    parser.add_argument("after", type=Path, help="Changed Program.dat")
    parser.add_argument(
        "--context",
        type=int,
        default=8,
        help="Bytes of context around changed regions (default: 8)",
    )
    parser.add_argument(
        "--max-regions",
        type=int,
        default=80,
        help="Maximum changed regions to print (default: 80)",
    )
    parser.add_argument(
        "--max-offsets",
        type=int,
        default=120,
        help="Maximum individual changed offsets to print (default: 120)",
    )
    return parser.parse_args()


def hex_bytes(data: bytes) -> str:
    return " ".join(f"{byte:02x}" for byte in data)


def ascii_preview(data: bytes) -> str:
    return "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in data)


def changed_offsets(before: bytes, after: bytes) -> list[int]:
    shared = min(len(before), len(after))
    offsets = [offset for offset in range(shared) if before[offset] != after[offset]]
    if len(before) != len(after):
        offsets.extend(range(shared, max(len(before), len(after))))
    return offsets


def group_regions(offsets: list[int]) -> list[tuple[int, int]]:
    if not offsets:
        return []
    regions = []
    start = previous = offsets[0]
    for offset in offsets[1:]:
        if offset == previous + 1:
            previous = offset
            continue
        regions.append((start, previous))
        start = previous = offset
    regions.append((start, previous))
    return regions


def slice_with_context(data: bytes, start: int, end: int, context: int) -> tuple[int, bytes]:
    left = max(0, start - context)
    right = min(len(data), end + context + 1)
    return left, data[left:right]


def print_region(before: bytes, after: bytes, start: int, end: int, context: int) -> None:
    before_start, before_slice = slice_with_context(before, start, end, context)
    after_start, after_slice = slice_with_context(after, start, end, context)
    length = end - start + 1
    print(f"0x{start:08x}-0x{end:08x} len={length}")
    print(f"  before @0x{before_start:08x}: {hex_bytes(before_slice)}")
    print(f"           ascii: {ascii_preview(before_slice)!r}")
    print(f"  after  @0x{after_start:08x}: {hex_bytes(after_slice)}")
    print(f"           ascii: {ascii_preview(after_slice)!r}")


def main() -> int:
    args = parse_args()
    before = args.before.read_bytes()
    after = args.after.read_bytes()

    offsets = changed_offsets(before, after)
    regions = group_regions(offsets)

    print("== Files ==")
    print(f"before: {args.before}")
    print(f"  size: {len(before)} bytes")
    print(f"  sha256: {hashlib.sha256(before).hexdigest()}")
    print(f"after: {args.after}")
    print(f"  size: {len(after)} bytes")
    print(f"  sha256: {hashlib.sha256(after).hexdigest()}")

    print("\n== Summary ==")
    print(f"changed bytes: {len(offsets)}")
    print(f"changed regions: {len(regions)}")
    if len(before) != len(after):
        delta = len(after) - len(before)
        print(f"size delta: {delta:+d} bytes")

    print("\n== Changed Offsets ==")
    if not offsets:
        print("files are identical")
    else:
        for offset in offsets[: args.max_offsets]:
            before_value = before[offset] if offset < len(before) else None
            after_value = after[offset] if offset < len(after) else None
            before_text = "--" if before_value is None else f"{before_value:02x}"
            after_text = "--" if after_value is None else f"{after_value:02x}"
            print(f"0x{offset:08x}: {before_text} -> {after_text}")
        if len(offsets) > args.max_offsets:
            print(f"... {len(offsets) - args.max_offsets} more offsets not shown")

    print("\n== Changed Regions ==")
    if not regions:
        print("files are identical")
    else:
        for start, end in regions[: args.max_regions]:
            print_region(before, after, start, end, args.context)
        if len(regions) > args.max_regions:
            print(f"... {len(regions) - args.max_regions} more regions not shown")

    return 0 if not offsets else 1


if __name__ == "__main__":
    raise SystemExit(main())

