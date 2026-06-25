#!/usr/bin/env python3
"""Analyze dominant XOR rewrites between KPG111 Program.dat files."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect dominant XOR deltas and normalized logical changes."
    )
    parser.add_argument("baseline", type=Path, help="Baseline .dat file")
    parser.add_argument("modified", nargs="+", type=Path, help="Modified .dat file(s)")
    parser.add_argument(
        "--payload-start",
        type=lambda value: int(value, 0),
        default=0x40,
        help="Offset where encoded payload begins (default: 0x40)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Optional path to write machine-readable JSON results",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Rows per markdown section (default: 20)",
    )
    return parser.parse_args()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def group_offsets(offsets: list[int]) -> list[dict[str, int]]:
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


def hex_bytes(data: bytes) -> str:
    return " ".join(f"{byte:02x}" for byte in data)


def ascii_preview(data: bytes) -> str:
    return "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in data)


def common_prefix_len(left: bytes, right: bytes) -> int:
    size = min(len(left), len(right))
    for offset in range(size):
        if left[offset] != right[offset]:
            return offset
    return size


def common_suffix_len(left: bytes, right: bytes, prefix_len: int) -> int:
    size = min(len(left), len(right))
    count = 0
    while count < size - prefix_len:
        if left[len(left) - count - 1] != right[len(right) - count - 1]:
            break
        count += 1
    return count


def byte_profile(data: bytes) -> dict[str, Any]:
    counts = Counter(data)
    printable = sum(count for byte, count in counts.items() if 32 <= byte <= 126)
    return {
        "unique": len(counts),
        "zero": counts.get(0, 0),
        "ff": counts.get(0xFF, 0),
        "printable": printable,
        "most_common": [
            {"byte": byte, "count": count} for byte, count in counts.most_common(12)
        ],
    }


def analyze_pair(baseline_path: Path, baseline: bytes, modified_path: Path, payload_start: int) -> dict[str, Any]:
    modified = modified_path.read_bytes()
    shared = min(len(baseline), len(modified))
    payload_end = shared
    xor_values = [
        baseline[offset] ^ modified[offset]
        for offset in range(payload_start, payload_end)
    ]
    xor_counts = Counter(xor_values)
    dominant_xor, dominant_count = xor_counts.most_common(1)[0]

    normalized = bytearray(modified)
    for offset in range(payload_start, shared):
        normalized[offset] ^= dominant_xor

    normalized_offsets = [
        offset
        for offset in range(shared)
        if baseline[offset] != normalized[offset]
    ]
    if len(baseline) != len(modified):
        normalized_offsets.extend(range(shared, max(len(baseline), len(modified))))

    exception_offsets = [
        offset
        for offset in range(payload_start, payload_end)
        if (baseline[offset] ^ modified[offset]) != dominant_xor
    ]
    exception_xors = Counter(
        baseline[offset] ^ modified[offset] for offset in exception_offsets
    )

    return {
        "modified": {
            "path": str(modified_path),
            "size": len(modified),
            "sha256": sha256(modified),
        },
        "common_prefix_length": common_prefix_len(baseline, modified),
        "common_suffix_length": common_suffix_len(baseline, modified, 0),
        "payload_start": payload_start,
        "payload_length_compared": max(0, payload_end - payload_start),
        "dominant_xor": dominant_xor,
        "dominant_xor_count": dominant_count,
        "dominant_xor_ratio": dominant_count / len(xor_values) if xor_values else 0.0,
        "xor_counts_top": [
            {"xor": value, "count": count}
            for value, count in xor_counts.most_common(20)
        ],
        "xor_exception_count": len(exception_offsets),
        "xor_exception_regions": group_offsets(exception_offsets),
        "xor_exception_counts_top": [
            {"xor": value, "count": count}
            for value, count in exception_xors.most_common(20)
        ],
        "normalized_changed_count": len(normalized_offsets),
        "normalized_changed_regions": group_offsets(normalized_offsets),
        "normalized_changed_samples": samples(baseline, bytes(normalized), normalized_offsets),
        "modified_profile": byte_profile(modified[payload_start:]),
        "normalized_profile": byte_profile(bytes(normalized[payload_start:])),
    }


def samples(before: bytes, after: bytes, offsets: list[int], context: int = 8, limit: int = 20) -> list[dict[str, Any]]:
    rows = []
    for region in group_offsets(offsets)[:limit]:
        left = max(0, region["start"] - context)
        right = min(min(len(before), len(after)), region["end"] + context + 1)
        before_slice = before[left:right]
        after_slice = after[left:right]
        rows.append(
            {
                "start": region["start"],
                "end": region["end"],
                "length": region["length"],
                "context_start": left,
                "before_hex": hex_bytes(before_slice),
                "after_hex": hex_bytes(after_slice),
                "before_ascii": ascii_preview(before_slice),
                "after_ascii": ascii_preview(after_slice),
            }
        )
    return rows


def markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(row) + " |")


def render(result: dict[str, Any], top: int) -> None:
    print("# KPG111 Dominant XOR Rewrite Analysis")
    print()
    print("This report derives byte-level evidence only. Normalized changes are not decoded field meanings.")
    print()
    base = result["baseline"]
    print("## Baseline")
    print()
    print(f"- Path: `{base['path']}`")
    print(f"- Size: {base['size']} bytes")
    print(f"- SHA-256: `{base['sha256']}`")
    print()

    print("## Pair Summary")
    rows = []
    for pair in result["pairs"]:
        rows.append(
            [
                pair["modified"]["path"],
                f"0x{pair['common_prefix_length']:x}",
                f"0x{pair['dominant_xor']:02x}",
                str(pair["dominant_xor_count"]),
                f"{pair['dominant_xor_ratio']:.4%}",
                str(pair["xor_exception_count"]),
                str(pair["normalized_changed_count"]),
                str(len(pair["normalized_changed_regions"])),
            ]
        )
    markdown_table(
        [
            "Modified",
            "Common Prefix",
            "Dominant XOR",
            "Dominant Count",
            "Dominant Ratio",
            "XOR Exceptions",
            "Normalized Changed Bytes",
            "Normalized Regions",
        ],
        rows,
    )
    print()

    for pair in result["pairs"]:
        print(f"## {Path(pair['modified']['path']).name}")
        print()
        print("### Top XOR Deltas")
        rows = [
            [f"0x{item['xor']:02x}", str(item["count"])]
            for item in pair["xor_counts_top"][:top]
        ]
        markdown_table(["XOR", "Count"], rows)
        print()
        print("### Normalized Changed Regions")
        rows = [
            [
                f"0x{item['start']:08x}-0x{item['end']:08x}",
                str(item["length"]),
            ]
            for item in pair["normalized_changed_regions"][:top]
        ]
        markdown_table(["Range", "Length"], rows)
        print()
        print("### Normalized Change Samples")
        for sample in pair["normalized_changed_samples"][: min(top, 10)]:
            print(f"- `0x{sample['start']:08x}-0x{sample['end']:08x}` len={sample['length']}")
            print(f"  - before @`0x{sample['context_start']:08x}`: `{sample['before_hex']}`")
            print(f"  - after  @`0x{sample['context_start']:08x}`: `{sample['after_hex']}`")
            print(f"  - before ASCII: `{sample['before_ascii']}`")
            print(f"  - after ASCII: `{sample['after_ascii']}`")
        print()


def main() -> int:
    args = parse_args()
    baseline = args.baseline.read_bytes()
    result = {
        "schema": "kpg111-helper.xor-analysis.v1",
        "baseline": {
            "path": str(args.baseline),
            "size": len(baseline),
            "sha256": sha256(baseline),
        },
        "baseline_payload_profile": byte_profile(baseline[args.payload_start:]),
        "pairs": [
            analyze_pair(args.baseline, baseline, modified, args.payload_start)
            for modified in args.modified
        ],
    }
    if args.json:
        args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    render(result, args.top)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
