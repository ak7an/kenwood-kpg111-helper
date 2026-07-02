"""Generic CSV channel import normalization for OpenKPG."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

CHANNEL_FIELDS = (
    "name",
    "rx_frequency",
    "tx_frequency",
    "offset",
    "mode",
    "bandwidth",
    "tone",
    "ran",
    "color_code",
    "nac",
    "zone",
    "city",
    "state",
    "county",
    "callsign",
)
REQUIRED_FIELDS = ("name", "rx_frequency")

OPENKPG_PROFILE = {
    "name": "name",
    "channelname": "name",
    "rxfrequency": "rx_frequency",
    "rxfreq": "rx_frequency",
    "receivefrequency": "rx_frequency",
    "txfrequency": "tx_frequency",
    "txfreq": "tx_frequency",
    "transmitfrequency": "tx_frequency",
    "offset": "offset",
    "mode": "mode",
    "bandwidth": "bandwidth",
    "tone": "tone",
    "ran": "ran",
    "colorcode": "color_code",
    "nac": "nac",
    "zone": "zone",
    "city": "city",
    "state": "state",
    "county": "county",
    "callsign": "callsign",
    "call": "callsign",
}

REPEATERBOOK_PROFILE = {
    "name": "name",
    "callsign": "callsign",
    "call": "callsign",
    "output": "rx_frequency",
    "outputfrequency": "rx_frequency",
    "frequency": "rx_frequency",
    "input": "tx_frequency",
    "inputfrequency": "tx_frequency",
    "offset": "offset",
    "uplinktone": "tone",
    "downlinktone": "tone",
    "tone": "tone",
    "pl": "tone",
    "ctcss": "tone",
    "mode": "mode",
    "bandwidth": "bandwidth",
    "ran": "ran",
    "colorcode": "color_code",
    "nac": "nac",
    "nearestcity": "city",
    "city": "city",
    "state": "state",
    "county": "county",
    "zone": "zone",
}

PROFILES = {
    "openkpg": OPENKPG_PROFILE,
    "repeaterbook": REPEATERBOOK_PROFILE,
}


@dataclass(frozen=True)
class ImportedChannel:
    name: str
    rx_frequency: str
    tx_frequency: str | None = None
    offset: str | None = None
    mode: str | None = None
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
class RejectedImportRow:
    source: str
    source_row: int
    reason: str
    raw: Mapping[str, str]


@dataclass(frozen=True)
class ImportReport:
    profile: str
    source: str
    accepted: tuple[ImportedChannel, ...]
    rejected: tuple[RejectedImportRow, ...]

    @property
    def accepted_count(self) -> int:
        return len(self.accepted)

    @property
    def rejected_count(self) -> int:
        return len(self.rejected)


def import_channel_csv(
    path: Path | str,
    *,
    profile: str = "openkpg",
    column_mapping: Mapping[str, str] | None = None,
) -> ImportReport:
    source = Path(path)
    profile_mapping = profile_column_mapping(profile)
    if column_mapping:
        profile_mapping = {**profile_mapping, **normalize_column_mapping(column_mapping)}

    accepted: list[ImportedChannel] = []
    rejected: list[RejectedImportRow] = []
    with source.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            return ImportReport(
                profile,
                str(source),
                (),
                (RejectedImportRow(str(source), 1, "missing header row", {}),),
            )

        normalized_headers = {normalize_header(header): header for header in reader.fieldnames}
        mapped_headers = {
            field: normalized_headers[header_key]
            for header_key, field in profile_mapping.items()
            if header_key in normalized_headers
        }
        missing_columns = [field for field in REQUIRED_FIELDS if field not in mapped_headers]
        if missing_columns:
            reason = "missing required columns: " + ", ".join(missing_columns)
            return ImportReport(
                profile,
                str(source),
                (),
                (RejectedImportRow(str(source), 1, reason, {}),),
            )

        for source_row, row in enumerate(reader, start=2):
            values = extract_values(row, mapped_headers)
            reasons = validate_values(values)
            if reasons:
                rejected.append(
                    RejectedImportRow(
                        source=str(source),
                        source_row=source_row,
                        reason="; ".join(reasons),
                        raw=dict(row),
                    )
                )
                continue
            accepted.append(
                ImportedChannel(
                    source=str(source),
                    source_row=source_row,
                    **values,
                )
            )
    return ImportReport(profile, str(source), tuple(accepted), tuple(rejected))


def profile_column_mapping(profile: str) -> dict[str, str]:
    key = profile.strip().casefold()
    if key not in PROFILES:
        raise ValueError(f"unsupported CSV import profile: {profile}")
    return dict(PROFILES[key])


def normalize_column_mapping(column_mapping: Mapping[str, str]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for source_header, target_field in column_mapping.items():
        if target_field not in CHANNEL_FIELDS:
            raise ValueError(f"unsupported imported channel field: {target_field}")
        normalized[normalize_header(source_header)] = target_field
    return normalized


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.strip().casefold())


def clean_value(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(value.strip().split())
    return cleaned or None


def extract_values(row: Mapping[str, str], mapped_headers: Mapping[str, str]) -> dict[str, str | None]:
    values = {field: None for field in CHANNEL_FIELDS}
    for field, header in mapped_headers.items():
        values[field] = clean_value(row.get(header))
    return values


def validate_values(values: Mapping[str, str | None]) -> list[str]:
    reasons = []
    for field in REQUIRED_FIELDS:
        if not values.get(field):
            reasons.append(f"{field} is required")
    return reasons
