#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

TG_START = 0x14F80
REC_SIZE = 32
COUNT = 400
EMPTY = 0xAE
NAME_START = 1
NAME_LEN = 14
DECODE_KEY = 0x51


def decode_name(raw: bytes, key: int = DECODE_KEY) -> str:
    decoded = bytes(b ^ key for b in raw)
    decoded = decoded.split(b"\x00", 1)[0]
    out = []
    for b in decoded:
        if 32 <= b <= 126:
            out.append(chr(b))
        else:
            out.append(f"\\x{b:02x}")
    return "".join(out)


def classify_record(rec: bytes) -> str:
    if all(b == EMPTY for b in rec):
        return "empty"

    name = decode_name(rec[NAME_START:NAME_START + NAME_LEN])
    name_printable = bool(name) and "\\x" not in name

    id0 = rec[0x13]
    id1 = rec[0x14]
    id_complete = id0 != EMPTY and id1 != EMPTY

    if name_printable and id_complete:
        return "tg-shape"
    if name_printable and not id_complete:
        return "name-no-full-id"
    return "reserved/junk"


def calc_id_13_14(rec: bytes) -> int:
    return int.from_bytes(rec[0x13:0x15], "little") ^ 0xFFFF


def print_header() -> None:
    cols = " ".join(f"{i:02X}" for i in range(REC_SIZE))
    print(f"{'slot':>4} {'off':>7} {'class':<15} {'id13_14':>7} {'name':<18} {cols}")


def print_record(slot: int, data: bytes) -> None:
    off = TG_START + slot * REC_SIZE
    rec = data[off:off + REC_SIZE]
    name = decode_name(rec[NAME_START:NAME_START + NAME_LEN])
    cls = classify_record(rec)
    id_calc = calc_id_13_14(rec)
    hx = " ".join(f"{b:02x}" for b in rec)
    print(f"{slot:4d} 0x{off:05x} {cls:<15} {id_calc:7d} {name[:18]:<18} {hx}")


def parse_slots(text: str) -> list[int]:
    slots: list[int] = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            slots.extend(range(int(a), int(b) + 1))
        else:
            slots.append(int(part))
    return slots


def main() -> None:
    ap = argparse.ArgumentParser(description="Read-only TG record byte matrix")
    ap.add_argument("dat", type=Path)
    ap.add_argument(
        "--slots",
        default="280-299,351-353",
        help="Comma-separated slots/ranges, default: 280-299,351-353",
    )
    args = ap.parse_args()

    data = args.dat.read_bytes()
    slots = parse_slots(args.slots)

    print_header()
    for slot in slots:
        if not 0 <= slot < COUNT:
            raise SystemExit(f"slot out of range: {slot}")
        print_record(slot, data)


if __name__ == "__main__":
    main()
