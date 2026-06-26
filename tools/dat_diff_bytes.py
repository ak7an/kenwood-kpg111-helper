#!/usr/bin/env python3
"""Controlled same-size byte diff for KPG111 DAT reverse engineering."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.decoder import (
    INDIVIDUAL_ID_TABLE_START,
    TALK_GROUP_TABLE_START,
    xor_bytes,
)
from tools.dat_channel_analysis import analyze_candidates


CSV_FIELDNAMES = [
    "range",
    "start",
    "end",
    "length",
    "before_hex",
    "after_hex",
    "before_xor_text",
    "after_xor_text",
    "notes",
]
DEFAULT_PREVIEW_CHARS = 64


@dataclass(frozen=True)
class ChangedRange:
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1


@dataclass(frozen=True)
class KnownRegion:
    name: str
    start: int
    end: int
    notes: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two same-size KPG111 DAT files for controlled byte changes."
    )
    parser.add_argument("before", type=Path, help="Before/baseline DAT file")
    parser.add_argument("after", type=Path, help="After/modified DAT file")
    parser.add_argument(
        "--context",
        type=int,
        default=8,
        help="Bytes before and after each changed range to show (default: 8)",
    )
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        default=0x5B,
        help="XOR key for decoded text previews (default: 0x5b)",
    )
    parser.add_argument(
        "--max-ranges",
        type=int,
        help="Maximum changed ranges to display (default: no limit)",
    )
    parser.add_argument("--csv", type=Path, help="Optional CSV report path")
    parser.add_argument(
        "--preview-chars",
        type=int,
        default=DEFAULT_PREVIEW_CHARS,
        help="Maximum characters for each console preview field (default: 64)",
    )
    return parser.parse_args()


def find_changed_ranges(before: bytes, after: bytes) -> list[ChangedRange]:
    ranges: list[ChangedRange] = []
    current_start: int | None = None
    previous = -1
    for offset, (left, right) in enumerate(zip(before, after)):
        if left == right:
            continue
        if current_start is None:
            current_start = previous = offset
            continue
        if offset == previous + 1:
            previous = offset
            continue
        ranges.append(ChangedRange(current_start, previous))
        current_start = previous = offset
    if current_start is not None:
        ranges.append(ChangedRange(current_start, previous))
    return ranges


def hex_bytes(data: bytes) -> str:
    return data.hex(" ")


def xor_text_preview(data: bytes, decode_key: int) -> str:
    decoded = xor_bytes(data, decode_key)
    return "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in decoded)


def console_preview(value: str, source_bytes: int, preview_chars: int) -> str:
    if len(value) <= preview_chars:
        return value
    return f"{value[:preview_chars]}... (truncated, {source_bytes} bytes)"


def bounded_range(data: bytes, changed: ChangedRange, context: int) -> tuple[int, int]:
    start = max(0, changed.start - context)
    end = min(len(data) - 1, changed.end + context)
    return start, end


def overlaps(left_start: int, left_end: int, right_start: int, right_end: int) -> bool:
    return left_start <= right_end and right_start <= left_end


def known_regions(data: bytes, decode_key: int) -> list[KnownRegion]:
    regions = []
    if len(data) > INDIVIDUAL_ID_TABLE_START:
        regions.append(
            KnownRegion(
                "known Individual ID table",
                INDIVIDUAL_ID_TABLE_START,
                min(TALK_GROUP_TABLE_START - 1, len(data) - 1),
                "decoded TG/ID table region; not a channel field",
            )
        )
    if len(data) > TALK_GROUP_TABLE_START:
        regions.append(
            KnownRegion(
                "known Talk Group table",
                TALK_GROUP_TABLE_START,
                len(data) - 1,
                "decoded TG/ID table start; table end is bounded by file size here",
            )
        )
    for candidate in analyze_candidates(data, decode_key, top=50):
        regions.append(
            KnownRegion(
                "candidate channel-like region",
                candidate.offset,
                candidate.offset + candidate.record_size - 1,
                "heuristic candidate only; channel record is not decoded",
            )
        )
    return regions


def nearby_known_region(changed: ChangedRange, regions: list[KnownRegion]) -> str:
    matches = [
        region
        for region in regions
        if overlaps(changed.start, changed.end, region.start, region.end)
    ]
    if not matches:
        return "unknown region"
    return "; ".join(
        f"{region.name} 0x{region.start:08x}-0x{region.end:08x} ({region.notes})"
        for region in matches
    )


def report_rows(
    before: bytes,
    after: bytes,
    ranges: list[ChangedRange],
    decode_key: int,
    regions: list[KnownRegion],
) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for index, changed in enumerate(ranges, start=1):
        before_slice = before[changed.start : changed.end + 1]
        after_slice = after[changed.start : changed.end + 1]
        rows.append(
            {
                "range": index,
                "start": f"0x{changed.start:08x}",
                "end": f"0x{changed.end:08x}",
                "length": changed.length,
                "before_hex": hex_bytes(before_slice),
                "after_hex": hex_bytes(after_slice),
                "before_xor_text": xor_text_preview(before_slice, decode_key),
                "after_xor_text": xor_text_preview(after_slice, decode_key),
                "notes": nearby_known_region(changed, regions),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str | int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def render_report(
    before_path: Path,
    after_path: Path,
    before: bytes,
    after: bytes,
    rows: list[dict[str, str | int]],
    ranges: list[ChangedRange],
    context: int,
    max_ranges: int | None,
    preview_chars: int,
) -> str:
    displayed_rows = rows if max_ranges is None else rows[:max_ranges]
    displayed_ranges = ranges if max_ranges is None else ranges[:max_ranges]
    lines = [
        "DAT Byte Diff Report",
        f"Before: {before_path}",
        f"After: {after_path}",
        f"Size: {len(before)} bytes",
        f"Changed ranges: {len(ranges)}",
        f"Changed bytes: {sum(changed.length for changed in ranges)}",
    ]
    if not ranges:
        lines.append("No byte changes.")
        return "\n".join(lines)

    lines.append("")
    for row, changed in zip(displayed_rows, displayed_ranges):
        context_start, context_end = bounded_range(before, changed, context)
        before_context = before[context_start : context_end + 1]
        after_context = after[context_start : context_end + 1]
        before_hex = console_preview(str(row["before_hex"]), changed.length, preview_chars)
        after_hex = console_preview(str(row["after_hex"]), changed.length, preview_chars)
        before_text = console_preview(str(row["before_xor_text"]), changed.length, preview_chars)
        after_text = console_preview(str(row["after_xor_text"]), changed.length, preview_chars)
        before_context_hex = console_preview(hex_bytes(before_context), len(before_context), preview_chars)
        after_context_hex = console_preview(hex_bytes(after_context), len(after_context), preview_chars)
        lines.extend(
            [
                f"Range {row['range']}: {row['start']}-{row['end']} length={row['length']}",
                f"  before hex: {before_hex}",
                f"  after hex:  {after_hex}",
                f"  before XOR text: {before_text!r}",
                f"  after XOR text:  {after_text!r}",
                f"  context: 0x{context_start:08x}-0x{context_end:08x}",
                f"    before: {before_context_hex}",
                f"    after:  {after_context_hex}",
                f"  nearby known region: {row['notes']}",
            ]
        )
    if max_ranges is not None and len(rows) > max_ranges:
        lines.append(f"... {len(rows) - max_ranges} more ranges not shown")
    return "\n".join(lines)


def validate_args(context: int, max_ranges: int | None, preview_chars: int) -> None:
    if context < 0:
        raise ValueError("--context must be >= 0")
    if max_ranges is not None and max_ranges < 0:
        raise ValueError("--max-ranges must be >= 0")
    if preview_chars < 1:
        raise ValueError("--preview-chars must be >= 1")


def main() -> int:
    args = parse_args()
    try:
        validate_args(args.context, args.max_ranges, args.preview_chars)
        before = args.before.read_bytes()
        after = args.after.read_bytes()
        if len(before) != len(after):
            raise ValueError(
                f"files must be the same size: before={len(before)} after={len(after)}"
            )

        ranges = find_changed_ranges(before, after)
        regions = known_regions(before, args.decode_key)
        rows = report_rows(before, after, ranges, args.decode_key, regions)
        if args.csv is not None:
            write_csv(args.csv, rows)
        print(
            render_report(
                args.before,
                args.after,
                before,
                after,
                rows,
                ranges,
                args.context,
                args.max_ranges,
                args.preview_chars,
            )
        )
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
