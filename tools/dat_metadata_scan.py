#!/usr/bin/env python3
"""Scan metadata changes outside known KPG111 table ranges."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.metadata import MetadataComparison, MetadataRegion, compare_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only metadata diff outside known KPG111 table record areas."
    )
    parser.add_argument("baseline", type=Path, help="Baseline Program.dat")
    parser.add_argument("modified", type=Path, help="Modified Program.dat")
    parser.add_argument(
        "--decode-key",
        type=lambda value: int(value, 0),
        help="Optional decode key for future metadata heuristics.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("metadata_report.md"),
        help="Markdown report path (default: metadata_report.md)",
    )
    return parser.parse_args()


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    if not rows:
        lines.append("| " + " | ".join("none" for _ in headers) + " |")
        return lines
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def region_row(region: MetadataRegion) -> list[str]:
    return [
        f"0x{region.offset:08x}",
        str(region.length),
        region.classification,
        region.reason,
        region.before_hex,
        region.after_hex,
        region.before_ascii,
        region.after_ascii,
        str(region.distance_from_nearest_table),
    ]


def render_report(comparison: MetadataComparison) -> str:
    lines: list[str] = []
    lines.extend(
        [
            "# KPG111 Metadata Change Report",
            "",
            "This is a read-only report. It shows raw byte differences and differences after applying the dominant payload XOR observed between the two files.",
            "",
            "## Summary",
            "",
            f"- Baseline: `{comparison.baseline_path}`",
            f"- Modified: `{comparison.modified_path}`",
            f"- File size: {comparison.file_size} bytes",
            f"- Raw changed metadata bytes outside known tables: {comparison.raw_changed_metadata_bytes}",
            f"- Raw changed metadata regions outside known tables: {len(comparison.raw_changed_metadata_regions)}",
            f"- Normalized changed metadata bytes outside known tables: {comparison.normalized_changed_metadata_bytes}",
            f"- Normalized changed metadata regions outside known tables: {len(comparison.normalized_changed_metadata_regions)}",
            "",
            "## Normalization",
            "",
            f"- Dominant payload XOR used for normalization: `0x{comparison.dominant_payload_xor:02x}`",
            f"- Dominant payload XOR ratio: {comparison.dominant_payload_xor_ratio:.4%}",
            "",
        ]
    )
    if not comparison.normalized_changed_metadata_regions:
        lines.extend(
            [
                "No metadata changes detected after dominant payload XOR normalization.",
                "",
            ]
        )

    lines.extend(section("Raw Changed Metadata Regions", comparison.raw_changed_metadata_regions))
    lines.extend(section("Normalized Changed Metadata Regions", comparison.normalized_changed_metadata_regions))
    lines.extend(section("Candidate Count Fields", filter_regions(comparison, "possible_counter")))
    lines.extend(section("Candidate Index Tables", filter_regions(comparison, "possible_index_table")))
    lines.extend(section("Candidate Checksum Fields", filter_regions(comparison, "possible_checksum")))
    lines.extend(section("Unknown Regions", filter_regions(comparison, "unknown")))
    return "\n".join(lines) + "\n"


def filter_regions(comparison: MetadataComparison, classification: str) -> list[MetadataRegion]:
    return [
        region
        for region in comparison.normalized_changed_metadata_regions
        if region.classification == classification
    ]


def section(title: str, regions: list[MetadataRegion]) -> list[str]:
    lines = [f"## {title}", ""]
    lines.extend(
        markdown_table(
            [
                "Offset",
                "Length",
                "Classification",
                "Reason",
                "Before Hex",
                "After Hex",
                "Before ASCII",
                "After ASCII",
                "Distance From Table",
            ],
            [region_row(region) for region in regions],
        )
    )
    lines.append("")
    return lines


def main() -> int:
    args = parse_args()
    comparison = compare_files(args.baseline, args.modified, decode_key=args.decode_key)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_report(comparison), encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"raw changed metadata regions: {len(comparison.raw_changed_metadata_regions)}")
    print(f"normalized changed metadata regions: {len(comparison.normalized_changed_metadata_regions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
