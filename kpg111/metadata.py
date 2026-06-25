"""Read-only metadata change scanner for KPG111 Program.dat comparisons."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections import Counter

from .decoder import (
    INDIVIDUAL_ID_TABLE_START,
    PAYLOAD_START,
    TALK_GROUP_TABLE_START,
)


TALK_GROUP_TABLE_END = 0x17B60
IGNORED_TABLE_RANGES = (
    (INDIVIDUAL_ID_TABLE_START, TALK_GROUP_TABLE_START),
    (TALK_GROUP_TABLE_START, TALK_GROUP_TABLE_END),
)
REGION_PREVIEW_BYTES = 32


@dataclass(frozen=True)
class MetadataRegion:
    offset: int
    length: int
    before_hex: str
    after_hex: str
    before_ascii: str
    after_ascii: str
    classification: str
    reason: str
    distance_from_nearest_table: int


@dataclass(frozen=True)
class MetadataComparison:
    baseline_path: str
    modified_path: str
    file_size: int
    dominant_payload_xor: int
    dominant_payload_xor_ratio: float
    raw_changed_metadata_bytes: int
    raw_changed_metadata_regions: list[MetadataRegion]
    normalized_changed_metadata_bytes: int
    normalized_changed_metadata_regions: list[MetadataRegion]


def compare_files(
    baseline: Path | str,
    modified: Path | str,
    decode_key: int | None = None,
) -> MetadataComparison:
    baseline_path = Path(baseline)
    modified_path = Path(modified)
    before = baseline_path.read_bytes()
    after_raw = modified_path.read_bytes()
    dominant_xor, ratio = dominant_payload_xor(before, after_raw)
    after = normalize_payload(after_raw, dominant_xor)
    raw_offsets = changed_metadata_offsets(before, after_raw)
    normalized_offsets = changed_metadata_offsets(before, after)
    raw_regions = build_regions(before, after_raw, raw_offsets)
    normalized_regions = build_regions(before, after, normalized_offsets)
    return MetadataComparison(
        baseline_path=str(baseline_path),
        modified_path=str(modified_path),
        file_size=max(len(before), len(after_raw)),
        dominant_payload_xor=dominant_xor,
        dominant_payload_xor_ratio=ratio,
        raw_changed_metadata_bytes=len(raw_offsets),
        raw_changed_metadata_regions=raw_regions,
        normalized_changed_metadata_bytes=len(normalized_offsets),
        normalized_changed_metadata_regions=normalized_regions,
    )


def changed_metadata_offsets(before: bytes, after: bytes) -> list[int]:
    shared = min(len(before), len(after))
    offsets = [
        offset
        for offset in range(shared)
        if before[offset] != after[offset] and not in_ignored_table(offset)
    ]
    if len(before) != len(after):
        offsets.extend(
            offset
            for offset in range(shared, max(len(before), len(after)))
            if not in_ignored_table(offset)
        )
    return offsets


def build_regions(before: bytes, after: bytes, offsets: list[int]) -> list[MetadataRegion]:
    return [
        build_region(before, after, start, end)
        for start, end in group_offsets(offsets)
    ]


def dominant_payload_xor(before: bytes, after: bytes) -> tuple[int, float]:
    shared = min(len(before), len(after))
    if shared <= PAYLOAD_START:
        return 0, 1.0
    values = [before[offset] ^ after[offset] for offset in range(PAYLOAD_START, shared)]
    counts = Counter(values)
    value, count = counts.most_common(1)[0]
    return value, count / len(values)


def normalize_payload(data: bytes, xor_value: int) -> bytes:
    if xor_value == 0:
        return data
    normalized = bytearray(data)
    for offset in range(PAYLOAD_START, len(normalized)):
        normalized[offset] ^= xor_value
    return bytes(normalized)


def in_ignored_table(offset: int) -> bool:
    return any(start <= offset < end for start, end in IGNORED_TABLE_RANGES)


def group_offsets(offsets: list[int]) -> list[tuple[int, int]]:
    if not offsets:
        return []
    regions = []
    start = previous = offsets[0]
    for offset in offsets[1:]:
        if offset == previous + 1:
            previous = offset
            continue
        regions.append((start, previous))
        start = previous = offset
    regions.append((start, previous))
    return regions


def build_region(before: bytes, after: bytes, start: int, end: int) -> MetadataRegion:
    before_slice = before[start : min(end + 1, len(before))]
    after_slice = after[start : min(end + 1, len(after))]
    before_preview = preview_bytes(before_slice)
    after_preview = preview_bytes(after_slice)
    classification, reason = classify_region(start, before_slice, after_slice)
    return MetadataRegion(
        offset=start,
        length=end - start + 1,
        before_hex=hex_preview(before_slice),
        after_hex=hex_preview(after_slice),
        before_ascii=ascii_preview(before_preview),
        after_ascii=ascii_preview(after_preview),
        classification=classification,
        reason=reason,
        distance_from_nearest_table=distance_from_nearest_table(start, end),
    )


def preview_bytes(data: bytes) -> bytes:
    return data[:REGION_PREVIEW_BYTES]


def hex_preview(data: bytes) -> str:
    preview = preview_bytes(data).hex(" ")
    if len(data) > REGION_PREVIEW_BYTES:
        return f"{preview} ... ({len(data)} bytes total)"
    return preview


def ascii_preview(data: bytes) -> str:
    return "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in data)


def distance_from_nearest_table(start: int, end: int) -> int:
    distances = []
    for table_start, table_end in IGNORED_TABLE_RANGES:
        if end < table_start:
            distances.append(table_start - end)
        elif start >= table_end:
            distances.append(start - table_end + 1)
        else:
            distances.append(0)
    return min(distances) if distances else -1


def classify_region(offset: int, before: bytes, after: bytes) -> tuple[str, str]:
    length = max(len(before), len(after))
    if offset < PAYLOAD_START:
        return "header", "changed before payload start"
    if is_possible_counter(before, after, 2):
        return "possible_counter", "2-byte little-endian value changed by a small delta"
    if is_possible_counter(before, after, 4):
        return "possible_counter", "4-byte little-endian value changed by a small delta"
    if is_possible_bitmap(before, after):
        return "possible_bitmap", "sparse bit-level changes in a multi-byte region"
    if is_possible_index_table(before, after):
        return "possible_index_table", "changed bytes resemble a small sequential array"
    if is_possible_checksum(offset, length, before, after):
        return "possible_checksum", "small isolated changed region, checksum-like but unproven"
    return "unknown", "no conservative heuristic matched"


def is_possible_counter(before: bytes, after: bytes, width: int) -> bool:
    if len(before) != width or len(after) != width:
        return False
    before_value = int.from_bytes(before, "little")
    after_value = int.from_bytes(after, "little")
    delta = abs(after_value - before_value)
    return 0 < delta <= 16


def is_possible_bitmap(before: bytes, after: bytes) -> bool:
    if len(before) < 4 or len(before) != len(after):
        return False
    changed_bits = sum((left ^ right).bit_count() for left, right in zip(before, after))
    return 0 < changed_bits <= max(4, len(before))


def is_possible_index_table(before: bytes, after: bytes) -> bool:
    if len(before) < 4 or len(before) != len(after):
        return False
    return is_mostly_sequential(before) or is_mostly_sequential(after)


def is_mostly_sequential(data: bytes) -> bool:
    if len(data) < 4:
        return False
    steps = [
        (right - left) % 256
        for left, right in zip(data, data[1:])
    ]
    common_step, count = Counter(steps).most_common(1)[0]
    return common_step in (1, 2, 4) and count >= len(steps) - 1


def is_possible_checksum(offset: int, length: int, before: bytes, after: bytes) -> bool:
    if length not in (1, 2, 4, 8, 16, 32):
        return False
    if offset < PAYLOAD_START:
        return False
    if before == after:
        return False
    return True
