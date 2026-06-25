"""Read-only project facade for KPG111 Program.dat table workflows."""

from __future__ import annotations

from pathlib import Path

from .decoder import decode_program_tables
from .export import export_tables
from .imports import ImportRecord, load_import_csv, load_import_csvs
from .model import DecodedRecord, ProgramTables
from .planner import MergePlan, plan_merge
from .tables import trim_after_table


class KPG111Project:
    """Coordinate decoding, imports, and merge planning without writing Program.dat."""

    def __init__(self) -> None:
        self.program_path: Path | None = None
        self.decode_key: int | None = None
        self.tables: ProgramTables | None = None
        self.import_records: list[ImportRecord] = []
        self.latest_merge_plan: MergePlan | None = None

    def load_program(self, path: Path | str, decode_key: int) -> "KPG111Project":
        self.program_path = Path(path)
        self.decode_key = decode_key
        self.tables = decode_program_tables(self.program_path, decode_key, include_empty=True)
        self.latest_merge_plan = None
        return self

    def import_csv(self, path: Path | str) -> list[ImportRecord]:
        records = load_import_csv(path)
        self.import_records.extend(records)
        self.latest_merge_plan = None
        return records

    def import_csvs(self, paths: list[Path] | list[str]) -> list[ImportRecord]:
        records = load_import_csvs(paths)
        self.import_records.extend(records)
        self.latest_merge_plan = None
        return records

    def plan_merge(self) -> MergePlan:
        self._require_program()
        self.latest_merge_plan = plan_merge(
            self.program_path,
            self.decode_key,
            self.import_records,
        )
        return self.latest_merge_plan

    def export_tables(
        self,
        out_dir: Path | str,
        prefix: str | None = None,
        include_empty: bool = False,
    ) -> dict[str, Path]:
        self._require_tables()
        return export_tables(self.tables, out_dir, prefix=prefix, include_empty=include_empty)

    def table_summary(self) -> dict[str, dict[str, int | str | None]]:
        self._require_tables()
        return {
            "individual_ids": self._record_summary(trim_after_table(self.tables.individual_ids)),
            "talk_groups": self._record_summary(trim_after_table(self.tables.talk_groups)),
        }

    def import_summary(self) -> dict[str, int]:
        return {
            "total": len(self.import_records),
            "individual_ids": sum(1 for record in self.import_records if record.record_type == "individual_ids"),
            "talk_groups": sum(1 for record in self.import_records if record.record_type == "talk_groups"),
        }

    def plan_summary(self) -> dict[str, int]:
        plan = self.latest_merge_plan or self.plan_merge()
        counts: dict[str, int] = {
            "total": len(plan.actions),
            "duplicate_exact": 0,
            "possible_update": 0,
            "duplicate_name_id_diff": 0,
            "new_record": 0,
            "invalid": 0,
            "individual_id_empty_slots_available": plan.empty_slots_available["individual_ids"],
            "talk_group_empty_slots_available": plan.empty_slots_available["talk_groups"],
            "individual_id_append_slots_needed": plan.append_slots_needed["individual_ids"],
            "talk_group_append_slots_needed": plan.append_slots_needed["talk_groups"],
        }
        for action in plan.actions:
            counts[action.action] = counts.get(action.action, 0) + 1
        return counts

    def _require_program(self) -> None:
        if self.program_path is None or self.decode_key is None:
            raise RuntimeError("load_program must be called first")

    def _require_tables(self) -> None:
        self._require_program()
        if self.tables is None:
            raise RuntimeError("program tables have not been decoded")

    @staticmethod
    def _occupied(record: DecodedRecord) -> bool:
        return bool(record.name) and not record.empty

    def _record_summary(self, records: list[DecodedRecord]) -> dict[str, int | str | None]:
        occupied = [record for record in records if self._occupied(record)]
        empty = [record for record in records if record.empty]
        first_empty = empty[0] if empty else None
        return {
            "records": len(records),
            "occupied": len(occupied),
            "empty": len(empty),
            "first_empty_slot": None if first_empty is None else first_empty.slot,
            "first_empty_offset": None if first_empty is None else f"0x{first_empty.offset:08x}",
        }
