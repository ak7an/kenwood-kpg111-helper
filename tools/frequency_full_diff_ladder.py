#!/usr/bin/env python3
"""Report normalized full-file diffs for KPG111 Line2 RX ladder samples."""

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


DEFAULT_INPUT_GLOB = "~/experiments/Line2_RX_1465*.dat"
DEFAULT_BASELINE = "~/AK7AN_Channel_Baseline.dat"
DEFAULT_REPORT = Path("/tmp/kpg111_frequency_full_diff_ladder.txt")
DEFAULT_CSV = Path("/tmp/kpg111_frequency_full_diff_ladder.csv")
CHANNEL_TABLE_START = 0x5E80
CHANNEL_STRIDE = 0x40
CHANNEL_NUMBER = 2
RECORD_SIZE = 0x40
RX_FIELD_OFFSET = 0x05
RX_FIELD_LENGTH = 3


@dataclass(frozen=True)
class ByteRun:
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1


@dataclass(frozen=True)
class SampleDiff:
    path: Path
    frequency_text: str
    frequency_hz: int
    xor_mask: int
    xor_ratio: float
    decoded_rx: bytes
    changed_offsets: frozenset[int]
    runs: tuple[ByteRun, ...]
    normalized: bytes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Diff normalized Line2_RX_1465 ladder DAT files against the channel baseline."
    )
    parser.add_argument("--input-glob", default=DEFAULT_INPUT_GLOB)
    parser.add_argument("--baseline", type=Path, default=Path(DEFAULT_BASELINE))
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    return parser.parse_args()


def expand_path(path: Path | str) -> Path:
    return Path(path).expanduser()


def input_paths(pattern: str) -> list[Path]:
    return [Path(path) for path in sorted(glob.glob(str(expand_path(pattern))))]


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


def channel_record_offset(channel: int = CHANNEL_NUMBER) -> int:
    return CHANNEL_TABLE_START + ((channel - 1) * CHANNEL_STRIDE)


def rx_field_bounds() -> tuple[int, int]:
    start = channel_record_offset() + RX_FIELD_OFFSET
    return start, start + RX_FIELD_LENGTH - 1


def fmt_range(run: ByteRun) -> str:
    if run.start == run.end:
        return f"0x{run.start:08x}"
    return f"0x{run.start:08x}-0x{run.end:08x}"


def fmt_bytes(data: bytes) -> str:
    return data.hex(" ")


def group_offsets(offsets: set[int] | frozenset[int] | list[int]) -> list[ByteRun]:
    sorted_offsets = sorted(offsets)
    if not sorted_offsets:
        return []
    runs = []
    start = previous = sorted_offsets[0]
    for offset in sorted_offsets[1:]:
        if offset == previous + 1:
            previous = offset
            continue
        runs.append(ByteRun(start, previous))
        start = previous = offset
    runs.append(ByteRun(start, previous))
    return runs


def diff_offsets(left: bytes, right: bytes) -> frozenset[int]:
    if len(left) != len(right):
        raise ValueError(
            f"baseline and sample sizes differ: {len(left)} vs {len(right)} bytes"
        )
    return frozenset(index for index, (a, b) in enumerate(zip(left, right)) if a != b)


def overlaps(run: ByteRun, start: int, end: int) -> bool:
    return run.start <= end and start <= run.end


def outside_rx_offsets(offsets: set[int] | frozenset[int]) -> set[int]:
    rx_start, rx_end = rx_field_bounds()
    return {offset for offset in offsets if not (rx_start <= offset <= rx_end)}


def load_samples(baseline: bytes, paths: list[Path]) -> list[SampleDiff]:
    samples = []
    rx_start, rx_end = rx_field_bounds()
    for path in paths:
        data = path.read_bytes()
        xor_mask, xor_ratio = dominant_payload_xor(baseline, data)
        normalized = normalize_payload(data, xor_mask)
        offsets = diff_offsets(baseline, normalized)
        frequency_text, frequency_hz = parse_frequency_from_filename(path)
        decoded_rx = normalized[rx_start : rx_end + 1]
        samples.append(
            SampleDiff(
                path=path,
                frequency_text=frequency_text,
                frequency_hz=frequency_hz,
                xor_mask=xor_mask,
                xor_ratio=xor_ratio,
                decoded_rx=decoded_rx,
                changed_offsets=offsets,
                runs=tuple(group_offsets(offsets)),
                normalized=normalized,
            )
        )
    return sorted(samples, key=lambda sample: (sample.frequency_hz, sample.path.name))


