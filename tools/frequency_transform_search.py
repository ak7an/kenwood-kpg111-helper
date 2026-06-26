#!/usr/bin/env python3
"""Search simple reversible transforms for KPG111 3-byte frequency samples."""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass


MASK24 = 0xFFFFFF
WIDTH24 = 24
NEAR_MATCH_THRESHOLD = 8

VERIFIED_SAMPLES = (
    ("146.000", "c1 89 f2"),
    ("146.100", "61 0e f4"),
    ("146.120", "01 dc f4"),
    ("146.200", "81 94 f7"),
    ("146.300", "21 1d f9"),
    ("146.400", "41 a2 f8"),
    ("146.500", "e1 28 fa"),
    ("146.510", "f1 d1 fa"),
    ("146.520", "81 f6 fa"),
    ("146.530", "91 9f fa"),
    ("146.600", "01 b1 fd"),
    ("146.700", "a1 37 ff"),
    ("146.720", "41 84 ff"),
    ("146.800", "c1 bc fe"),
    ("146.900", "61 c5 80"),
    ("147.000", "81 4b 82"),
)


@dataclass(frozen=True)
class FrequencySample:
    frequency_text: str
    frequency_hz: int
    encoded: bytes


@dataclass(frozen=True)
class SourceValue:
    label: str
    value: int


@dataclass(frozen=True)
class TransformCandidate:
    name: str
    source_label: str
    predicted: tuple[bytes, ...]


@dataclass(frozen=True)
class TransformMatch:
    name: str
    source_label: str
    matched: int
    failed: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search simple reversible transforms for verified KPG111 frequency samples."
    )
    parser.add_argument(
        "--near-threshold",
        type=int,
        default=NEAR_MATCH_THRESHOLD,
        help=f"Minimum sample count for near matches (default: {NEAR_MATCH_THRESHOLD})",
    )
    return parser.parse_args()


def parse_frequency_hz(value: str) -> int:
    whole, fractional = value.split(".", 1)
    fractional = (fractional + "000000")[:6]
    return int(whole) * 1_000_000 + int(fractional)


def verified_samples() -> list[FrequencySample]:
    return [
        FrequencySample(frequency_text, parse_frequency_hz(frequency_text), bytes.fromhex(raw))
        for frequency_text, raw in VERIFIED_SAMPLES
    ]


