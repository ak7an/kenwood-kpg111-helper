#!/usr/bin/env python3
"""Analyze 24-bit KPG111 RX frequency field bit dependencies."""

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


DEFAULT_INPUT_GLOB = "data/experiments/channel_dats/Line2_RX_1465*.dat"
DEFAULT_BASELINE = "data/experiments/channel_dats/Line2_RX_146500.dat"
DEFAULT_REPORT = Path("/tmp/kpg111_bit_dependency.txt")
DEFAULT_CSV = Path("/tmp/kpg111_bit_dependency.csv")
CHANNEL_TABLE_START = 0x5E80
CHANNEL_STRIDE = 0x40
CHANNEL_NUMBER = 2
RX_FIELD_OFFSET = 0x05
RX_FIELD_LENGTH = 3
STEP_HZ = 6250
MASK24 = 0xFFFFFF
BIT_COUNT = 24


@dataclass(frozen=True)
class Sample:
    path: Path
    frequency_text: str
    frequency_hz: int
    step_index_from_146mhz: int
    xor_mask: int
    xor_ratio: float
    rx: bytes

    @property
    def value(self) -> int:
        return int.from_bytes(self.rx, "big")

    @property
    def bits_msb(self) -> str:
        return f"{self.value:024b}"


@dataclass(frozen=True)
class Transition:
    left: Sample
    right: Sample
    delta_hz: int
    delta_steps: float
    delta_mask: int
    hamming: int


