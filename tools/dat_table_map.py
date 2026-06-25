#!/usr/bin/env python3
"""Map candidate fixed-width KPG111 table records in a read-only way."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan a .dat file for candidate 32-byte table records."
    )
    parser.add_argument("dat_file", type=Path, help="Path to Program.dat")
    parser.add_argument(
        "--payload-start",
        type=lambda value: int(value, 0),
        default=0x40,
        help="Offset where payload starts (default: 0x40)",
    )
    parser.add_argument(
        "--record-size",
        type=int,
        default=32,
        help="Fixed record size to scan (default: 32)",
    )
    parser.add_argument(
        "--decode-xor",
        type=lambda value: int(value, 0),
        required=True,
        help="XOR byte used to decode record-name and numeric bytes",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Optional path to write machine-readable JSON results",
    )
    parser.add_argument(
        "--min-run",
        type=int,
        default=2,
        help="Minimum occupied records for a candidate run (default: 2)",
    )
    return parser.parse_args()


def decode_name(record: bytes, key: int) -> tuple[str, bytes]:
    decoded = bytes(byte ^ key for byte in record[1:15])
    name_bytes = decoded.split(b"\x00", 1)[0]
    return name_bytes.decode("ascii", errors="replace"), decoded


def printable_name(name: str) -> bool:
    if not name:
        return False
    return all(32 <= ord(char) <= 126 for char in name)


def numeric_field(record: bytes, key: int) -> dict[str, Any]:
    raw = record[19:21]
    decoded = bytes(byte ^ key for byte in raw)
    return {
        "raw_hex": raw.hex(" "),
        "decoded_hex": decoded.hex(" "),
        "little_endian": int.from_bytes(decoded, "little"),
    }


def is_empty_record(record: bytes) -> bool:
    return bool(record) and len(set(record)) == 1


def record_info(data: bytes, offset: int, record_size: int, key: int) -> dict[str, Any]:
    record = data[offset : offset + record_size]
    name, decoded_name_bytes = decode_name(record, key)
    numeric = numeric_field(record, key)
    empty = is_empty_record(record)
    printable = printable_name(name)
    occupied = printable and not empty
    return {
        "offset": offset,
        "record_size": len(record),
        "raw_hex": record.hex(" "),
        "decoded_name": name,
        "decoded_name_hex": decoded_name_bytes.hex(" "),
        "name_is_printable": printable,
        "empty": empty,
        "occupied_candidate": occupied,
        "numeric_raw_hex": numeric["raw_hex"],
        "numeric_decoded_hex": numeric["decoded_hex"],
        "numeric_little_endian": numeric["little_endian"],
    }


def scan_records(data: bytes, payload_start: int, record_size: int, key: int) -> list[dict[str, Any]]:
    records = []
    end = len(data) - ((len(data) - payload_start) % record_size)
    for offset in range(payload_start, end, record_size):
        records.append(record_info(data, offset, record_size, key))
    return records


def candidate_runs(records: list[dict[str, Any]], min_run: int) -> list[dict[str, Any]]:
    runs = []
    current: list[dict[str, Any]] = []
    record_size = records[0]["record_size"] if records else 0

    def flush() -> None:
        nonlocal current
        if len(current) >= min_run:
            start = current[0]["offset"]
            end = current[-1]["offset"] + record_size - 1
            next_records = records_by_offset.get(current[-1]["offset"] + record_size)
            empty_after = 0
            cursor = current[-1]["offset"] + record_size
            while cursor in records_by_offset and records_by_offset[cursor]["empty"]:
                empty_after += 1
                cursor += record_size
            runs.append(
                {
                    "start": start,
                    "end": end,
                    "record_count": len(current),
                    "empty_slots_after": empty_after,
                    "next_record": next_records,
                    "records": current,
                }
            )
        current = []

    records_by_offset = {record["offset"]: record for record in records}
    for record in records:
        if record["occupied_candidate"]:
            current.append(record)
            continue
        flush()
    flush()
    return runs


def analyze(path: Path, payload_start: int, record_size: int, key: int, min_run: int) -> dict[str, Any]:
    data = path.read_bytes()
    records = scan_records(data, payload_start, record_size, key)
    runs = candidate_runs(records, min_run)
    return {
        "schema": "kpg111-helper.table-map.v1",
        "file": {
            "path": str(path),
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        },
        "payload_start": payload_start,
        "record_size": record_size,
        "decode_xor": key,
        "record_count_scanned": len(records),
        "occupied_candidate_count": sum(1 for record in records if record["occupied_candidate"]),
        "empty_record_count": sum(1 for record in records if record["empty"]),
        "candidate_runs": runs,
        "records": records,
    }


def markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(row) + " |")


def render_markdown(result: dict[str, Any]) -> None:
    file_info = result["file"]
    print("# KPG111 Candidate Table Map")
    print()
    print("This is a read-only structural scan. Printable decoded names are evidence for candidate records, not proof of table purpose.")
    print()
    print("## File")
    print()
    print(f"- Path: `{file_info['path']}`")
    print(f"- Size: {file_info['size']} bytes")
    print(f"- SHA-256: `{file_info['sha256']}`")
    print(f"- Payload start: `0x{result['payload_start']:x}`")
    print(f"- Record size: {result['record_size']}")
    print(f"- Decode XOR: `0x{result['decode_xor']:02x}`")
    print(f"- Records scanned: {result['record_count_scanned']}")
    print(f"- Occupied candidates: {result['occupied_candidate_count']}")
    print(f"- Empty records: {result['empty_record_count']}")
    print()

    print("## Candidate Runs")
    rows = []
    for run in result["candidate_runs"]:
        next_record = run.get("next_record")
        next_summary = "none"
        if next_record:
            next_summary = (
                f"0x{next_record['offset']:08x} "
                f"empty={next_record['empty']} "
                f"name={next_record['decoded_name']!r}"
            )
        rows.append(
            [
                f"0x{run['start']:08x}-0x{run['end']:08x}",
                str(run["record_count"]),
                str(run["empty_slots_after"]),
                next_summary,
            ]
        )
    markdown_table(["Range", "Records", "Empty Slots After", "Next Record"], rows)
    print()

    for index, run in enumerate(result["candidate_runs"], start=1):
        print(f"## Run {index}: `0x{run['start']:08x}-0x{run['end']:08x}`")
        rows = []
        for record in run["records"]:
            rows.append(
                [
                    f"0x{record['offset']:08x}",
                    record["decoded_name"],
                    record["numeric_raw_hex"],
                    record["numeric_decoded_hex"],
                    str(record["numeric_little_endian"]),
                    "yes" if record["empty"] else "no",
                ]
            )
        markdown_table(
            [
                "Offset",
                "Decoded Name",
                "Raw +19/+20",
                "Decoded +19/+20",
                "LE Value",
                "Empty",
            ],
            rows,
        )
        print()

        tail_records = trailing_records(result["records"], run["end"], result["record_size"], count=8)
        print("### Following Records")
        rows = []
        for record in tail_records:
            rows.append(
                [
                    f"0x{record['offset']:08x}",
                    record["decoded_name"],
                    record["numeric_raw_hex"],
                    str(record["numeric_little_endian"]),
                    "yes" if record["empty"] else "no",
                    "yes" if record["name_is_printable"] else "no",
                ]
            )
        markdown_table(["Offset", "Decoded Name", "Raw +19/+20", "LE Value", "Empty", "Printable Name"], rows)
        print()


def trailing_records(
    records: list[dict[str, Any]], run_end: int, record_size: int, count: int
) -> list[dict[str, Any]]:
    by_offset = {record["offset"]: record for record in records}
    rows = []
    cursor = run_end + 1
    for _ in range(count):
        record = by_offset.get(cursor)
        if not record:
            break
        rows.append(record)
        cursor += record_size
    return rows


def main() -> int:
    args = parse_args()
    result = analyze(
        args.dat_file,
        args.payload_start,
        args.record_size,
        args.decode_xor,
        args.min_run,
    )
    if args.json:
        args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    render_markdown(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
