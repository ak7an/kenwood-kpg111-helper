#!/usr/bin/env python3
"""Build observation-only reports for KPG111 channel frequency datasets."""

from __future__ import annotations

import argparse
import csv
import glob
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.metadata import dominant_payload_xor, normalize_payload


DEFAULT_INPUT_GLOB = "experiments/**/*.dat"
DEFAULT_CSV = "frequency_dataset.csv"
DEFAULT_REPORT = "frequency_dataset_report.md"
CHANNEL_TABLE_START = 0x5E80
CHANNEL_STRIDE = 0x40
CHANNEL_NUMBER = 2
RECORD_SIZE = 0x40
FREQUENCY_SIZE = 3
RX_FREQUENCY_OFFSET = 0x05
TX_FREQUENCY_OFFSET = 0x09
MASK24 = 0xFFFFFF


@dataclass(frozen=True)
class FrequencyFieldAnalysis:
    raw: bytes
    big_endian: int
    little_endian: int
    bit_reversed_bytes: bytes
    bit_reversed_big_endian: int
    bit_reversed_little_endian: int
    byte_swap_021: bytes
    byte_swap_102: bytes
    byte_swap_120: bytes
    byte_swap_201: bytes
    byte_swap_210: bytes
    ones_complement: bytes
    ones_complement_big_endian: int
    ones_complement_little_endian: int
    gray_big_decode: int
    gray_little_decode: int


@dataclass(frozen=True)
class DatasetSample:
    path: Path
    frequency_text: str
    frequency_hz: int | None
    xor_mask: int
    xor_ratio: float
    rx: FrequencyFieldAnalysis
    tx: FrequencyFieldAnalysis


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze KPG111 channel frequency experiment DAT files without decoding formulas."
    )
    parser.add_argument(
        "--input-glob",
        default=DEFAULT_INPUT_GLOB,
        help=f"Input DAT glob (default: {DEFAULT_INPUT_GLOB})",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        help="Reference DAT for dominant payload XOR detection (default: first sorted input DAT)",
    )
    parser.add_argument(
        "--channel",
        type=int,
        default=CHANNEL_NUMBER,
        help=f"Channel number to extract, 1-based (default: {CHANNEL_NUMBER})",
    )
    parser.add_argument(
        "--start",
        type=parse_int,
        default=CHANNEL_TABLE_START,
        help=f"Channel table start offset (default: 0x{CHANNEL_TABLE_START:x})",
    )
    parser.add_argument(
        "--stride",
        type=parse_int,
        default=CHANNEL_STRIDE,
        help=f"Channel record stride (default: 0x{CHANNEL_STRIDE:x})",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(DEFAULT_CSV),
        help=f"CSV output path (default: {DEFAULT_CSV})",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(DEFAULT_REPORT),
        help=f"Markdown report output path (default: {DEFAULT_REPORT})",
    )
    return parser.parse_args()


def parse_int(value: str) -> int:
    try:
        return int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer: {value!r}") from exc


def input_paths(pattern: str) -> list[Path]:
    return [Path(path) for path in sorted(glob.glob(pattern, recursive=True))]


def parse_frequency_from_filename(path: Path) -> tuple[str, int | None]:
    matches = re.findall(r"\d+(?:\.\d+)?", path.stem)
    if not matches:
        return "", None
    token = matches[-1]
    if "." in token:
        mhz_text = token
    elif len(token) > 3:
        mhz_text = f"{token[:-3]}.{token[-3:]}"
    else:
        mhz_text = token
    whole, _dot, fractional = mhz_text.partition(".")
    frequency_hz = int(whole) * 1_000_000 + int((fractional + "000000")[:6])
    return mhz_text, frequency_hz


def bit_reverse_byte(value: int) -> int:
    result = 0
    for _index in range(8):
        result = (result << 1) | (value & 1)
        value >>= 1
    return result


def bit_reverse_bytes(data: bytes) -> bytes:
    return bytes(bit_reverse_byte(byte) for byte in data)


def gray_decode(value: int) -> int:
    value &= MASK24
    shift = 1
    while shift < 24:
        value ^= value >> shift
        shift <<= 1
    return value & MASK24


def byte_swap(data: bytes, order: tuple[int, int, int]) -> bytes:
    return bytes(data[index] for index in order)