def offset_change_counts(samples: list[SampleDiff]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for sample in samples:
        for offset in sample.changed_offsets:
            counts[offset] = counts.get(offset, 0) + 1
    return counts


def classify_offset_correlation(samples: list[SampleDiff], offset: int) -> str:
    values = [sample.normalized[offset] for sample in samples]
    unique_values = len(set(values))
    if unique_values <= 1:
        return "constant across samples"
    nondecreasing = all(left <= right for left, right in zip(values, values[1:]))
    nonincreasing = all(left >= right for left, right in zip(values, values[1:]))
    if nondecreasing or nonincreasing:
        return "monotonic with frequency"
    if unique_values == len({sample.frequency_hz for sample in samples}):
        return "varies uniquely with frequency"
    return "varies, not monotonic"


def correlated_outside_offsets(samples: list[SampleDiff]) -> dict[int, str]:
    counts = offset_change_counts(samples)
    rx_start, rx_end = rx_field_bounds()
    result = {}
    for offset in sorted(counts):
        if rx_start <= offset <= rx_end:
            continue
        classification = classify_offset_correlation(samples, offset)
        if classification != "constant across samples":
            result[offset] = classification
    return result


def format_counted_runs(offsets: list[int], counts: dict[int, int]) -> list[str]:
    lines = []
    for run in group_offsets(offsets):
        count_values = {counts[offset] for offset in range(run.start, run.end + 1)}
        count_text = (
            f"{next(iter(count_values))} samples"
            if len(count_values) == 1
            else "mixed sample counts"
        )
        lines.append(f"- {fmt_range(run)} ({run.length} byte(s), {count_text})")
    return lines or ["- none"]


def format_runs(runs: list[ByteRun]) -> list[str]:
    return [f"- {fmt_range(run)} ({run.length} byte(s))" for run in runs] or ["- none"]


def write_report(
    report_path: Path,
    baseline_path: Path,
    baseline: bytes,
    samples: list[SampleDiff],
    counts: dict[int, int],
    correlated_offsets: dict[int, str],
) -> None:
    rx_start, rx_end = rx_field_bounds()
    sample_count = len(samples)
    every_offsets = sorted(offset for offset, count in counts.items() if count == sample_count)
    sometimes_offsets = sorted(offset for offset, count in counts.items() if 0 < count < sample_count)
    every_outside = outside_rx_offsets(frozenset(every_offsets))
    sometimes_outside = outside_rx_offsets(frozenset(sometimes_offsets))

    lines = [
        "KPG111 Line2 RX 1465 ladder normalized full-file diff",
        "",
        f"Baseline: {baseline_path}",
        f"Samples: {sample_count}",
        f"Zone 1 Channel 2 record: 0x{channel_record_offset():08x}-0x{channel_record_offset() + RECORD_SIZE - 1:08x}",
        f"Decoded RX field: 0x{rx_start:08x}-0x{rx_end:08x}",
        "Normalization: sample bytes are normalized with kpg111.metadata dominant_payload_xor/normalize_payload before diffing.",
        "",
        "Offsets changed in every frequency sample:",
    ]
    lines.extend(format_runs(group_offsets(every_offsets)))
    lines.extend(["", "Offsets changed only sometimes:"])
    lines.extend(format_counted_runs(sometimes_offsets, counts))
    lines.extend(["", "Changes outside the decoded 3-byte RX field:"])
    if every_outside or sometimes_outside:
        lines.append("- Yes. Normalized changes exist outside 0x%08x-0x%08x." % (rx_start, rx_end))
        lines.append("- Outside offsets changed in every sample:")
        lines.extend(format_runs(group_offsets(every_outside)))
        lines.append("- Outside offsets changed only sometimes:")
        lines.extend(format_counted_runs(sorted(sometimes_outside), counts))
    else:
        lines.append("- No normalized changes outside the decoded RX field were found.")

    lines.extend(["", "Outside-offset frequency correlation check:"])
    if correlated_offsets:
        for run in group_offsets(correlated_offsets.keys()):
            labels = {correlated_offsets[offset] for offset in range(run.start, run.end + 1)}
            label_text = next(iter(labels)) if len(labels) == 1 else "mixed"
            lines.append(f"- {fmt_range(run)}: {label_text}")
    else:
        lines.append("- No outside changed offsets varied across the sorted frequency ladder.")

    lines.extend(["", "Per-sample details:"])
    for sample in samples:
        outside = sorted(outside_rx_offsets(sample.changed_offsets))
        correlated_here = [
            offset for offset in outside if offset in correlated_offsets
        ]
        lines.extend(
            [
                "",
                f"{sample.path.name}",
                f"- intended frequency: {sample.frequency_text} MHz ({sample.frequency_hz} Hz)",
                f"- xor mask/ratio: 0x{sample.xor_mask:02x} / {sample.xor_ratio:.6f}",
                f"- decoded RX 3 bytes: {fmt_bytes(sample.decoded_rx)}",
                "- normalized changed byte ranges:",
            ]
        )
        for run in sample.runs:
            before = fmt_bytes(baseline[run.start : run.end + 1])
            after = fmt_bytes(sample.normalized[run.start : run.end + 1])
            marker = "overlaps RX field" if overlaps(run, rx_start, rx_end) else "outside RX field"
            lines.append(
                f"  - {fmt_range(run)} ({run.length} byte(s), {marker}) "
                f"baseline={before} sample={after}"
            )
        if correlated_here:
            lines.append(
                "- outside range(s) with observed frequency-varying values: "
                + ", ".join(fmt_range(run) for run in group_offsets(correlated_here))
            )
        elif outside:
            lines.append("- outside changed ranges: present, but constant across sorted ladder samples")
        else:
            lines.append("- outside changed ranges: none")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(
    csv_path: Path,
    baseline: bytes,
    samples: list[SampleDiff],
    counts: dict[int, int],
    correlated_offsets: dict[int, str],
) -> None:
    rx_start, rx_end = rx_field_bounds()
    fieldnames = [
        "row_type",
        "filename",
        "frequency_text_mhz",
        "frequency_hz",
        "xor_mask",
        "xor_ratio",
        "decoded_rx_hex",
        "range_start",
        "range_end",
        "length",
        "baseline_hex",
        "normalized_hex",
        "overlaps_rx_field",
        "outside_rx_field",
        "changed_sample_count",
        "correlation",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for sample in samples:
            for run in sample.runs:
                run_offsets = range(run.start, run.end + 1)
                correlations = {
                    correlated_offsets[offset]
                    for offset in run_offsets
                    if offset in correlated_offsets
                }
                writer.writerow(
                    {
                        "row_type": "sample_range",
                        "filename": str(sample.path),
                        "frequency_text_mhz": sample.frequency_text,
                        "frequency_hz": sample.frequency_hz,
                        "xor_mask": f"0x{sample.xor_mask:02x}",
                        "xor_ratio": f"{sample.xor_ratio:.6f}",
                        "decoded_rx_hex": sample.decoded_rx.hex(" "),
                        "range_start": f"0x{run.start:08x}",
                        "range_end": f"0x{run.end:08x}",
                        "length": run.length,
                        "baseline_hex": baseline[run.start : run.end + 1].hex(" "),
                        "normalized_hex": sample.normalized[run.start : run.end + 1].hex(" "),
                        "overlaps_rx_field": str(overlaps(run, rx_start, rx_end)).lower(),
                        "outside_rx_field": str(any(offset < rx_start or offset > rx_end for offset in run_offsets)).lower(),
                        "changed_sample_count": ",".join(str(counts[offset]) for offset in run_offsets),
                        "correlation": "; ".join(sorted(correlations)),
                    }
                )
        for offset, count in sorted(counts.items()):
            writer.writerow(
                {
                    "row_type": "offset_summary",
                    "range_start": f"0x{offset:08x}",
                    "range_end": f"0x{offset:08x}",
                    "length": 1,
                    "overlaps_rx_field": str(rx_start <= offset <= rx_end).lower(),
                    "outside_rx_field": str(not (rx_start <= offset <= rx_end)).lower(),
                    "changed_sample_count": count,
                    "correlation": correlated_offsets.get(offset, "constant across samples"),
                }
            )


def main() -> int:
    args = parse_args()
    baseline_path = expand_path(args.baseline)
    paths = input_paths(args.input_glob)
    if not paths:
        raise SystemExit(f"no input files matched {args.input_glob!r}")
    baseline = baseline_path.read_bytes()
    samples = load_samples(baseline, paths)
    counts = offset_change_counts(samples)
    correlated_offsets = correlated_outside_offsets(samples)
    write_report(args.report, baseline_path, baseline, samples, counts, correlated_offsets)
    write_csv(args.csv, baseline, samples, counts, correlated_offsets)
    print(f"wrote {args.report}")
    print(f"wrote {args.csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
