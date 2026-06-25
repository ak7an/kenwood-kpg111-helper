"""Selection state for OpenKPG views."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Selection:
    entity_type: str | None = None
    entity_key: str | None = None

    def clear(self) -> None:
        self.entity_type = None
        self.entity_key = None
