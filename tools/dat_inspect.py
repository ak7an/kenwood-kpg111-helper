#!/usr/bin/env python3
"""Read-only binary inspection helper for KPG111 Program.dat files."""

from __future__ import annotations

import argparse
import hashlib
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


PRINTABLE_RE = re.compile(rb"[\x20-\x7e]{4,}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect a binary .dat file without modifying it."
    )
    parser.add_argument("dat_file", type=Path, help="Path to Program.dat")
    parser.add_argument(
        "--block-size",
        type=int,
        default=256,
        help="Block size for entropy and table-region heuristics (default: 256)",
    )
    parser.add_argument(
        "--strings-limit",
        type=int,
        default=80,
        help="Maximum printable strings to show (default: 80)",
    )
    parser.add_argument(
        "--repeat-widths",
        default="4,8,16,32",
        help="Comma-separated structure widths to test (default: 4,8,16,32)",
    )
    parser.add_argument(
        "--max-repeats",
        type=int,
        default=20,
        help="Maximum repeated structures to show per width (default: 20)",
    )
    return parser.parse_args()


def entropy(chunk: bytes) -> float:
    if not chunk:
        return 0.0
    counts = Counter(chunk)
    total = len(chunk)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def hex_ascii(data: bytes, start: int = 0, width: int = 16) -> list[str]:
    lines = []
    for offset in range(0, len(data), width):
        chunk = data[offset : offset + width]
        hex_part = " ".join(f"{byte:02x}" for byte in chunk)
        ascii_part = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in chunk)
        lines.append(f"{start + offset:08x}  {hex_part:<{width * 3}} {ascii_part}")
    return lines


def summarize_hex(data: bytes) -> None:
    print("\n== Hex Summary ==")
    if not data:
        print("empty file")
        return

    print("-- first 256 bytes --")
    for line in hex_ascii(data[:256]):
        print(line)

    if len(data) > 512:
        midpoint = max(0, (len(data) // 2) - 128)
        print(f"-- middle 256 bytes at 0x{midpoint:08x} --")
        for line in hex_ascii(data[midpoint : midpoint + 256], midpoint):
            print(line)

    if len(data) > 256:
        tail_start = max(0, len(data) - 256)
        print(f"-- last 256 bytes at 0x{tail_start:08x} --")
        for line in hex_ascii(data[tail_start:], tail_start):
            print(line)


def summarize_strings(data: bytes, limit: int) -> None:
    print("\n== Printable Strings ==")
    matches = list(PRINTABLE_RE.finditer(data))
    if not matches:
        print("none found")
        return

    for match in matches[:limit]:
        value = match.group().decode("ascii", errors="replace")
        print(f"0x{match.start():08x}  len={len(match.group()):>4}  {value!r}")
    if len(matches) > limit:
        print(f"... {len(matches) - limit} more strings not shown")


def byte_profile(data: bytes) -> None:
    print("\n== Byte Profile ==")
    if not data:
        print("empty file")
        return

    counts = Counter(data)
    zero_count = counts.get(0, 0)
    ff_count = counts.get(0xFF, 0)
    printable_count = sum(count for byte, count in counts.items() if 32 <= byte <= 126)
    print(f"unique byte values: {len(counts)}")
    print(f"0x00 bytes: {zero_count} ({zero_count / len(data):.2%})")
    print(f"0xff bytes: {ff_count} ({ff_count / len(data):.2%})")
    print(f"printable ASCII bytes: {printable_count} ({printable_count / len(data):.2%})")
    common = " ".join(f"{byte:02x}:{count}" for byte, count in counts.most_common(12))
    print(f"most common bytes: {common}")


def likely_table_regions(data: bytes, block_size: int) -> None:
    print("\n== Likely Table Regions ==")
    if block_size <= 0:
        print("block size must be positive")
        return
    if not data:
        print("empty file")
        return

    blocks = []
    for start in range(0, len(data), block_size):
        chunk = data[start : start + block_size]
        ent = entropy(chunk)
        zero_ratio = chunk.count(0) / len(chunk)
        ff_ratio = chunk.count(0xFF) / len(chunk)
        printable_ratio = sum(1 for byte in chunk if 32 <= byte <= 126) / len(chunk)
        blocks.append((start, len(chunk), ent, zero_ratio, ff_ratio, printable_ratio))

    candidates = []
    for start, size, ent, zero_ratio, ff_ratio, printable_ratio in blocks:
        padded = zero_ratio >= 0.20 or ff_ratio >= 0.20
        mixed = 1.0 <= ent <= 6.5
        has_text = printable_ratio >= 0.08
        if mixed and (padded or has_text):
            candidates.append((start, size, ent, zero_ratio, ff_ratio, printable_ratio))

    if not candidates:
        print("no obvious table-like regions found by generic heuristics")
        return

    for start, size, ent, zero_ratio, ff_ratio, printable_ratio in candidates[:40]:
        print(
            f"0x{start:08x}-0x{start + size - 1:08x} "
            f"entropy={ent:.2f} zero={zero_ratio:.1%} "
            f"ff={ff_ratio:.1%} printable={printable_ratio:.1%}"
        )
    if len(candidates) > 40:
        print(f"... {len(candidates) - 40} more candidate blocks not shown")


def repeated_structures(data: bytes, widths: list[int], max_repeats: int) -> None:
    print("\n== Repeated Structures ==")
    if not data:
        print("empty file")
        return

    for width in widths:
        if width <= 0:
            print(f"-- width {width}: skipped, must be positive")
            continue
        if width > len(data):
            print(f"-- width {width}: skipped, larger than file")
            continue

        locations: dict[bytes, list[int]] = defaultdict(list)
        for offset in range(0, len(data) - width + 1, width):
            chunk = data[offset : offset + width]
            if chunk == b"\x00" * width or chunk == b"\xff" * width:
                continue
            locations[chunk].append(offset)

        repeated = [
            (chunk, offsets)
            for chunk, offsets in locations.items()
            if len(offsets) >= 3
        ]
        repeated.sort(key=lambda item: (-len(item[1]), item[1][0]))

        print(f"-- width {width} bytes --")
        if not repeated:
            print("no non-trivial repeats found")
            continue
        for chunk, offsets in repeated[:max_repeats]:
            preview = " ".join(f"{byte:02x}" for byte in chunk[: min(width, 16)])
            more = " ..." if width > 16 else ""
            first_offsets = ", ".join(f"0x{offset:08x}" for offset in offsets[:8])
            if len(offsets) > 8:
                first_offsets += ", ..."
            print(f"count={len(offsets):>4} first={first_offsets} bytes={preview}{more}")


def parse_widths(value: str) -> list[int]:
    widths = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        widths.append(int(item, 10))
    return widths


def main() -> int:
    args = parse_args()
    data = args.dat_file.read_bytes()

    print("== File ==")
    print(f"path: {args.dat_file}")
    print(f"size: {len(data)} bytes")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    print(f"md5: {hashlib.md5(data).hexdigest()}")

    byte_profile(data)
    summarize_hex(data)
    summarize_strings(data, args.strings_limit)
    likely_table_regions(data, args.block_size)
    repeated_structures(data, parse_widths(args.repeat_widths), args.max_repeats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

