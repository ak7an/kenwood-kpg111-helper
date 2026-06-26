#!/usr/bin/env python3
"""Report uniform-byte runs in the DAT payload without modifying files."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


HEADER_SIZE = 0x40
DEFAULT_MIN_RUN = 16


@dataclass(frozen=True)
class ByteRun:
    start: int
    end: int
    value: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only DAT payload uniform-byte run diagnostic."
    )
    parser.add_argument("dat_files", nargs="+", type=Path, help="Input .dat file(s)")
    parser.add_argument(
        "--min-run",
        type=int,
        default=DEFAULT_MIN_RUN,
        help="Minimum uniform-byte run length to report (default: 16)",
    )
    return parser.parse_args()


def find_byte_runs(data: bytes, payload_start: int = HEADER_SIZE) -> list[ByteRun]:
    if payload_start >= len(data):
        return []

    runs: list[ByteRun] = []
    start = payload_start
    value = data[start]
    for offset in range(payload_start + 1, len(data)):
        if data[offset] == value:
            continue
        runs.append(ByteRun(start, offset - 1, value))
        start = offset
        value = data[offset]
    runs.append(ByteRun(start, len(data) - 1, value))
    return runs


def filtered_runs(data: bytes, min_run: int) -> list[ByteRun]:
    return [run for run in find_byte_runs(data) if run.length >= min_run]


def first_non_long_filler_offset(data: bytes, min_run: int) -> int | None:
    payload_runs = find_byte_runs(data)
    if not payload_runs:
        return None

    for run in payload_runs:
        if run.length < min_run:
            return run.start
    return len(data)


def markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(row) + " |")


def render_file(path: Path, min_run: int) -> None:
    data = path.read_bytes()
    runs = filtered_runs(data, min_run)
    first_non_filler = first_non_long_filler_offset(data, min_run)

    print(f"## `{path}`")
    print()
    print(f"- File size: {len(data)} bytes")
    print(f"- Header bytes skipped: 0x{HEADER_SIZE:02x} ({HEADER_SIZE})")
    print(f"- Payload bytes scanned: {max(0, len(data) - HEADER_SIZE)}")
    print(f"- Minimum run length: {min_run}")
    if first_non_filler is None:
        print("- First non-long-filler offset after payload start: none (no payload)")
    elif first_non_filler == len(data):
        print("- First non-long-filler offset after payload start: none (payload is all long uniform runs)")
    else:
        print(
            "- First non-long-filler offset after payload start: "
            f"0x{first_non_filler:08x} ({first_non_filler})"
        )
    print()
    markdown_table(
        ["offset_start", "offset_end", "length", "byte"],
        [
            [
                f"0x{run.start:08x}",
                f"0x{run.end:08x}",
                str(run.length),
                f"0x{run.value:02x}",
            ]
            for run in runs
        ],
    )
    print()


def validate_min_run(min_run: int) -> None:
    if min_run < 1:
        raise SystemExit("--min-run must be >= 1")


def main() -> int:
    args = parse_args()
    validate_min_run(args.min_run)

    print("# DAT Payload Uniform Run Report")
    print()
    print("Read-only diagnostic. This reports filler-like byte runs only and does not infer fields.")
    print()
    for path in args.dat_files:
        render_file(path, args.min_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
