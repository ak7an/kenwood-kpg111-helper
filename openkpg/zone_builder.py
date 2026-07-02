"""Zone build planning for validated OpenKPG channel definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from openkpg.channel_builder import ChannelDefinition

DEFAULT_ZONE_NAME = "Default"


@dataclass(frozen=True)
class ZoneDefinition:
    name: str
    channels: tuple[ChannelDefinition, ...]


@dataclass(frozen=True)
class RejectedZoneChannel:
    source: str | None
    source_row: int | None
    zone: str | None
    channel_name: str | None
    reason: str


@dataclass(frozen=True)
class ZoneBuildPlan:
    zones: tuple[ZoneDefinition, ...]
    rejected: tuple[RejectedZoneChannel, ...]

    @property
    def accepted_count(self) -> int:
        return sum(len(zone.channels) for zone in self.zones)

    @property
    def rejected_count(self) -> int:
        return len(self.rejected)


class ZoneBuilder:
    """Group channel definitions into validated zone plans without DAT writes."""

    def __init__(self, default_zone: str = DEFAULT_ZONE_NAME) -> None:
        cleaned_default = clean_text(default_zone)
        if cleaned_default is None:
            raise ValueError("default zone name is required")
        self.default_zone = cleaned_default

    def build(self, channels: Iterable[ChannelDefinition]) -> ZoneBuildPlan:
        grouped: dict[str, list[ChannelDefinition]] = {}
        seen_names: dict[str, set[str]] = {}
        rejected: list[RejectedZoneChannel] = []

        for channel in channels:
            zone_name = normalize_zone_name(channel.zone, default=self.default_zone)
            channel_name = clean_text(channel.name)
            if channel_name is None:
                rejected.append(rejected_channel(channel, zone_name, "channel name is required"))
                continue
            normalized_channel_name = channel_name.casefold()
            used_names = seen_names.setdefault(zone_name, set())
            if normalized_channel_name in used_names:
                rejected.append(
                    rejected_channel(
                        channel,
                        zone_name,
                        f"duplicate channel name in zone {zone_name!r}: {channel_name}",
                    )
                )
                continue
            used_names.add(normalized_channel_name)
            grouped.setdefault(zone_name, []).append(channel)

        zones = tuple(ZoneDefinition(name, tuple(zone_channels)) for name, zone_channels in grouped.items())
        return ZoneBuildPlan(zones=zones, rejected=tuple(rejected))


def normalize_zone_name(value: str | None, *, default: str = DEFAULT_ZONE_NAME) -> str:
    cleaned = clean_text(value)
    if cleaned is None:
        cleaned = clean_text(default)
    if cleaned is None:
        raise ValueError("default zone name is required")
    return cleaned


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(value.strip().split())
    return cleaned or None


def rejected_channel(channel: ChannelDefinition, zone_name: str, reason: str) -> RejectedZoneChannel:
    return RejectedZoneChannel(
        source=channel.source,
        source_row=channel.source_row,
        zone=zone_name,
        channel_name=channel.name,
        reason=reason,
    )
