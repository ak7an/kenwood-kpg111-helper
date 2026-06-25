#!/usr/bin/env python3
"""Check that a KPG111 DAT file round-trips byte-for-byte unchanged."""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.project import KPG111Project


CONTEXT_BYTES = 16


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse a .dat file, write it back unchanged, and compare bytes."
    )
    parser.add_argument("dat_file", type=Path, help="Input KPG111 .dat file")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output .dat path. If omitted, a temporary file is used and removed after comparison.",
    )
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        default=0x5B,
        help="Decode key used by existing table parser (default: 0x5b)",
    )
    return parser.parse_args()


def first_difference(left: bytes, right: bytes) -> int | None:
    shared = min(len(left), len(right))
    for offset in range(shared):
        if left[offset] != right[offset]:
            return offset
    if len(left) != len(right):
        return shared
    return None


def hex_context(data: bytes, center: int, context: int = CONTEXT_BYTES) -> str:
    start = max(0, center - context)
    end = min(len(data), center + context + 1)
    return " ".join(f"{byte:02x}" for byte in data[start:end])


def byte_at(data: bytes, offset: int) -> str:
    if offset >= len(data):
        return "<EOF>"
    return f"0x{data[offset]:02x}"


def report_failure(original: bytes, output: bytes, diff_offset: int) -> None:
    print("FAIL")
    print(f"Original size: {len(original)}")
    print(f"Output size: {len(output)}")
    print(f"First differing offset: 0x{diff_offset:08x} ({diff_offset})")
    print(f"Original byte: {byte_at(original, diff_offset)}")
    print(f"Output byte: {byte_at(output, diff_offset)}")
    print(f"Original context: {hex_context(original, diff_offset)}")
    print(f"Output context:   {hex_context(output, diff_offset)}")


def temporary_output_path() -> Path:
    handle = tempfile.NamedTemporaryFile(prefix="kpg111_roundtrip_", suffix=".dat", delete=False)
    try:
        return Path(handle.name)
    finally:
        handle.close()


def main() -> int:
    args = parse_args()
    output_path = args.output or temporary_output_path()
    remove_output = args.output is None

    try:
        project = KPG111Project().load_program(args.dat_file, args.decode_key)
        project.write_bytes(output_path)

        original = args.dat_file.read_bytes()
        output = output_path.read_bytes()
        diff = first_difference(original, output)
        if diff is None:
            print("PASS")
            print(f"Input: {args.dat_file}")
            print(f"Output: {output_path}")
            print(f"Size: {len(original)}")
            return 0

        report_failure(original, output, diff)
        print(f"Input: {args.dat_file}")
        print(f"Output: {output_path}")
        return 1
    finally:
        if remove_output:
            output_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
