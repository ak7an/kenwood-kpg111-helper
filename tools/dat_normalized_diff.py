#!/usr/bin/env python3
"""Compare DAT files after normalizing the right payload by dominant XOR."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import sys


HEADER_SIZE = 0x40
DEFAULT_LIMIT = 200


@dataclass(frozen=True)
class NormalizedDifference:
    offset: int
    left: int
    right_raw: int
    right_normalized: int


@dataclass(frozen=True)
class NormalizedDiffResult:
    header_differing_bytes: int
    payload_compared_bytes: int
    dominant_xor_mask: int | None
    normalized_differing_bytes: int
    differences: list[NormalizedDifference]


def parse_int(value: str) -> int:
    try:
        return int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer: {value!r}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare same-size DAT files after dominant payload XOR normalization."
    )
    parser.add_argument("left", type=Path, help="Left/baseline DAT file")
    parser.add_argument("right", type=Path, help="Right DAT file to normalize")
    parser.add_argument(
        "--header-size",
        type=parse_int,
        default=HEADER_SIZE,
        help="Bytes to treat as header, decimal or hex (default: 0x40)",
    )
    parser.add_argument(
        "--limit",
        type=parse_int,
        default=DEFAULT_LIMIT,
        help="Maximum normalized differences to display (default: 200)",
    )
    return parser.parse_args()


def validate_args(header_size: int, limit: int) -> None:
    if header_size < 0:
        raise ValueError("--header-size must be >= 0")
    if limit < 0:
        raise ValueError("--limit must be >= 0")


def dominant_payload_xor(left: bytes, right: bytes, payload_start: int) -> int | None:
    if payload_start >= len(left):
        return None
    counts = Counter(
        left[offset] ^ right[offset]
        for offset in range(payload_start, len(left))
    )
    return counts.most_common(1)[0][0]


def normalized_diff(
    left: bytes,
    right: bytes,
    header_size: int = HEADER_SIZE,
) -> NormalizedDiffResult:
    if len(left) != len(right):
        raise ValueError(f"files must be the same size: left={len(left)} right={len(right)}")

    header_end = min(header_size, len(left))
    header_differing = sum(1 for offset in range(header_end) if left[offset] != right[offset])
    payload_start = min(header_size, len(left))
    payload_compared = len(left) - payload_start
    mask = dominant_payload_xor(left, right, payload_start)

    differences: list[NormalizedDifference] = []
    if mask is not None:
        for offset in range(payload_start, len(left)):
            right_normalized = right[offset] ^ mask
            if left[offset] != right_normalized:
                differences.append(
                    NormalizedDifference(
                        offset=offset,
                        left=left[offset],
                        right_raw=right[offset],
                        right_normalized=right_normalized,
                    )
                )

    return NormalizedDiffResult(
        header_differing_bytes=header_differing,
        payload_compared_bytes=payload_compared,
        dominant_xor_mask=mask,
        normalized_differing_bytes=len(differences),
        differences=differences,
    )


def render_result(
    left_path: Path,
    right_path: Path,
    result: NormalizedDiffResult,
    header_size: int,
    limit: int,
) -> str:
    displayed = result.differences[:limit]
    mask_text = "none" if result.dominant_xor_mask is None else f"0x{result.dominant_xor_mask:02x}"
    lines = [
        "DAT Normalized Diff Report",
        f"Left: {left_path}",
        f"Right: {right_path}",
        f"Header size: 0x{header_size:08x} ({header_size})",
        f"Header differing bytes: {result.header_differing_bytes}",
        f"Payload bytes compared: {result.payload_compared_bytes}",
        f"Dominant XOR mask: {mask_text}",
        f"Normalized differing bytes: {result.normalized_differing_bytes}",
        "",
        "Normalized Differences",
        "| offset | left | right_raw | right_normalized |",
        "| --- | --- | --- | --- |",
    ]
    if not displayed:
        lines.append("| none | none | none | none |")
    else:
        for diff in displayed:
            lines.append(
                f"| 0x{diff.offset:08x} | 0x{diff.left:02x} | "
                f"0x{diff.right_raw:02x} | 0x{diff.right_normalized:02x} |"
            )
    if len(displayed) < result.normalized_differing_bytes:
        lines.append(
            f"... {result.normalized_differing_bytes - len(displayed)} more normalized diffs not shown"
        )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        validate_args(args.header_size, args.limit)
        left = args.left.read_bytes()
        right = args.right.read_bytes()
        result = normalized_diff(left, right, args.header_size)
        print(render_result(args.left, args.right, result, args.header_size, args.limit))
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