@dataclass(frozen=True)
class AffineResult:
    exact: bool
    input_rank: int
    equations: int
    output_rows: tuple[int | None, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze bit dependencies in the 24-bit Line2 RX frequency field."
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


def rx_field_start() -> int:
    record_start = CHANNEL_TABLE_START + ((CHANNEL_NUMBER - 1) * CHANNEL_STRIDE)
    return record_start + RX_FIELD_OFFSET


def load_samples(baseline: bytes, paths: list[Path]) -> list[Sample]:
    samples = []
    start = rx_field_start()
    for path in paths:
        data = path.read_bytes()
        xor_mask, xor_ratio = dominant_payload_xor(baseline, data)
        normalized = normalize_payload(data, xor_mask)
        frequency_text, frequency_hz = parse_frequency_from_filename(path)
        samples.append(
            Sample(
                path=path,
                frequency_text=frequency_text,
                frequency_hz=frequency_hz,
                step_index_from_146mhz=round((frequency_hz - 146_000_000) / STEP_HZ),
                xor_mask=xor_mask,
                xor_ratio=xor_ratio,
                rx=normalized[start : start + RX_FIELD_LENGTH],
            )
        )
    return sorted(samples, key=lambda sample: (sample.frequency_hz, sample.path.name))


def unique_by_frequency_and_value(samples: list[Sample]) -> list[Sample]:
    unique = []
    seen: set[tuple[int, int]] = set()
    for sample in samples:
        key = (sample.frequency_hz, sample.value)
        if key in seen:
            continue
        seen.add(key)
        unique.append(sample)
    return unique


def transitions(samples: list[Sample]) -> list[Transition]:
    rows = []
    for left, right in zip(samples, samples[1:]):
        mask = left.value ^ right.value
        rows.append(
            Transition(
                left=left,
                right=right,
                delta_hz=right.frequency_hz - left.frequency_hz,
                delta_steps=(right.frequency_hz - left.frequency_hz) / STEP_HZ,
                delta_mask=mask,
                hamming=mask.bit_count(),
            )
        )
    return rows


def bit_mask(bit_msb: int) -> int:
    return 1 << (BIT_COUNT - 1 - bit_msb)


def bit_value(value: int, bit_msb: int) -> int:
    return 1 if value & bit_mask(bit_msb) else 0


def interval_pairs(samples: list[Sample], delta_hz: int) -> list[tuple[Sample, Sample]]:
    by_frequency = {sample.frequency_hz: sample for sample in samples}
    pairs = []
    for sample in samples:
        other = by_frequency.get(sample.frequency_hz + delta_hz)
        if other is not None:
            pairs.append((sample, other))
    return pairs


def interval_toggle_text(samples: list[Sample], bit: int, delta_hz: int) -> str:
    pairs = interval_pairs(samples, delta_hz)
    if not pairs:
        return "no sample pairs"
    toggles = sum(
        1 for left, right in pairs if bit_value(left.value ^ right.value, bit)
    )
    if toggles == len(pairs):
        return f"yes ({toggles}/{len(pairs)})"
    if toggles:
        return f"sometimes ({toggles}/{len(pairs)})"
    return f"no (0/{len(pairs)})"


def bit_transition_summary(samples: list[Sample], transitions_: list[Transition]) -> list[dict[str, str]]:
    periods = (6250, 12500, 25000, 100000)
    rows = []
    for bit in range(BIT_COUNT):
        mask = bit_mask(bit)
        toggles = [transition for transition in transitions_ if transition.delta_mask & mask]
        by_period = {period: interval_toggle_text(samples, bit, period) for period in periods}
        rows.append(
            {
                "bit": str(bit),
                "byte_bit": f"byte{bit // 8}.b{7 - (bit % 8)}",
                "toggle_count": str(len(toggles)),
                "toggle_deltas_hz": ", ".join(str(transition.delta_hz) for transition in toggles),
                "changes_every_6250": by_period[6250],
                "changes_every_12500": by_period[12500],
                "changes_every_25000": by_period[25000],
                "changes_every_100000": by_period[100000],
            }
        )
    return rows


def gray_encode(value: int) -> int:
    return (value ^ (value >> 1)) & MASK24


def gray_decode(value: int) -> int:
    value &= MASK24
    shift = 1
    while shift < BIT_COUNT:
        value ^= value >> shift
        shift <<= 1
    return value & MASK24


def bit_reverse(value: int, width: int = BIT_COUNT) -> int:
    result = 0
    for _index in range(width):
        result = (result << 1) | (value & 1)
        value >>= 1
    return result


def deinterleave_even_odd(value: int) -> int:
    bits = [(value >> shift) & 1 for shift in range(BIT_COUNT - 1, -1, -1)]
    reordered = bits[::2] + bits[1::2]
    result = 0
    for bit in reordered:
        result = (result << 1) | bit
    return result


def score_exact_series(name: str, actual: list[int], expected: list[int]) -> tuple[str, int]:
    return name, sum(1 for left, right in zip(actual, expected) if left == right)


def candidate_scores(samples: list[Sample]) -> list[tuple[str, int]]:
    actual = [sample.value for sample in samples]
    indexes = [sample.step_index_from_146mhz for sample in samples]
    min_index = min(indexes)
    relative = [index - min_index for index in indexes]
    candidates = []
    for label, values in (("step index from 146 MHz", indexes), ("relative step index", relative)):
        candidates.extend(
            [
                score_exact_series(label, actual, [value & MASK24 for value in values]),
                score_exact_series(f"{label} bit-reversed", actual, [bit_reverse(value) for value in values]),
                score_exact_series(f"{label} reflected Gray", actual, [gray_encode(value) for value in values]),
                score_exact_series(
                    f"{label} reflected Gray bit-reversed",
                    actual,
                    [bit_reverse(gray_encode(value)) for value in values],
                ),
                score_exact_series(
                    f"{label} even/odd bit interleave",
                    actual,
                    [deinterleave_even_odd(value) for value in values],
                ),
                score_exact_series(
                    f"{label} XOR whitened by first sample",
                    actual,
                    [(value ^ actual[0]) & MASK24 for value in values],
                ),
            ]
        )
    return sorted(candidates, key=lambda row: (-row[1], row[0]))


def exact_bit_source_matches(samples: list[Sample], source: str) -> list[str]:
    indexes = [sample.step_index_from_146mhz for sample in samples]
    if source == "relative binary":
        min_index = min(indexes)
        inputs = [index - min_index for index in indexes]
    elif source == "absolute binary":
        inputs = indexes
    elif source == "relative gray":
        min_index = min(indexes)
        inputs = [gray_encode(index - min_index) for index in indexes]
    elif source == "absolute gray":
        inputs = [gray_encode(index) for index in indexes]
    else:
        raise ValueError(source)

    matches = []
    for out_bit in range(BIT_COUNT):
        actual = [bit_value(sample.value, out_bit) for sample in samples]
        if len(set(actual)) <= 1:
            continue
        for in_bit in range(BIT_COUNT):
            candidate = [bit_value(value, in_bit) for value in inputs]
            if len(set(candidate)) <= 1:
                continue
            if actual == candidate:
                matches.append(f"out{out_bit}=in{in_bit}")
            elif actual == [1 - bit for bit in candidate]:
                matches.append(f"out{out_bit}=not in{in_bit}")
    return matches


def constant_output_bits(samples: list[Sample]) -> list[str]:
    rows = []
    for bit in range(BIT_COUNT):
        values = {bit_value(sample.value, bit) for sample in samples}
        if len(values) == 1:
            rows.append(f"out{bit}={next(iter(values))}")
    return rows


def gf2_rank(rows: list[int], width: int) -> int:
    rows = rows[:]
    rank = 0
    for col in range(width - 1, -1, -1):
        pivot_index = next((index for index in range(rank, len(rows)) if rows[index] & (1 << col)), None)
        if pivot_index is None:
            continue
        rows[rank], rows[pivot_index] = rows[pivot_index], rows[rank]
        for index, row in enumerate(rows):
            if index != rank and (row & (1 << col)):
                rows[index] ^= rows[rank]
        rank += 1
    return rank


def solve_gf2(rows: list[int], rhs: list[int], width: int) -> tuple[bool, int | None, int]:
    augmented = [(row & ((1 << width) - 1)) | ((bit & 1) << width) for row, bit in zip(rows, rhs)]
    rank = 0
    pivots: list[int] = []
    for col in range(width - 1, -1, -1):
        pivot_index = next(
            (index for index in range(rank, len(augmented)) if augmented[index] & (1 << col)),
            None,
        )
        if pivot_index is None:
            continue
        augmented[rank], augmented[pivot_index] = augmented[pivot_index], augmented[rank]
        for index, row in enumerate(augmented):
            if index != rank and (row & (1 << col)):
                augmented[index] ^= augmented[rank]
        pivots.append(col)
        rank += 1

    coefficient_mask = (1 << width) - 1
    for row in augmented[rank:]:
        if (row & coefficient_mask) == 0 and ((row >> width) & 1):
            return False, None, rank

    solution = 0
    for row_index, col in enumerate(pivots):
        if (augmented[row_index] >> width) & 1:
            solution |= 1 << col
    return True, solution, rank


def affine_fit(samples: list[Sample], relative: bool) -> AffineResult:
    indexes = [sample.step_index_from_146mhz for sample in samples]
    min_index = min(indexes)
    values = [index - min_index if relative else index for index in indexes]
    # 25 input columns: constant bit in column 24 plus 24 data bits.
    rows = [(1 << BIT_COUNT) | (value & MASK24) for value in values]
    rank = gf2_rank(rows, BIT_COUNT + 1)
    output_rows: list[int | None] = []
    exact = True
    for out_bit in range(BIT_COUNT):
        rhs = [bit_value(sample.value, out_bit) for sample in samples]
        ok, solution, _rank = solve_gf2(rows, rhs, BIT_COUNT + 1)
        output_rows.append(solution if ok else None)
        exact = exact and ok
    return AffineResult(
        exact=exact,
        input_rank=rank,
        equations=len(samples),
        output_rows=tuple(output_rows),
    )


def lfsr_transition_candidates(samples: list[Sample]) -> list[str]:
    values = [sample.value for sample in samples]
    rows = []
    for direction in ("left", "right"):
        for taps in range(BIT_COUNT):
            ok = True
            for previous, current in zip(values, values[1:]):
                if direction == "left":
                    feedback = ((previous >> taps) & 1)
                    predicted = ((previous << 1) & MASK24) | feedback
                else:
                    feedback = ((previous >> taps) & 1) << (BIT_COUNT - 1)
                    predicted = (previous >> 1) | feedback
                if predicted != current:
                    ok = False
                    break
            if ok:
                rows.append(f"{direction} shift, single feedback tap bit {taps}")
    return rows


def write_report(
    path: Path,
    samples: list[Sample],
    unique_samples: list[Sample],
    transitions_: list[Transition],
    bit_rows: list[dict[str, str]],
    scores: list[tuple[str, int]],
    affine_absolute: AffineResult,
    affine_relative: AffineResult,
) -> None:
    lines = [
        "KPG111 24-bit RX frequency bit dependency analysis",
        "",
        f"Samples: {len(samples)} files, {len(unique_samples)} unique frequency/value points",
        f"RX bytes: 0x{rx_field_start():08x}-0x{rx_field_start() + RX_FIELD_LENGTH - 1:08x}",
        "Bit numbering: bit 0 is the MSB of byte 0; bit 23 is the LSB of byte 2.",
        "",
        "24-column bit matrix:",
    ]
    header = "freq_hz,rx_hex," + ",".join(f"b{bit:02d}" for bit in range(BIT_COUNT))
    lines.append(header)
    for sample in unique_samples:
        lines.append(
            f"{sample.frequency_hz},{sample.rx.hex(' ')},"
            + ",".join(sample.bits_msb)
        )

    lines.extend(["", "Adjacent frequency vs bit transitions:"])
    lines.append("left_hz -> right_hz | delta_hz | delta_steps | delta_bitmask | hamming")
    for transition in transitions_:
        lines.append(
            f"{transition.left.frequency_hz} -> {transition.right.frequency_hz} | "
            f"{transition.delta_hz} | {transition.delta_steps:g} | "
            f"0x{transition.delta_mask:06x} | {transition.hamming}"
        )

    lines.extend(["", "Per-bit transition periodicity:"])
    lines.append(
        "bit byte.bit toggles every_6.25k every_12.5k every_25k every_100k toggle_deltas_hz"
    )
    for row in bit_rows:
        lines.append(
            f"{row['bit']} {row['byte_bit']} {row['toggle_count']} "
            f"{row['changes_every_6250']} | {row['changes_every_12500']} | "
            f"{row['changes_every_25000']} | {row['changes_every_100000']} | "
            f"{row['toggle_deltas_hz'] or 'none'}"
        )

    gray_hamming = [
        transition.hamming for transition in transitions_ if transition.delta_hz == STEP_HZ
    ]
    lines.extend(
        [
            "",
            "Gray-code observations:",
            f"- 6.25 kHz adjacent Hamming distances: {gray_hamming or 'none'}",
            "- Standard/reflected Gray code would normally flip exactly one bit for each adjacent one-step increment.",
        ]
    )
    if gray_hamming and all(distance == 1 for distance in gray_hamming):
        lines.append("- Observed one-step transitions are Gray-code-compatible.")
    elif gray_hamming:
        lines.append("- Observed one-step transitions are not direct reflected Gray-code-compatible.")

    lines.extend(["", "Candidate exact-value scores:"])
    for name, matched in scores[:12]:
        lines.append(f"- {name}: {matched}/{len(unique_samples)} exact values")

    lines.extend(["", "Exact output-bit source matches:"])
    constants = constant_output_bits(unique_samples)
    lines.append(f"- constant output bits: {', '.join(constants) if constants else 'none'}")
    for source in ("absolute binary", "relative binary", "absolute gray", "relative gray"):
        matches = exact_bit_source_matches(unique_samples, source)
        lines.append(f"- {source}: {', '.join(matches) if matches else 'none'}")

    lines.extend(["", "Affine GF(2) transform checks:"])
    for label, result in (("absolute step index", affine_absolute), ("relative step index", affine_relative)):
        lines.append(
            f"- {label}: exact={result.exact}, input rank={result.input_rank}/25, equations={result.equations}"
        )
        if result.exact:
            lines.append("  output rows are one possible affine solution; bit 24 is the constant term:")
            for bit, solution in enumerate(result.output_rows):
                lines.append(f"  out{bit:02d}: 0x{solution:07x}")

    lines.extend(["", "LFSR behavior check:"])
    lfsr_rows = lfsr_transition_candidates(unique_samples)
    if lfsr_rows:
        lines.extend(f"- {row}" for row in lfsr_rows)
    else:
        lines.append("- No simple one-bit-shift/single-tap LFSR transition matched adjacent samples.")

    lines.extend(["", "Carry propagation and bit-plane notes:"])
    lines.append("- Direct binary carry behavior is not visible in stored bit order from the adjacent delta masks.")
    lines.append("- Several high-frequency transitions change many stored bits, which is consistent with whitening/permutation/affine mixing rather than plain contiguous binary fields.")
    lines.append("- The affine check can fit the observed ladder if marked exact, but rank below 25 means the available samples do not uniquely identify a 24-bit transform.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(
    path: Path,
    samples: list[Sample],
    unique_samples: list[Sample],
    transitions_: list[Transition],
    bit_rows: list[dict[str, str]],
    scores: list[tuple[str, int]],
    affine_absolute: AffineResult,
    affine_relative: AffineResult,
) -> None:
    fieldnames = [
        "row_type",
        "frequency_hz",
        "frequency_text_mhz",
        "filename",
        "rx_hex",
        "rx_value_be",
        "bit",
        "bit_value",
        "left_frequency_hz",
        "right_frequency_hz",
        "delta_frequency_hz",
        "delta_steps",
        "delta_bitmask_hex",
        "hamming_distance",
        "byte_bit",
        "toggle_count",
        "changes_every_6250",
        "changes_every_12500",
        "changes_every_25000",
        "changes_every_100000",
        "toggle_deltas_hz",
        "candidate",
        "matched",
        "total",
        "affine_source",
        "affine_exact",
        "affine_input_rank",
        "affine_row_hex",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for sample in unique_samples:
            for bit, value in enumerate(sample.bits_msb):
                writer.writerow(
                    {
                        "row_type": "bit_matrix",
                        "frequency_hz": sample.frequency_hz,
                        "frequency_text_mhz": sample.frequency_text,
                        "filename": str(sample.path),
                        "rx_hex": sample.rx.hex(" "),
                        "rx_value_be": f"0x{sample.value:06x}",
                        "bit": bit,
                        "bit_value": value,
                    }
                )
        for transition in transitions_:
            writer.writerow(
                {
                    "row_type": "transition",
                    "left_frequency_hz": transition.left.frequency_hz,
                    "right_frequency_hz": transition.right.frequency_hz,
                    "delta_frequency_hz": transition.delta_hz,
                    "delta_steps": f"{transition.delta_steps:g}",
                    "delta_bitmask_hex": f"0x{transition.delta_mask:06x}",
                    "hamming_distance": transition.hamming,
                }
            )
        for row in bit_rows:
            out = {"row_type": "bit_summary"}
            out.update(row)
            writer.writerow(out)
        for name, matched in scores:
            writer.writerow(
                {
                    "row_type": "candidate_score",
                    "candidate": name,
                    "matched": matched,
                    "total": len(unique_samples),
                }
            )
        for label, result in (("absolute", affine_absolute), ("relative", affine_relative)):
            for bit, row in enumerate(result.output_rows):
                writer.writerow(
                    {
                        "row_type": "affine_gf2",
                        "bit": bit,
                        "affine_source": label,
                        "affine_exact": str(result.exact).lower(),
                        "affine_input_rank": result.input_rank,
                        "affine_row_hex": "" if row is None else f"0x{row:07x}",
                    }
                )


def main() -> int:
    args = parse_args()
    paths = input_paths(args.input_glob)
    if not paths:
        raise SystemExit(f"no input files matched {args.input_glob!r}")
    baseline = expand_path(args.baseline).read_bytes()
    samples = load_samples(baseline, paths)
    unique_samples = unique_by_frequency_and_value(samples)
    transition_rows = transitions(unique_samples)
    bit_rows = bit_transition_summary(unique_samples, transition_rows)
    scores = candidate_scores(unique_samples)
    affine_absolute = affine_fit(unique_samples, relative=False)
    affine_relative = affine_fit(unique_samples, relative=True)
    write_report(
        args.report,
        samples,
        unique_samples,
        transition_rows,
        bit_rows,
        scores,
        affine_absolute,
        affine_relative,
    )
    write_csv(
        args.csv,
        samples,
        unique_samples,
        transition_rows,
        bit_rows,
        scores,
        affine_absolute,
        affine_relative,
    )
    print(f"wrote {args.report}")
    print(f"wrote {args.csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
