#!/usr/bin/env python3
"""Build a read-only-derived 100-channel KPG111 ITM from a text template."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys


CHANNEL_SECTION = "NXCNVDATA"
CHANNEL_COUNT = 100
START_MHZ = 146.000000
STEP_MHZ = 0.010000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a 100 analog wide channel ITM from a KPG111 text template."
    )
    parser.add_argument("template", type=Path, help="Input .itm template")
    parser.add_argument("output", type=Path, help="Output .itm path")
    return parser.parse_args()


def detect_newline(raw: bytes) -> str:
    if b"\r\n" in raw:
        return "\r\n"
    if b"\n" in raw:
        return "\n"
    return "\r\n"


def read_text(path: Path) -> tuple[str, str]:
    raw = path.expanduser().read_bytes()
    if b"\x00" in raw:
        raise ValueError(f"{path} appears to be binary; found NUL bytes")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path} is not ASCII text") from exc
    return text, detect_newline(raw)


def parse_csv_line(line: str) -> list[str]:
    return next(csv.reader([line]))


def format_csv_row(row: list[str]) -> str:
    output = []
    for value in row:
        if any(char in value for char in {",", '"', "\r", "\n"}):
            output.append('"' + value.replace('"', '""') + '"')
        else:
            output.append(value)
    return ",".join(output)


def find_channel_header(lines: list[str]) -> tuple[int, list[str]]:
    for index, line in enumerate(lines):
        if not line.startswith("$$,"):
            continue
        fields = parse_csv_line(line)
        if len(fields) > 1 and fields[1] == CHANNEL_SECTION:
            return index, fields
    raise ValueError(f"could not find $$,{CHANNEL_SECTION} section header")


def find_section_end(lines: list[str], start_index: int) -> int:
    for index in range(start_index + 1, len(lines)):
        if lines[index].startswith("$$,"):
            section_comment = index - 1
            if section_comment >= 0 and lines[section_comment].startswith("//"):
                return section_comment
            return index
    return len(lines)


def channel_row(header: list[str], channel_number: int) -> list[str]:
    values = {
        "$$": "$",
        "": "",
        "ZN": "1",
        "CH": str(channel_number),
        "RXF": f"{START_MHZ + (channel_number - 1) * STEP_MHZ:.6f}",
        "TXF": f"{START_MHZ + (channel_number - 1) * STEP_MHZ:.6f}",
        "CHTYPE": "AN",
        "TXMODE": "AN",
        "RXSIG": "None",
        "TXSIG": "None",
        "RXRAN": "None",
        "TXRAN": "None",
        "NAME": f"CH{channel_number:03d}",
        "CHSPAN": "WI",
        "CHSPNX": "NA",
    }
    row: list[str] = []
    for index, field in enumerate(header):
        if index == 0:
            row.append("$")
        elif field in values:
            row.append(values[field])
        else:
            row.append("")
    return row


def build_itm(template_text: str, newline: str) -> str:
    lines = template_text.splitlines()
    header_index, header = find_channel_header(lines)
    section_end = find_section_end(lines, header_index)
    rows = [format_csv_row(channel_row(header, channel)) for channel in range(1, CHANNEL_COUNT + 1)]
    output_lines = lines[: header_index + 1] + rows + lines[section_end:]
    return newline.join(output_lines) + newline


def main() -> int:
    args = parse_args()
    try:
        text, newline = read_text(args.template)
        output = build_itm(text, newline)
        args.output.expanduser().write_text(output, encoding="ascii", newline="")
        return 0
    except (OSError, ValueError, csv.Error) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
