#!/usr/bin/env python3
"""Search KPG111 DAT files for candidate channel-like records read-only."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.decoder import PAYLOAD_START
from kpg111.project import KPG111Project


RECORD_SIZE_CANDIDATES = (32, 44, 48, 64, 80, 96, 128)
PRINTABLE_RE = re.compile(rb"[\x20-\x7e]{4,}")
CHANNEL_WORDS = (
    "CALL",
    "CHAN",
    "CH",
    "DIRECT",
    "DISPATCH",
    "LOCAL",
    "RX",
    "TX",
    "TAC",
    "ZONE",
)
FEATURE_WORDS = (
    "WIDE",
    "NARROW",
    "POWER",
    "HIGH",
    "LOW",
    "QT",
    "DQT",
    "RAN",
    "MODE",
    "ZONE",
    "ANALOG",
    "NXDN",
)


@dataclass(frozen=True)
class FrequencyHit:
    offset: int
    encoding: str
    value: int


@dataclass(frozen=True)
class CandidateRecord:
    offset: int
    record_size: int
    score: int
    confidence: str
    decoded_names: tuple[str, ...]
    raw_strings: tuple[str, ...]
    frequency_hits: tuple[FrequencyHit, ...]
    feature_hints: tuple[str, ...]
    repeated_count: int
    repeated_offsets: tuple[int, ...]
    notes: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Heuristically search DAT files for candidate channel records."
    )
    parser.add_argument("dat_files", nargs="+", type=Path, help="Input .dat file(s)")
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        default=0x5B,
        help="Decode key used by existing project parser and XOR string probes (default: 0x5b)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=30,
        help="Maximum candidate records to show per file (default: 30)",
    )
    return parser.parse_args()


def printable_text(data: bytes) -> str:
    if not data:
        return ""
    if all(32 <= byte <= 126 or byte == 0 for byte in data):
        text = data.split(b"\x00", 1)[0]
        if len(text) >= 3:
            return text.decode("ascii", errors="replace")
    return ""


def decoded_name_windows(chunk: bytes, decode_key: int) -> tuple[str, ...]:
    names = set()
    for start in range(0, max(0, len(chunk) - 14) + 1):
        field = bytes(byte ^ decode_key for byte in chunk[start : start + 14])
        text = printable_text(field)
        if text:
            names.add(text)
    return tuple(sorted(names))


def raw_ascii_strings(chunk: bytes) -> tuple[str, ...]:
    return tuple(
        match.group().decode("ascii", errors="replace")
        for match in PRINTABLE_RE.finditer(chunk)
    )


def looks_like_frequency(value: int) -> bool:
    return 25_000_000 <= value <= 999_999_999 and value % 5 == 0


def uint32_frequency_hits(chunk: bytes, base_offset: int) -> list[FrequencyHit]:
    hits = []
    for rel in range(0, max(0, len(chunk) - 4) + 1):
        raw = chunk[rel : rel + 4]
        little = int.from_bytes(raw, "little")
        big = int.from_bytes(raw, "big")
        if looks_like_frequency(little):
            hits.append(FrequencyHit(base_offset + rel, "uint32 little-endian", little))
        if big != little and looks_like_frequency(big):
            hits.append(FrequencyHit(base_offset + rel, "uint32 big-endian", big))
    return hits


def bcd_value(raw: bytes) -> int | None:
    digits = []
    for byte in raw:
        low = byte & 0x0F
        high = byte >> 4
        if low > 9 or high > 9:
            return None
        digits.extend([low, high])
    if not digits:
        return None
    return int("".join(str(digit) for digit in digits).rstrip("0") or "0")


def bcd_frequency_hits(chunk: bytes, base_offset: int) -> list[FrequencyHit]:
    hits = []
    for width in (4, 5):
        for rel in range(0, max(0, len(chunk) - width) + 1):
            value = bcd_value(chunk[rel : rel + width])
            if value is not None and looks_like_frequency(value):
                hits.append(FrequencyHit(base_offset + rel, f"packed BCD {width} byte", value))
    return hits


def frequency_hits(chunk: bytes, base_offset: int) -> tuple[FrequencyHit, ...]:
    hits = uint32_frequency_hits(chunk, base_offset) + bcd_frequency_hits(chunk, base_offset)
    unique = {(hit.offset, hit.encoding, hit.value): hit for hit in hits}
    return tuple(unique[key] for key in sorted(unique))


def confidence(score: int) -> str:
    if score >= 12:
        return "MODERATE"
    if score >= 3:
        return "LOW"
    return "VERY LOW"


def repeated_chunks(data: bytes, record_size: int) -> dict[bytes, list[int]]:
    locations: dict[bytes, list[int]] = {}
    for offset in range(PAYLOAD_START, len(data) - record_size + 1, record_size):
        chunk = data[offset : offset + record_size]
        if len(set(chunk)) == 1:
            continue
        locations.setdefault(chunk, []).append(offset)
    return locations


def feature_hints(names: tuple[str, ...], strings: tuple[str, ...]) -> tuple[str, ...]:
    text = " ".join(names + strings).upper()
    return tuple(word for word in FEATURE_WORDS if word in text)


def analyze_candidates(data: bytes, decode_key: int, top: int) -> list[CandidateRecord]:
    candidates: list[CandidateRecord] = []
    for record_size in RECORD_SIZE_CANDIDATES:
        repeats = repeated_chunks(data, record_size)
        for offset in range(PAYLOAD_START, len(data) - record_size + 1, 16):
            chunk = data[offset : offset + record_size]
            if len(set(chunk)) <= 2:
                continue

            names = decoded_name_windows(chunk, decode_key)
            strings = raw_ascii_strings(chunk)
            freqs = frequency_hits(chunk, offset)
            hints = feature_hints(names, strings)
            repeat_offsets = tuple(repeats.get(chunk, [])[:8])
            repeat_count = len(repeats.get(chunk, []))

            notes = []
            score = 0
            if names:
                score += 2
                notes.append("has XOR-decoded printable name-like window")
            if strings:
                score += 1
                notes.append("has raw printable string")
            if freqs:
                score += 3
                notes.append("has frequency-like integer or BCD value")
            if repeat_count >= 2:
                score += 2
                notes.append("same record-sized chunk repeats on this stride")
            if any(word in " ".join(names + strings).upper() for word in CHANNEL_WORDS):
                score += 2
                notes.append("contains channel/zone-related word")
            if hints:
                score += 1
                notes.append("contains feature-related word")

            if score == 0:
                continue

            candidates.append(
                CandidateRecord(
                    offset=offset,
                    record_size=record_size,
                    score=score,
                    confidence=confidence(score),
                    decoded_names=names[:5],
                    raw_strings=strings[:5],
                    frequency_hits=freqs[:6],
                    feature_hints=hints,
                    repeated_count=repeat_count,
                    repeated_offsets=repeat_offsets,
                    notes=tuple(notes),
                )
            )

    candidates.sort(key=lambda item: (-item.score, item.offset, item.record_size))
    return candidates[:top]


def md_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |")


def render_frequency_hits(hits: tuple[FrequencyHit, ...]) -> str:
    if not hits:
        return ""
    return "; ".join(
        f"0x{hit.offset:08x} {hit.encoding}={hit.value}"
        for hit in hits
    )


def render_file(path: Path, decode_key: int, top: int) -> None:
    data = path.read_bytes()
    project = KPG111Project().load_program(path, decode_key)
    summary = project.table_summary()
    candidates = analyze_candidates(data, decode_key, top)

    print(f"## `{path}`")
    print()
    print(f"- Size: {len(data)} bytes")
    print(f"- Decode key used for existing parser: `0x{decode_key:02x}`")
    print(f"- Parsed Individual IDs: {summary['individual_ids']['occupied']}")
    print(f"- Parsed Talk Groups: {summary['talk_groups']['occupied']}")
    print()
    print("### Candidate Channel-Like Records")
    print()
    print("These are heuristic candidates, not confirmed channel records.")
    print()
    md_table(
        [
            "Offset",
            "Record Size",
            "Score",
            "Confidence",
            "Decoded Name-Like Windows",
            "Raw Strings",
            "Frequency-Like Values",
            "Feature Hints",
            "Repeats",
            "Notes",
        ],
        [
            [
                f"0x{item.offset:08x}",
                str(item.record_size),
                str(item.score),
                item.confidence,
                ", ".join(item.decoded_names),
                ", ".join(item.raw_strings),
                render_frequency_hits(item.frequency_hits),
                ", ".join(item.feature_hints),
                f"{item.repeated_count}: "
                + ", ".join(f"0x{offset:08x}" for offset in item.repeated_offsets),
                "; ".join(item.notes),
            ]
            for item in candidates
        ],
    )
    print()


def main() -> int:
    args = parse_args()
    print("# KPG111 Channel Record Candidate Analysis")
    print()
    print("Read-only heuristic scan. Confirmed facts are limited to existing parser output; channel candidates are hypotheses until controlled experiments isolate them.")
    print()
    print("The scan looks for name-like strings, possible RX/TX frequency encodings, repeated fixed-size structure, and literal feature hints such as wide/narrow, power, QT/DQT, RAN, NXDN, and zone text. It does not confirm field meanings.")
    print()
    for path in args.dat_files:
        render_file(path, args.decode_key, args.top)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
