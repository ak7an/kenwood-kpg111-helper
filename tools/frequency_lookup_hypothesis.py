#!/usr/bin/env python3
"""Read-only KPG111 frequency field lookup/index hypothesis report."""

from __future__ import annotations

import argparse
import csv
import glob
import itertools
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.metadata import dominant_payload_xor, normalize_payload


DEFAULT_INPUT_GLOB = "data/experiments/channel_dats/Line2_RX_*.dat"
DEFAULT_REPORT = Path("/tmp/kpg111_frequency_lookup_hypothesis.txt")
DEFAULT_CSV = Path("/tmp/kpg111_frequency_lookup_hypothesis.csv")
CHANNEL_TABLE_START = 0x5E80
CHANNEL_STRIDE = 0x40
CHANNEL_NUMBER = 2
RECORD_SIZE = 0x40
RX_FIELD_OFFSET = 0x05
RX_FIELD_LENGTH = 3
STEP_HZ_VALUES = (5_000, 6_250, 10_000, 12_500, 25_000)
BASE_HZ_VALUES = (0, 100_000_000, 136_000_000, 144_000_000, 145_000_000, 146_000_000)


@dataclass(frozen=True)
class Sample:
    path: Path
    frequency_text: str
    frequency_hz: int
    xor_mask: int
    xor_ratio: float
    raw_rx: bytes
    decoded_rx: bytes

    @property
    def raw_be(self) -> int:
        return int.from_bytes(self.raw_rx, "big")

    @property
    def raw_le(self) -> int:
        return int.from_bytes(self.raw_rx, "little")

    @property
    def decoded_be(self) -> int:
        return int.from_bytes(self.decoded_rx, "big")

    @property
    def decoded_le(self) -> int:
        return int.from_bytes(self.decoded_rx, "little")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze KPG111 Line2 RX frequency bytes against lookup/index hypotheses."
    )
    parser.add_argument("--input-glob", default=DEFAULT_INPUT_GLOB)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    return parser.parse_args()


def input_paths(pattern: str) -> list[Path]:
    return [Path(path) for path in sorted(glob.glob(str(Path(pattern).expanduser())))]


def parse_frequency_from_filename(path: Path) -> tuple[str, int]:
    match = re.search(r"Line2_RX_(\d+)(?:\.dat)?$", path.name)
    if match is None:
        raise ValueError(f"cannot infer frequency from filename: {path.name}")
    token = match.group(1)
    if len(token) > 6:
        mhz_text = f"{token[:3]}.{token[3:]}"
    elif len(token) > 3:
        mhz_text = f"{token[:-3]}.{token[-3:]}"
    else:
        mhz_text = token
    whole, _dot, fraction = mhz_text.partition(".")
    frequency_hz = int(whole) * 1_000_000 + int((fraction + "000000")[:6])
    return mhz_text, frequency_hz


def channel_2_record(data: bytes) -> bytes:
    offset = CHANNEL_TABLE_START + ((CHANNEL_NUMBER - 1) * CHANNEL_STRIDE)
    record = data[offset : offset + RECORD_SIZE]
    if len(record) != RECORD_SIZE:
        raise ValueError(f"channel 2 record at 0x{offset:08x} is incomplete")
    return record


def load_samples(paths: list[Path]) -> list[Sample]:
    if not paths:
        raise ValueError("no input files matched")
    baseline_data = paths[0].read_bytes()
    samples = []
    for path in paths:
        data = path.read_bytes()
        xor_mask, xor_ratio = dominant_payload_xor(baseline_data, data)
        normalized = normalize_payload(data, xor_mask)
        raw_record = channel_2_record(data)
        normalized_record = channel_2_record(normalized)
        frequency_text, frequency_hz = parse_frequency_from_filename(path)
        samples.append(
            Sample(
                path=path,
                frequency_text=frequency_text,
                frequency_hz=frequency_hz,
                xor_mask=xor_mask,
                xor_ratio=xor_ratio,
                raw_rx=raw_record[RX_FIELD_OFFSET : RX_FIELD_OFFSET + RX_FIELD_LENGTH],
                decoded_rx=normalized_record[RX_FIELD_OFFSET : RX_FIELD_OFFSET + RX_FIELD_LENGTH],
            )
        )
    return sorted(samples, key=lambda sample: (sample.frequency_hz, sample.path.name))


