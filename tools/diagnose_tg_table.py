#!/usr/bin/env python3

from pathlib import Path
import argparse

RECORD_SIZE = 32
XOR_KEY = 0x5151
MIN_CLUSTER_RECORDS = 3
NAME_START = 1
NAME_END = 15
TG_LO_OFFSET = 0x13
TG_HI_OFFSET = 0x14
FILLER_BYTES = {0x00, 0xFF}
PADDING_RANGES = (
    range(0x0F, 0x13),
    range(0x15, RECORD_SIZE),
)


def decode_name(raw):
    chars = []
    for b in raw:
        if b in (0x00, 0xFF):
            break
        if 32 <= b <= 126:
            chars.append(chr(b))
        else:
            chars.append(".")
    return "".join(chars)


def decode_tg(lo, hi):
    return ((hi << 8) | lo) ^ XOR_KEY


def is_mostly_filler_or_repeated(rec):
    if not rec:
        return True

    if len(set(rec)) == 1:
        return True

    filler_count = sum(b in FILLER_BYTES for b in rec)
    if filler_count >= len(rec) * 3 // 4:
        return True

    most_common = max(rec.count(b) for b in set(rec))
    return most_common >= len(rec) * 3 // 4


def has_conservative_name_shape(raw):
    name = decode_name(raw)

    if not name:
        return False

    if len(name) > 1 and len(set(name)) == 1:
        return False

    for b in raw:
        if b in FILLER_BYTES:
            break
        if not 32 <= b <= 126:
            return False

    meaningful = sum(b not in FILLER_BYTES and b != 0x20 for b in raw)
    return meaningful >= 2


def has_tg_record_shape(rec):
    pad = rec[0]
    return all(rec[i] == pad for padding in PADDING_RANGES for i in padding)


def looks_like_record(rec):
    # This scanner is diagnostic evidence, not importer logic.  The heuristic is
    # intentionally conservative: a false negative is less harmful than showing
    # a KPG111 header, padding, or an unrelated printable structure as a TG table.
    if len(rec) != RECORD_SIZE:
        return False

    if is_mostly_filler_or_repeated(rec):
        return False

    if not has_tg_record_shape(rec):
        return False

    name = rec[NAME_START:NAME_END]
    if not has_conservative_name_shape(name):
        return False

    tg = decode_tg(rec[TG_LO_OFFSET], rec[TG_HI_OFFSET])

    return 1 <= tg <= 65000


def scan_clusters(data):
    clusters = []
    start = 0

    while start + RECORD_SIZE <= len(data):
        count = 0
        pos = start

        while pos + RECORD_SIZE <= len(data):
            rec = data[pos:pos + RECORD_SIZE]

            if not looks_like_record(rec):
                break

            count += 1
            pos += RECORD_SIZE

        # Require a real run of consecutive records and then advance past it.
        # This avoids overlapping duplicate reports from every record inside the
        # same candidate table.
        if count >= MIN_CLUSTER_RECORDS:
            clusters.append((start, count))
            start = pos
        else:
            start += RECORD_SIZE

    return clusters


def dump_cluster(data, start, count):

    print("=" * 72)
    print(f"Cluster @ 0x{start:06X}")
    print(f"Records : {count}")
    print()

    for i in range(count):

        off = start + i * RECORD_SIZE
        rec = data[off:off + RECORD_SIZE]

        name = decode_name(rec[1:15])
        tg = decode_tg(rec[0x13], rec[0x14])

        print(
            f"{i:3d} "
            f"0x{off:06X} "
            f"TG={tg:5d} "
            f"Name='{name}'"
        )

        print(
            "      Raw:",
            rec.hex(" ")
        )

    print()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("dat")

    args = parser.parse_args()

    data = Path(args.dat).read_bytes()

    clusters = scan_clusters(data)

    if not clusters:
        print("No TG-like clusters found.")
        return

    for start, count in clusters:
        dump_cluster(data, start, count)


if __name__ == "__main__":
    main()
