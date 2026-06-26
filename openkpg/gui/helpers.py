"""Display-independent helpers for the read-only OpenKPG tkinter GUI."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from openkpg.dat.frequency import decode_frequency_low24


DAT_HEADER_SIZE = 0x40
HEX_VIEW_DEFAULT_LENGTH = 4096
HEXDUMP_WIDTH = 16

CHANNEL_TABLE_START = 0x5E80
CHANNEL_RECORD_STRIDE = 0x40
CHANNEL_RECORD_SIZE = 0x40
CHANNEL_RECORD_COUNT = 128
CHANNEL_COMPARE_RECORD_COUNT = 512
CHANNEL_RX_OFFSET = 0x05
CHANNEL_TX_OFFSET = 0x09
CHANNEL_MARKER_08_OFFSET = 0x08
CHANNEL_MARKER_0C_OFFSET = 0x0C
CHANNEL_FREQUENCY_SIZE = 3


@dataclass(frozen=True)
class ChannelRecordRow:
    channel: int
    offset: int
    rx_bytes: str
    tx_bytes: str
    rx_low24_decoded: str
    tx_low24_decoded: str
    marker_08: str
    marker_0c: str
    ascii_preview: str
    raw_record: bytes
    normalized_record: bytes


@dataclass(frozen=True)
class LoadedDatSummary:
    path: Path
    size: int
    talk_group_count: int
    individual_id_count: int
    channel_count: int


@dataclass(frozen=True)
class ChannelLocation:
    channel: int
    relative_offset: int
    label: str


@dataclass(frozen=True)
class NormalizedDifference:
    offset: int
    left_byte: int
    right_raw_byte: int
    right_normalized_byte: int
    channel_location: ChannelLocation | None


@dataclass(frozen=True)
class NormalizedDiffResult:
    dominant_xor_mask: int
    payload_bytes_compared: int
    normalized_differing_byte_count: int
    differences: list[NormalizedDifference]


def parse_int_auto_base(value: str | int) -> int:
    """Parse decimal or 0x-prefixed hexadecimal integers."""
    if isinstance(value, int):
        return value
    return int(value.strip(), 0)


def parse_offset(value: str | int) -> int:
    parsed = parse_int_auto_base(value)
    if parsed < 0:
        raise ValueError("offset must be >= 0")
    return parsed


def format_offset(offset: int | None) -> str:
    if offset is None:
        return ""
    return f"0x{offset:08x}"


def format_hex_bytes(data: bytes) -> str:
    return data.hex(" ")


def format_frequency_low24(raw: bytes) -> str:
    return str(decode_frequency_low24(raw))


def format_bytes(data: bytes) -> str:
    """Compatibility alias for older callers."""
    return format_hex_bytes(data)


def ascii_safe(data: bytes) -> str:
    return "".join(chr(byte) if 0x20 <= byte <= 0x7E else "." for byte in data)


def format_record_hex(data: bytes) -> str:
    return "\n".join(
        format_hex_bytes(data[offset : offset + HEXDUMP_WIDTH])
        for offset in range(0, len(data), HEXDUMP_WIDTH)
    )


def make_hexdump_rows(
    data: bytes,
    start: int | str = 0,
    length: int | str | None = HEX_VIEW_DEFAULT_LENGTH,
    width: int = HEXDUMP_WIDTH,
) -> list[str]:
    start_offset = parse_offset(start)
    if width <= 0:
        raise ValueError("width must be > 0")
    if length is None:
        end = len(data)
    else:
        parsed_length = parse_int_auto_base(length)
        if parsed_length < 0:
            raise ValueError("length must be >= 0")
        end = min(len(data), start_offset + parsed_length)

    rows: list[str] = []
    for offset in range(start_offset, end, width):
        chunk = data[offset : offset + width]
        hex_part = format_hex_bytes(chunk).ljust((width * 3) - 1)
        rows.append(f"{offset:08x}  {hex_part}  |{ascii_safe(chunk)}|")
    return rows


def detect_self_payload_xor_mask(data: bytes) -> int:
    """Placeholder mask detection for a DAT compared with itself."""
    return 0x00


def normalize_record(record: bytes, xor_mask: int) -> bytes:
    return bytes(byte ^ xor_mask for byte in record)


def dominant_xor_mask(left_payload: bytes, right_payload: bytes) -> int:
    compared = min(len(left_payload), len(right_payload))
    if compared == 0:
        return 0x00
    counts = Counter(left_payload[index] ^ right_payload[index] for index in range(compared))
    return counts.most_common(1)[0][0]


def channel_location_for_offset(
    offset: int,
    start: int = CHANNEL_TABLE_START,
    stride: int = CHANNEL_RECORD_STRIDE,
    count: int = CHANNEL_COMPARE_RECORD_COUNT,
) -> ChannelLocation | None:
    if stride <= 0:
        raise ValueError("stride must be > 0")
    if count < 0:
        raise ValueError("count must be >= 0")
    if offset < start:
        return None
    relative_from_start = offset - start
    index, relative_offset = divmod(relative_from_start, stride)
    if index >= count or relative_offset >= CHANNEL_RECORD_SIZE:
        return None

    if CHANNEL_RX_OFFSET <= relative_offset < CHANNEL_RX_OFFSET + CHANNEL_FREQUENCY_SIZE:
        label = "RX frequency"
    elif CHANNEL_TX_OFFSET <= relative_offset < CHANNEL_TX_OFFSET + CHANNEL_FREQUENCY_SIZE:
        label = "TX frequency"
    else:
        label = f"channel record +0x{relative_offset:02x}"
    return ChannelLocation(channel=index + 1, relative_offset=relative_offset, label=label)


def normalized_differences(
    left: bytes,
    right: bytes,
    header_size: int = DAT_HEADER_SIZE,
    limit: int | None = None,
) -> NormalizedDiffResult:
    if len(left) != len(right):
        raise ValueError("files must be the same size")
    if header_size < 0:
        raise ValueError("header_size must be >= 0")

    left_payload = left[header_size:]
    right_payload = right[header_size:]
    mask = dominant_xor_mask(left_payload, right_payload)
    differences: list[NormalizedDifference] = []
    differing_count = 0
    for payload_index, (left_byte, right_raw_byte) in enumerate(zip(left_payload, right_payload)):
        right_normalized_byte = right_raw_byte ^ mask
        if left_byte == right_normalized_byte:
            continue
        differing_count += 1
        if limit is None or len(differences) < limit:
            absolute_offset = header_size + payload_index
            differences.append(
                NormalizedDifference(
                    offset=absolute_offset,
                    left_byte=left_byte,
                    right_raw_byte=right_raw_byte,
                    right_normalized_byte=right_normalized_byte,
                    channel_location=channel_location_for_offset(absolute_offset),
                )
            )
    return NormalizedDiffResult(
        dominant_xor_mask=mask,
        payload_bytes_compared=len(left_payload),
        normalized_differing_byte_count=differing_count,
        differences=differences,
    )


def extract_channel_records(
    data: bytes,
    start: int | str = CHANNEL_TABLE_START,
    stride: int | str = CHANNEL_RECORD_STRIDE,
    count: int = CHANNEL_RECORD_COUNT,
    xor_mask: int = 0x00,
) -> list[ChannelRecordRow]:
    """Return raw experimental channel record fields without decoding frequency."""
    return channel_row_model(data, start=start, stride=stride, count=count, xor_mask=xor_mask)


def channel_row_model(
    data: bytes,
    start: int | str = CHANNEL_TABLE_START,
    stride: int | str = CHANNEL_RECORD_STRIDE,
    count: int = CHANNEL_RECORD_COUNT,
    xor_mask: int = 0x00,
) -> list[ChannelRecordRow]:
    """Build read-only channel table rows from raw DAT bytes."""
    start_offset = parse_offset(start)
    record_stride = parse_offset(stride)
    if record_stride <= 0:
        raise ValueError("stride must be > 0")
    if count < 0:
        raise ValueError("count must be >= 0")

    rows: list[ChannelRecordRow] = []
    for index in range(count):
        offset = start_offset + (index * record_stride)
        record = data[offset : offset + CHANNEL_RECORD_SIZE]
        if len(record) < CHANNEL_RECORD_SIZE:
            break
        normalized_record = normalize_record(record, xor_mask)
        rx_frequency_bytes = record[CHANNEL_RX_OFFSET : CHANNEL_RX_OFFSET + CHANNEL_FREQUENCY_SIZE]
        tx_frequency_bytes = record[CHANNEL_TX_OFFSET : CHANNEL_TX_OFFSET + CHANNEL_FREQUENCY_SIZE]
        normalized_rx_frequency_bytes = normalized_record[
            CHANNEL_RX_OFFSET : CHANNEL_RX_OFFSET + CHANNEL_FREQUENCY_SIZE
        ]
        normalized_tx_frequency_bytes = normalized_record[
            CHANNEL_TX_OFFSET : CHANNEL_TX_OFFSET + CHANNEL_FREQUENCY_SIZE
        ]
        rows.append(
            ChannelRecordRow(
                channel=index + 1,
                offset=offset,
                rx_bytes=format_hex_bytes(rx_frequency_bytes),
                tx_bytes=format_hex_bytes(tx_frequency_bytes),
                rx_low24_decoded=format_frequency_low24(normalized_rx_frequency_bytes),
                tx_low24_decoded=format_frequency_low24(normalized_tx_frequency_bytes),
                marker_08=format_hex_bytes(record[CHANNEL_MARKER_08_OFFSET : CHANNEL_MARKER_08_OFFSET + 1]),
                marker_0c=format_hex_bytes(record[CHANNEL_MARKER_0C_OFFSET : CHANNEL_MARKER_0C_OFFSET + 1]),
                ascii_preview=ascii_safe(record[:16]),
                raw_record=record,
                normalized_record=normalized_record,
            )
        )
    return rows


def record_table_values(record: object) -> tuple[object, ...]:
    return (
        getattr(record, "slot"),
        format_offset(getattr(record, "source_offset")),
        getattr(record, "numeric_id"),
        getattr(record, "name"),
        "yes" if getattr(record, "empty") else "no",
        getattr(record, "confidence"),
    )


def filter_table_rows(rows: Iterable[object], query: str) -> list[object]:
    needle = query.strip().lower()
    row_list = list(rows)
    if not needle:
        return row_list

    filtered: list[object] = []
    for row in row_list:
        if isinstance(row, dict):
            values = row.values()
        elif isinstance(row, Sequence) and not isinstance(row, (str, bytes, bytearray)):
            values = row
        else:
            values = record_table_values(row)
        haystack = " ".join(str(value).lower() for value in values)
        if needle in haystack:
            filtered.append(row)
    return filtered
