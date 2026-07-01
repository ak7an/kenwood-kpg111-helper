#!/usr/bin/env python3
"""Read-only layout differential analysis for two KPG111 DAT files."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import string
import sys


HEADER_SIZE = 0x40
BLANK_TG_START = 0x14940
TRAVEL_TG_START = 0x14F80
TG_RECORD_SIZE = 32
TG_NAME_START = 0x01
TG_NAME_END_EXCLUSIVE = 0x0F
TG_NUMBER_START = 0x13
TG_NUMBER_SIZE = 2
TG_NUMBER_XOR = 0x5151
DEFAULT_MAX_RECORDS = 512
DEFAULT_EARLY_END = 0x16000
SEARCH_VALUES = (0x14940, 0x14F80, 0x5E80, 400, 397, 340, 12800, 10880)


@dataclass(frozen=True)
class ByteRange:
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1


@dataclass(frozen=True)
class SearchHit:
    file_label: str
    value: int
    width: int
    endian: str
    offset: int
    area: str


@dataclass(frozen=True)
class TgRecord:
    slot: int
    offset: int
    raw_name_hex: str
    raw_name_ascii: str
    decoded_number: int
    uniform: bool
    apparent_valid: bool


def parse_int(value: str) -> int:
    try:
        return int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer: {value!r}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only evidence report comparing two DAT layouts."
    )
    parser.add_argument("blank", type=Path, help="Blank/baseline DAT file")
    parser.add_argument("travel", type=Path, help="Travel/modified DAT file")
    parser.add_argument(
        "--header-size",
        type=parse_int,
        default=HEADER_SIZE,
        help="Header size for raw header comparison (default: 0x40)",
    )
    parser.add_argument(
        "--early-end",
        type=parse_int,
        default=DEFAULT_EARLY_END,
        help="End offset for early-area candidate reporting (default: 0x16000)",
    )
    parser.add_argument(
        "--max-records",
        type=parse_int,
        default=DEFAULT_MAX_RECORDS,
        help="Maximum TG records to scan at each candidate start (default: 512)",
    )
    return parser.parse_args()


def validate_args(header_size: int, early_end: int, max_records: int) -> None:
    if header_size < 0:
        raise ValueError("--header-size must be >= 0")
    if early_end < 0:
        raise ValueError("--early-end must be >= 0")
    if max_records < 1:
        raise ValueError("--max-records must be >= 1")


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
    return right[: min(header_size, compare_len)] + bytes(
        byte ^ mask for byte in right[min(header_size, compare_len) : compare_len]
    )


def changed_ranges(left: bytes, right: bytes) -> list[ByteRange]:
    ranges: list[ByteRange] = []
    start: int | None = None
    previous = -1
    for offset, (left_byte, right_byte) in enumerate(zip(left, right)):
        if left_byte == right_byte:
            continue
        if start is None:
            start = previous = offset
        elif offset == previous + 1:
            previous = offset
        else:
            ranges.append(ByteRange(start, previous))
            start = previous = offset
    if start is not None:
        ranges.append(ByteRange(start, previous))
    return ranges


def bounded_hex(data: bytes, byte_range: ByteRange, limit: int = 16) -> str:
    sample = data[byte_range.start : min(byte_range.end + 1, byte_range.start + limit)]
    suffix = "" if byte_range.length <= limit else " ..."
    return sample.hex(" ") + suffix


def region_label(start: int, end: int) -> str:
    if end < HEADER_SIZE:
        return "header"
    if start < BLANK_TG_START:
        return "early-before-blank-tg"
    if start <= BLANK_TG_START + 400 * TG_RECORD_SIZE - 1 and end >= BLANK_TG_START:
        if start <= TRAVEL_TG_START + 400 * TG_RECORD_SIZE - 1 and end >= TRAVEL_TG_START:
            return "overlaps-both-tg-candidates"
        return "blank-tg-candidate"
    if start <= TRAVEL_TG_START + 400 * TG_RECORD_SIZE - 1 and end >= TRAVEL_TG_START:
        return "travel-tg-candidate"
    return "unknown"


def area_label(offset: int) -> str:
    if offset < HEADER_SIZE:
        return "header"
    if offset < BLANK_TG_START:
        return "early-before-blank-tg"
    if BLANK_TG_START <= offset < BLANK_TG_START + 400 * TG_RECORD_SIZE:
        return "blank-tg-candidate"
    if TRAVEL_TG_START <= offset < TRAVEL_TG_START + 400 * TG_RECORD_SIZE:
        return "travel-tg-candidate"
    return "unknown"


def is_printable_ascii_name(raw_name: bytes) -> tuple[bool, str]:
    stripped = raw_name.split(b"\x00", 1)[0].rstrip(b" ")
    if not stripped:
        return False, ""
    printable = set(bytes(string.printable, "ascii"))
    if all(byte in printable and byte not in b"\r\n\t\x0b\x0c" for byte in stripped):
        return True, stripped.decode("ascii", errors="replace")
    return False, ""


def decode_tg_records(data: bytes, start: int, max_records: int) -> list[TgRecord]:
    records: list[TgRecord] = []
    for slot in range(max_records):
        offset = start + slot * TG_RECORD_SIZE
        if offset + TG_RECORD_SIZE > len(data):
            break
        record = data[offset : offset + TG_RECORD_SIZE]
        raw_name = record[TG_NAME_START:TG_NAME_END_EXCLUSIVE]
        name_ok, raw_name_ascii = is_printable_ascii_name(raw_name)
        encoded_number = int.from_bytes(
            record[TG_NUMBER_START : TG_NUMBER_START + TG_NUMBER_SIZE], "little"
        )
        decoded_number = encoded_number ^ TG_NUMBER_XOR
        uniform = len(set(record)) == 1
        apparent_valid = name_ok and not uniform and 1 <= decoded_number <= 65535
        records.append(
            TgRecord(
                slot=slot,
                offset=offset,
                raw_name_hex=raw_name.hex(" "),
                raw_name_ascii=raw_name_ascii,
                decoded_number=decoded_number,
                uniform=uniform,
                apparent_valid=apparent_valid,
            )
        )
    return records


def search_widths(value: int) -> tuple[int, ...]:
    widths: list[int] = []
    if value <= 0xFFFF:
        widths.append(2)
    if value <= 0xFFFFFFFF:
        widths.append(4)
    return tuple(widths)


def search_occurrences(data: bytes, file_label: str, values: tuple[int, ...]) -> list[SearchHit]:
    hits: list[SearchHit] = []
    for value in values:
        for width in search_widths(value):
            for endian in ("little", "big"):
                needle = value.to_bytes(width, endian)
                start = 0
                while True:
                    offset = data.find(needle, start)
                    if offset == -1:
                        break
                    hits.append(SearchHit(file_label, value, width, endian, offset, area_label(offset)))
                    start = offset + 1
    return hits


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


def tg_summary_rows(label: str, start: int, records: list[TgRecord]) -> list[object]:
    valid = [record for record in records if record.apparent_valid]
    occupied_like = [record for record in records if not record.uniform]
    first_valid = "none"
    if valid:
        first = valid[0]
        first_valid = (
            f"slot {first.slot} @ 0x{first.offset:08x}: "
            f"{first.raw_name_ascii!r} #{first.decoded_number}"
        )
    return [
        label,
        f"0x{start:08x}",
        len(records),
        len(occupied_like),
        len(valid),
        first_valid,
    ]


def render_report(blank_path: Path, travel_path: Path, blank: bytes, travel: bytes, args: argparse.Namespace) -> str:
    mask, mask_count, payload_compared = dominant_payload_xor(blank, travel, args.header_size)
    normalized = normalized_right(blank, travel, args.header_size, mask)
    compare_len = min(len(blank), len(travel))
    ranges = changed_ranges(blank[:compare_len], normalized)
    header_ranges = [
        byte_range
        for byte_range in changed_ranges(blank[: min(args.header_size, compare_len)], travel[: min(args.header_size, compare_len)])
    ]
    search_hits = search_occurrences(blank, "blank", SEARCH_VALUES) + search_occurrences(
        travel, "travel", SEARCH_VALUES
    )
    early_candidates = [
        byte_range
        for byte_range in ranges
        if byte_range.start < min(args.early_end, compare_len)
    ]
    unknown_ranges = [
        byte_range
        for byte_range in ranges
        if region_label(byte_range.start, byte_range.end) == "unknown"
    ]

    tg_jobs = [
        ("blank @ blank TG start", blank, BLANK_TG_START),
        ("blank @ travel TG start", blank, TRAVEL_TG_START),
        ("travel @ blank TG start", travel, BLANK_TG_START),
        ("travel @ travel TG start", travel, TRAVEL_TG_START),
    ]
    tg_decoded = [
        (label, start, decode_tg_records(data, start, args.max_records))
        for label, data, start in tg_jobs
    ]

    mask_text = "none"
    if mask is not None:
        pct = (mask_count / payload_compared * 100.0) if payload_compared else 0.0
        mask_text = f"0x{mask:02x} ({mask_count}/{payload_compared}, {pct:.2f}% of compared payload)"

    lines: list[str] = [
        "# Layout Differential Analysis",
        "",
        "Read-only diagnostic. This report compares existing bytes only and does not infer or implement write behavior.",
        "",
        "## Inputs",
        "",
    ]
    lines.extend(
        markdown_table(
            ["File", "Size", "SHA-256"],
            [
                [str(blank_path), len(blank), sha256(blank).hexdigest()],
                [str(travel_path), len(travel), sha256(travel).hexdigest()],
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Payload Normalization Evidence",
            "",
            f"- Header size: 0x{args.header_size:08x} ({args.header_size})",
            f"- Compared bytes: {compare_len}",
            f"- Dominant payload XOR mask applied to travel for diff ranges: {mask_text}",
            f"- Length mismatch bytes outside comparison: {abs(len(blank) - len(travel))}",
            "",
            "## Header Comparison",
            "",
            f"- Raw header differing ranges: {len(header_ranges)}",
        ]
    )
    lines.extend(
        markdown_table(
            ["Start", "End", "Length", "Blank Hex", "Travel Hex"],
            [
                [
                    f"0x{byte_range.start:08x}",
                    f"0x{byte_range.end:08x}",
                    byte_range.length,
                    bounded_hex(blank, byte_range),
                    bounded_hex(travel, byte_range),
                ]
                for byte_range in header_ranges
            ],
        )
    )

    lines.extend(
        [
            "",
            "## Normalized Differing Byte Ranges",
            "",
            f"- Range count: {len(ranges)}",
            f"- Differing bytes: {sum(byte_range.length for byte_range in ranges)}",
            "",
        ]
    )
    lines.extend(
        markdown_table(
            ["Start", "End", "Length", "Region", "Blank Hex", "Travel Normalized Hex"],
            [
                [
                    f"0x{byte_range.start:08x}",
                    f"0x{byte_range.end:08x}",
                    byte_range.length,
                    region_label(byte_range.start, byte_range.end),
                    bounded_hex(blank, byte_range),
                    bounded_hex(normalized, byte_range),
                ]
                for byte_range in ranges
            ],
        )
    )

    lines.extend(
        [
            "",
            "## Candidate Header/Early Descriptor Evidence",
            "",
            "Candidate means the byte range is in the header/early area or contains one of the requested raw numeric values. It is not proof of a pointer or allocator.",
            "",
        ]
    )
    lines.extend(
        markdown_table(
            ["Start", "End", "Length", "Region", "Blank Hex", "Travel Normalized Hex"],
            [
                [
                    f"0x{byte_range.start:08x}",
                    f"0x{byte_range.end:08x}",
                    byte_range.length,
                    region_label(byte_range.start, byte_range.end),
                    bounded_hex(blank, byte_range),
                    bounded_hex(normalized, byte_range),
                ]
                for byte_range in early_candidates
            ],
        )
    )

    lines.extend(["", "## Raw Numeric Search", ""])
    lines.extend(
        markdown_table(
            ["File", "Value", "Width", "Endian", "Offset", "Area"],
            [
                [
                    hit.file_label,
                    f"0x{hit.value:x} ({hit.value})",
                    hit.width,
                    hit.endian,
                    f"0x{hit.offset:08x}",
                    hit.area,
                ]
                for hit in sorted(search_hits, key=lambda item: (item.file_label, item.offset, item.value, item.width, item.endian))
            ],
        )
    )

    lines.extend(["", "## TG Record Scan", ""])
    lines.extend(
        markdown_table(
            ["Scan", "Start", "Records Scanned", "Non-Uniform Records", "Apparent Valid Records", "First Apparent Valid"],
            [tg_summary_rows(label, start, records) for label, start, records in tg_decoded],
        )
    )
    lines.extend(
        [
            "",
            "Apparent valid record criterion: record is non-uniform, raw name bytes at +0x01..+0x0e form printable ASCII after NUL/space trimming, and +0x13..+0x14 little-endian XOR 0x5151 is 1..65535.",
            "",
            "## Unknown Differing Regions",
            "",
        ]
    )
    lines.extend(
        markdown_table(
            ["Start", "End", "Length", "Blank Hex", "Travel Normalized Hex"],
            [
                [
                    f"0x{byte_range.start:08x}",
                    f"0x{byte_range.end:08x}",
                    byte_range.length,
                    bounded_hex(blank, byte_range),
                    bounded_hex(normalized, byte_range),
                ]
                for byte_range in unknown_ranges
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Hypotheses",
            "",
            "- No layout algorithm is inferred by this tool. Any candidate descriptor rows above are evidence locations only.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        validate_args(args.header_size, args.early_end, args.max_records)
        blank = args.blank.read_bytes()
        travel = args.travel.read_bytes()
        print(render_report(args.blank, args.travel, blank, travel, args))
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
