"""Application-level project model for OpenKPG."""

from __future__ import annotations

from dataclasses import dataclass, field

from openkpg.entities import Channel, Contact, Radio, ScanList, TalkGroup, UnknownRecord, Zone


@dataclass
class OpenKPGProject:
    """Modern CPS project model independent of backend record formats."""

    radio: Radio = field(default_factory=Radio)
    channels: list[Channel] = field(default_factory=list)
    zones: list[Zone] = field(default_factory=list)
    talkgroups: list[TalkGroup] = field(default_factory=list)
    contacts: list[Contact] = field(default_factory=list)
    scan_lists: list[ScanList] = field(default_factory=list)
    unknown_records: list[UnknownRecord] = field(default_factory=list)
    raw_bytes: bytes | None = None

    def memory_usage_summary(self) -> dict[str, int]:
        return {
            "channels": len(self.channels),
            "zones": len(self.zones),
            "talkgroups": len([record for record in self.talkgroups if not record.empty]),
            "contacts": len([record for record in self.contacts if not record.empty]),
            "scan_lists": len(self.scan_lists),
            "unknown_records": len(self.unknown_records),
        }
