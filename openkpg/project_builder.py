"""Project-level build planning for OpenKPG channel generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from kpg111.project import Codeplug
from openkpg.channel_builder import ChannelBuilder, ChannelDefinition
from openkpg.csv_import import ImportedChannel, RejectedImportRow, import_channel_csv
from openkpg.zone_builder import DEFAULT_ZONE_NAME, ZoneBuilder, ZoneDefinition


@dataclass(frozen=True)
class BuildLimits:
    max_channels: int | None = None
    max_zones: int | None = None


@dataclass(frozen=True)
class BuildRequest:
    path: Path
    profile: str = "openkpg"
    column_mapping: Mapping[str, str] | None = None


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    code: str
    message: str
    source: str | None = None
    source_row: int | None = None


@dataclass(frozen=True)
class BuildStatistics:
    csv_files: int
    channels_imported: int
    channels_accepted: int
    channels_rejected: int
    zones_created: int
    duplicate_channels_removed: int
    warnings: int
    errors: int


@dataclass(frozen=True)
class BuildResult:
    accepted_channels: tuple[ChannelDefinition, ...]
    rejected_channels: tuple[ValidationIssue, ...]
    zones: tuple[ZoneDefinition, ...]
    validation_issues: tuple[ValidationIssue, ...]
    statistics: BuildStatistics

    @property
    def accepted_count(self) -> int:
        return len(self.accepted_channels)

    @property
    def rejected_count(self) -> int:
        return len(self.rejected_channels)

    @property
    def zone_count(self) -> int:
        return len(self.zones)

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.validation_issues if issue.severity == "warning")

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.validation_issues if issue.severity == "error")


@dataclass(frozen=True)
class BuildProject:
    requests: tuple[BuildRequest, ...] = ()
    limits: BuildLimits = BuildLimits()
    default_zone: str = DEFAULT_ZONE_NAME

    def import_csv(
        self,
        path: Path | str,
        *,
        profile: str = "openkpg",
        column_mapping: Mapping[str, str] | None = None,
    ) -> "BuildProject":
        request = BuildRequest(Path(path), profile=profile, column_mapping=column_mapping)
        return BuildProject(
            requests=(*self.requests, request),
            limits=self.limits,
            default_zone=self.default_zone,
        )

    def build(self, codeplug: Codeplug | None = None) -> BuildResult:
        active_codeplug = codeplug if codeplug is not None else Codeplug(b"")
        imported: list[ImportedChannel] = []
        issues: list[ValidationIssue] = []
        rejected_channels: list[ValidationIssue] = []
        imported_row_count = 0

        for request in self.requests:
            report = import_channel_csv(
                request.path,
                profile=request.profile,
                column_mapping=request.column_mapping,
            )
            imported.extend(report.accepted)
            imported_row_count += report.accepted_count + report.rejected_count
            for rejected in report.rejected:
                issue = import_rejection_issue(rejected)
                issues.append(issue)
                rejected_channels.append(issue)

        unique_imports, duplicate_count, duplicate_issues = remove_exact_duplicates(imported)
        issues.extend(duplicate_issues)

        buildable_imports, conflict_issues = remove_conflicting_duplicates(unique_imports)
        issues.extend(conflict_issues)
        rejected_channels.extend(conflict_issues)

        channel_plan = ChannelBuilder(active_codeplug).build(buildable_imports)
        for rejected in channel_plan.rejected:
            issue = ValidationIssue(
                severity="error",
                code="channel_rejected",
                message=rejected.reason,
                source=rejected.source,
                source_row=rejected.source_row,
            )
            issues.append(issue)
            rejected_channels.append(issue)

        zone_plan = ZoneBuilder(default_zone=self.default_zone).build(channel_plan.channels)
        for rejected in zone_plan.rejected:
            issue = ValidationIssue(
                severity="error",
                code="zone_channel_rejected",
                message=rejected.reason,
                source=rejected.source,
                source_row=rejected.source_row,
            )
            issues.append(issue)
            rejected_channels.append(issue)

        accepted_channels = tuple(channel for zone in zone_plan.zones for channel in zone.channels)
        issues.extend(validate_project(accepted_channels, zone_plan.zones, self.limits))

        warnings = sum(1 for issue in issues if issue.severity == "warning")
        errors = sum(1 for issue in issues if issue.severity == "error")
        statistics = BuildStatistics(
            csv_files=len(self.requests),
            channels_imported=imported_row_count,
            channels_accepted=len(accepted_channels),
            channels_rejected=len(rejected_channels),
            zones_created=len(zone_plan.zones),
            duplicate_channels_removed=duplicate_count,
            warnings=warnings,
            errors=errors,
        )
        return BuildResult(
            accepted_channels=accepted_channels,
            rejected_channels=tuple(rejected_channels),
            zones=zone_plan.zones,
            validation_issues=tuple(issues),
            statistics=statistics,
        )


def import_rejection_issue(rejected: RejectedImportRow) -> ValidationIssue:
    return ValidationIssue(
        severity="error",
        code="csv_row_rejected",
        message=rejected.reason,
        source=rejected.source,
        source_row=rejected.source_row,
    )


def remove_exact_duplicates(
    channels: list[ImportedChannel],
) -> tuple[tuple[ImportedChannel, ...], int, tuple[ValidationIssue, ...]]:
    seen: set[tuple[str | None, ...]] = set()
    unique: list[ImportedChannel] = []
    issues: list[ValidationIssue] = []
    duplicate_count = 0
    for channel in channels:
        key = imported_channel_key(channel)
        if key in seen:
            duplicate_count += 1
            issues.append(
                ValidationIssue(
                    severity="warning",
                    code="exact_duplicate_channel_removed",
                    message=f"exact duplicate channel removed: {channel.name}",
                    source=channel.source,
                    source_row=channel.source_row,
                )
            )
            continue
        seen.add(key)
        unique.append(channel)
    return tuple(unique), duplicate_count, tuple(issues)


def remove_conflicting_duplicates(
    channels: tuple[ImportedChannel, ...],
) -> tuple[tuple[ImportedChannel, ...], tuple[ValidationIssue, ...]]:
    by_name: dict[str, ImportedChannel] = {}
    buildable: list[ImportedChannel] = []
    issues: list[ValidationIssue] = []
    for channel in channels:
        key = normalize_name(channel.name)
        previous = by_name.get(key)
        if previous is None:
            by_name[key] = channel
            buildable.append(channel)
            continue
        if imported_channel_conflict_key(channel) != imported_channel_conflict_key(previous):
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="conflicting_duplicate_channel",
                    message=f"conflicting duplicate channel name: {channel.name}",
                    source=channel.source,
                    source_row=channel.source_row,
                )
            )
            continue
        buildable.append(channel)
    return tuple(buildable), tuple(issues)


def validate_project(
    channels: tuple[ChannelDefinition, ...],
    zones: tuple[ZoneDefinition, ...],
    limits: BuildLimits,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    if limits.max_channels is not None and len(channels) > limits.max_channels:
        issues.append(
            ValidationIssue(
                severity="error",
                code="max_channels_exceeded",
                message=f"maximum channels exceeded: {len(channels)} > {limits.max_channels}",
            )
        )
    if limits.max_zones is not None and len(zones) > limits.max_zones:
        issues.append(
            ValidationIssue(
                severity="error",
                code="max_zones_exceeded",
                message=f"maximum zones exceeded: {len(zones)} > {limits.max_zones}",
            )
        )
    issues.extend(duplicate_channel_name_issues(channels))
    issues.extend(duplicate_frequency_issues(channels))
    return tuple(issues)


def duplicate_channel_name_issues(channels: tuple[ChannelDefinition, ...]) -> tuple[ValidationIssue, ...]:
    seen: dict[str, ChannelDefinition] = {}
    issues: list[ValidationIssue] = []
    for channel in channels:
        key = normalize_name(channel.name)
        if key in seen:
            issues.append(
                ValidationIssue(
                    severity="warning",
                    code="duplicate_channel_name",
                    message=f"duplicate channel name across project: {channel.name}",
                    source=channel.source,
                    source_row=channel.source_row,
                )
            )
            continue
        seen[key] = channel
    return tuple(issues)


def duplicate_frequency_issues(channels: tuple[ChannelDefinition, ...]) -> tuple[ValidationIssue, ...]:
    seen: dict[tuple[str, str], ChannelDefinition] = {}
    issues: list[ValidationIssue] = []
    for channel in channels:
        key = (channel.rx_frequency, channel.tx_frequency)
        if key in seen:
            issues.append(
                ValidationIssue(
                    severity="warning",
                    code="duplicate_frequency",
                    message=(
                        "duplicate frequency pair: "
                        f"rx {channel.rx_frequency}, tx {channel.tx_frequency}"
                    ),
                    source=channel.source,
                    source_row=channel.source_row,
                )
            )
            continue
        seen[key] = channel
    return tuple(issues)


def imported_channel_key(channel: ImportedChannel) -> tuple[str | None, ...]:
    return (
        normalize_value(channel.name),
        normalize_value(channel.rx_frequency),
        normalize_value(channel.tx_frequency),
        normalize_value(channel.offset),
        normalize_value(channel.mode),
        normalize_value(channel.bandwidth),
        normalize_value(channel.tone),
        normalize_value(channel.ran),
        normalize_value(channel.color_code),
        normalize_value(channel.nac),
        normalize_value(channel.zone),
        normalize_value(channel.city),
        normalize_value(channel.state),
        normalize_value(channel.county),
        normalize_value(channel.callsign),
    )


def imported_channel_conflict_key(channel: ImportedChannel) -> tuple[str | None, ...]:
    return (
        normalize_value(channel.rx_frequency),
        normalize_value(channel.tx_frequency),
        normalize_value(channel.offset),
        normalize_value(channel.mode),
        normalize_value(channel.bandwidth),
        normalize_value(channel.tone),
        normalize_value(channel.ran),
        normalize_value(channel.color_code),
        normalize_value(channel.nac),
    )


def normalize_value(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(value.strip().split())
    return cleaned.casefold() if cleaned else None


def normalize_name(value: str | None) -> str:
    normalized = normalize_value(value)
    return normalized or ""
