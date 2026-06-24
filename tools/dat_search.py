#!/usr/bin/env python3
"""Search a Program.dat file for strings and integer encodings."""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search a .dat file for strings and integer byte encodings."
    )
    parser.add_argument("dat_file", type=Path, help="Path to Program.dat")
    parser.add_argument("value", help="String or decimal integer to search for")
    parser.add_argument(
        "--case-insensitive",
        action="store_true",
        help="Use case-insensitive ASCII and UTF-16LE string searches",
    )
    return parser.parse_args()


def find_all(data: bytes, needle: bytes) -> list[int]:
    offsets = []
    if not needle:
        return offsets
    start = 0
    while True:
        offset = data.find(needle, start)
        if offset == -1:
            return offsets
        offsets.append(offset)
        start = offset + 1


def parse_decimal_integer(value: str) -> int | None:
    stripped = value.strip()
    if stripped.startswith("+"):
        stripped = stripped[1:]
    if not stripped.isdecimal():
        return None
    return int(stripped, 10)


def add_string_matches(
    matches: list[tuple[int, str, str]],
    data: bytes,
    value: str,
    case_insensitive: bool,
) -> None:
    ascii_needle = value.encode("ascii", errors="ignore")
    utf16le_needle = value.encode("utf-16le")

    if case_insensitive:
        ascii_offsets = find_all(data.lower(), ascii_needle.lower())
        utf16le_offsets = find_all(lower_ascii_utf16le_bytes(data), utf16le_needle.lower())
    else:
        ascii_offsets = find_all(data, ascii_needle)
        utf16le_offsets = find_all(data, utf16le_needle)

    for offset in ascii_offsets:
        matches.append((offset, "ASCII string", ascii_needle.hex(" ")))
    for offset in utf16le_offsets:
        matches.append((offset, "UTF-16LE string", utf16le_needle.hex(" ")))


def lower_ascii_utf16le_bytes(data: bytes) -> bytes:
    lowered = bytearray(data)
    for offset in range(0, len(data) - 1, 2):
        if data[offset + 1] == 0 and 65 <= data[offset] <= 90:
            lowered[offset] = data[offset] + 32
    return bytes(lowered)


def integer_encodings(value: int) -> list[tuple[str, bytes]]:
    encodings = []
    decimal_ascii = str(value).encode("ascii")
    encodings.append(("decimal ASCII", decimal_ascii))

    if 0 <= value <= 0xFFFF:
        encodings.append(("little-endian uint16", struct.pack("<H", value)))
        encodings.append(("big-endian uint16", struct.pack(">H", value)))
    if 0 <= value <= 0xFFFFFFFF:
        encodings.append(("little-endian uint32", struct.pack("<I", value)))
        encodings.append(("big-endian uint32", struct.pack(">I", value)))
    return encodings


def add_integer_matches(
    matches: list[tuple[int, str, str]],
    data: bytes,
    value: int,
) -> None:
    for label, needle in integer_encodings(value):
        for offset in find_all(data, needle):
            matches.append((offset, label, needle.hex(" ")))


def main() -> int:
    args = parse_args()
    data = args.dat_file.read_bytes()
    matches: list[tuple[int, str, str]] = []

    add_string_matches(matches, data, args.value, args.case_insensitive)
    integer = parse_decimal_integer(args.value)
    if integer is not None:
        add_integer_matches(matches, data, integer)

    matches.sort(key=lambda item: (item[0], item[1], item[2]))

    print("== Search ==")
    print(f"file: {args.dat_file}")
    print(f"size: {len(data)} bytes")
    print(f"value: {args.value!r}")
    if integer is not None:
        print(f"decimal integer: {integer}")

    print("\n== Matches ==")
    if not matches:
        print("no matches")
        return 1

    for offset, interpretation, encoded in matches:
        print(f"0x{offset:08x}  {interpretation:<22}  bytes={encoded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
