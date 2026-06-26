#!/usr/bin/env python3
"""
Experimental utility.

Purpose:
    Used during OpenKPG reverse engineering to determine whether
    KPG111 DAT payloads used a fixed XOR relationship.

Status:
    Historical diagnostic.
    Superseded for KPG111 by:
        - tools/dat_xor_relation.py
        - tools/dat_normalized_diff.py

Retained because the same methodology may be useful when
investigating KPG89 and other Kenwood CPS file formats.
"""

# ...rest of file...


#!/usr/bin/env python3
from pathlib import Path
import sys

HEADER_LEN = 0x40

def score_decode(raw: bytes, key: int):
    dec = bytes(b ^ key for b in raw[HEADER_LEN:])

    score = 0
    notes = []

    # Known-good decoded padding candidates
    for pat in (b"\xE5", b"\xFF", b"\x00"):
        count = dec.count(pat)
        if count > 1000:
            score += count // 1000
            notes.append(f"{pat.hex()}x{count}")

    # ASCII-ish readable bytes
    ascii_count = sum(1 for b in dec if b in range(0x20, 0x7f))
    score += ascii_count // 500
    notes.append(f"ascii={ascii_count}")

    # Existing known key hint
    if key == 0x5B:
        notes.append("known_current_key")

    return score, notes, dec[:96].hex(" ")

def main():
    if len(sys.argv) < 2:
        print("usage: tools/key_probe.py FILE.dat [FILE2.dat...]")
        raise SystemExit(2)

    for name in sys.argv[1:]:
        raw = Path(name).read_bytes()
        print()
        print("=" * 80)
        print(name)
        print(f"size={len(raw)} header={raw[:HEADER_LEN].hex(' ')}")
        results = []

        for key in range(256):
            score, notes, preview = score_decode(raw, key)
            results.append((score, key, notes, preview))

        for score, key, notes, preview in sorted(results, reverse=True)[:12]:
            print(f"key=0x{key:02X} score={score:6d} notes={', '.join(notes)}")
            print(f"  decoded@0x40: {preview}")

if __name__ == "__main__":
    main()
