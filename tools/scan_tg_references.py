#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

TG_START = 0x14F80
REC_SIZE = 32
DEFAULT_TG_COUNT = 400
NAME_START = 1
NAME_LEN = 14
TEXT_KEY = 0x51
TG_NUMERIC_XOR = 0x5151


def decode_name(record: bytes, key: int) -> str:
    raw = bytes(b ^ key for b in record[NAME_START:NAME_START + NAME_LEN])
    return raw.split(b"\x00", 1)[0].decode("ascii", "ignore")


def collect_tgs(data: bytes, count: int, key: int) -> dict[int, tuple[int, str]]:
    out: dict[int, tuple[int, str]] = {}
    for slot in range(count):
        off = TG_START + slot * REC_SIZE
        rec = data[off:off + REC_SIZE]
        if len(rec) < REC_SIZE or all(b == 0xae for b in rec):
            continue
        name = decode_name(rec, key)
        m = re.match(r"^(\d+)\b", name)
        if not m:
            continue
        tg = int(m.group(1))
        out[tg] = (slot, name)
    return out


def in_tg_table(offset: int, count: int) -> bool:
    return TG_START <= offset < TG_START + count * REC_SIZE


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Search an entire DAT for encoded Talk Group numeric IDs."
    )
    ap.add_argument("dat", type=Path)
    ap.add_argument("--tg-count", type=int, default=DEFAULT_TG_COUNT)
    ap.add_argument("--text-key", type=lambda x: int(x, 0), default=TEXT_KEY)
    ap.add_argument("--limit", type=int, default=200)
    args = ap.parse_args()

    data = args.dat.read_bytes()
    tgs = collect_tgs(data, args.tg_count, args.text_key)

    print(f"DAT: {args.dat}")
    print(f"Talk Groups collected from numeric-prefixed names: {len(tgs)}")
    print(f"TG numeric encoding: uint16le ^ 0x{TG_NUMERIC_XOR:04x}")
    print()

    hits_by_tg: dict[int, list[int]] = defaultdict(list)

    for tg in sorted(tgs):
        encoded = tg ^ TG_NUMERIC_XOR
        needle = encoded.to_bytes(2, "little")
        start = 0
        while True:
            pos = data.find(needle, start)
            if pos < 0:
                break
            hits_by_tg[tg].append(pos)
            start = pos + 1

    outside_rows = []
    for tg, hits in sorted(hits_by_tg.items()):
        slot, name = tgs[tg]
        outside = [h for h in hits if not in_tg_table(h, args.tg_count)]
        if outside:
            outside_rows.append((tg, slot, name, outside))

    print(f"TGs with encoded-ID hits outside TG table: {len(outside_rows)}")
    print()

    shown = 0
    for tg, slot, name, outside in outside_rows:
        print(f"TG {tg} slot={slot} name={name!r} outside_hits={len(outside)}")
        for pos in outside[:20]:
            lo = max(0, pos - 8)
            hi = min(len(data), pos + 10)
            print(f"  0x{pos:05x}: {data[lo:hi].hex(' ')}")
        if len(outside) > 20:
            print(f"  ... {len(outside) - 20} more")
        shown += 1
        if shown >= args.limit:
            print(f"... stopped after {args.limit} TGs")
            break

    print()
    print("Summary:")
    print(f"- Total TGs searched: {len(tgs)}")
    print(f"- TGs with any hit: {sum(1 for hits in hits_by_tg.values() if hits)}")
    print(f"- TGs with outside-table hit: {len(outside_rows)}")


if __name__ == "__main__":
    main()
