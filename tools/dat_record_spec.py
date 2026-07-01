#!/usr/bin/env python3
"""Generate a read-only byte-level KPG111 record specification."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.record_spec import ByteSpec, FieldSpec, RecordSpecification, TableRecordSpec
from kpg111.record_spec import record_spec


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate byte-level specification for known KPG111 TG/ID records."
    )
    parser.add_argument(
        "research_roots",
        nargs="*",
        type=Path,
        default=[
            Path("data/normalized/dattest"),
            Path("data/normalized/dattest2"),
            Path("data/normalized/dattest3"),
            Path("data/normalized/dattest4"),
        ],
        help="Research roots to scan.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("record_specification.json"),
        help="JSON output path (default: record_specification.json)",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path("record_specification.md"),
        help="Markdown output path (default: record_specification.md)",
    )
    parser.add_argument(
        "--docs-output",
        type=Path,
        default=Path("docs/RECORD_SPECIFICATION.md"),
        help="Documentation output path (default: docs/RECORD_SPECIFICATION.md)",
    )
    parser.add_argument("--max-records", type=int, default=1024)
    return parser.parse_args()


def json_default(value: object) -> object:
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def compact(values: tuple[str, ...], limit: int = 8) -> str:
    if not values:
        return ""
    if len(values) <= limit:
        return ", ".join(values)
    remaining = len(values) - limit
    return ", ".join(values[:limit]) + f", ... ({remaining} more)"


def table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    if not rows:
        lines.append("| " + " | ".join("none" for _ in headers) + " |")
        return lines
    for row in rows:
        lines.append("| " + " | ".join(md_escape(item) for item in row) + " |")
    return lines


def field_rows(fields: tuple[FieldSpec, ...]) -> list[list[object]]:
    return [
        [
            f"+{field.offset}",
            field.length,
            field.meaning,
            field.encoding,
            compact(field.observed_values),
            field.confidence,
            field.notes,
        ]
        for field in fields
    ]


def byte_rows(bytes_: tuple[ByteSpec, ...]) -> list[list[object]]:
    return [
        [
            f"+{item.offset}",
            item.meaning,
            item.encoding,
            compact(item.observed_decoded_values),
            compact(item.observed_raw_values),
            len(item.files_observed),
            "yes" if item.constant_decoded else "no",
            "yes" if item.variable else "no",
            "yes" if item.reserved else "no",
            item.changes_with_record_edits,
            item.confidence,
            item.notes,
        ]
        for item in bytes_
    ]


def unknown_rows(spec: TableRecordSpec) -> list[list[object]]:
    return [
        [
            spec.table_name,
            f"+{item.offset}",
            item.meaning,
            compact(item.observed_decoded_values),
            compact(item.observed_raw_values),
            ", ".join(item.files_observed),
            "yes" if item.constant_decoded else "no",
            item.changes_with_record_edits,
            item.confidence,
        ]
        for item in spec.bytes
        if item.meaning.startswith("UNKNOWN")
    ]


def summary_rows(spec: RecordSpecification) -> list[list[object]]:
    return [
        [
            item.table_name,
            item.record_size,
            item.known_bytes,
            item.unknown_bytes,
            item.reserved_bytes,
            f"{item.known_percentage:.1f}%",
            item.record_count_observed,
            len(item.files_observed),
        ]
        for item in (spec.talk_group, spec.individual_id)
    ]


def render_table_spec(spec: TableRecordSpec) -> list[str]:
    lines = [
        f"## {spec.table_name}",
        "",
        f"- Record size: {spec.record_size} bytes",
        f"- Occupied records observed: {spec.record_count_observed}",
        f"- Files observed: {len(spec.files_observed)}",
        f"- Known semantic bytes: {spec.known_bytes}",
        f"- Unknown/reserved bytes: {spec.unknown_bytes}",
        f"- Known percentage: {spec.known_percentage:.1f}%",
        "",
        "### Field Summary",
        "",
    ]
    lines.extend(
        table(
            ["Offset", "Length", "Meaning", "Encoding", "Observed Values", "Confidence", "Notes"],
            field_rows(spec.fields),
        )
    )
    lines.extend(["", "### Byte-Level Table", ""])
    lines.extend(
        table(
            [
                "Offset",
                "Meaning",
                "Encoding",
                "Observed Decoded Values",
                "Observed Raw Values",
                "Files Observed",
                "Constant Decoded?",
                "Variable?",
                "Reserved?",
                "Changes With Record Edits",
                "Confidence",
                "Notes",
            ],
            byte_rows(spec.bytes),
        )
    )
    lines.append("")
    return lines


def render_markdown(spec: RecordSpecification) -> str:
    lines = [
        "# KPG111 Record Specification",
        "",
        "This specification is generated from existing research files only. It is read-only and does not implement an encoder or writer.",
        "",
        "The current supported TG/ID table record size is 32 bytes. This is the complete observed record slice used by the read-only decoder, not a 32-byte decoded payload inside a proven larger record. Bytes `+1..+14` and `+19..+20` have supported meanings from controlled experiments. Other bytes are listed as UNKNOWN / candidate reserved or padding; they must not be modified by any future writer until their behavior is proven.",
        "",
        "## Summary Statistics",
        "",
    ]
    lines.extend(
        table(
            [
                "Record",
                "Record Size",
                "Known Bytes",
                "Unknown Bytes",
                "Reserved Candidate Bytes",
                "Known Percentage",
                "Records Observed",
                "Files Observed",
            ],
            summary_rows(spec),
        )
    )

    lines.extend(["", "## Shared Fields", ""])
    lines.extend(
        table(
            ["Offset", "Length", "Meaning", "Encoding", "Observed Values", "Confidence", "Notes"],
            field_rows(spec.shared_fields),
        )
    )
    lines.append("")

    lines.extend(render_table_spec(spec.talk_group))
    lines.extend(render_table_spec(spec.individual_id))

    lines.extend(["## Unknown Fields", ""])
    lines.extend(
        table(
            [
                "Record",
                "Offset",
                "Meaning",
                "Observed Decoded Values",
                "Observed Raw Values",
                "Files Observed",
                "Constant Decoded?",
                "Changes With Record Edits",
                "Confidence",
            ],
            unknown_rows(spec.talk_group) + unknown_rows(spec.individual_id),
        )
    )

    lines.extend(
        [
            "",
            "## Reserved Fields",
            "",
            "The UNKNOWN bytes are candidate reserved or padding bytes only because their decoded values are stable in the current occupied-record observations and they were not observed changing independently with name or numeric edits. This is not proof that they are safe to modify.",
            "",
            "## Notes",
            "",
            "- `constant decoded` means the byte has one observed value after applying the active decode key for each file.",
            "- `constant raw` is tracked in `record_specification.json`; raw values can differ across files because the whole payload XOR key changes.",
            "- Known percentage counts only bytes with supported semantic meanings: name and numeric ID.",
            "- Unknown bytes must remain untouched by any future writer design until proven otherwise.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    spec = record_spec(args.research_roots, max_records=args.max_records)
    args.json_output.write_text(
        json.dumps(asdict(spec), indent=2, default=json_default) + "\n",
        encoding="utf-8",
    )
    markdown = render_markdown(spec)
    args.markdown_output.write_text(markdown, encoding="utf-8")
    args.docs_output.parent.mkdir(parents=True, exist_ok=True)
    args.docs_output.write_text(markdown, encoding="utf-8")
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")
    print(f"Wrote {args.docs_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
