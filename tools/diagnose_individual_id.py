#!/usr/bin/env python3
"""Read-only Individual ID differential diagnostic for KPG111 DAT files."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import sys


HEADER_SIZE = 0x40
DEFAULT_FOCUS = 0x11D80
DEFAULT_BEFORE = 5
DEFAULT_AFTER = 10
DEFAULT_RECORD_STRIDE = 32
CANDIDATE_STRIDES = (16, 24, 32)
XOR_16 = 0x5151


@dataclass(frozen=True)
class ByteRange:
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1


def parse_int(value: str) -> int:
    try:
        return int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer: {value!r}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only diagnostic for an apparent Individual ID record change."
    )
    parser.add_argument("before", type=Path, help="Baseline DAT file")
    parser.add_argument("after", type=Path, help="Modified DAT file")
    parser.add_argument(
        "--header-size",
        type=parse_int,
        default=HEADER_SIZE,
        help="Bytes excluded from dominant payload XOR calculation (default: 0x40)",
    )
    parser.add_argument(
        "--focus",
        type=parse_int,
        default=DEFAULT_FOCUS,
        help="Offset around which candidate records are dumped (default: 0x11d80)",
    )
    parser.add_argument(
        "--before-records",
        type=parse_int,
        default=DEFAULT_BEFORE,
        help="Candidate records to dump before the focus record (default: 5)",
    )
    parser.add_argument(
        "--after-records",
        type=parse_int,
        default=DEFAULT_AFTER,
        help="Candidate records to dump after the focus record (default: 10)",
    )
    parser.add_argument(
        "--record-base",
        type=parse_int,
        help="Print a concise focused report for one candidate record at OFFSET",
    )
    parser.add_argument(
        "--record-stride",
        type=parse_int,
        default=DEFAULT_RECORD_STRIDE,
        help="Record size for --record-base mode (default: 32)",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.header_size < 0:
        raise ValueError("--header-size must be >= 0")
    if args.focus < 0:
        raise ValueError("--focus must be >= 0")
    if args.before_records < 0:
        raise ValueError("--before-records must be >= 0")
    if args.after_records < 0:
        raise ValueError("--after-records must be >= 0")
    if args.record_base is not None and args.record_base < 0:
        raise ValueError("--record-base must be >= 0")
    if args.record_stride < 1:
        raise ValueError("--record-stride must be >= 1")


def dominant_payload_xor(left: bytes, right: bytes, payload_start: int) -> tuple[int | None, int, int]:
    compare_len = min(len(left), len(right))
    if payload_start >= compare_len:
        return None, 0, 0
    counts = Counter(left[offset] ^ right[offset] for offset in range(payload_start, compare_len))
    value, count = counts.most_common(1)[0]
    return value, count, compare_len - payload_start


def normalized_right(left: bytes, right: bytes, header_size: int, mask: int | None) -> bytes:
    compare_len = min(len(left), len(right))
    if mask is None:
        return right[:compare_len]
    header_end = min(header_size, compare_len)
    return right[:header_end] + bytes(byte ^ mask for byte in right[header_end:compare_len])


def changed_ranges(left: bytes, right: bytes) -> list[ByteRange]:
    ranges: list[ByteRange] = []
    start: int | None = None
    previous = -1
    for offset, (left_byte, right_byte) in enumerate(zip(left, right)):
        if left_byte == right_byte:
            continue
        if start is None:
            start = previous = offset
            continue
        if offset == previous + 1:
            previous = offset
            continue
        ranges.append(ByteRange(start, previous))
        start = previous = offset
    if start is not None:
        ranges.append(ByteRange(start, previous))
    return ranges


def hex_bytes(data: bytes) -> str:
    return data.hex(" ")


def ascii_view(data: bytes) -> str:
    return "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in data)


def changed_positions(record_start: int, size: int, ranges: list[ByteRange]) -> str:
    positions: list[str] = []
    record_end = record_start + size - 1
    for byte_range in ranges:
        start = max(record_start, byte_range.start)
        end = min(record_end, byte_range.end)
        if start > end:
            continue
        for offset in range(start, end + 1):
            positions.append(f"+0x{offset - record_start:02x}")
    return ", ".join(positions) if positions else "none"


def le16_candidates(data: bytes) -> list[str]:
    rows: list[str] = []
    for index in range(max(0, len(data) - 1)):
        raw = int.from_bytes(data[index : index + 2], "little")
        decoded = raw ^ XOR_16
        rows.append(
            f"+0x{index:02x}: le=0x{raw:04x} ({raw}), xor5151=0x{decoded:04x} ({decoded})"
        )
    return rows


def field_slice(record: bytes, start: int, end_exclusive: int) -> bytes:
    if start >= len(record):
        return b""
    return record[start : min(end_exclusive, len(record))]


def render_focused_record_report(
    before_path: Path,
    after_path: Path,
    before: bytes,
    after: bytes,
    args: argparse.Namespace,
) -> str:
    mask, mask_count, payload_compared = dominant_payload_xor(before, after, args.header_size)
    after_normalized = normalized_right(before, after, args.header_size, mask)
    compare_len = min(len(before), len(after))
    ranges = changed_ranges(before[:compare_len], after_normalized)
    base = args.record_base
    stride = args.record_stride
    if base is None:
        raise ValueError("--record-base is required for focused record mode")
    if base + stride > compare_len:
        raise ValueError(
            f"record extends beyond compared data: base=0x{base:08x} stride={stride} compared={compare_len}"
        )

    before_record = before[base : base + stride]
    after_record = after_normalized[base : base + stride]
    name_before = field_slice(before_record, 0x01, 0x0F)
    name_after = field_slice(after_record, 0x01, 0x0F)
    numeric_before = field_slice(before_record, 0x13, 0x15)
    numeric_after = field_slice(after_record, 0x13, 0x15)
    mask_text = "none"
    if mask is not None:
        percent = mask_count / payload_compared * 100.0 if payload_compared else 0.0
        mask_text = f"0x{mask:02x} ({mask_count}/{payload_compared}, {percent:.2f}% of compared payload)"

    lines = [
        "# Individual ID Focused Record Diagnostic",
        "",
        "Read-only evidence report. This tool compares existing bytes only and does not infer or implement write behavior.",
        "",
        f"- Before: {before_path}",
        f"- After: {after_path}",
        f"- Dominant payload XOR mask applied to second file: {mask_text}",
        f"- Record base offset: 0x{base:08x}",
        f"- Record stride: {stride}",
        f"- Changed byte positions: {changed_positions(base, stride, ranges)}",
        "",
        "## Record Hex",
        "",
        f"- Before: `{hex_bytes(before_record)}`",
        f"- After normalized: `{hex_bytes(after_record)}`",
        "",
        "## Field-Style Summary",
        "",
        "| Field | Before Hex | Before ASCII | After Normalized Hex | After Normalized ASCII |",
        "| --- | --- | --- | --- | --- |",
        (
            f"| +0x01..+0x0E name/label candidate | {hex_bytes(name_before)} | "
            f"`{ascii_view(name_before)}` | {hex_bytes(name_after)} | `{ascii_view(name_after)}` |"
        ),
        (
            f"| +0x13..+0x14 numeric candidate | {hex_bytes(numeric_before)} | "
            f"`{ascii_view(numeric_before)}` | {hex_bytes(numeric_after)} | `{ascii_view(numeric_after)}` |"
        ),
        "",
        "## Numeric Candidate +0x13..+0x14",
        "",
    ]
    if len(numeric_after) == 2:
        raw = int.from_bytes(numeric_after, "little")
        decoded = raw ^ XOR_16
        lines.extend(
            [
                f"- Raw little-endian value: 0x{raw:04x} ({raw})",
                f"- XOR 0x5151 decoded value: 0x{decoded:04x} ({decoded})",
            ]
        )
    else:
        lines.append("- Raw little-endian value: unavailable; record is shorter than +0x14")
    return "\n".join(lines)


def candidate_offsets(focus: int, stride: int, before: int, after: int) -> list[int]:
    anchor = focus - (focus % stride)
    first = max(0, anchor - before * stride)
    return [first + index * stride for index in range(before + after + 1)]


def markdown_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    if not rows:
        lines.append("| " + " | ".join("none" for _ in headers) + " |")
        return lines
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    return lines


def render_record(
    before: bytes,
    after_normalized: bytes,
    offset: int,
    stride: int,
    ranges: list[ByteRange],
) -> list[str]:
    before_record = before[offset : offset + stride]
    after_record = after_normalized[offset : offset + stride]
    lines = [
        f"### Record candidate @ 0x{offset:08x} stride {stride}",
        "",
        f"- Changed byte positions in candidate: {changed_positions(offset, stride, ranges)}",
        f"- Before hex: `{hex_bytes(before_record)}`",
        f"- After normalized hex: `{hex_bytes(after_record)}`",
        f"- Before ASCII: `{ascii_view(before_record)}`",
        f"- After normalized ASCII: `{ascii_view(after_record)}`",
        "",
        "Possible 16-bit little-endian values in after-normalized candidate:",
        "",
    ]
    lines.extend(f"- {row}" for row in le16_candidates(after_record))
    lines.append("")
    return lines


def render_report(before_path: Path, after_path: Path, before: bytes, after: bytes, args: argparse.Namespace) -> str:
    mask, mask_count, payload_compared = dominant_payload_xor(before, after, args.header_size)
    after_normalized = normalized_right(before, after, args.header_size, mask)
    compare_len = min(len(before), len(after))
    ranges = changed_ranges(before[:compare_len], after_normalized)
    mask_text = "none"
    if mask is not None:
        percent = mask_count / payload_compared * 100.0 if payload_compared else 0.0
        mask_text = f"0x{mask:02x} ({mask_count}/{payload_compared}, {percent:.2f}% of compared payload)"

    focus_start = max(0, args.focus - 0x40)
    focus_end = min(compare_len, args.focus + 0x80)
    focus_ranges = [
        byte_range
        for byte_range in ranges
        if byte_range.start < focus_end and byte_range.end >= focus_start
    ]

    lines: list[str] = [
        "# Individual ID Diagnostic",
        "",
        "Read-only evidence report. This tool compares existing bytes only and does not infer or implement write behavior.",
        "",
        "## Inputs",
        "",
    ]
    lines.extend(
        markdown_table(
            ["File", "Size"],
            [[str(before_path), len(before)], [str(after_path), len(after)]],
        )
    )
    lines.extend(
        [
            "",
            "## Normalization",
            "",
            f"- Header size: 0x{args.header_size:08x} ({args.header_size})",
            f"- Compared bytes: {compare_len}",
            f"- Dominant payload XOR mask applied to second file: {mask_text}",
            f"- Length mismatch bytes outside comparison: {abs(len(before) - len(after))}",
            "",
            "## All Normalized Differing Ranges",
            "",
            f"- Range count: {len(ranges)}",
            f"- Differing bytes: {sum(byte_range.length for byte_range in ranges)}",
            "",
        ]
    )
    lines.extend(
        markdown_table(
            ["Start", "End", "Length", "Before Hex", "After Normalized Hex"],
            [
                [
                    f"0x{byte_range.start:08x}",
                    f"0x{byte_range.end:08x}",
                    byte_range.length,
                    hex_bytes(before[byte_range.start : byte_range.end + 1]),
                    hex_bytes(after_normalized[byte_range.start : byte_range.end + 1]),
                ]
                for byte_range in ranges
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Focus Around 0x11d80",
            "",
            f"- Focus offset: 0x{args.focus:08x}",
            f"- Focus window: 0x{focus_start:08x}..0x{max(focus_start, focus_end - 1):08x}",
            "",
        ]
    )
    lines.extend(
        markdown_table(
            ["Start", "End", "Length", "Before Hex", "After Normalized Hex"],
            [
                [
                    f"0x{byte_range.start:08x}",
                    f"0x{byte_range.end:08x}",
                    byte_range.length,
                    hex_bytes(before[byte_range.start : byte_range.end + 1]),
                    hex_bytes(after_normalized[byte_range.start : byte_range.end + 1]),
                ]
                for byte_range in focus_ranges
            ],
        )
    )

    lines.extend(["", "## Candidate Record Dumps", ""])
    for stride in CANDIDATE_STRIDES:
        anchor = args.focus - (args.focus % stride)
        lines.extend(
            [
                f"## Stride {stride} Bytes",
                "",
                f"- Anchor: 0x{anchor:08x}",
                f"- Records before anchor: {args.before_records}",
                f"- Records after anchor: {args.after_records}",
                "",
            ]
        )
        for offset in candidate_offsets(args.focus, stride, args.before_records, args.after_records):
            if offset + stride > compare_len:
                continue
            lines.extend(render_record(before, after_normalized, offset, stride, ranges))

    lines.extend(
        [
            "## Hypotheses",
            "",
            "- None. This diagnostic intentionally reports byte evidence only.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        validate_args(args)
        before = args.before.expanduser().read_bytes()
        after = args.after.expanduser().read_bytes()
        if args.record_base is not None:
            print(render_focused_record_report(args.before, args.after, before, after, args))
        else:
            print(render_report(args.before, args.after, before, after, args))
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