def source_values(sample: FrequencySample) -> list[SourceValue]:
    hz = sample.frequency_hz
    return [
        SourceValue("Hz", hz),
        SourceValue("Hz / 10", hz // 10),
        SourceValue("Hz / 100", hz // 100),
        SourceValue("Hz / 1000", hz // 1000),
        SourceValue("kHz", hz // 1000),
        SourceValue("offset from 0 Hz", hz),
        SourceValue("offset from 100 MHz", hz - 100_000_000),
        SourceValue("offset from 136 MHz", hz - 136_000_000),
        SourceValue("offset from 144 MHz", hz - 144_000_000),
        SourceValue("offset from 146 MHz", hz - 146_000_000),
    ]


def all_source_series(samples: list[FrequencySample]) -> dict[str, list[int]]:
    series: dict[str, list[int]] = {}
    for sample in samples:
        for source in source_values(sample):
            series.setdefault(source.label, []).append(source.value)
    return series


def bit_reverse_byte(value: int) -> int:
    result = 0
    for _index in range(8):
        result = (result << 1) | (value & 1)
        value >>= 1
    return result


def bit_reverse_each_byte(data: bytes) -> bytes:
    return bytes(bit_reverse_byte(byte) for byte in data)


def nibble_swap_byte(value: int) -> int:
    return ((value & 0x0F) << 4) | ((value & 0xF0) >> 4)


def nibble_swap_each_byte(data: bytes) -> bytes:
    return bytes(nibble_swap_byte(byte) for byte in data)


def gray_encode(value: int) -> int:
    return (value ^ (value >> 1)) & MASK24


def gray_decode(value: int) -> int:
    value &= MASK24
    shift = 1
    while shift < WIDTH24:
        value ^= value >> shift
        shift <<= 1
    return value & MASK24


def rotate_left(value: int, amount: int, width: int = WIDTH24) -> int:
    amount %= width
    mask = (1 << width) - 1
    value &= mask
    return ((value << amount) | (value >> (width - amount))) & mask


def rotate_right(value: int, amount: int, width: int = WIDTH24) -> int:
    amount %= width
    mask = (1 << width) - 1
    value &= mask
    return ((value >> amount) | (value << (width - amount))) & mask


def int_transforms() -> list[tuple[str, object]]:
    transforms: list[tuple[str, object]] = [
        ("identity", lambda value: value & MASK24),
        ("Gray encode", gray_encode),
        ("Gray decode", gray_decode),
    ]
    for amount in range(1, WIDTH24):
        transforms.append((f"rotate left {amount}", lambda value, shift=amount: rotate_left(value, shift)))
        transforms.append((f"rotate right {amount}", lambda value, shift=amount: rotate_right(value, shift)))
    return transforms


def byte_operations() -> list[tuple[str, object]]:
    operations: list[tuple[str, object]] = [
        ("no byte op", lambda data: data),
        ("bit reverse each byte", bit_reverse_each_byte),
        ("nibble swap each byte", nibble_swap_each_byte),
    ]
    for mask in range(0x100):
        operations.append((f"XOR 0x{mask:02x} repeated", lambda data, value=mask: bytes(byte ^ value for byte in data)))
    return operations


def pack24(value: int, endian: str) -> bytes:
    return (value & MASK24).to_bytes(3, endian)


def permute_bytes(data: bytes, order: tuple[int, int, int]) -> bytes:
    return bytes(data[index] for index in order)


def generate_structural_matches(
    samples: list[FrequencySample],
    minimum_matches: int = 1,
) -> list[TransformMatch]:
    matches: list[TransformMatch] = []
    source_series = all_source_series(samples)
    permutations = tuple(itertools.permutations(range(3)))
    int_ops = int_transforms()

    for source_label, values in source_series.items():
        for int_name, int_op in int_ops:
            transformed_values = [int_op(value) for value in values]  # type: ignore[operator]
            for endian in ("little", "big"):
                packed = [pack24(value, endian) for value in transformed_values]
                for order in permutations:
                    permuted = [permute_bytes(data, order) for data in packed]
                    order_label = "".join(str(index) for index in order)
                    prefix = f"{int_name}; raw 24-bit {endian} endian; byte permutation {order_label}"
                    for byte_name, predicted in (
                        ("no byte op", tuple(permuted)),
                        ("bit reverse each byte", tuple(bit_reverse_each_byte(data) for data in permuted)),
                        ("nibble swap each byte", tuple(nibble_swap_each_byte(data) for data in permuted)),
                    ):
                        add_match(
                            matches,
                            evaluate_predicted(
                                f"{prefix}; {byte_name}",
                                source_label,
                                predicted,
                                samples,
                            ),
                            minimum_matches,
                        )

                    for mask, matched in repeated_xor_match_counts(permuted, samples).items():
                        if matched < minimum_matches:
                            continue
                        predicted = tuple(bytes(byte ^ mask for byte in data) for data in permuted)
                        add_match(
                            matches,
                            evaluate_predicted(
                                f"{prefix}; XOR 0x{mask:02x} repeated",
                                source_label,
                                predicted,
                                samples,
                            ),
                            minimum_matches,
                        )
    return matches


def repeated_xor_match_counts(
    base_values: list[bytes],
    samples: list[FrequencySample],
) -> dict[int, int]:
    counts: dict[int, int] = {}
    for base, sample in zip(base_values, samples):
        observed = {left ^ right for left, right in zip(base, sample.encoded)}
        if len(observed) != 1:
            continue
        mask = observed.pop()
        counts[mask] = counts.get(mask, 0) + 1
    return counts


def add_match(matches: list[TransformMatch], match: TransformMatch, minimum_matches: int) -> None:
    if match.matched >= minimum_matches:
        matches.append(match)


def solve_affine_candidates(samples: list[FrequencySample]) -> list[TransformCandidate]:
    candidates: dict[tuple[str, str, int, int], TransformCandidate] = {}
    source_series = all_source_series(samples)

    for source_label, values in source_series.items():
        for endian in ("little", "big"):
            targets = [int.from_bytes(sample.encoded, endian) for sample in samples]
            for left in range(len(samples)):
                for right in range(left + 1, len(samples)):
                    for a_value, b_value in solve_affine_pair(
                        values[left],
                        targets[left],
                        values[right],
                        targets[right],
                    ):
                        predicted = tuple(
                            pack24(((value * a_value) + b_value) & MASK24, endian)
                            for value in values
                        )
                        key = (source_label, endian, a_value, b_value)
                        candidates[key] = TransformCandidate(
                            name=(
                                "affine "
                                f"encoded = ((value * 0x{a_value:06x}) + 0x{b_value:06x}) "
                                f"& 0xffffff; raw 24-bit {endian} endian"
                            ),
                            source_label=source_label,
                            predicted=predicted,
                        )
    return list(candidates.values())


def solve_affine_pair(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    modulus = MASK24 + 1
    dx = (x1 - x0) % modulus
    dy = (y1 - y0) % modulus
    if dx == 0:
        return []

    divisor = math.gcd(dx, modulus)
    if dy % divisor != 0:
        return []

    reduced_dx = dx // divisor
    reduced_dy = dy // divisor
    reduced_modulus = modulus // divisor
    inverse = pow(reduced_dx, -1, reduced_modulus)
    base_a = (reduced_dy * inverse) % reduced_modulus

    solutions = []
    for index in range(divisor):
        a_value = (base_a + index * reduced_modulus) % modulus
        b_value = (y0 - (a_value * x0)) % modulus
        solutions.append((a_value, b_value))
    return solutions


def evaluate_candidate(
    candidate: TransformCandidate,
    samples: list[FrequencySample],
) -> TransformMatch:
    return evaluate_predicted(candidate.name, candidate.source_label, candidate.predicted, samples)


def evaluate_predicted(
    name: str,
    source_label: str,
    predicted_values: tuple[bytes, ...],
    samples: list[FrequencySample],
) -> TransformMatch:
    failed = []
    matched = 0
    for sample, predicted in zip(samples, predicted_values):
        if predicted == sample.encoded:
            matched += 1
            continue
        failed.append(
            f"{sample.frequency_text}: expected {sample.encoded.hex(' ')}, got {predicted.hex(' ')}"
        )
    return TransformMatch(
        name=name,
        source_label=source_label,
        matched=matched,
        failed=tuple(failed),
    )


def search_transforms(
    samples: list[FrequencySample],
    near_threshold: int = NEAR_MATCH_THRESHOLD,
) -> tuple[list[TransformMatch], list[TransformMatch]]:
    best_by_description: dict[tuple[str, str], TransformMatch] = {}
    for result in generate_structural_matches(samples, near_threshold):
        key = (result.name, result.source_label)
        best_by_description[key] = result
    for candidate in solve_affine_candidates(samples):
        result = evaluate_candidate(candidate, samples)
        key = (result.name, result.source_label)
        best_by_description[key] = result

    exact = [match for match in best_by_description.values() if match.matched == len(samples)]
    near = [
        match
        for match in best_by_description.values()
        if near_threshold <= match.matched < len(samples)
    ]
    exact.sort(key=lambda match: (match.source_label, match.name))
    near.sort(key=lambda match: (-match.matched, match.source_label, match.name))
    return exact, near


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


def render_matches(title: str, matches: list[TransformMatch], sample_count: int) -> list[str]:
    lines = [f"## {title}", ""]
    if not matches:
        lines.append("No matches found.")
        return lines

    rows = []
    for match in matches:
        failed = "all samples matched" if not match.failed else "; ".join(match.failed)
        rows.append([match.source_label, match.name, f"{match.matched}/{sample_count}", failed])
    lines.extend(markdown_table(["Source", "Transform", "Matched", "Failed samples"], rows))
    return lines


def render_report(samples: list[FrequencySample], near_threshold: int = NEAR_MATCH_THRESHOLD) -> str:
    exact, near = search_transforms(samples, near_threshold)
    lines = [
        "# Frequency Transform Search",
        "",
        "Read-only exploratory report. Do not treat near matches as an encoding formula.",
        "",
        "## Samples",
    ]
    lines.extend(
        markdown_table(
            ["Frequency", "Hz", "Encoded bytes"],
            [
                [sample.frequency_text, str(sample.frequency_hz), sample.encoded.hex(" ")]
                for sample in samples
            ],
        )
    )
    lines.append("")
    if exact:
        lines.extend(render_matches("Exact Transforms", exact, len(samples)))
    else:
        lines.extend(["## Exact Transforms", "", "No exact transform matched all samples."])
    lines.append("")
    lines.extend(render_matches(f"Near Matches (at least {near_threshold} samples)", near, len(samples)))
    lines.append("")
    if exact:
        lines.append("All-sample matches above are exact candidates, not proof of the radio encoding.")
    else:
        lines.append("No encoding formula is claimed because no searched transform matched all samples exactly.")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    if args.near_threshold < 1:
        print("FAIL: --near-threshold must be >= 1")
        return 1
    samples = verified_samples()
    print(render_report(samples, args.near_threshold))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
