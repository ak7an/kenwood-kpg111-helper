#!/usr/bin/env python3
"""Produce byte-level difference reports for controlled KPG111 DAT experiments."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ChangedRange:
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two KPG111 .dat files byte-for-byte without modifying them."
    )
    parser.add_argument("baseline", type=Path, help="Baseline .dat file")
    parser.add_argument("modified", type=Path, help="Modified .dat file")
    parser.add_argument(
        "--context",
        type=int,
        default=8,
        help="Unchanged bytes to show before and after each changed range (default: 8)",
    )
    parser.add_argument(
        "--max-ranges",
        type=int,
        help="Maximum changed ranges to display (default: no limit)",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Emit a markdown-friendly report.",
    )
    return parser.parse_args()


def find_changed_ranges(baseline: bytes, modified: bytes) -> list[ChangedRange]:
    changed_offsets = []
    shared = min(len(baseline), len(modified))
    for offset in range(shared):
        if baseline[offset] != modified[offset]:
            changed_offsets.append(offset)

    if len(baseline) != len(modified):
        changed_offsets.extend(range(shared, max(len(baseline), len(modified))))

    if not changed_offsets:
        return []

    ranges: list[ChangedRange] = []
    start = previous = changed_offsets[0]
    for offset in changed_offsets[1:]:
        if offset == previous + 1:
            previous = offset
            continue
        ranges.append(ChangedRange(start, previous))
        start = previous = offset
    ranges.append(ChangedRange(start, previous))
    return ranges


def hex_preview(data: bytes, start: int = 0, end: int | None = None) -> str:
    if end is None:
        end = len(data)
    return " ".join(f"{byte:02x}" for byte in data[start:end])


def ascii_preview(data: bytes, start: int = 0, end: int | None = None) -> str:
    if end is None:
        end = len(data)
    return "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in data[start:end])


def bounded_slice(data: bytes, start: int, end: int, context: int) -> tuple[int, int, bytes]:
    left = max(0, start - context)
    right = min(len(data), end + context + 1)
    return left, right, data[left:right]


def total_changed_bytes(ranges: list[ChangedRange]) -> int:
    return sum(changed.length for changed in ranges)


def format_range_plain(
    changed: ChangedRange, baseline: bytes, modified: bytes, context: int
) -> str:
    baseline_start, baseline_end, baseline_slice = bounded_slice(
        baseline, changed.start, changed.end, context
    )
    modified_start, modified_end, modified_slice = bounded_slice(
        modified, changed.start, changed.end, context
    )
    lines = [
        f"0x{changed.start:08x}-0x{changed.end:08x} length={changed.length}",
        f"  baseline @0x{baseline_start:08x}-0x{max(baseline_start, baseline_end - 1):08x}:",
        f"    hex:   {hex_preview(baseline_slice)}",
        f"    ascii: {ascii_preview(baseline_slice)!r}",
        f"  modified @0x{modified_start:08x}-0x{max(modified_start, modified_end - 1):08x}:",
        f"    hex:   {hex_preview(modified_slice)}",
        f"    ascii: {ascii_preview(modified_slice)!r}",
    ]
    if changed.start >= len(baseline):
        lines.append("  note: range begins after baseline EOF")
    if changed.start >= len(modified):
        lines.append("  note: range begins after modified EOF")
    return "\n".join(lines)


def format_range_markdown(
    changed: ChangedRange, baseline: bytes, modified: bytes, context: int
) -> str:
    baseline_start, baseline_end, baseline_slice = bounded_slice(
        baseline, changed.start, changed.end, context
    )
    modified_start, modified_end, modified_slice = bounded_slice(
        modified, changed.start, changed.end, context
    )
    baseline_label = f"0x{baseline_start:08x}-0x{max(baseline_start, baseline_end - 1):08x}"
    modified_label = f"0x{modified_start:08x}-0x{max(modified_start, modified_end - 1):08x}"
    notes = []
    if changed.start >= len(baseline):
        notes.append("range begins after baseline EOF")
    if changed.start >= len(modified):
        notes.append("range begins after modified EOF")
    note_text = "; ".join(notes) if notes else ""
    return (
        f"### 0x{changed.start:08x}-0x{changed.end:08x} length={changed.length}\n\n"
        "| Side | Slice | Hex | ASCII |\n"
        "| --- | --- | --- | --- |\n"
        f"| Baseline | `{baseline_label}` | `{hex_preview(baseline_slice)}` | "
        f"`{ascii_preview(baseline_slice)}` |\n"
        f"| Modified | `{modified_label}` | `{hex_preview(modified_slice)}` | "
        f"`{ascii_preview(modified_slice)}` |\n"
        + (f"\nNote: {note_text}\n" if note_text else "")
    )


def report_plain(
    baseline_path: Path,
    modified_path: Path,
    baseline: bytes,
    modified: bytes,
    ranges: list[ChangedRange],
    context: int,
    max_ranges: int | None,
) -> str:
    displayed = ranges if max_ranges is None else ranges[:max_ranges]
    lines = [
        "DAT Binary Difference Report",
        f"Baseline file: {baseline_path}",
        f"Modified file: {modified_path}",
        f"Baseline size: {len(baseline)} bytes",
        f"Modified size: {len(modified)} bytes",
        f"Total changed bytes: {total_changed_bytes(ranges)}",
        f"Changed ranges: {len(ranges)}",
    ]
    if len(baseline) != len(modified):
        lines.append(f"Size delta: {len(modified) - len(baseline):+d} bytes")

    if not ranges:
        lines.append("Files are identical.")
        return "\n".join(lines)

    lines.append("")
    lines.append("Changed Ranges")
    for changed in displayed:
        lines.append(format_range_plain(changed, baseline, modified, context))
    if len(displayed) < len(ranges):
        lines.append(f"... {len(ranges) - len(displayed)} more ranges not shown")
    return "\n".join(lines)


def report_markdown(
    baseline_path: Path,
    modified_path: Path,
    baseline: bytes,
    modified: bytes,
    ranges: list[ChangedRange],
    context: int,
    max_ranges: int | None,
) -> str:
    displayed = ranges if max_ranges is None else ranges[:max_ranges]
    lines = [
        "# DAT Binary Difference Report",
        "",
        f"- Baseline file: `{baseline_path}`",
        f"- Modified file: `{modified_path}`",
        f"- Baseline size: {len(baseline)} bytes",
        f"- Modified size: {len(modified)} bytes",
        f"- Total changed bytes: {total_changed_bytes(ranges)}",
        f"- Changed ranges: {len(ranges)}",
    ]
    if len(baseline) != len(modified):
        lines.append(f"- Size delta: {len(modified) - len(baseline):+d} bytes")

    if not ranges:
        lines.append("")
        lines.append("Files are identical.")
        return "\n".join(lines)

    lines.append("")
    lines.append("## Changed Ranges")
    lines.append("")
    for changed in displayed:
        lines.append(format_range_markdown(changed, baseline, modified, context))
    if len(displayed) < len(ranges):
        lines.append(f"... {len(ranges) - len(displayed)} more ranges not shown")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    if args.context < 0:
        raise SystemExit("--context must be zero or greater")
    if args.max_ranges is not None and args.max_ranges < 0:
        raise SystemExit("--max-ranges must be zero or greater")

    baseline = args.baseline.read_bytes()
    modified = args.modified.read_bytes()
    ranges = find_changed_ranges(baseline, modified)

    if args.markdown:
        print(
            report_markdown(
                args.baseline,
                args.modified,
                baseline,
                modified,
                ranges,
                args.context,
                args.max_ranges,
            )
        )
    else:
        print(
            report_plain(
                args.baseline,
                args.modified,
                baseline,
                modified,
                ranges,
                args.context,
                args.max_ranges,
            )
        )
    return 0 if not ranges else 1


if __name__ == "__main__":
    raise SystemExit(main())
