#!/usr/bin/env python3
"""Create a read-only JSON comparison session for two Program.dat files."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ASCII_RE = re.compile(rb"[\x20-\x7e]{4,}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two .dat files and write read-only session.json evidence."
    )
    parser.add_argument("baseline", type=Path, help="Baseline Program.dat")
    parser.add_argument("modified", type=Path, help="Modified Program.dat")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("session.json"),
        help="Output JSON path (default: session.json)",
    )
    parser.add_argument(
        "--block-size",
        type=int,
        default=256,
        help="Block size for entropy comparison (default: 256)",
    )
    return parser.parse_args()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def changed_offsets(before: bytes, after: bytes) -> list[int]:
    shared = min(len(before), len(after))
    offsets = [offset for offset in range(shared) if before[offset] != after[offset]]
    offsets.extend(range(shared, max(len(before), len(after))))
    return offsets


def group_regions(offsets: list[int]) -> list[dict[str, int]]:
    if not offsets:
        return []
    regions = []
    start = previous = offsets[0]
    for offset in offsets[1:]:
        if offset == previous + 1:
            previous = offset
            continue
        regions.append({"start": start, "end": previous, "length": previous - start + 1})
        start = previous = offset
    regions.append({"start": start, "end": previous, "length": previous - start + 1})
    return regions


def changed_bytes(before: bytes, after: bytes, offsets: list[int]) -> list[dict[str, Any]]:
    rows = []
    for offset in offsets:
        before_value = before[offset] if offset < len(before) else None
        after_value = after[offset] if offset < len(after) else None
        rows.append(
            {
                "offset": offset,
                "before": None if before_value is None else f"{before_value:02x}",
                "after": None if after_value is None else f"{after_value:02x}",
            }
        )
    return rows


def ascii_strings(data: bytes) -> set[str]:
    return {match.group().decode("ascii", errors="replace") for match in ASCII_RE.finditer(data)}


def utf16le_strings(data: bytes) -> set[str]:
    strings = set()
    for offset in range(0, max(0, len(data) - 7), 2):
        chars = []
        cursor = offset
        while cursor + 1 < len(data):
            code_unit = data[cursor] | (data[cursor + 1] << 8)
            if 32 <= code_unit <= 126:
                chars.append(chr(code_unit))
                cursor += 2
                continue
            break
        if len(chars) >= 4:
            strings.add("".join(chars))
    return strings


def string_delta(before: bytes, after: bytes) -> dict[str, list[str]]:
    before_strings = ascii_strings(before) | utf16le_strings(before)
    after_strings = ascii_strings(after) | utf16le_strings(after)
    return {
        "added": sorted(after_strings - before_strings),
        "removed": sorted(before_strings - after_strings),
    }


def entropy_blocks(before: bytes, after: bytes, block_size: int) -> list[dict[str, Any]]:
    blocks = []
    if block_size <= 0:
        return blocks
    max_size = max(len(before), len(after))
    for start in range(0, max_size, block_size):
        before_chunk = before[start : start + block_size]
        after_chunk = after[start : start + block_size]
        before_entropy = entropy(before_chunk)
        after_entropy = entropy(after_chunk)
        if before_chunk != after_chunk:
            blocks.append(
                {
                    "start": start,
                    "end": start + max(len(before_chunk), len(after_chunk)) - 1,
                    "before_entropy": round(before_entropy, 6),
                    "after_entropy": round(after_entropy, 6),
                    "delta": round(after_entropy - before_entropy, 6),
                }
            )
    return blocks


def file_record(path: Path, data: bytes) -> dict[str, Any]:
    return {
        "path": str(path),
        "size": len(data),
        "sha256": sha256(data),
        "md5": hashlib.md5(data).hexdigest(),
    }


def main() -> int:
    args = parse_args()
    before = args.baseline.read_bytes()
    after = args.modified.read_bytes()
    offsets = changed_offsets(before, after)
    strings = string_delta(before, after)

    session = {
        "schema": "kpg111-helper.compare-session.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "baseline": file_record(args.baseline, before),
        "modified": file_record(args.modified, after),
        "size_change": len(after) - len(before),
        "changed_offsets": offsets,
        "changed_regions": group_regions(offsets),
        "changed_bytes": changed_bytes(before, after, offsets),
        "entropy_comparison": {
            "block_size": args.block_size,
            "whole_file": {
                "baseline": round(entropy(before), 6),
                "modified": round(entropy(after), 6),
                "delta": round(entropy(after) - entropy(before), 6),
            },
            "changed_blocks": entropy_blocks(before, after, args.block_size),
        },
        "strings_added": strings["added"],
        "strings_removed": strings["removed"],
        "notes": "Read-only comparison data. No field meanings are inferred.",
    }

    args.output.write_text(json.dumps(session, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    print(f"changed bytes: {len(offsets)}")
    print(f"changed regions: {len(session['changed_regions'])}")
    print(f"size change: {session['size_change']:+d} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

