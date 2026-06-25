"""Workspace state for OpenKPG."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .commands import Command
from .project import OpenKPGProject


@dataclass
class Workspace:
    current_project: OpenKPGProject | None = None
    open_filename: Path | None = None
    dirty: bool = False
    undo_stack: list[Command] = field(default_factory=list)

    def open_project(self, project: OpenKPGProject, filename: Path | str | None = None) -> None:
        self.current_project = project
        self.open_filename = None if filename is None else Path(filename)
        self.dirty = False
        self.undo_stack.clear()

    def mark_dirty(self) -> None:
        self.dirty = True
