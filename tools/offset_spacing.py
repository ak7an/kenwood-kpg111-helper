#!/usr/bin/env python3
"""Analyze spacing and alignment in one or more comparison session files."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


ALIGNMENTS = (2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 256)
RECORD_SIZE_CANDIDATES = (8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report statistical spacing observations from session.json files."
    )
    parser.add_argument("sessions", nargs="+", type=Path, help="Session JSON files")
    parser.add_argument(
        "--top",
        type=int,
        default=30,
        help="Maximum rows per section (default: 30)",
    )
    return parser.parse_args()


def load_session(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["_session_path"] = str(path)
    return data


def positive_spacings(values: list[int]) -> list[int]:
    unique_values = sorted(set(values))
    return [
        right - left
        for left, right in zip(unique_values, unique_values[1:])
        if right > left
    ]


def common_divisors(values: list[int], limit: int = 256) -> Counter[int]:
    counts: Counter[int] = Counter()
    for value in values:
        if value <= 0:
            continue
        for divisor in range(2, min(value, limit) + 1):
            if value % divisor == 0:
                counts[divisor] += 1
    return counts


def alignment_histogram(values: list[int]) -> Counter[int]:
    counts: Counter[int] = Counter()
    for value in values:
        for alignment in ALIGNMENTS:
            if value % alignment == 0:
                counts[alignment] += 1
    return counts


def likely_record_sizes(offset_spacings: list[int], region_start_spacings: list[int]) -> list[tuple[int, int]]:
    combined = offset_spacings + region_start_spacings
    rows = []
    for candidate in RECORD_SIZE_CANDIDATES:
        support = 0
        for spacing in combined:
            if spacing and spacing % candidate == 0:
                support += 1
        rows.append((candidate, support))
    rows.sort(key=lambda item: (-item[1], item[0]))
    return rows


def markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(row) + " |")


def main() -> int:
    args = parse_args()
    sessions = [load_session(path) for path in args.sessions]
    all_offsets: list[int] = []
    all_region_starts: list[int] = []
    all_region_lengths: list[int] = []

    for session in sessions:
        all_offsets.extend(int(offset) for offset in session.get("changed_offsets", []))
        for region in session.get("changed_regions", []):
            all_region_starts.append(int(region["start"]))
            all_region_lengths.append(int(region["length"]))

    offset_spacings = positive_spacings(all_offsets)
    region_start_spacings = positive_spacings(all_region_starts)
    spacing_counts = Counter(offset_spacings)
    region_spacing_counts = Counter(region_start_spacings)
    divisor_counts = common_divisors(offset_spacings + region_start_spacings)
    offset_alignment_counts = alignment_histogram(all_offsets)
    region_alignment_counts = alignment_histogram(all_region_starts)
    length_counts = Counter(all_region_lengths)

    print("# KPG111 Offset Spacing Report")
    print()
    print("This report contains statistical observations only. It does not infer field meanings.")
    print()
    print(f"- Sessions analyzed: {len(sessions)}")
    print(f"- Unique changed offsets: {len(set(all_offsets))}")
    print(f"- Unique changed region starts: {len(set(all_region_starts))}")
    print()

    print("## Spacing Between Changed Offsets")
    rows = [
        [str(spacing), str(count)]
        for spacing, count in spacing_counts.most_common(args.top)
    ]
    markdown_table(["Spacing", "Observations"], rows)
    print()

    print("## Spacing Between Changed Region Starts")
    rows = [
        [str(spacing), str(count)]
        for spacing, count in region_spacing_counts.most_common(args.top)
    ]
    markdown_table(["Spacing", "Observations"], rows)
    print()

    print("## Common Divisors")
    rows = [
        [str(divisor), str(count)]
        for divisor, count in divisor_counts.most_common(args.top)
    ]
    markdown_table(["Divisor", "Supported Spacings"], rows)
    print()

    print("## Likely Record-Size Candidates")
    print()
    print("Candidate support means observed spacings are multiples of that size; this is not proof of record size.")
    rows = [
        [str(candidate), str(support)]
        for candidate, support in likely_record_sizes(offset_spacings, region_start_spacings)
        if support > 0
    ][: args.top]
    markdown_table(["Candidate Size", "Spacing-Multiple Support"], rows)
    print()

    print("## Alignment Histograms")
    rows = []
    for alignment in ALIGNMENTS:
        rows.append(
            [
                str(alignment),
                str(offset_alignment_counts.get(alignment, 0)),
                str(region_alignment_counts.get(alignment, 0)),
            ]
        )
    markdown_table(["Alignment", "Changed Offsets", "Region Starts"], rows)
    print()

    print("## Repeated Changed-Region Lengths")
    rows = [
        [str(length), str(count)]
        for length, count in length_counts.most_common(args.top)
    ]
    markdown_table(["Region Length", "Observations"], rows)
    print()

    if all_region_lengths:
        print("## Region Length Summary")
        print()
        print(f"- Minimum length: {min(all_region_lengths)}")
        print(f"- Maximum length: {max(all_region_lengths)}")
        print(f"- GCD of region lengths: {math.gcd(*all_region_lengths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

