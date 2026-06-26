#!/usr/bin/env python3
"""Read-only DAT diff that masks known filler-byte substitutions."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_HEADER_SIZE = 0x40
DEFAULT_LIMIT = 200
DEFAULT_IGNORE_PAIR = (0xBE, 0xC6)


@dataclass(frozen=True)
class MeaningfulDifference:
    offset: int
    left: int
    right: int


@dataclass(frozen=True)
class MaskedDiffResult:
    total_compared: int
    raw_differing: int
    ignored_filler_substitutions: int
    meaningful_differing: int
    meaningful_differences: list[MeaningfulDifference]


def parse_int(value: str) -> int:
    try:
        return int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer: {value!r}") from exc


def parse_byte(value: str) -> int:
    text = value.strip()
    try:
        byte = int(text, 16) if not text.lower().startswith("0x") else int(text, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid byte value: {value!r}") from exc
    if byte < 0 or byte > 0xFF:
        raise argparse.ArgumentTypeError(f"byte value out of range: {value!r}")
    return byte


def parse_ignore_pair(value: str) -> tuple[int, int]:
    parts = value.split(":")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("--ignore-pair must be A:B")
    left = parse_byte(parts[0])
    right = parse_byte(parts[1])
    return left, right


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two DAT files while ignoring known filler-byte substitutions."
    )
    parser.add_argument("left", type=Path, help="Left/baseline DAT file")
    parser.add_argument("right", type=Path, help="Right/modified DAT file")
    parser.add_argument(
        "--header-size",
        type=parse_int,
        default=DEFAULT_HEADER_SIZE,
        help="Bytes to skip before comparing, decimal or hex (default: 0x40)",
    )
    parser.add_argument(
        "--ignore-pair",
        type=parse_ignore_pair,
        default=DEFAULT_IGNORE_PAIR,
        help="Equivalent filler byte pair, e.g. BE:C6 or 0xBE:0xC6 (default: BE:C6)",
    )
    parser.add_argument(
        "--limit",
        type=parse_int,
        default=DEFAULT_LIMIT,
        help="Maximum meaningful differences to display (default: 200)",
    )
    return parser.parse_args()


def validate_args(header_size: int, limit: int) -> None:
    if header_size < 0:
        raise ValueError("--header-size must be >= 0")
    if limit < 0:
        raise ValueError("--limit must be >= 0")


def is_ignored_substitution(left: int, right: int, ignore_pair: tuple[int, int]) -> bool:
    first, second = ignore_pair
    return (left == first and right == second) or (left == second and right == first)


def masked_diff(
    left: bytes,
    right: bytes,
    header_size: int = DEFAULT_HEADER_SIZE,
    ignore_pair: tuple[int, int] = DEFAULT_IGNORE_PAIR,
) -> MaskedDiffResult:
    if len(left) != len(right):
        raise ValueError(f"files must be the same size: left={len(left)} right={len(right)}")
    if header_size > len(left):
        total_compared = 0
        start = len(left)
    else:
        total_compared = len(left) - header_size
        start = header_size

    raw_differing = 0
    ignored = 0
    meaningful: list[MeaningfulDifference] = []
    for offset in range(start, len(left)):
        left_byte = left[offset]
        right_byte = right[offset]
        if left_byte == right_byte:
            continue
        raw_differing += 1
        if is_ignored_substitution(left_byte, right_byte, ignore_pair):
            ignored += 1
            continue
        meaningful.append(MeaningfulDifference(offset, left_byte, right_byte))

    return MaskedDiffResult(
        total_compared=total_compared,
        raw_differing=raw_differing,
        ignored_filler_substitutions=ignored,
        meaningful_differing=len(meaningful),
        meaningful_differences=meaningful,
    )


def render_result(
    left_path: Path,
    right_path: Path,
    result: MaskedDiffResult,
    header_size: int,
    ignore_pair: tuple[int, int],
    limit: int,
) -> str:
    displayed = result.meaningful_differences[:limit]
    lines = [
        "DAT Masked Diff Report",
        f"Left: {left_path}",
        f"Right: {right_path}",
        f"Header skipped: 0x{header_size:08x} ({header_size})",
        f"Ignored filler pair: 0x{ignore_pair[0]:02x}<->0x{ignore_pair[1]:02x}",
        f"Total compared bytes: {result.total_compared}",
        f"Raw differing bytes: {result.raw_differing}",
        f"Ignored filler substitutions: {result.ignored_filler_substitutions}",
        f"Meaningful differing bytes: {result.meaningful_differing}",
        "",
        "Meaningful Differences",
        "| offset | left | right |",
        "| --- | --- | --- |",
    ]
    if not displayed:
        lines.append("| none | none | none |")
    else:
        for diff in displayed:
            lines.append(f"| 0x{diff.offset:08x} | 0x{diff.left:02x} | 0x{diff.right:02x} |")
    if len(displayed) < result.meaningful_differing:
        lines.append(f"... {result.meaningful_differing - len(displayed)} more meaningful diffs not shown")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        validate_args(args.header_size, args.limit)
        left = args.left.read_bytes()
        right = args.right.read_bytes()
        result = masked_diff(left, right, args.header_size, args.ignore_pair)
        print(render_result(args.left, args.right, result, args.header_size, args.ignore_pair, args.limit))
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
