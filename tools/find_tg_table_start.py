#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

REC_SIZE = 32
NAME_START = 1
NAME_LEN = 14
NUM_START = 19
NUM_LEN = 2
TG_XOR = 0x5151
EMPTY_VALUES = {0xae, 0xc7}


def decode_name(rec: bytes, key: int) -> str:
    raw = bytes(b ^ key for b in rec[NAME_START:NAME_START + NAME_LEN])
    return raw.split(b"\x00", 1)[0].decode("ascii", "ignore")


def valid_tg(rec: bytes, key: int) -> bool:
    if len(rec) != REC_SIZE:
        return False
    if len(set(rec)) == 1 and rec[0] in EMPTY_VALUES:
        return False

    name = decode_name(rec, key)
    m = re.match(r"^(\d+)\b", name)
    if not m:
        return False

    name_id = int(m.group(1))
    numeric_id = int.from_bytes(rec[NUM_START:NUM_START + NUM_LEN], "little") ^ TG_XOR
    return name_id == numeric_id


def score_start(data: bytes, start: int, key: int, max_records: int) -> tuple[int, int, list[int]]:
    valid_slots = []
    empty = 0

    for slot in range(max_records):
        off = start + slot * REC_SIZE
        rec = data[off:off+REC_SIZE]
        if len(rec) != REC_SIZE:
            break
        if len(set(rec)) == 1 and rec[0] in EMPTY_VALUES:
            empty += 1
            continue
        if valid_tg(rec, key):
            valid_slots.append(slot)

    return len(valid_slots), empty, valid_slots


def main() -> None:
    ap = argparse.ArgumentParser(description="Find likely KPG111 Talk Group table starts")
    ap.add_argument("dat", type=Path)
    ap.add_argument("--key", type=lambda x: int(x, 0), default=0x51)
    ap.add_argument("--from-offset", type=lambda x: int(x, 0), default=0x13000)
    ap.add_argument("--to-offset", type=lambda x: int(x, 0), default=0x18200)
    ap.add_argument("--max-records", type=int, default=400)
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    data = args.dat.read_bytes()

    rows = []
    for start in range(args.from_offset, args.to_offset, REC_SIZE):
        valid, empty, slots = score_start(data, start, args.key, args.max_records)
        if valid:
            first = min(slots)
            last = max(slots)
            rows.append((valid, empty, first, last, start, slots))

    rows.sort(reverse=True)

    print(f"DAT: {args.dat}")
    print(f"text key: 0x{args.key:02x}")
    print()
    print("valid empty first last start")
    for valid, empty, first, last, start, slots in rows[:args.top]:
        print(f"{valid:5d} {empty:5d} {first:5d} {last:4d} 0x{start:05x}")


if __name__ == "__main__":
    main()
