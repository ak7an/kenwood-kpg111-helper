#!/usr/bin/env python3
"""Report statistical evidence for possible fixed-width tables in a .dat file."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


RECORD_SIZES = (8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128)
PADDING_WIDTHS = (2, 4, 8, 16)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze possible fixed-length table regions without decoding fields."
    )
    parser.add_argument("dat_file", type=Path, help="Path to Program.dat")
    parser.add_argument(
        "--block-size",
        type=int,
        default=256,
        help="Block size for density and entropy analysis (default: 256)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Optional path to write machine-readable JSON results",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=30,
        help="Maximum rows per markdown section (default: 30)",
    )
    return parser.parse_args()


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def printable_density(data: bytes) -> float:
    if not data:
        return 0.0
    printable = sum(1 for byte in data if 32 <= byte <= 126)
    return printable / len(data)


def zero_ratio(data: bytes) -> float:
    return 0.0 if not data else data.count(0) / len(data)


def ff_ratio(data: bytes) -> float:
    return 0.0 if not data else data.count(0xFF) / len(data)


def is_unused_slot(record: bytes) -> bool:
    return bool(record) and (record == b"\x00" * len(record) or record == b"\xff" * len(record))


def repeated_pattern_count(record: bytes) -> int:
    count = 0
    for width in PADDING_WIDTHS:
        if len(record) < width * 2 or len(record) % width != 0:
            continue
        pattern = record[:width]
        if pattern not in (b"\x00" * width, b"\xff" * width) and pattern * (len(record) // width) == record:
            count += 1
    return count


def analyze_blocks(data: bytes, block_size: int) -> list[dict[str, Any]]:
    blocks = []
    if block_size <= 0:
        return blocks
    for start in range(0, len(data), block_size):
        chunk = data[start : start + block_size]
        blocks.append(
            {
                "start": start,
                "end": start + len(chunk) - 1,
                "length": len(chunk),
                "entropy": round(entropy(chunk), 6),
                "printable_density": round(printable_density(chunk), 6),
                "zero_ratio": round(zero_ratio(chunk), 6),
                "ff_ratio": round(ff_ratio(chunk), 6),
            }
        )
    return blocks


def record_stats_for_region(data: bytes, start: int, record_size: int, count: int) -> dict[str, Any]:
    records = [
        data[start + index * record_size : start + (index + 1) * record_size]
        for index in range(count)
    ]
    counter = Counter(records)
    unused_zero = sum(1 for record in records if record == b"\x00" * record_size)
    unused_ff = sum(1 for record in records if record == b"\xff" * record_size)
    repeated_records = sum(1 for _record, occurrences in counter.items() if occurrences > 1)
    repeated_padding = sum(repeated_pattern_count(record) for record in records)
    non_unused = [record for record in records if not is_unused_slot(record)]
    avg_entropy = sum(entropy(record) for record in non_unused) / len(non_unused) if non_unused else 0.0
    avg_printable = (
        sum(printable_density(record) for record in non_unused) / len(non_unused)
        if non_unused
        else 0.0
    )
    return {
        "start": start,
        "end": start + record_size * count - 1,
        "record_size": record_size,
        "record_count": count,
        "zero_slots": unused_zero,
        "ff_slots": unused_ff,
        "repeated_record_values": repeated_records,
        "repeated_padding_patterns": repeated_padding,
        "avg_record_entropy": round(avg_entropy, 6),
        "avg_record_printable_density": round(avg_printable, 6),
    }


def table_score(stats: dict[str, Any]) -> float:
    count = stats["record_count"]
    score = 0.0
    score += min(count, 32) / 32
    score += min(stats["zero_slots"] + stats["ff_slots"], 16) / 16
    score += min(stats["repeated_record_values"], 16) / 16
    score += min(stats["repeated_padding_patterns"], 16) / 16
    density = stats["avg_record_printable_density"]
    if 0.05 <= density <= 0.70:
        score += 0.75
    entropy_value = stats["avg_record_entropy"]
    if 0.5 <= entropy_value <= 6.5:
        score += 0.75
    return round(score, 6)


def candidate_regions(data: bytes) -> list[dict[str, Any]]:
    candidates = []
    for record_size in RECORD_SIZES:
        min_records = 4
        for start in range(0, len(data) - record_size * min_records + 1, record_size):
            max_count = min(64, (len(data) - start) // record_size)
            if max_count < min_records:
                continue
            stats = record_stats_for_region(data, start, record_size, max_count)
            stats["score"] = table_score(stats)
            if stats["score"] >= 1.5:
                candidates.append(stats)

    candidates.sort(
        key=lambda item: (
            -item["score"],
            -item["record_count"],
            item["start"],
            item["record_size"],
        )
    )
    return dedupe_candidates(candidates)


def dedupe_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    kept: list[dict[str, Any]] = []
    for candidate in candidates:
        overlaps = False
        for existing in kept:
            if (
                candidate["record_size"] == existing["record_size"]
                and candidate["start"] <= existing["end"]
                and existing["start"] <= candidate["end"]
            ):
                overlaps = True
                break
        if not overlaps:
            kept.append(candidate)
    return kept


def repeated_padding_patterns(data: bytes) -> list[dict[str, Any]]:
    rows = []
    for width in PADDING_WIDTHS:
        locations: dict[bytes, list[int]] = defaultdict(list)
        for offset in range(0, len(data) - width + 1, width):
            chunk = data[offset : offset + width]
            if chunk in (b"\x00" * width, b"\xff" * width):
                continue
            locations[chunk].append(offset)
        for pattern, offsets in locations.items():
            if len(offsets) >= 4:
                rows.append(
                    {
                        "width": width,
                        "pattern": pattern.hex(" "),
                        "count": len(offsets),
                        "first_offsets": offsets[:10],
                    }
                )
    rows.sort(key=lambda item: (-item["count"], item["width"], item["first_offsets"][0]))
    return rows


def markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(row) + " |")


def render_markdown(result: dict[str, Any], top: int) -> None:
    file_info = result["file"]
    print("# Program.dat Table Discovery")
    print()
    print("This report contains statistical observations only. It does not infer field meanings.")
    print()
    print("## File")
    print()
    print(f"- Path: `{file_info['path']}`")
    print(f"- Size: {file_info['size']} bytes")
    print(f"- SHA-256: `{file_info['sha256']}`")
    print()

    print("## Candidate Fixed-Width Table Regions")
    rows = []
    for item in result["candidate_regions"][:top]:
        rows.append(
            [
                f"0x{item['start']:08x}-0x{item['end']:08x}",
                str(item["record_size"]),
                str(item["record_count"]),
                str(item["zero_slots"]),
                str(item["ff_slots"]),
                str(item["repeated_record_values"]),
                str(item["repeated_padding_patterns"]),
                f"{item['avg_record_entropy']:.3f}",
                f"{item['avg_record_printable_density']:.1%}",
                f"{item['score']:.3f}",
            ]
        )
    markdown_table(
        [
            "Range",
            "Record Size",
            "Records",
            "Zero Slots",
            "FF Slots",
            "Repeated Records",
            "Padding Patterns",
            "Avg Entropy",
            "Avg Printable",
            "Score",
        ],
        rows,
    )
    print()

    print("## Block Density And Entropy")
    rows = []
    for block in result["blocks"][:top]:
        rows.append(
            [
                f"0x{block['start']:08x}-0x{block['end']:08x}",
                str(block["length"]),
                f"{block['entropy']:.3f}",
                f"{block['printable_density']:.1%}",
                f"{block['zero_ratio']:.1%}",
                f"{block['ff_ratio']:.1%}",
            ]
        )
    markdown_table(["Range", "Length", "Entropy", "Printable", "Zero", "FF"], rows)
    print()

    print("## Repeated Padding-Like Patterns")
    rows = []
    for item in result["repeated_padding_patterns"][:top]:
        offsets = ", ".join(f"0x{offset:08x}" for offset in item["first_offsets"])
        rows.append([str(item["width"]), item["pattern"], str(item["count"]), offsets])
    markdown_table(["Width", "Pattern", "Count", "First Offsets"], rows)
    print()

    print("## Notes")
    print()
    print("- Candidate starts and ends are alignment-based observations, not confirmed table boundaries.")
    print("- Zero-filled and FF-filled slots can indicate unused space, padding, or unrelated data.")
    print("- Repeated record widths can suggest structure, but do not prove field layout or meaning.")


def analyze_file(path: Path, block_size: int) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "schema": "kpg111-helper.table-discovery.v1",
        "file": {
            "path": str(path),
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        },
        "record_sizes_tested": list(RECORD_SIZES),
        "block_size": block_size,
        "blocks": analyze_blocks(data, block_size),
        "candidate_regions": candidate_regions(data),
        "repeated_padding_patterns": repeated_padding_patterns(data),
    }


def main() -> int:
    args = parse_args()
    result = analyze_file(args.dat_file, args.block_size)
    if args.json:
        args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    render_markdown(result, args.top)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

