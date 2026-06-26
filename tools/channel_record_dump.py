#!/usr/bin/env python3
"""Dump raw candidate channel records from a DAT file without decoding them."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import BinaryIO


HEADER_SIZE = 0x40
DEFAULT_START = 0x5E80
DEFAULT_STRIDE = 0x40
DEFAULT_COUNT = 16
RECORD_SIZE = 0x40
FREQUENCY_SIZE = 3
RX_FREQUENCY_OFFSET = 0x05
TX_FREQUENCY_OFFSET = 0x09


def parse_int(value: str) -> int:
    try:
        return int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"expected a decimal or hexadecimal integer, got {value!r}"
        ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print raw candidate channel records from a DAT file."
    )
    parser.add_argument("dat_file", type=Path, help="DAT file to inspect")
    parser.add_argument(
        "--start",
        type=parse_int,
        default=DEFAULT_START,
        help=f"Channel table start offset, decimal or hex (default: 0x{DEFAULT_START:x})",
    )
    parser.add_argument(
        "--stride",
        type=parse_int,
        default=DEFAULT_STRIDE,
        help=f"Channel record stride, decimal or hex (default: 0x{DEFAULT_STRIDE:x})",
    )
    parser.add_argument(
        "--count",
        type=parse_int,
        default=DEFAULT_COUNT,
        help=f"Number of records to dump (default: {DEFAULT_COUNT})",
    )
    return parser.parse_args()


def validate_args(start: int, stride: int, count: int) -> None:
    if start < 0:
        raise ValueError("--start must be >= 0")
    if stride <= 0:
        raise ValueError("--stride must be > 0")
    if count < 0:
        raise ValueError("--count must be >= 0")


def ascii_safe(data: bytes) -> str:
    return "".join(chr(byte) if 0x20 <= byte <= 0x7E else "." for byte in data)


def hex_rows(data: bytes) -> list[str]:
    return [data[offset : offset + 16].hex(" ") for offset in range(0, RECORD_SIZE, 16)]


def record_at(dat_file: BinaryIO, offset: int) -> bytes:
    dat_file.seek(offset)
    record = dat_file.read(RECORD_SIZE)
    if len(record) != RECORD_SIZE:
        raise ValueError(
            f"record at 0x{offset:08x} is incomplete: expected 0x{RECORD_SIZE:x} "
            f"bytes, found 0x{len(record):x}"
        )
    return record


def dump_record(channel: int, offset: int, record: bytes) -> None:
    rx = record[RX_FREQUENCY_OFFSET : RX_FREQUENCY_OFFSET + FREQUENCY_SIZE]
    tx = record[TX_FREQUENCY_OFFSET : TX_FREQUENCY_OFFSET + FREQUENCY_SIZE]

    print(f"Channel {channel}")
    print(f"Record start: 0x{offset:08x}")
    print("Raw bytes:")
    for row in hex_rows(record):
        print(f"  {row}")
    print(f"RX frequency bytes (+0x{RX_FREQUENCY_OFFSET:02x}, length {FREQUENCY_SIZE}): {rx.hex(' ')}")
    print(f"TX frequency bytes (+0x{TX_FREQUENCY_OFFSET:02x}, length {FREQUENCY_SIZE}): {tx.hex(' ')}")
    print(f"ASCII-safe: {ascii_safe(record)}")


def main() -> int:
    args = parse_args()
    try:
        validate_args(args.start, args.stride, args.count)
        print(f"DAT file: {args.dat_file}")
        print(f"Header size: 0x{HEADER_SIZE:x}")
        print(f"Channel table start: 0x{args.start:08x}")
        print(f"Record stride: 0x{args.stride:x}")
        print(f"Record count: {args.count}")
        print()
        with args.dat_file.open("rb") as dat_file:
            for index in range(args.count):
                offset = args.start + (index * args.stride)
                dump_record(index + 1, offset, record_at(dat_file, offset))
                if index != args.count - 1:
                    print()
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
