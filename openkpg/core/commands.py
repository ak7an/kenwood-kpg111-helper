"""Command pattern placeholders for future edit operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Command(Protocol):
    label: str

    def execute(self) -> None:
        ...

    def undo(self) -> None:
        ...


@dataclass
class CommandPlaceholder:
    label: str

    def execute(self) -> None:
        raise NotImplementedError("Editing commands are not implemented yet")

    def undo(self) -> None:
        raise NotImplementedError("Undo is not implemented yet")


class AddChannel(CommandPlaceholder):
    def __init__(self) -> None:
        super().__init__("Add Channel")


class DeleteChannel(CommandPlaceholder):
    def __init__(self) -> None:
        super().__init__("Delete Channel")


class EditChannel(CommandPlaceholder):
    def __init__(self) -> None:
        super().__init__("Edit Channel")
