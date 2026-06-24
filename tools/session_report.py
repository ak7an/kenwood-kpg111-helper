#!/usr/bin/env python3
"""Create a markdown report from read-only comparison session JSON files."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ALIGNMENTS = (2, 4, 8, 16, 32, 64, 128, 256)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize statistical observations across session.json files."
    )
    parser.add_argument("sessions", nargs="+", type=Path, help="Session JSON files")
    parser.add_argument(
        "--top",
        type=int,
        default=25,
        help="Maximum rows per section (default: 25)",
    )
    return parser.parse_args()


def load_session(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["_session_path"] = str(path)
    return data


def region_overlap(left: dict[str, int], right: dict[str, int]) -> bool:
    return left["start"] <= right["end"] and right["start"] <= left["end"]


def recurring_regions(sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clusters: list[dict[str, Any]] = []
    for session in sessions:
        session_path = session["_session_path"]
        for region in session.get("changed_regions", []):
            placed = False
            for cluster in clusters:
                cluster_region = {"start": cluster["start"], "end": cluster["end"]}
                if region_overlap(cluster_region, region):
                    cluster["start"] = min(cluster["start"], region["start"])
                    cluster["end"] = max(cluster["end"], region["end"])
                    cluster["sessions"].add(session_path)
                    cluster["lengths"].append(region["length"])
                    placed = True
                    break
            if not placed:
                clusters.append(
                    {
                        "start": region["start"],
                        "end": region["end"],
                        "sessions": {session_path},
                        "lengths": [region["length"]],
                    }
                )

    clusters.sort(key=lambda item: (-len(item["sessions"]), item["start"]))
    return clusters


def byte_delta(byte_change: dict[str, Any]) -> int | None:
    before = byte_change.get("before")
    after = byte_change.get("after")
    if before is None or after is None:
        return None
    return int(after, 16) - int(before, 16)


def markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(row) + " |")


def main() -> int:
    args = parse_args()
    sessions = [load_session(path) for path in args.sessions]
    session_count = len(sessions)

    offset_sessions: dict[int, set[str]] = defaultdict(set)
    offset_deltas: dict[int, list[int | None]] = defaultdict(list)
    short_region_offsets: Counter[int] = Counter()
    tail_region_offsets: Counter[int] = Counter()
    alignment_counts: Counter[int] = Counter()
    region_length_counts: Counter[int] = Counter()

    for session in sessions:
        session_path = session["_session_path"]
        modified_size = session.get("modified", {}).get("size", 0)

        for offset in session.get("changed_offsets", []):
            offset_sessions[int(offset)].add(session_path)

        for byte_change in session.get("changed_bytes", []):
            offset = int(byte_change["offset"])
            offset_deltas[offset].append(byte_delta(byte_change))

        for region in session.get("changed_regions", []):
            start = int(region["start"])
            length = int(region["length"])
            region_length_counts[length] += 1
            for alignment in ALIGNMENTS:
                if start % alignment == 0:
                    alignment_counts[alignment] += 1
            if length <= 4:
                short_region_offsets[start] += 1
            if modified_size and start >= max(0, modified_size - 512):
                tail_region_offsets[start] += 1

    print("# KPG111 Comparison Session Report")
    print()
    print("This report contains statistical observations only. It does not decode or claim field meanings.")
    print()
    print(f"- Sessions analyzed: {session_count}")
    print(f"- Total changed-offset observations: {sum(len(s.get('changed_offsets', [])) for s in sessions)}")
    print(f"- Total changed-region observations: {sum(len(s.get('changed_regions', [])) for s in sessions)}")
    print()

    print("## Sessions")
    rows = []
    for session in sessions:
        rows.append(
            [
                session["_session_path"],
                str(session.get("baseline", {}).get("size", "")),
                str(session.get("modified", {}).get("size", "")),
                f"{int(session.get('size_change', 0)):+d}",
                str(len(session.get("changed_offsets", []))),
                str(len(session.get("changed_regions", []))),
            ]
        )
    markdown_table(
        ["Session", "Baseline Size", "Modified Size", "Size Change", "Changed Offsets", "Changed Regions"],
        rows,
    )
    print()

    print("## Recurring Changed Offsets")
    recurring_offsets = sorted(
        ((offset, paths) for offset, paths in offset_sessions.items() if len(paths) > 1),
        key=lambda item: (-len(item[1]), item[0]),
    )
    rows = []
    for offset, paths in recurring_offsets[: args.top]:
        deltas = [delta for delta in offset_deltas[offset] if delta is not None]
        delta_summary = ", ".join(str(delta) for delta in sorted(set(deltas))) if deltas else "varied or size-only"
        rows.append([f"0x{offset:08x}", str(len(paths)), delta_summary])
    markdown_table(["Offset", "Sessions", "Observed Byte Deltas"], rows)
    print()

    print("## Recurring Changed Regions")
    rows = []
    for cluster in recurring_regions(sessions)[: args.top]:
        if len(cluster["sessions"]) <= 1:
            continue
        min_len = min(cluster["lengths"])
        max_len = max(cluster["lengths"])
        rows.append(
            [
                f"0x{cluster['start']:08x}-0x{cluster['end']:08x}",
                str(len(cluster["sessions"])),
                f"{min_len}-{max_len}",
            ]
        )
    markdown_table(["Region Span", "Sessions", "Observed Region Lengths"], rows)
    print()

    print("## Probable Record Boundary Signals")
    print()
    print("These are alignment and length observations from changed regions, not confirmed record sizes.")
    rows = [
        [str(alignment), str(count)]
        for alignment, count in alignment_counts.most_common()
        if count > 0
    ][: args.top]
    markdown_table(["Region Start Alignment", "Observations"], rows)
    print()
    rows = [[str(length), str(count)] for length, count in region_length_counts.most_common(args.top)]
    markdown_table(["Changed Region Length", "Observations"], rows)
    print()

    print("## Possible Count Field Signals")
    print()
    print("Short recurring changed regions can be count fields, indexes, flags, or unrelated small values.")
    rows = [
        [f"0x{offset:08x}", str(count)]
        for offset, count in short_region_offsets.most_common(args.top)
        if count > 1
    ]
    markdown_table(["Short Region Offset", "Observations"], rows)
    print()

    print("## Possible Checksum Field Signals")
    print()
    print("Recurring changes near the end of files can be checksum-like, but may also be normal data.")
    rows = [
        [f"0x{offset:08x}", str(count)]
        for offset, count in tail_region_offsets.most_common(args.top)
        if count > 1
    ]
    markdown_table(["Tail Region Offset", "Observations"], rows)
    print()

    print("## String Changes")
    rows = []
    for session in sessions:
        rows.append(
            [
                session["_session_path"],
                str(len(session.get("strings_added", []))),
                str(len(session.get("strings_removed", []))),
            ]
        )
    markdown_table(["Session", "Strings Added", "Strings Removed"], rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