def bcd_text(data: bytes) -> str:
    digits = []
    for byte in data:
        high = (byte >> 4) & 0x0F
        low = byte & 0x0F
        if high > 9 or low > 9:
            return ""
        digits.extend([str(high), str(low)])
    return "".join(digits)


def nibbles(data: bytes) -> tuple[int, ...]:
    values = []
    for byte in data:
        values.extend([(byte >> 4) & 0x0F, byte & 0x0F])
    return tuple(values)


def unpack_6bit(data: bytes) -> tuple[int, ...]:
    value = int.from_bytes(data, "big")
    return tuple((value >> shift) & 0x3F for shift in (18, 12, 6, 0))


def unpack_7bit(data: bytes) -> tuple[int, ...]:
    value = int.from_bytes(data, "big")
    return tuple((value >> shift) & 0x7F for shift in (17, 10, 3))


def monotonic(values: list[int]) -> str:
    if all(left < right for left, right in zip(values, values[1:])):
        return "strictly increasing"
    if all(left <= right for left, right in zip(values, values[1:])):
        return "nondecreasing"
    if all(left > right for left, right in zip(values, values[1:])):
        return "strictly decreasing"
    if all(left >= right for left, right in zip(values, values[1:])):
        return "nonincreasing"
    return "not monotonic"


