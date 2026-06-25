#!/usr/bin/env python3
"""Build read-only metadata reports across a KPG111 experiment."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.metadata import MetadataComparison, MetadataRegion, compare_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only metadata comparison report for one baseline and multiple modified KPG111 Program.dat files."
    )
    parser.add_argument("baseline", type=Path, help="Baseline Program.dat")
    parser.add_argument(
        "modified",
        type=Path,
        nargs="+",
        help="One or more modified Program.dat files",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Markdown report path",
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


def file_label(path: str) -> str:
    return Path(path).name


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


def render_region_section(
    title: str,
    comparisons: list[MetadataComparison],
    attr_name: str,
) -> list[str]:
    lines = [f"## {title}", ""]
    headers = [
        "File",
        "Offset",
        "Length",
        "Classification",
        "Reason",
        "Before Hex",
        "After Hex",
        "Before ASCII",
        "After ASCII",
        "Distance From Table",
    ]
    rows = []
    for comparison in comparisons:
        regions = getattr(comparison, attr_name)
        for region in regions:
            rows.append([file_label(comparison.modified_path), *region_row(region)])
    lines.extend(markdown_table(headers, rows))
    lines.append("")
    return lines


def recurring_region_rows(
    comparisons: list[MetadataComparison],
    attr_name: str,
) -> list[list[str]]:
    grouped: dict[tuple[int, int, str], list[str]] = defaultdict(list)
    for comparison in comparisons:
        for region in getattr(comparison, attr_name):
            key = (region.offset, region.length, region.classification)
            grouped[key].append(file_label(comparison.modified_path))
    rows = []
    for (offset, length, classification), files in sorted(grouped.items()):
        if len(files) < 2:
            continue
        rows.append(
            [
                f"0x{offset:08x}",
                str(length),
                classification,
                ", ".join(files),
            ]
        )
    return rows


def render_report(baseline: Path, comparisons: list[MetadataComparison]) -> str:
    lines: list[str] = [
        "# KPG111 Metadata Experiment Report",
        "",
        "This is a read-only experiment report. It summarizes raw byte differences and differences after applying the dominant payload XOR observed for each modified file.",
        "",
        f"- Baseline: `{baseline}`",
        f"- Modified files compared: {len(comparisons)}",
        "",
        "## Summary",
        "",
    ]
    lines.extend(
        markdown_table(
            [
                "file",
                "dominant_xor",
                "xor_ratio",
                "raw_regions",
                "raw_bytes",
                "normalized_regions",
                "normalized_bytes",
            ],
            [
                [
                    file_label(comparison.modified_path),
                    f"0x{comparison.dominant_payload_xor:02x}",
                    f"{comparison.dominant_payload_xor_ratio:.4%}",
                    str(len(comparison.raw_changed_metadata_regions)),
                    str(comparison.raw_changed_metadata_bytes),
                    str(len(comparison.normalized_changed_metadata_regions)),
                    str(comparison.normalized_changed_metadata_bytes),
                ]
                for comparison in comparisons
            ],
        )
    )
    lines.append("")
    lines.extend(normalization_table(comparisons))
    lines.extend(
        render_region_section(
            "Raw Metadata Regions By File",
            comparisons,
            "raw_changed_metadata_regions",
        )
    )
    lines.extend(
        render_region_section(
            "Normalized Metadata Regions By File",
            comparisons,
            "normalized_changed_metadata_regions",
        )
    )
    lines.extend(recurring_section("Cross-file Recurring Raw Regions", comparisons, "raw_changed_metadata_regions"))
    lines.extend(
        recurring_section(
            "Cross-file Recurring Normalized Regions",
            comparisons,
            "normalized_changed_metadata_regions",
        )
    )
    lines.extend(observations(comparisons))
    return "\n".join(lines) + "\n"


def normalization_table(comparisons: list[MetadataComparison]) -> list[str]:
    lines = ["## Normalization Table", ""]
    lines.extend(
        markdown_table(
            [
                "file",
                "dominant_xor",
                "xor_ratio",
                "raw_regions",
                "normalized_regions",
                "raw_disappeared_after_normalization",
            ],
            [
                [
                    file_label(comparison.modified_path),
                    f"0x{comparison.dominant_payload_xor:02x}",
                    f"{comparison.dominant_payload_xor_ratio:.4%}",
                    str(len(comparison.raw_changed_metadata_regions)),
                    str(len(comparison.normalized_changed_metadata_regions)),
                    yes_no(
                        bool(comparison.raw_changed_metadata_regions)
                        and not comparison.normalized_changed_metadata_regions
                    ),
                ]
                for comparison in comparisons
            ],
        )
    )
    lines.append("")
    return lines


def recurring_section(
    title: str,
    comparisons: list[MetadataComparison],
    attr_name: str,
) -> list[str]:
    lines = [f"## {title}", ""]
    lines.extend(
        markdown_table(
            ["Offset", "Length", "Classification", "Files"],
            recurring_region_rows(comparisons, attr_name),
        )
    )
    lines.append("")
    return lines


def observations(comparisons: list[MetadataComparison]) -> list[str]:
    all_normalized_zero = all(
        not comparison.normalized_changed_metadata_regions
        for comparison in comparisons
    )
    raw_disappeared = any(
        comparison.raw_changed_metadata_regions
        and not comparison.normalized_changed_metadata_regions
        for comparison in comparisons
    )
    lines = ["## Conservative Observations", ""]
    if all_normalized_zero:
        lines.append("- No normalized metadata changes were observed in this experiment.")
    if raw_disappeared:
        lines.append("- Raw metadata changes may reflect save-time encoding/XOR effects.")
    if not lines[-1].startswith("- "):
        lines.append("- Observed normalized metadata differences should be reviewed as candidate metadata behavior, not proof of a specific field type.")
    lines.append("- This report only describes observed differences outside the known table ranges.")
    lines.append("")
    return lines


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def main() -> int:
    args = parse_args()
    comparisons = [compare_files(args.baseline, modified) for modified in args.modified]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_report(args.baseline, comparisons), encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"modified files compared: {len(comparisons)}")
    print(
        "normalized changed metadata regions: "
        + str(
            sum(
                len(comparison.normalized_changed_metadata_regions)
                for comparison in comparisons
            )
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
