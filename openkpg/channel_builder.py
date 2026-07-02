"""Channel build planning for normalized OpenKPG imports."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Iterable

from kpg111.project import Codeplug
from openkpg.csv_import import ImportedChannel

SUPPORTED_MODES = {
    "": "FM",
    "analog": "FM",
    "fm": "FM",
    "nfm": "FM",
    "nxdn": "NXDN",
    "digital": "NXDN",
    "nxdn digital": "NXDN",
}


@dataclass(frozen=True)
class ChannelDefinition:
    name: str
    rx_frequency: str
    tx_frequency: str
    mode: str
    channel_type: str
    operation: str
    bandwidth: str | None = None
    tone: str | None = None
    ran: str | None = None
    color_code: str | None = None
    nac: str | None = None
    zone: str | None = None
    city: str | None = None
    state: str | None = None
    county: str | None = None
    callsign: str | None = None
    source: str | None = None
    source_row: int | None = None


@dataclass(frozen=True)
class RejectedChannel:
    source: str | None
    source_row: int | None
    name: str | None
    reason: str


@dataclass(frozen=True)
class ChannelBuildPlan:
    codeplug: Codeplug
    channels: tuple[ChannelDefinition, ...]
    rejected: tuple[RejectedChannel, ...]

    @property
    def accepted_count(self) -> int:
        return len(self.channels)

    @property
    def rejected_count(self) -> int:
        return len(self.rejected)


class ChannelBuilder:
    """Validate imported channels without writing channel bytes to the DAT."""

    def __init__(self, codeplug: Codeplug) -> None:
        self.codeplug = codeplug

    def build(self, imports: Iterable[ImportedChannel]) -> ChannelBuildPlan:
        channels: list[ChannelDefinition] = []
        rejected: list[RejectedChannel] = []
        for imported in imports:
            try:
                channels.append(self.build_one(imported))
            except ValueError as exc:
                rejected.append(
                    RejectedChannel(
                        source=imported.source,
                        source_row=imported.source_row,
                        name=imported.name,
                        reason=str(exc),
                    )
                )
        return ChannelBuildPlan(self.codeplug, tuple(channels), tuple(rejected))

    def build_one(self, imported: ImportedChannel) -> ChannelDefinition:
        name = require_text(imported.name, "name")
        rx = parse_frequency(imported.rx_frequency, "rx_frequency")
        mode = normalize_mode(imported.mode)
        tx = resolve_tx_frequency(rx, imported.tx_frequency, imported.offset)
        operation = "simplex" if tx == rx else "repeater"
        channel_type = "nxdn" if mode == "NXDN" else "analog"
        return ChannelDefinition(
            name=name,
            rx_frequency=format_frequency(rx),
            tx_frequency=format_frequency(tx),
            mode=mode,
            channel_type=channel_type,
            operation=operation,
            bandwidth=clean_optional(imported.bandwidth),
            tone=clean_optional(imported.tone),
            ran=clean_optional(imported.ran),
            color_code=clean_optional(imported.color_code),
            nac=clean_optional(imported.nac),
            zone=clean_optional(imported.zone),
            city=clean_optional(imported.city),
            state=clean_optional(imported.state),
            county=clean_optional(imported.county),
            callsign=clean_optional(imported.callsign),
            source=imported.source,
            source_row=imported.source_row,
        )


def require_text(value: str | None, field: str) -> str:
    cleaned = clean_optional(value)
    if cleaned is None:
        raise ValueError(f"{field} is required")
    return cleaned


def clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(value.strip().split())
    return cleaned or None


def parse_frequency(value: str | None, field: str) -> Decimal:
    text = require_text(value, field)
    try:
        frequency = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"{field} is not a valid frequency: {text!r}") from exc
    if frequency <= 0:
        raise ValueError(f"{field} must be greater than zero")
    return frequency


def parse_offset(value: str | None) -> Decimal | None:
    text = clean_optional(value)
    if text is None:
        return None
    try:
        return Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"offset is not a valid frequency offset: {text!r}") from exc


def resolve_tx_frequency(
    rx_frequency: Decimal,
    tx_frequency: str | None,
    offset: str | None,
) -> Decimal:
    tx_text = clean_optional(tx_frequency)
    if tx_text is not None:
        return parse_frequency(tx_text, "tx_frequency")
    parsed_offset = parse_offset(offset)
    if parsed_offset is None:
        return rx_frequency
    tx = rx_frequency + parsed_offset
    if tx <= 0:
        raise ValueError("calculated tx_frequency must be greater than zero")
    return tx


def normalize_mode(value: str | None) -> str:
    text = clean_optional(value)
    key = "" if text is None else text.casefold()
    if key not in SUPPORTED_MODES:
        raise ValueError(f"unsupported channel mode: {text}")
    return SUPPORTED_MODES[key]


def format_frequency(value: Decimal) -> str:
    normalized = value.normalize()
    text = format(normalized, "f")
    if "." not in text:
        return f"{text}.000"
    whole, fractional = text.split(".", 1)
    fractional = fractional.rstrip("0")
    if len(fractional) < 3:
        fractional = fractional.ljust(3, "0")
    return f"{whole}.{fractional}"
