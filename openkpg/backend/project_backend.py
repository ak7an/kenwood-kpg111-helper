"""Read-only backend facade for OpenKPG."""

from __future__ import annotations

from pathlib import Path

from kpg111.model import DecodedRecord
from kpg111.project import KPG111Project
from openkpg.core.project import OpenKPGProject
from openkpg.entities import Contact, Radio, TalkGroup


class OpenKPGProjectBackend:
    """Translate read-only kpg111 data into the OpenKPG application model."""

    def __init__(self, decode_key: int = 0x5B) -> None:
        self.decode_key = decode_key
        self.kpg111_project = KPG111Project()
        self.current_project: OpenKPGProject | None = None

    def load_dat(self, path: Path | str) -> OpenKPGProject:
        dat_path = Path(path)
        self.kpg111_project.load_program(dat_path, self.decode_key)
        if self.kpg111_project.tables is None:
            raise RuntimeError("DAT tables were not decoded")

        raw_bytes = self.kpg111_project.to_bytes()
        self.current_project = OpenKPGProject(
            radio=Radio(source_file=str(dat_path), raw_size=len(raw_bytes)),
            talkgroups=[
                self._talkgroup_from_record(record)
                for record in self.kpg111_project.tables.talk_groups
            ],
            contacts=[
                self._contact_from_record(record)
                for record in self.kpg111_project.tables.individual_ids
            ],
            raw_bytes=raw_bytes,
        )
        return self.current_project

    def table_summary(self) -> dict[str, dict[str, int | str | None]]:
        return self.kpg111_project.table_summary()

    def raw_bytes(self) -> bytes:
        if self.current_project is None or self.current_project.raw_bytes is None:
            raise RuntimeError("no project is loaded")
        return self.current_project.raw_bytes

    @staticmethod
    def _talkgroup_from_record(record: DecodedRecord) -> TalkGroup:
        return TalkGroup(
            slot=record.slot,
            name=record.name,
            numeric_id=record.numeric_id,
            source_offset=record.offset,
            empty=record.empty,
        )

    @staticmethod
    def _contact_from_record(record: DecodedRecord) -> Contact:
        return Contact(
            slot=record.slot,
            name=record.name,
            numeric_id=record.numeric_id,
            source_offset=record.offset,
            empty=record.empty,
        )
