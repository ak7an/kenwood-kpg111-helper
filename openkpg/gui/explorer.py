"""Codeplug Explorer tree for the OpenKPG tkinter GUI."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    ttk = None

from .helpers import CHANNEL_RECORD_STRIDE, CHANNEL_TABLE_START


@dataclass(frozen=True)
class ExplorerNode:
    label: str
    target: str
    channel_number: int | None = None
    children: tuple["ExplorerNode", ...] = field(default_factory=tuple)


def channel_number_to_offset(
    channel_number: int,
    start: int = CHANNEL_TABLE_START,
    stride: int = CHANNEL_RECORD_STRIDE,
) -> int:
    if channel_number <= 0:
        raise ValueError("channel_number must be >= 1")
    if stride <= 0:
        raise ValueError("stride must be > 0")
    return start + ((channel_number - 1) * stride)


def no_dat_explorer_model() -> ExplorerNode:
    return ExplorerNode(label="No DAT loaded", target="none")


def explorer_model_for_dat(
    path: Path,
    channel_count: int,
    talk_group_count: int,
    individual_id_count: int,
    channel_children_limit: int = 64,
) -> ExplorerNode:
    channel_children = tuple(
        ExplorerNode(label=f"Channel {channel}", target="channel", channel_number=channel)
        for channel in range(1, min(channel_count, channel_children_limit) + 1)
    )
    return ExplorerNode(
        label=path.name,
        target="root",
        children=(
            ExplorerNode(label="Summary", target="summary"),
            ExplorerNode(label=f"Channels ({channel_count})", target="channels", children=channel_children),
            ExplorerNode(label=f"Talk Groups ({talk_group_count})", target="talk_groups"),
            ExplorerNode(label=f"Individual IDs ({individual_id_count})", target="individual_ids"),
            ExplorerNode(label="Hex View", target="hex"),
            ExplorerNode(label="Compare", target="compare"),
        ),
    )


class CodeplugExplorer:
    def __init__(self, parent: ttk.PanedWindow, select_callback: object) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.select_callback = select_callback
        self.node_by_item: dict[str, ExplorerNode] = {}

        self.frame = ttk.Frame(parent, padding=4)
        ttk.Label(self.frame, text="Codeplug Explorer").pack(anchor=tk.W, pady=(0, 4))
        self.tree = ttk.Treeview(self.frame, show="tree", selectmode="browse")
        y_scroll = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self._on_selected)
        self.load_model(no_dat_explorer_model())

    def load_model(self, root_node: ExplorerNode) -> None:
        self.tree.delete(*self.tree.get_children())
        self.node_by_item.clear()
        root_item = self._insert_node("", root_node, open_node=True)
        self.tree.selection_set(root_item)

    def _insert_node(self, parent: str, node: ExplorerNode, open_node: bool = False) -> str:
        item = self.tree.insert(parent, tk.END, text=node.label, open=open_node)
        self.node_by_item[item] = node
        for child in node.children:
            self._insert_node(item, child, open_node=child.target == "channels")
        return item

    def _on_selected(self, _event: object) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        node = self.node_by_item.get(selection[0])
        if node is not None:
            self.select_callback(node)
