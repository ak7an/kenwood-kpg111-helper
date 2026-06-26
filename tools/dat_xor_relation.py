#!/usr/bin/env python3
"""Report whether two DAT payloads have a constant XOR relationship."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import sys


HEADER_SIZE = 0x40
DEFAULT_MISMATCH_LIMIT = 20


@dataclass(frozen=True)
class XorMismatch:
    offset: int
    left: int
    right: int
    xor_value: int


@dataclass(frozen=True)
class XorRelation:
    header_differing_bytes: int
    payload_compared_bytes: int
    constant: bool
    xor_value: int | None
    dominant_xor_value: int | None
    dominant_xor_count: int
    dominant_xor_percent: float
    mismatches: list[XorMismatch]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether two DAT payloads differ by a constant XOR value."
    )
    parser.add_argument("left", type=Path, help="Left DAT file")
    parser.add_argument("right", type=Path, help="Right DAT file")
    parser.add_argument(
        "--mismatch-limit",
        type=int,
        default=DEFAULT_MISMATCH_LIMIT,
        help="Maximum mismatches to display when XOR is not constant (default: 20)",
    )
    return parser.parse_args()


def xor_relation(left: bytes, right: bytes, payload_start: int = HEADER_SIZE) -> XorRelation:
    if len(left) != len(right):
        raise ValueError(f"files must be the same size: left={len(left)} right={len(right)}")

    header_end = min(payload_start, len(left))
    header_differing = sum(1 for index in range(header_end) if left[index] != right[index])
    if payload_start >= len(left):
        return XorRelation(header_differing, 0, True, None, None, 0, 0.0, [])

    observed = [
        left[offset] ^ right[offset]
        for offset in range(payload_start, len(left))
    ]
    counts = Counter(observed)
    dominant_xor, dominant_count = counts.most_common(1)[0]
    dominant_percent = dominant_count / len(observed) * 100.0
    mismatches: list[XorMismatch] = []
    for offset in range(payload_start, len(left)):
        xor_value = left[offset] ^ right[offset]
        if xor_value != dominant_xor:
            mismatches.append(XorMismatch(offset, left[offset], right[offset], xor_value))

    return XorRelation(
        header_differing_bytes=header_differing,
        payload_compared_bytes=len(left) - payload_start,
        constant=not mismatches,
        xor_value=dominant_xor if not mismatches else None,
        dominant_xor_value=dominant_xor,
        dominant_xor_count=dominant_count,
        dominant_xor_percent=dominant_percent,
        mismatches=mismatches,
    )


def render_relation(
    left_path: Path,
    right_path: Path,
    relation: XorRelation,
    mismatch_limit: int,
) -> str:
    lines = [
        "DAT XOR Relation Report",
        f"Left: {left_path}",
        f"Right: {right_path}",
        f"Header size: 0x{HEADER_SIZE:02x} ({HEADER_SIZE})",
        f"Header differing bytes: {relation.header_differing_bytes}",
        f"Payload compared bytes: {relation.payload_compared_bytes}",
    ]
    if relation.payload_compared_bytes == 0:
        lines.append("Payload XOR relation: empty payload")
        return "\n".join(lines)
    lines.append(
        "Dominant payload XOR: "
        f"0x{relation.dominant_xor_value:02x} "
        f"({relation.dominant_xor_count}/{relation.payload_compared_bytes}, "
        f"{relation.dominant_xor_percent:.2f}%)"
    )
    if relation.constant:
        lines.append(f"Payload XOR relation: constant 0x{relation.xor_value:02x}")
        return "\n".join(lines)

    displayed = relation.mismatches[:mismatch_limit]
    lines.extend(
        [
            "Payload XOR relation: not constant",
            f"Mismatches relative to dominant XOR: {len(relation.mismatches)}",
            "",
            "| offset | left | right | observed_xor |",
            "| --- | --- | --- | --- |",
        ]
    )
    for mismatch in displayed:
        lines.append(
            f"| 0x{mismatch.offset:08x} | 0x{mismatch.left:02x} | "
            f"0x{mismatch.right:02x} | 0x{mismatch.xor_value:02x} |"
        )
    if len(displayed) < len(relation.mismatches):
        lines.append(f"... {len(relation.mismatches) - len(displayed)} more mismatches not shown")
    return "\n".join(lines)


def validate_mismatch_limit(limit: int) -> None:
    if limit < 0:
        raise ValueError("--mismatch-limit must be >= 0")


def main() -> int:
    args = parse_args()
    try:
        validate_mismatch_limit(args.mismatch_limit)
        left = args.left.read_bytes()
        right = args.right.read_bytes()
        relation = xor_relation(left, right)
        print(render_relation(args.left, args.right, relation, args.mismatch_limit))
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