def analyze_field(raw: bytes) -> FrequencyFieldAnalysis:
    if len(raw) != FREQUENCY_SIZE:
        raise ValueError("frequency field must be exactly 3 bytes")
    bit_reversed = bit_reverse_bytes(raw)
    ones = bytes(byte ^ 0xFF for byte in raw)
    return FrequencyFieldAnalysis(
        raw=raw,
        big_endian=int.from_bytes(raw, "big"),
        little_endian=int.from_bytes(raw, "little"),
        bit_reversed_bytes=bit_reversed,
        bit_reversed_big_endian=int.from_bytes(bit_reversed, "big"),
        bit_reversed_little_endian=int.from_bytes(bit_reversed, "little"),
        byte_swap_021=byte_swap(raw, (0, 2, 1)),
        byte_swap_102=byte_swap(raw, (1, 0, 2)),
        byte_swap_120=byte_swap(raw, (1, 2, 0)),
        byte_swap_201=byte_swap(raw, (2, 0, 1)),
        byte_swap_210=byte_swap(raw, (2, 1, 0)),
        ones_complement=ones,
        ones_complement_big_endian=int.from_bytes(ones, "big"),
        ones_complement_little_endian=int.from_bytes(ones, "little"),
        gray_big_decode=gray_decode(int.from_bytes(raw, "big")),
        gray_little_decode=gray_decode(int.from_bytes(raw, "little")),
    )


def channel_record(data: bytes, channel: int, start: int, stride: int) -> bytes:
    if channel < 1:
        raise ValueError("--channel must be >= 1")
    if start < 0:
        raise ValueError("--start must be >= 0")
    if stride <= 0:
        raise ValueError("--stride must be > 0")
    offset = start + ((channel - 1) * stride)
    record = data[offset : offset + RECORD_SIZE]
    if len(record) != RECORD_SIZE:
        raise ValueError(
            f"channel {channel} record at 0x{offset:08x} is incomplete: "
            f"expected 0x{RECORD_SIZE:x} bytes, found 0x{len(record):x}"
        )
    return record


def analyze_dat(
    path: Path,
    baseline_data: bytes,
    channel: int = CHANNEL_NUMBER,
    start: int = CHANNEL_TABLE_START,
    stride: int = CHANNEL_STRIDE,
) -> DatasetSample:
    data = path.read_bytes()
    xor_mask, xor_ratio = dominant_payload_xor(baseline_data, data)
    normalized = normalize_payload(data, xor_mask)
    record = channel_record(normalized, channel, start, stride)
    rx = record[RX_FREQUENCY_OFFSET : RX_FREQUENCY_OFFSET + FREQUENCY_SIZE]
    tx = record[TX_FREQUENCY_OFFSET : TX_FREQUENCY_OFFSET + FREQUENCY_SIZE]
    frequency_text, frequency_hz = parse_frequency_from_filename(path)
    return DatasetSample(
        path=path,
        frequency_text=frequency_text,
        frequency_hz=frequency_hz,
        xor_mask=xor_mask,
        xor_ratio=xor_ratio,
        rx=analyze_field(rx),
        tx=analyze_field(tx),
    )


def analyze_dataset(
    paths: list[Path],
    baseline_path: Path | None = None,
    channel: int = CHANNEL_NUMBER,
    start: int = CHANNEL_TABLE_START,
    stride: int = CHANNEL_STRIDE,
) -> list[DatasetSample]:
    if not paths:
        raise ValueError("no input DAT files matched")
    baseline = baseline_path or paths[0]
    baseline_data = baseline.read_bytes()
    samples = [
        analyze_dat(path, baseline_data, channel=channel, start=start, stride=stride)
        for path in paths
    ]
    return sorted(samples, key=lambda sample: (sample.frequency_hz is None, sample.frequency_hz or 0, str(sample.path)))


def fmt_bytes(data: bytes) -> str:
    return data.hex(" ")


def fmt_int(value: int | None) -> str:
    return "" if value is None else str(value)


def hamming_distance(left: bytes, right: bytes) -> int:
    if len(left) != len(right):
        raise ValueError("byte sequences must be the same length")
    return sum((left_byte ^ right_byte).bit_count() for left_byte, right_byte in zip(left, right))


def bit_transition_summary(left: bytes, right: bytes) -> str:
    transitions = []
    for byte_index, (left_byte, right_byte) in enumerate(zip(left, right)):
        changed_bits = [
            str(bit)
            for bit in range(8)
            if ((left_byte ^ right_byte) >> bit) & 1
        ]
        transitions.append(f"byte{byte_index}: {' '.join(changed_bits) if changed_bits else 'none'}")
    return "; ".join(transitions)


def field_values(samples: list[DatasetSample], field: str, byte_index: int) -> list[int]:
    return [getattr(sample, field).raw[byte_index] for sample in samples]


