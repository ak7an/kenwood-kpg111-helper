#!/usr/bin/env python3
"""Read-only layout trigger diagnostic for KPG111 DAT experiments."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import string
import sys


HEADER_SIZE = 0x40
BLANK_TG_START = 0x14940
TRAVEL_TG_START = 0x14F80
TG_RECORD_SIZE = 32
TG_RECORD_COUNT = 400
TG_NAME_START = 0x01
TG_NAME_END_EXCLUSIVE = 0x0F
TG_NUMBER_START = 0x13
TG_NUMBER_SIZE = 2
TG_NUMBER_XOR = 0x5151
INDIVIDUAL_ID_START = 0x11D80
INDIVIDUAL_ID_RECORD_SIZE = 32
CHANNEL_START = 0x5E80
CHANNEL_STRIDE = 0x40
DEFAULT_WINDOW = 0x100


@dataclass(frozen=True)
class ByteRange:
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1


@dataclass(frozen=True)
class TgRecord:
    slot: int
    offset: int
    name_hex: str
    name_ascii: str
    numeric_raw: int
    numeric_decoded: int
    uniform: bool
    apparent_valid: bool


@dataclass(frozen=True)
class TgScan:
    start: int
    non_uniform_count: int
    apparent_valid_count: int
    first_apparent_valid: TgRecord | None
    first_changed_record: int | None
    changed: bool


def parse_int(value: str) -> int:
    try:
        return int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer: {value!r}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only diagnostic for DAT layout trigger experiments."
    )
    parser.add_argument("baseline", type=Path, help="Baseline DAT file")
    parser.add_argument("experiments", nargs="+", type=Path, help="Experiment DAT file(s)")
    parser.add_argument(
        "--header-size",
        type=parse_int,
        default=HEADER_SIZE,
        help="Bytes excluded from dominant payload XOR calculation (default: 0x40)",
    )
    parser.add_argument(
        "--window",
        type=parse_int,
        default=DEFAULT_WINDOW,
        help="Bytes before and after known starts for nearby range reporting (default: 0x100)",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.header_size < 0:
        raise ValueError("--header-size must be >= 0")
    if args.window < 0:
        raise ValueError("--window must be >= 0")


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


def ranges_overlap(start: int, end: int, byte_range: ByteRange) -> bool:
    return start <= byte_range.end and byte_range.start <= end


def range_changed(start: int, length: int, ranges: list[ByteRange]) -> bool:
    end = start + length - 1
    return any(ranges_overlap(start, end, byte_range) for byte_range in ranges)


def first_changed_record(start: int, record_size: int, count: int, ranges: list[ByteRange]) -> int | None:
    for slot in range(count):
        offset = start + slot * record_size
        if range_changed(offset, record_size, ranges):
            return slot
    return None


def hex_bytes(data: bytes) -> str:
    return data.hex(" ")


def bounded_hex(data: bytes, byte_range: ByteRange, limit: int = 16) -> str:
    sample = data[byte_range.start : min(byte_range.end + 1, byte_range.start + limit)]
    suffix = "" if byte_range.length <= limit else " ..."
    return hex_bytes(sample) + suffix


def ascii_view(data: bytes) -> str:
    return "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in data)


def printable_ascii_name(raw_name: bytes) -> tuple[bool, str]:
    stripped = raw_name.split(b"\x00", 1)[0].rstrip(b" ")
    if not stripped:
        return False, ""
    printable = set(bytes(string.printable, "ascii"))
    if all(byte in printable and byte not in b"\r\n\t\x0b\x0c" for byte in stripped):
        return True, stripped.decode("ascii", errors="replace")
    return False, ""


def decode_tg_record(data: bytes, offset: int, slot: int) -> TgRecord:
    record = data[offset : offset + TG_RECORD_SIZE]
    name = record[TG_NAME_START:TG_NAME_END_EXCLUSIVE]
    name_is_printable, name_ascii = printable_ascii_name(name)
    numeric_raw = int.from_bytes(
        record[TG_NUMBER_START : TG_NUMBER_START + TG_NUMBER_SIZE], "little"
    )
    numeric_decoded = numeric_raw ^ TG_NUMBER_XOR
    uniform = len(set(record)) == 1
    name_has_content = len(set(name)) > 1 or (name and name[0] not in {0x00, 0xFF})
    numeric_has_content = len(set(record[TG_NUMBER_START : TG_NUMBER_START + TG_NUMBER_SIZE])) > 1
    apparent_valid = (
        not uniform
        and 1 <= numeric_decoded <= 65535
        and (name_is_printable or name_has_content)
        and numeric_has_content
    )
    return TgRecord(
        slot=slot,
        offset=offset,
        name_hex=hex_bytes(name),
        name_ascii=name_ascii if name_ascii else ascii_view(name),
        numeric_raw=numeric_raw,
        numeric_decoded=numeric_decoded,
        uniform=uniform,
        apparent_valid=apparent_valid,
    )


def scan_tg_region(data: bytes, start: int, ranges: list[ByteRange]) -> TgScan:
    records: list[TgRecord] = []
    for slot in range(TG_RECORD_COUNT):
        offset = start + slot * TG_RECORD_SIZE
        if offset + TG_RECORD_SIZE > len(data):
            break
        records.append(decode_tg_record(data, offset, slot))
    non_uniform = [record for record in records if not record.uniform]
    apparent = [record for record in records if record.apparent_valid]
    return TgScan(
        start=start,
        non_uniform_count=len(non_uniform),
        apparent_valid_count=len(apparent),
        first_apparent_valid=apparent[0] if apparent else None,
        first_changed_record=first_changed_record(start, TG_RECORD_SIZE, len(records), ranges),
        changed=range_changed(start, TG_RECORD_SIZE * TG_RECORD_COUNT, ranges),
    )


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


def record_label(record: TgRecord | None) -> str:
    if record is None:
        return "none"
    return (
        f"slot {record.slot} @ 0x{record.offset:08x}; "
        f"name_hex={record.name_hex}; name_ascii={record.name_ascii!r}; "
        f"num_raw=0x{record.numeric_raw:04x}; num_xor5151={record.numeric_decoded}"
    )


def changed_record_label(slot: int | None, start: int) -> str:
    if slot is None:
        return "none"
    return f"slot {slot} @ 0x{start + slot * TG_RECORD_SIZE:08x}"


def nearby_ranges(
    ranges: list[ByteRange],
    data_before: bytes,
    data_after: bytes,
    center: int,
    window: int,
) -> list[list[object]]:
    start = max(0, center - window)
    end = center + window - 1
    rows: list[list[object]] = []
    for byte_range in ranges:
        if not ranges_overlap(start, end, byte_range):
            continue
        rows.append(
            [
                f"0x{byte_range.start:08x}",
                f"0x{byte_range.end:08x}",
                byte_range.length,
                bounded_hex(data_before, byte_range),
                bounded_hex(data_after, byte_range),
            ]
        )
    return rows


def render_experiment(
    baseline_path: Path,
    experiment_path: Path,
    baseline: bytes,
    experiment: bytes,
    header_size: int,
    window: int,
) -> str:
    mask, mask_count, payload_compared = dominant_payload_xor(baseline, experiment, header_size)
    normalized = normalized_right(baseline, experiment, header_size, mask)
    compare_len = min(len(baseline), len(experiment))
    ranges = changed_ranges(baseline[:compare_len], normalized)
    changed_bytes = sum(byte_range.length for byte_range in ranges)
    mask_text = "none"
    if mask is not None:
        percent = mask_count / payload_compared * 100.0 if payload_compared else 0.0
        mask_text = f"0x{mask:02x} ({mask_count}/{payload_compared}, {percent:.2f}%)"

    tg_scans = [
        scan_tg_region(normalized, BLANK_TG_START, ranges),
        scan_tg_region(normalized, TRAVEL_TG_START, ranges),
    ]
    known_areas = [
        ("channel area around 0x5E80", CHANNEL_START, f"channel start; stride 0x{CHANNEL_STRIDE:x}"),
        (
            "individual ID area around 0x11D80",
            INDIVIDUAL_ID_START,
            f"blank-layout individual ID start; record size {INDIVIDUAL_ID_RECORD_SIZE}",
        ),
        ("TG blank-layout area around 0x14940", BLANK_TG_START, "blank-layout TG candidate"),
        ("TG travel-layout area around 0x14F80", TRAVEL_TG_START, "travel-layout TG candidate"),
    ]

    lines: list[str] = [
        f"## `{experiment_path}`",
        "",
        "### File-Level Evidence",
        "",
    ]
    lines.extend(
        markdown_table(
            ["Baseline", "Experiment", "Baseline Size", "Experiment Size", "Dominant XOR", "Diff Bytes", "Diff Ranges"],
            [
                [
                    baseline_path,
                    experiment_path,
                    len(baseline),
                    len(experiment),
                    mask_text,
                    changed_bytes,
                    len(ranges),
                ]
            ],
        )
    )
    lines.extend(["", "### Candidate TG Region Scan", ""])
    lines.extend(
        markdown_table(
            [
                "Start",
                "TG Region Changed",
                "Non-Uniform Records",
                "Apparent Valid TG Records",
                "First Apparent Valid",
                "First Changed Record",
            ],
            [
                [
                    f"0x{scan.start:08x}",
                    "yes" if scan.changed else "no",
                    scan.non_uniform_count,
                    scan.apparent_valid_count,
                    record_label(scan.first_apparent_valid),
                    changed_record_label(scan.first_changed_record, scan.start),
                ]
                for scan in tg_scans
            ],
        )
    )

    lines.extend(["", "### Nearby Changed Ranges", ""])
    for title, center, note in known_areas:
        lines.extend(
            [
                f"#### {title}",
                "",
                f"- Window: 0x{max(0, center - window):08x}..0x{center + window - 1:08x}",
                f"- Note: {note}",
                "",
            ]
        )
        lines.extend(
            markdown_table(
                ["Start", "End", "Length", "Baseline Hex", "Experiment Normalized Hex"],
                nearby_ranges(ranges, baseline, normalized, center, window),
            )
        )
        lines.append("")

    lines.extend(
        [
            "### Evidence-Only Summary",
            "",
            f"- Normalized differing bytes: {changed_bytes} across {len(ranges)} ranges.",
            (
                "- Candidate TG region 0x14940 changed: "
                f"{'yes' if tg_scans[0].changed else 'no'}; "
                f"candidate TG region 0x14F80 changed: {'yes' if tg_scans[1].changed else 'no'}."
            ),
            "- No layout algorithm is inferred from this experiment by this tool.",
            "",
        ]
    )
    return "\n".join(lines)


def render_report(args: argparse.Namespace, baseline: bytes, experiments: list[tuple[Path, bytes]]) -> str:
    lines: list[str] = [
        "# Layout Trigger Check",
        "",
        "Read-only diagnostic. This report normalizes experiment DAT files against a baseline and reports evidence only.",
        "",
        "Apparent valid TG heuristic: non-uniform 32-byte record, non-empty/non-uniform name field at +0x01..+0x0E, and +0x13..+0x14 little-endian XOR 0x5151 decodes to 1..65535. This is a diagnostic heuristic, not proof of layout semantics.",
        "",
    ]
    for experiment_path, experiment in experiments:
        lines.append(
            render_experiment(
                args.baseline,
                experiment_path,
                baseline,
                experiment,
                args.header_size,
                args.window,
            )
        )
    lines.extend(
        [
            "## Overall Evidence-Only Summary",
            "",
            "- This tool reports observed normalized byte differences and candidate table-region effects only.",
            "- It does not infer a layout trigger algorithm and does not modify importer behavior.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        validate_args(args)
        baseline = args.baseline.expanduser().read_bytes()
        experiments = [
            (path, path.expanduser().read_bytes())
            for path in args.experiments
        ]
        print(render_report(args, baseline, experiments))
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
