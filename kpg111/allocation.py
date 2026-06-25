"""Read-only allocation analysis for KPG111 table experiments."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .decoder import RECORD_SIZE, decode_program_tables
from .model import DecodedRecord, ProgramTables


BASELINE_DECODE_KEYS = {
    "dattest": 0x5B,
    "dattest2": 0x34,
    "dattest3": 0x1F,
    "dattest4": 0x1E,
}


@dataclass(frozen=True)
class ExperimentPair:
    experiment: str
    baseline_path: Path
    modified_path: Path
    baseline_key: int
    modified_key: int
    source: str


@dataclass(frozen=True)
class SlotContext:
    slot: int | None
    offset: int | None
    state: str
    name: str
    numeric_id: int | None


@dataclass(frozen=True)
class AllocationEvent:
    experiment: str
    source: str
    baseline_path: Path
    modified_path: Path
    table_id: str
    table_name: str
    slot: int
    offset: int
    name: str
    numeric_id: int
    previous_slot_state: str
    previous_neighbor: SlotContext
    next_neighbor: SlotContext
    distance_from_previous_occupied: int | None
    distance_from_next_occupied: int | None
    candidate_policies: tuple[str, ...]


@dataclass(frozen=True)
class PolicyAssessment:
    policy: str
    matching_events: int
    counterexamples: int
    confidence: str
    notes: str


@dataclass(frozen=True)
class AllocationAnalysis:
    pairs: tuple[ExperimentPair, ...]
    events: tuple[AllocationEvent, ...]
    policies: tuple[PolicyAssessment, ...]
    unknowns: tuple[str, ...]


def occupied(record: DecodedRecord | None) -> bool:
    return bool(record and record.name and not record.empty)


def slot_state(record: DecodedRecord | None) -> str:
    if record is None:
        return "missing"
    if occupied(record):
        return "occupied"
    if record.empty:
        return "empty"
    return "non-empty undecoded"


def context_for(record: DecodedRecord | None) -> SlotContext:
    return SlotContext(
        slot=None if record is None else record.slot,
        offset=None if record is None else record.offset,
        state=slot_state(record),
        name="" if record is None else record.name,
        numeric_id=None if record is None else record.numeric_id,
    )


def table_rows(tables: ProgramTables) -> tuple[tuple[str, str, list[DecodedRecord]], ...]:
    return (
        ("individual_ids", "Individual IDs", tables.individual_ids),
        ("talk_groups", "Talk Groups", tables.talk_groups),
    )


def by_slot(records: list[DecodedRecord]) -> dict[int, DecodedRecord]:
    return {record.slot: record for record in records}


def previous_occupied(records_by_slot: dict[int, DecodedRecord], slot: int) -> DecodedRecord | None:
    for candidate in range(slot - 1, -1, -1):
        record = records_by_slot.get(candidate)
        if occupied(record):
            return record
    return None


def next_occupied(records_by_slot: dict[int, DecodedRecord], slot: int) -> DecodedRecord | None:
    for candidate in range(slot + 1, max(records_by_slot.keys(), default=slot) + 1):
        record = records_by_slot.get(candidate)
        if occupied(record):
            return record
    return None


def lowest_available_slot(records_by_slot: dict[int, DecodedRecord]) -> int | None:
    for slot in sorted(records_by_slot):
        record = records_by_slot[slot]
        if record.empty:
            return slot
    return None


def append_after_last_occupied_slot(records_by_slot: dict[int, DecodedRecord]) -> int | None:
    occupied_slots = [slot for slot, record in records_by_slot.items() if occupied(record)]
    if not occupied_slots:
        return 0
    return max(occupied_slots) + 1


def candidate_policies(records_by_slot: dict[int, DecodedRecord], slot: int) -> tuple[str, ...]:
    policies = []
    lowest = lowest_available_slot(records_by_slot)
    append = append_after_last_occupied_slot(records_by_slot)
    if lowest == slot:
        policies.append("lowest available slot")
        policies.append("first empty slot")
    if append == slot:
        policies.append("append after last occupied")
    if not policies:
        policies.append("unknown")
    return tuple(policies)


def discover_experiment_pairs(research_roots: list[Path]) -> list[ExperimentPair]:
    pairs: list[ExperimentPair] = []
    for root in research_roots:
        experiment = root.name
        baseline_key = BASELINE_DECODE_KEYS.get(experiment)
        xor_report = root / "reports" / "xor_analysis.json"
        if baseline_key is None or not xor_report.exists():
            continue

        report = json.loads(xor_report.read_text(encoding="utf-8"))
        baseline_path = Path(report["baseline"]["path"])
        for pair in report.get("pairs", []):
            modified_path = Path(pair["modified"]["path"])
            dominant_xor = int(pair["dominant_xor"])
            pairs.append(
                ExperimentPair(
                    experiment=experiment,
                    baseline_path=baseline_path,
                    modified_path=modified_path,
                    baseline_key=baseline_key,
                    modified_key=baseline_key ^ dominant_xor,
                    source=str(xor_report),
                )
            )

    dattest4 = next((root for root in research_roots if root.name == "dattest4"), None)
    if dattest4 is not None:
        program5 = dattest4 / "Dattest4" / "Program5.dat"
        program6 = dattest4 / "Dattest4" / "Program6.dat"
        if program5.exists() and program6.exists():
            pairs.append(
                ExperimentPair(
                    experiment="dattest4",
                    baseline_path=program5,
                    modified_path=program6,
                    baseline_key=0x1E ^ 0x46,
                    modified_key=0x1E ^ 0x4A,
                    source="research/dattest4/README.md sequential Program5-to-Program6 observation",
                )
            )
    return pairs


def analyze_pair(pair: ExperimentPair, max_records: int) -> list[AllocationEvent]:
    baseline = decode_program_tables(
        pair.baseline_path,
        pair.baseline_key,
        include_empty=True,
        max_records=max_records,
    )
    modified = decode_program_tables(
        pair.modified_path,
        pair.modified_key,
        include_empty=True,
        max_records=max_records,
    )

    events: list[AllocationEvent] = []
    modified_tables = {table_id: rows for table_id, _name, rows in table_rows(modified)}
    for table_id, table_name, baseline_records in table_rows(baseline):
        before_by_slot = by_slot(baseline_records)
        after_by_slot = by_slot(modified_tables[table_id])
        added_slots = []
        for slot in sorted(set(before_by_slot) | set(after_by_slot)):
            before = before_by_slot.get(slot)
            after = after_by_slot.get(slot)
            if occupied(before) or not occupied(after):
                continue
            added_slots.append(slot)

        working_by_slot = dict(before_by_slot)
        for slot in added_slots:
            before = before_by_slot.get(slot)
            after = after_by_slot[slot]
            previous = before_by_slot.get(slot - 1)
            next_record = before_by_slot.get(slot + 1)
            previous_occ = previous_occupied(before_by_slot, slot)
            next_occ = next_occupied(before_by_slot, slot)
            events.append(
                AllocationEvent(
                    experiment=pair.experiment,
                    source=pair.source,
                    baseline_path=pair.baseline_path,
                    modified_path=pair.modified_path,
                    table_id=table_id,
                    table_name=table_name,
                    slot=slot,
                    offset=after.offset,
                    name=after.name,
                    numeric_id=after.numeric_id,
                    previous_slot_state=slot_state(before),
                    previous_neighbor=context_for(previous),
                    next_neighbor=context_for(next_record),
                    distance_from_previous_occupied=(
                        None if previous_occ is None else slot - previous_occ.slot
                    ),
                    distance_from_next_occupied=(
                        None if next_occ is None else next_occ.slot - slot
                    ),
                    candidate_policies=candidate_policies(working_by_slot, slot),
                )
            )
            working_by_slot[slot] = after
    return events


def assess_policies(events: list[AllocationEvent]) -> tuple[PolicyAssessment, ...]:
    if not events:
        return (
            PolicyAssessment(
                policy="unknown",
                matching_events=0,
                counterexamples=0,
                confidence="LOW",
                notes="No newly occupied records were observed.",
            ),
        )

    assessed = []

    first_available_matches = sum(
        1
        for event in events
        if "lowest available slot" in event.candidate_policies
        or "first empty slot" in event.candidate_policies
    )
    assessed.append(
        PolicyAssessment(
            "observed first available empty record in slot order",
            first_available_matches,
            len(events) - first_available_matches,
            "HIGH" if first_available_matches == len(events) else "MODERATE",
            "Observed behavior is consistent with selecting the first available empty record in slot order.",
        )
    )

    for policy in ("sequential scan implementation", "lowest-available-slot implementation"):
        matches = first_available_matches
        misses = len(events) - matches
        assessed.append(
            PolicyAssessment(
                policy,
                matches,
                misses,
                "MODERATE" if matches else "LOW",
                "Current experiments do not distinguish this mechanism from other implementations that produce the same observable result.",
            )
        )

    for policy in ("append after last occupied", "bitmap allocation", "free list"):
        matches = sum(1 for event in events if policy in event.candidate_policies)
        misses = len(events) - matches
        if matches == len(events):
            confidence = "HIGH"
            notes = "All observed allocations are consistent with this policy."
        elif matches and misses:
            confidence = "MODERATE"
            notes = "Some observed allocations are consistent with this policy, but counterexamples exist."
        else:
            confidence = "LOW"
            notes = "No current experiment identifies evidence for this policy."
        assessed.append(PolicyAssessment(policy, matches, misses, confidence, notes))

    unknown_matches = sum(1 for event in events if "unknown" in event.candidate_policies)
    assessed.append(
        PolicyAssessment(
            policy="unknown",
            matching_events=unknown_matches,
            counterexamples=len(events) - unknown_matches,
            confidence="LOW" if unknown_matches == 0 else "MODERATE",
            notes="Used only when an allocation does not match first-empty/lowest-available/append evidence.",
        )
    )
    return tuple(assessed)


def analyze_allocation(
    research_roots: list[Path | str] | None = None,
    max_records: int = 1024,
) -> AllocationAnalysis:
    roots = [Path(root) for root in research_roots] if research_roots else [
        Path("research/dattest"),
        Path("research/dattest2"),
        Path("research/dattest3"),
        Path("research/dattest4"),
    ]
    pairs = discover_experiment_pairs(roots)
    events: list[AllocationEvent] = []
    for pair in pairs:
        events.extend(analyze_pair(pair, max_records=max_records))

    unknowns = (
        "Program files do not prove UI operation order when multiple records appear in one modified file.",
        "No allocation bitmap, free list, count field, or pointer table has been identified.",
        "Maximum table capacity and complete table boundaries remain unresolved.",
        "The current evidence cannot distinguish lowest-available from first-empty scanning when they select the same slot.",
        "Append behavior is observed, but not enough to prove the general rule for full tables or multiple gaps.",
    )
    return AllocationAnalysis(
        pairs=tuple(pairs),
        events=tuple(events),
        policies=assess_policies(events),
        unknowns=unknowns,
    )