def monotonic_regions(samples: list[DatasetSample], field: str, byte_index: int) -> list[str]:
    values = field_values(samples, field, byte_index)
    if len(values) < 2:
        return []
    regions = []
    start = 0
    direction = 0
    for index in range(1, len(values)):
        delta = values[index] - values[index - 1]
        new_direction = 1 if delta > 0 else -1 if delta < 0 else 0
        if direction == 0:
            direction = new_direction
            continue
        if new_direction == 0 or new_direction == direction:
            continue
        if index - 1 > start:
            regions.append(region_text(samples, start, index - 1, direction))
        start = index - 1
        direction = new_direction
    if direction != 0 and len(values) - 1 > start:
        regions.append(region_text(samples, start, len(values) - 1, direction))
    return regions


def region_text(samples: list[DatasetSample], start: int, end: int, direction: int) -> str:
    direction_text = "increasing" if direction > 0 else "decreasing"
    return f"{samples[start].frequency_text or samples[start].path.name}->{samples[end].frequency_text or samples[end].path.name} {direction_text}"


def duplicate_byte_values(samples: list[DatasetSample], field: str, byte_index: int) -> list[str]:
    locations: dict[int, list[str]] = {}
    for sample in samples:
        value = getattr(sample, field).raw[byte_index]
        locations.setdefault(value, []).append(sample.frequency_text or sample.path.name)
    return [
        f"0x{value:02x}: {', '.join(labels)}"
        for value, labels in sorted(locations.items())
        if len(labels) > 1
    ]


def csv_rows(samples: list[DatasetSample]) -> list[dict[str, str]]:
    rows = []
    for sample in samples:
        row = {
            "filename": str(sample.path),
            "frequency": sample.frequency_text,
            "frequency_hz": fmt_int(sample.frequency_hz),
            "xor_mask": f"0x{sample.xor_mask:02x}",
            "xor_ratio": f"{sample.xor_ratio:.6f}",
        }
        for prefix, field in (("rx", sample.rx), ("tx", sample.tx)):
            row.update(field_csv_values(prefix, field))
        rows.append(row)
    return rows


def field_csv_values(prefix: str, field: FrequencyFieldAnalysis) -> dict[str, str]:
    return {
        f"{prefix}0": str(field.raw[0]),
        f"{prefix}1": str(field.raw[1]),
        f"{prefix}2": str(field.raw[2]),
        f"{prefix}_hex": fmt_bytes(field.raw),
        f"{prefix}_big_endian": str(field.big_endian),
        f"{prefix}_little_endian": str(field.little_endian),
        f"{prefix}_bit_reversed_hex": fmt_bytes(field.bit_reversed_bytes),
        f"{prefix}_bit_reversed_big_endian": str(field.bit_reversed_big_endian),
        f"{prefix}_bit_reversed_little_endian": str(field.bit_reversed_little_endian),
        f"{prefix}_byte_swap_021": fmt_bytes(field.byte_swap_021),
        f"{prefix}_byte_swap_102": fmt_bytes(field.byte_swap_102),
        f"{prefix}_byte_swap_120": fmt_bytes(field.byte_swap_120),
        f"{prefix}_byte_swap_201": fmt_bytes(field.byte_swap_201),
        f"{prefix}_byte_swap_210": fmt_bytes(field.byte_swap_210),
        f"{prefix}_ones_complement_hex": fmt_bytes(field.ones_complement),
        f"{prefix}_ones_complement_big_endian": str(field.ones_complement_big_endian),
        f"{prefix}_ones_complement_little_endian": str(field.ones_complement_little_endian),
        f"{prefix}_gray_big_decode": str(field.gray_big_decode),
        f"{prefix}_gray_little_decode": str(field.gray_little_decode),
    }


def write_csv(path: Path, samples: list[DatasetSample]) -> None:
    rows = csv_rows(samples)
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _header in headers) + " |",
    ]
    if not rows:
        lines.append("| " + " | ".join("none" for _header in headers) + " |")
        return lines
    lines.extend("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |" for row in rows)
    return lines


def render_report(samples: list[DatasetSample], baseline_path: Path, channel: int, start: int, stride: int) -> str:
    lines = [
        "# Frequency Dataset Analysis",
        "",
        "Read-only observation report. No frequency decoding is performed.",
        "",
        f"- Baseline for payload XOR normalization: `{baseline_path}`",
        f"- Channel: {channel}",
        f"- Channel table start: `0x{start:08x}`",
        f"- Channel stride: `0x{stride:x}`",
        "",
        "## Dataset",
    ]
    lines.extend(render_dataset_table(samples))
    lines.extend(["", "## Byte Position Analysis"])
    for field in ("rx", "tx"):
        lines.extend(render_byte_position_analysis(samples, field.upper(), field))
        lines.append("")
    lines.extend(["## Transform Observations"])
    lines.extend(render_transform_table(samples))
    lines.extend(["", "## Adjacent Transitions"])
    lines.extend(render_transition_table(samples))
    lines.extend(["", "## Observations", "- No encoding formula determined."])
    return "\n".join(lines)


