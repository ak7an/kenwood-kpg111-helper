"""In-memory recent project tracking for OpenKPG."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RecentProject:
    path: Path
    label: str | None = None

    @property
    def display_name(self) -> str:
        return self.label or self.path.name


class RecentProjects:
    def __init__(self, max_items: int = 10) -> None:
        if max_items < 1:
            raise ValueError("max_items must be at least 1")
        self.max_items = max_items
        self._items: list[RecentProject] = []

    def add(self, path: Path | str, label: str | None = None) -> RecentProject:
        project = RecentProject(Path(path), label)
        self._items = [item for item in self._items if item.path != project.path]
        self._items.insert(0, project)
        del self._items[self.max_items :]
        return project

    def list(self) -> list[RecentProject]:
        return list(self._items)

    def clear(self) -> None:
        self._items.clear()
