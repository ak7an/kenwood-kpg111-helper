"""Validation placeholders for OpenKPG projects."""

from __future__ import annotations

from dataclasses import dataclass

from .project import OpenKPGProject


@dataclass(frozen=True)
class ValidationWarning:
    code: str
    message: str
    severity: str = "WARNING"
    entity_type: str | None = None
    entity_key: str | None = None


def validate_duplicate_channels(project: OpenKPGProject) -> list[ValidationWarning]:
    warnings: list[ValidationWarning] = []
    seen: dict[str, int] = {}
    for channel in project.channels:
        key = channel.name.strip().casefold()
        if not key:
            continue
        seen[key] = seen.get(key, 0) + 1
    for name, count in seen.items():
        if count > 1:
            warnings.append(
                ValidationWarning(
                    code="duplicate_channel_name",
                    message=f"Channel name appears {count} times.",
                    entity_type="channel",
                    entity_key=name,
                )
            )
    return warnings


def validate_duplicate_talkgroups(project: OpenKPGProject) -> list[ValidationWarning]:
    warnings: list[ValidationWarning] = []
    seen_ids: dict[int, int] = {}
    for talkgroup in project.talkgroups:
        if talkgroup.empty:
            continue
        seen_ids[talkgroup.numeric_id] = seen_ids.get(talkgroup.numeric_id, 0) + 1
    for numeric_id, count in seen_ids.items():
        if count > 1:
            warnings.append(
                ValidationWarning(
                    code="duplicate_talkgroup_id",
                    message=f"Talkgroup ID {numeric_id} appears {count} times.",
                    entity_type="talkgroup",
                    entity_key=str(numeric_id),
                )
            )
    return warnings


def validate_memory_limits(project: OpenKPGProject) -> list[ValidationWarning]:
    return [
        ValidationWarning(
            code="memory_limits_unknown",
            message="Radio memory limits are not fully decoded yet.",
            severity="INFO",
        )
    ]


def validate_project(project: OpenKPGProject) -> list[ValidationWarning]:
    return (
        validate_duplicate_channels(project)
        + validate_duplicate_talkgroups(project)
        + validate_memory_limits(project)
    )