def render_dataset_table(samples: list[DatasetSample]) -> list[str]:
    rows = [
        [
            sample.path.name,
            sample.frequency_text,
            fmt_bytes(sample.rx.raw),
            fmt_bytes(sample.tx.raw),
            str(sample.rx.big_endian),
            str(sample.rx.little_endian),
            str(sample.tx.big_endian),
            str(sample.tx.little_endian),
            f"0x{sample.xor_mask:02x}",
        ]
        for sample in samples
    ]
    return markdown_table(
        [
            "Filename",
            "Detected frequency",
            "RX bytes",
            "TX bytes",
            "RX big endian",
            "RX little endian",
            "TX big endian",
            "TX little endian",
            "XOR mask",
        ],
        rows,
    )


def render_byte_position_analysis(samples: list[DatasetSample], title: str, field: str) -> list[str]:
    lines = [f"### {title}", ""]
    for byte_index in range(FREQUENCY_SIZE):
        rows = []
        previous_value: int | None = None
        for sample in samples:
            value = getattr(sample, field).raw[byte_index]
            delta = "" if previous_value is None else f"{value - previous_value:+d}"
            rows.append([sample.frequency_text, f"0x{value:02x}", delta])
            previous_value = value
        lines.extend([f"#### byte{byte_index}", ""])
        lines.extend(markdown_table(["frequency", f"byte{byte_index}", "delta from previous sample"], rows))
        regions = monotonic_regions(samples, field, byte_index)
        duplicates = duplicate_byte_values(samples, field, byte_index)
        lines.append("")
        lines.append(f"- monotonic regions: {'; '.join(regions) if regions else 'none observed'}")
        lines.append(f"- duplicate byte values: {'; '.join(duplicates) if duplicates else 'none observed'}")
        lines.append("")
    return lines


def render_transform_table(samples: list[DatasetSample]) -> list[str]:
    rows = []
    for sample in samples:
        for label, field in (("RX", sample.rx), ("TX", sample.tx)):
            rows.append(
                [
                    sample.frequency_text,
                    label,
                    fmt_bytes(field.raw),
                    str(field.big_endian),
                    str(field.little_endian),
                    fmt_bytes(field.bit_reversed_bytes),
                    fmt_bytes(field.byte_swap_021),
                    fmt_bytes(field.byte_swap_102),
                    fmt_bytes(field.byte_swap_120),
                    fmt_bytes(field.byte_swap_201),
                    fmt_bytes(field.byte_swap_210),
                    fmt_bytes(field.ones_complement),
                    str(field.gray_big_decode),
                    str(field.gray_little_decode),
                ]
            )
    return markdown_table(
        [
            "frequency",
            "field",
            "bytes",
            "big endian",
            "little endian",
            "bit-reversed bytes",
            "byte swap 021",
            "byte swap 102",
            "byte swap 120",
            "byte swap 201",
            "byte swap 210",
            "ones-complement",
            "Gray big decode",
            "Gray little decode",
        ],
        rows,
    )


def render_transition_table(samples: list[DatasetSample]) -> list[str]:
    rows = []
    for previous, current in zip(samples, samples[1:]):
        rows.append(
            [
                f"{previous.frequency_text}->{current.frequency_text}",
                str(hamming_distance(previous.rx.raw, current.rx.raw)),
                bit_transition_summary(previous.rx.raw, current.rx.raw),
                str(hamming_distance(previous.tx.raw, current.tx.raw)),
                bit_transition_summary(previous.tx.raw, current.tx.raw),
            ]
        )
    return markdown_table(
        ["frequency step", "RX Hamming distance", "RX bit transitions", "TX Hamming distance", "TX bit transitions"],
        rows,
    )


def main() -> int:
    args = parse_args()
    try:
        paths = input_paths(args.input_glob)
        if not paths:
            raise ValueError(f"no input DAT files matched: {args.input_glob}")
        baseline_path = args.baseline or paths[0]
        samples = analyze_dataset(
            paths,
            baseline_path=baseline_path,
            channel=args.channel,
            start=args.start,
            stride=args.stride,
        )
        write_csv(args.csv, samples)
        args.report.write_text(
            render_report(samples, baseline_path, args.channel, args.start, args.stride),
            encoding="utf-8",
        )
        print(f"Wrote {args.csv}")
        print(f"Wrote {args.report}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