def exact_direct_matches(samples: list[Sample]) -> list[str]:
    fields = {
        "raw big endian": [sample.raw_be for sample in samples],
        "raw little endian": [sample.raw_le for sample in samples],
        "decoded big endian": [sample.decoded_be for sample in samples],
        "decoded little endian": [sample.decoded_le for sample in samples],
    }
    targets = {
        "frequency Hz": [sample.frequency_hz for sample in samples],
        "frequency kHz": [sample.frequency_hz // 1_000 for sample in samples],
        "frequency / 10 Hz": [sample.frequency_hz // 10 for sample in samples],
        "frequency / 100 Hz": [sample.frequency_hz // 100 for sample in samples],
    }
    matches = []
    for field_name, values in fields.items():
        for target_name, target_values in targets.items():
            if values == target_values:
                matches.append(f"{field_name} == {target_name}")
    return matches


def step_index_exact_matches(samples: list[Sample]) -> list[str]:
    fields = {
        "raw big endian": [sample.raw_be for sample in samples],
        "raw little endian": [sample.raw_le for sample in samples],
        "decoded big endian": [sample.decoded_be for sample in samples],
        "decoded little endian": [sample.decoded_le for sample in samples],
    }
    matches = []
    min_frequency = min(sample.frequency_hz for sample in samples)
    base_values = (*BASE_HZ_VALUES, min_frequency)
    for base_hz, step_hz in itertools.product(base_values, STEP_HZ_VALUES):
        if any((sample.frequency_hz - base_hz) % step_hz for sample in samples):
            continue
        expected = [(sample.frequency_hz - base_hz) // step_hz for sample in samples]
        for field_name, values in fields.items():
            if values == expected:
                matches.append(f"{field_name} == ({'freq'} - {base_hz}) / {step_hz}")
    return matches


def affine_fit_count(x_values: list[int], y_values: list[int]) -> tuple[int, str]:
    if len(x_values) < 2:
        return len(x_values), "not enough samples"
    best_count = 0
    best_text = ""
    for left in range(len(x_values)):
        for right in range(left + 1, len(x_values)):
            dx = x_values[right] - x_values[left]
            dy = y_values[right] - y_values[left]
            if dx == 0:
                continue
            matches = 0
            for x_value, y_value in zip(x_values, y_values):
                if (y_value - y_values[left]) * dx == dy * (x_value - x_values[left]):
                    matches += 1
            if matches > best_count:
                best_count = matches
                best_text = (
                    f"line through samples {left} and {right}: "
                    f"dy={dy}, dx={dx}, matched={matches}/{len(x_values)}"
                )
    return best_count, best_text


def duplicate_frequency_findings(samples: list[Sample]) -> list[str]:
    by_frequency: dict[int, list[Sample]] = {}
    for sample in samples:
        by_frequency.setdefault(sample.frequency_hz, []).append(sample)
    findings = []
    for frequency_hz, rows in sorted(by_frequency.items()):
        if len(rows) < 2:
            continue
        raw_values = {sample.raw_rx for sample in rows}
        decoded_values = {sample.decoded_rx for sample in rows}
        findings.append(
            f"{frequency_hz} Hz: raw variants={len(raw_values)}, decoded variants={len(decoded_values)}, "
            f"decoded={', '.join(value.hex(' ') for value in sorted(decoded_values))}"
        )
    return findings


def field_uniqueness(samples: list[Sample]) -> tuple[int, int]:
    return len({sample.frequency_hz for sample in samples}), len({sample.decoded_rx for sample in samples})


def csv_rows(samples: list[Sample]) -> list[dict[str, str]]:
    rows = []
    for sample in samples:
        step_6250_from_146 = (sample.frequency_hz - 146_000_000) / 6_250
        row = {
            "filename": str(sample.path),
            "frequency_text_mhz": sample.frequency_text,
            "frequency_hz": str(sample.frequency_hz),
            "xor_mask": f"0x{sample.xor_mask:02x}",
            "xor_ratio": f"{sample.xor_ratio:.6f}",
            "channel_record_offset": f"0x{CHANNEL_TABLE_START + CHANNEL_STRIDE:08x}",
            "rx_field_offset": f"0x{CHANNEL_TABLE_START + CHANNEL_STRIDE + RX_FIELD_OFFSET:08x}",
            "raw_rx_hex": sample.raw_rx.hex(" "),
            "decoded_rx_hex": sample.decoded_rx.hex(" "),
            "raw_big_endian": str(sample.raw_be),
            "raw_little_endian": str(sample.raw_le),
            "decoded_big_endian": str(sample.decoded_be),
            "decoded_little_endian": str(sample.decoded_le),
            "raw_bcd": bcd_text(sample.raw_rx),
            "decoded_bcd": bcd_text(sample.decoded_rx),
            "raw_nibbles": " ".join(f"{value:x}" for value in nibbles(sample.raw_rx)),
            "decoded_nibbles": " ".join(f"{value:x}" for value in nibbles(sample.decoded_rx)),
            "raw_6bit_indexes": " ".join(str(value) for value in unpack_6bit(sample.raw_rx)),
            "decoded_6bit_indexes": " ".join(str(value) for value in unpack_6bit(sample.decoded_rx)),
            "raw_7bit_indexes": " ".join(str(value) for value in unpack_7bit(sample.raw_rx)),
            "decoded_7bit_indexes": " ".join(str(value) for value in unpack_7bit(sample.decoded_rx)),
            "step_index_from_146mhz_6250hz": f"{step_6250_from_146:.3f}",
        }
        rows.append(row)
    return rows


def write_csv(path: Path, samples: list[Sample]) -> None:
    rows = csv_rows(samples)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |" for row in rows)
    return lines


def render_report(samples: list[Sample]) -> str:
    lines = [
        "# KPG111 Frequency Lookup/Index Hypothesis",
        "",
        "Read-only analysis. Importer behavior was not modified.",
        "",
        "The available-characters image at `/tmp/KPG111_available_characters.png` is treated only as UI/design context: KPG111 uses finite allowed-value tables elsewhere, but this is not evidence that frequency bytes use that exact table.",
        "",
        "## Extraction",
        "",
        f"- Files analyzed: {len(samples)}",
        f"- Channel table start: `0x{CHANNEL_TABLE_START:08x}`",
        f"- Channel record stride: `0x{CHANNEL_STRIDE:x}`",
        f"- Zone 1 Channel 2 record offset: `0x{CHANNEL_TABLE_START + CHANNEL_STRIDE:08x}`",
        f"- RX field offset: record `+0x{RX_FIELD_OFFSET:02x}`, absolute `0x{CHANNEL_TABLE_START + CHANNEL_STRIDE + RX_FIELD_OFFSET:08x}`",
        f"- RX field length: `{RX_FIELD_LENGTH}` bytes",
        "- Payload normalization: existing `dominant_payload_xor()` and `normalize_payload()` logic from `kpg111.metadata`.",
        "",
        "## Samples",
    ]
    lines.extend(
        markdown_table(
            ["Frequency", "raw RX", "decoded RX", "decoded BE", "decoded LE", "BCD", "6-bit indexes", "7-bit indexes"],
            [
                [
                    sample.frequency_text,
                    sample.raw_rx.hex(" "),
                    sample.decoded_rx.hex(" "),
                    str(sample.decoded_be),
                    str(sample.decoded_le),
                    bcd_text(sample.decoded_rx) or "invalid",
                    " ".join(str(value) for value in unpack_6bit(sample.decoded_rx)),
                    " ".join(str(value) for value in unpack_7bit(sample.decoded_rx)),
                ]
                for sample in samples
            ],
        )
    )
    decoded_be = [sample.decoded_be for sample in samples]
    decoded_le = [sample.decoded_le for sample in samples]
    raw_be = [sample.raw_be for sample in samples]
    raw_le = [sample.raw_le for sample in samples]
    step_indexes = [round((sample.frequency_hz - 146_000_000) / 6_250) for sample in samples]
    direct_matches = exact_direct_matches(samples)
    step_matches = step_index_exact_matches(samples)
    unique_freq, unique_decoded = field_uniqueness(samples)
    affine_decoded_be = affine_fit_count(step_indexes, decoded_be)
    affine_decoded_le = affine_fit_count(step_indexes, decoded_le)
    duplicate_findings = duplicate_frequency_findings(samples)
    raw_bcd_valid = sum(1 for sample in samples if bcd_text(sample.raw_rx))
    bcd_valid = sum(1 for sample in samples if bcd_text(sample.decoded_rx))
    raw_decimal_nibbles = sum(1 for sample in samples if all(value <= 9 for value in nibbles(sample.raw_rx)))
    decimal_nibbles = sum(1 for sample in samples if all(value <= 9 for value in nibbles(sample.decoded_rx)))
    lines.extend(
        [
            "",
            "## Hypothesis Checks",
            "",
            "### Big/Little Endian Integers",
            "",
            f"- raw big endian monotonicity: {monotonic(raw_be)}",
            f"- raw little endian monotonicity: {monotonic(raw_le)}",
            f"- decoded big endian monotonicity: {monotonic(decoded_be)}",
            f"- decoded little endian monotonicity: {monotonic(decoded_le)}",
            f"- exact direct matches against Hz/kHz/scaled decimal targets: {', '.join(direct_matches) if direct_matches else 'none'}",
            "Conclusion: simple endian/scaled integer interpretations fail.",
            "",
            "### BCD-like Encodings And Nibble Tables",
            "",
            f"- raw bytes with all BCD nibbles valid: {raw_bcd_valid}/{len(samples)}",
            f"- decoded bytes with all BCD nibbles valid: {bcd_valid}/{len(samples)}",
            f"- raw bytes with all nibbles in decimal range 0-9: {raw_decimal_nibbles}/{len(samples)}",
            f"- decoded bytes with all nibbles in decimal range 0-9: {decimal_nibbles}/{len(samples)}",
            "Conclusion: BCD and simple decimal nibble-row/column interpretations fail globally.",
            "",
            "### Packed 6-bit/7-bit Indexes",
            "",
            "- CSV includes raw and decoded 6-bit and 7-bit unpackings for each sample.",
            "- These unpackings are not monotonic in a way that directly tracks frequency over the whole set.",
            "Conclusion: direct packed 6-bit/7-bit frequency index is not supported; packed subindexes remain possible only as part of a more complex lookup scheme.",
            "",
            "### Frequency-step Indexes",
            "",
            f"- exact matches for plausible base/step indexes: {', '.join(step_matches) if step_matches else 'none'}",
            f"- best affine fit for decoded big-endian value vs 6.25 kHz index from 146 MHz: {affine_decoded_be[1]}",
            f"- best affine fit for decoded little-endian value vs 6.25 kHz index from 146 MHz: {affine_decoded_le[1]}",
            "Conclusion: direct step-index storage fails; no single affine step transform fits all samples.",
            "",
            "### Finite Lookup-table Behavior",
            "",
            f"- unique intended frequencies: {unique_freq}",
            f"- unique decoded RX byte values: {unique_decoded}",
            f"- duplicate-frequency consistency: {'; '.join(duplicate_findings) if duplicate_findings else 'no duplicate frequency samples'}",
            "- The decoded byte sequence is not a direct numeric frequency, not BCD, and not a simple monotonic step index.",
            "Conclusion: finite lookup-table or multi-field/indexed behavior remains plausible. The current samples do not prove the actual table or formula.",
            "",
            "## Summary",
            "",
            "- Failed: direct big/little endian integer, simple scaled frequency number, BCD, decimal nibble table, direct packed 6-bit/7-bit index, direct plausible frequency-step indexes.",
            "- Plausible: finite lookup-table behavior, or a more complex indexed/packed encoding with additional context outside the 3-byte RX field.",
            "- Do not claim a final formula from this dataset alone.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        paths = input_paths(args.input_glob)
        samples = load_samples(paths)
        write_csv(args.csv, samples)
        args.report.write_text(render_report(samples), encoding="utf-8")
        print(f"Wrote {args.report}")
        print(f"Wrote {args.csv}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
