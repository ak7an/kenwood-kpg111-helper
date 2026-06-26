#!/usr/bin/env python3
"""Analyze controlled Line 2 frequency sweep DAT files without inferring encoding."""

from __future__ import annotations

import argparse
import glob
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.metadata import dominant_payload_xor, normalize_payload


DEFAULT_INPUT_GLOB = "~/experiments/Line2_RX_*.dat"
DEFAULT_BASELINE = "~/AK7AN_Channel_Baseline.dat"
CHANNEL_TABLE_START = 0x5E80
CHANNEL_STRIDE = 0x40
CHANNEL_NUMBER = 2
RECORD_SIZE = 0x40
FREQUENCY_SIZE = 3
RX_FREQUENCY_OFFSET = 0x05
TX_FREQUENCY_OFFSET = 0x09


@dataclass(frozen=True)
class SweepSample:
    path: Path
    frequency_text: str
    frequency_hz: int
    xor_mask: int
    xor_ratio: float
    rx_bytes: bytes
    tx_bytes: bytes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze controlled Line 2 RX frequency sweep DAT files."
    )
    parser.add_argument(
        "--input-glob",
        default=DEFAULT_INPUT_GLOB,
        help=f"Input DAT glob (default: {DEFAULT_INPUT_GLOB})",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=Path(DEFAULT_BASELINE),
        help=f"Reference baseline DAT (default: {DEFAULT_BASELINE})",
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
    return parser.parse_args()


def parse_int(value: str) -> int:
    try:
        return int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer: {value!r}") from exc


def expand_path(path: Path | str) -> Path:
    return Path(path).expanduser()


def input_paths(pattern: str) -> list[Path]:
    return [Path(path) for path in sorted(glob.glob(str(expand_path(pattern))))]


def parse_frequency_from_filename(path: Path) -> tuple[str, int]:
    matches = re.findall(r"\d+(?:\.\d+)?", path.stem)
    if not matches:
        raise ValueError(f"cannot parse frequency from filename: {path.name}")

    token = matches[-1]
    if "." in token:
        mhz_text = token
    elif len(token) > 3:
        mhz_text = f"{token[:-3]}.{token[-3:]}"
    else:
        mhz_text = token

    whole, dot, fractional = mhz_text.partition(".")
    frequency_text = mhz_text
    hz_fraction = ((fractional if fractional else "") + "000000")[:6]
    frequency_hz = int(whole) * 1_000_000 + int(hz_fraction)
    return frequency_text, frequency_hz


def xor_bytes(left: bytes, right: bytes) -> bytes:
    if len(left) != len(right):
        raise ValueError("byte sequences must be the same length")
    return bytes(left_byte ^ right_byte for left_byte, right_byte in zip(left, right))


def fmt_bytes(data: bytes) -> str:
    return data.hex(" ")


def fmt_xor(previous: bytes | None, current: bytes) -> str:
    if previous is None:
        return ""
    return fmt_bytes(xor_bytes(previous, current))


def fmt_delta(value: int | None) -> str:
    if value is None:
        return ""
    return f"{value:+d}"


def fmt_delta_series(values: list[int | None]) -> str:
    return ", ".join("start" if value is None else fmt_delta(value) for value in values)


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


def frequency_bytes(record: bytes) -> tuple[bytes, bytes]:
    rx = record[RX_FREQUENCY_OFFSET : RX_FREQUENCY_OFFSET + FREQUENCY_SIZE]
    tx = record[TX_FREQUENCY_OFFSET : TX_FREQUENCY_OFFSET + FREQUENCY_SIZE]
    return rx, tx


def analyze_file(
    baseline: bytes,
    path: Path,
    channel: int = CHANNEL_NUMBER,
    start: int = CHANNEL_TABLE_START,
    stride: int = CHANNEL_STRIDE,
) -> SweepSample:
    data = path.read_bytes()
    mask, ratio = dominant_payload_xor(baseline, data)
    normalized = normalize_payload(data, mask)
    record = channel_record(normalized, channel, start, stride)
    rx, tx = frequency_bytes(record)
    frequency_text, frequency_hz = parse_frequency_from_filename(path)
    return SweepSample(
        path=path,
        frequency_text=frequency_text,
        frequency_hz=frequency_hz,
        xor_mask=mask,
        xor_ratio=ratio,
        rx_bytes=rx,
        tx_bytes=tx,
    )


def analyze_sweep(
    baseline_path: Path,
    paths: list[Path],
    channel: int = CHANNEL_NUMBER,
    start: int = CHANNEL_TABLE_START,
    stride: int = CHANNEL_STRIDE,
) -> list[SweepSample]:
    baseline = baseline_path.read_bytes()
    samples = [
        analyze_file(baseline, path, channel=channel, start=start, stride=stride)
        for path in paths
    ]
    return sorted(samples, key=lambda sample: (sample.frequency_hz, str(sample.path)))


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


def byte_deltas(samples: list[SweepSample], field: str, byte_index: int) -> list[int | None]:
    deltas: list[int | None] = [None]
    for previous, current in zip(samples, samples[1:]):
        previous_bytes = getattr(previous, field)
        current_bytes = getattr(current, field)
        deltas.append(current_bytes[byte_index] - previous_bytes[byte_index])
    return deltas


def is_monotonic(values: list[int]) -> bool:
    return len(values) <= 1 or all(left <= right for left, right in zip(values, values[1:])) or all(
        left >= right for left, right in zip(values, values[1:])
    )


def rollover_points(samples: list[SweepSample], field: str, byte_index: int) -> list[str]:
    points = []
    for previous, current in zip(samples, samples[1:]):
        previous_value = getattr(previous, field)[byte_index]
        current_value = getattr(current, field)[byte_index]
        if current_value < previous_value:
            points.append(f"{previous.frequency_text}->{current.frequency_text}: decrease")
    return points


def repeated_patterns(samples: list[SweepSample], field: str) -> list[str]:
    seen: dict[bytes, list[str]] = {}
    for sample in samples:
        seen.setdefault(getattr(sample, field), []).append(sample.frequency_text)
    return [
        f"{fmt_bytes(value)} at {', '.join(frequencies)}"
        for value, frequencies in sorted(seen.items())
        if len(frequencies) > 1
    ]


def observations_for_field(samples: list[SweepSample], field: str, label: str) -> list[str]:
    lines = [f"### {label} Bytes", ""]
    if not samples:
        lines.append("- no samples")
        return lines

    repeats = repeated_patterns(samples, field)
    lines.append("- repeated patterns: " + ("; ".join(repeats) if repeats else "none observed"))

    for index in range(FREQUENCY_SIZE):
        values = [getattr(sample, field)[index] for sample in samples]
        unique = sorted(set(values))
        deltas = [
            delta for delta in byte_deltas(samples, field, index)[1:]
            if delta is not None
        ]
        rollovers = rollover_points(samples, field, index)
        constant = len(unique) == 1
        monotonic = is_monotonic(values)
        lines.append(
            f"- byte{index}: values {', '.join(f'0x{value:02x}' for value in values)}; "
            f"deltas {', '.join(fmt_delta(delta) for delta in deltas) if deltas else 'none'}; "
            f"constant {'yes' if constant else 'no'}; "
            f"monotonic {'yes' if monotonic else 'no'}; "
            f"rollover points {', '.join(rollovers) if rollovers else 'none observed'}"
        )
    return lines


def render_report(
    baseline_path: Path,
    samples: list[SweepSample],
    channel: int = CHANNEL_NUMBER,
    start: int = CHANNEL_TABLE_START,
    stride: int = CHANNEL_STRIDE,
) -> str:
    lines = [
        "# Frequency Sweep Report",
        "",
        "Observation-only report. No encoding formula is inferred.",
        "",
        f"- Baseline: `{baseline_path}`",
        f"- Channel: {channel}",
        f"- Channel table start: `0x{start:08x}`",
        f"- Channel stride: `0x{stride:x}`",
        "",
        "## Samples",
    ]

    sample_rows = []
    previous_rx: bytes | None = None
    previous_tx: bytes | None = None
    for sample in samples:
        sample_rows.append(
            [
                sample.frequency_text,
                fmt_bytes(sample.rx_bytes),
                fmt_bytes(sample.tx_bytes),
                fmt_xor(previous_rx, sample.rx_bytes),
                fmt_xor(previous_tx, sample.tx_bytes),
            ]
        )
        previous_rx = sample.rx_bytes
        previous_tx = sample.tx_bytes
    lines.extend(markdown_table(["Frequency", "RX bytes", "TX bytes", "RX xor previous", "TX xor previous"], sample_rows))

    lines.extend(["", "## Detected Payload XOR Masks"])
    mask_rows = [
        [
            sample.frequency_text,
            sample.path.name,
            f"0x{sample.xor_mask:02x}",
            f"{sample.xor_ratio:.4%}",
        ]
        for sample in samples
    ]
    lines.extend(markdown_table(["Frequency", "File", "Dominant payload XOR mask", "Ratio"], mask_rows))

    lines.extend(["", "## Adjacent Byte Deltas"])
    delta_rows = []
    for index in range(FREQUENCY_SIZE):
        rx_deltas = byte_deltas(samples, "rx_bytes", index)
        tx_deltas = byte_deltas(samples, "tx_bytes", index)
        delta_rows.append(
            [
                f"byte{index}",
                fmt_delta_series(rx_deltas),
                fmt_delta_series(tx_deltas),
            ]
        )
    lines.extend(markdown_table(["Byte", "RX adjacent deltas", "TX adjacent deltas"], delta_rows))

    lines.extend(["", "## Observations"])
    lines.extend(observations_for_field(samples, "rx_bytes", "RX"))
    lines.append("")
    lines.extend(observations_for_field(samples, "tx_bytes", "TX"))
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        baseline = expand_path(args.baseline)
        paths = input_paths(args.input_glob)
        if not paths:
            raise ValueError(f"no input DAT files matched: {args.input_glob}")
        samples = analyze_sweep(
            baseline,
            paths,
            channel=args.channel,
            start=args.start,
            stride=args.stride,
        )
        print(render_report(baseline, samples, channel=args.channel, start=args.start, stride=args.stride))
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
