#!/usr/bin/env python3
"""Export read-only candidate KPG111 channel-like records to CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.dat_channel_analysis import CandidateRecord, analyze_candidates, render_frequency_hits


FIELDNAMES = [
    "row",
    "slot",
    "record_offset",
    "name",
    "rx_frequency",
    "tx_frequency",
    "mode",
    "bandwidth",
    "power",
    "group_list",
    "unit_list",
    "scan_list",
    "raw_hex",
    "confidence",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export read-only candidate channel-like records for structure research."
    )
    parser.add_argument("dat_file", type=Path, help="Input KPG111 .dat file")
    parser.add_argument("--output", required=True, type=Path, help="Output CSV path")
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        default=0x5B,
        help="Decode key used for heuristic string probes (default: 0x5b)",
    )
    parser.add_argument(
        "--include-unknown",
        action="store_true",
        help="Include raw candidate bytes in the raw_hex column.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Maximum candidate records to export (default: 30)",
    )
    return parser.parse_args()


def candidate_notes(candidate: CandidateRecord, include_unknown: bool) -> str:
    notes = [
        "candidate channel-like record only; channel table is not confirmed",
        f"candidate_size={candidate.record_size}",
        f"score={candidate.score}",
    ]
    if candidate.decoded_names:
        notes.append("name-like windows: " + ", ".join(candidate.decoded_names))
    if candidate.raw_strings:
        notes.append("raw strings: " + ", ".join(candidate.raw_strings))
    if candidate.frequency_hits:
        notes.append("frequency-like values: " + render_frequency_hits(candidate.frequency_hits))
    if candidate.feature_hints:
        notes.append("feature hints: " + ", ".join(candidate.feature_hints))
    if candidate.repeated_count:
        notes.append(f"repeat_count={candidate.repeated_count}")
    notes.extend(candidate.notes)
    if not include_unknown:
        notes.append("raw_hex omitted; use --include-unknown to include candidate bytes")
    notes.append("blank decoded fields are unknown, not confirmed absent")
    return "; ".join(notes)


def row_for_candidate(
    data: bytes,
    candidate: CandidateRecord,
    index: int,
    include_unknown: bool,
) -> dict[str, str | int]:
    raw = data[candidate.offset : candidate.offset + candidate.record_size]
    return {
        "row": index + 1,
        "slot": index,
        "record_offset": f"0x{candidate.offset:08x}",
        "name": "",
        "rx_frequency": "",
        "tx_frequency": "",
        "mode": "",
        "bandwidth": "",
        "power": "",
        "group_list": "",
        "unit_list": "",
        "scan_list": "",
        "raw_hex": raw.hex(" ") if include_unknown else "",
        "confidence": candidate.confidence,
        "notes": candidate_notes(candidate, include_unknown),
    }


def export_channels(
    dat_file: Path,
    output: Path,
    decode_key: int,
    include_unknown: bool,
    limit: int,
) -> int:
    if limit < 0:
        raise ValueError("--limit must be >= 0")
    data = dat_file.read_bytes()
    candidates = analyze_candidates(data, decode_key, top=limit)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for index, candidate in enumerate(candidates):
            writer.writerow(row_for_candidate(data, candidate, index, include_unknown))
    return len(candidates)


def main() -> int:
    args = parse_args()
    try:
        count = export_channels(
            args.dat_file,
            args.output,
            args.decode_key,
            args.include_unknown,
            args.limit,
        )
        print(f"wrote {args.output} ({count} candidate rows)")
        return 0
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
