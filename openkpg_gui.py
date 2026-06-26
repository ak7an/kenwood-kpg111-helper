#!/usr/bin/env python3
"""Simple read-only tkinter GUI for OpenKPG."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    filedialog = None
    messagebox = None
    ttk = None

from openkpg.backend import OpenKPGProjectBackend


CHANNEL_TABLE_START = 0x5E80
CHANNEL_RECORD_STRIDE = 0x40
CHANNEL_RECORD_SIZE = 0x40
CHANNEL_RECORD_COUNT = 16
CHANNEL_RX_OFFSET = 0x05
CHANNEL_TX_OFFSET = 0x09
CHANNEL_FREQUENCY_SIZE = 3


@dataclass(frozen=True)
class ChannelRecordRow:
    channel: int
    offset: int
    rx_bytes: str
    tx_bytes: str


def format_offset(offset: int | None) -> str:
    if offset is None:
        return ""
    return f"0x{offset:08x}"


def format_bytes(data: bytes) -> str:
    return data.hex(" ")


def extract_channel_records(
    data: bytes,
    start: int = CHANNEL_TABLE_START,
    stride: int = CHANNEL_RECORD_STRIDE,
    count: int = CHANNEL_RECORD_COUNT,
) -> list[ChannelRecordRow]:
    """Return raw experimental channel record fields without decoding frequency."""
    rows: list[ChannelRecordRow] = []
    for index in range(count):
        offset = start + (index * stride)
        record = data[offset : offset + CHANNEL_RECORD_SIZE]
        if len(record) < CHANNEL_RECORD_SIZE:
            break
        rows.append(
            ChannelRecordRow(
                channel=index + 1,
                offset=offset,
                rx_bytes=format_bytes(record[CHANNEL_RX_OFFSET : CHANNEL_RX_OFFSET + CHANNEL_FREQUENCY_SIZE]),
                tx_bytes=format_bytes(record[CHANNEL_TX_OFFSET : CHANNEL_TX_OFFSET + CHANNEL_FREQUENCY_SIZE]),
            )
        )
    return rows


class OpenKPGTkApp:
    def __init__(self, root: tk.Tk) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.root = root
        self.root.title("OpenKPG")
        self.backend = OpenKPGProjectBackend()

        self.path_var = tk.StringVar(value="No DAT loaded")
        self.size_var = tk.StringVar(value="")

        self._build_menu()
        self._build_layout()

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Open DAT", command=self.open_dat)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

    def _build_layout(self) -> None:
        summary = ttk.Frame(self.root, padding=8)
        summary.pack(fill=tk.X)

        ttk.Label(summary, text="File:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.path_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(summary, text="Size:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.size_var).grid(row=1, column=1, sticky=tk.W)
        summary.columnconfigure(1, weight=1)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        self.talk_groups_table = self._record_table(notebook)
        notebook.add(self.talk_groups_table.master, text="Talk Groups")

        self.individual_ids_table = self._record_table(notebook)
        notebook.add(self.individual_ids_table.master, text="Individual IDs")

        channels_frame = ttk.Frame(notebook, padding=4)
        ttk.Label(
            channels_frame,
            text=(
                "Experimental read-only channel record view. "
                "Layout: start 0x5e80, stride 0x40. Frequency bytes are not decoded."
            ),
        ).pack(anchor=tk.W, pady=(0, 4))
        self.channels_table = self._tree_with_scrollbars(
            channels_frame,
            columns=("channel", "offset", "rx_bytes", "tx_bytes"),
            headings={
                "channel": "Channel",
                "offset": "Offset",
                "rx_bytes": "RX bytes",
                "tx_bytes": "TX bytes",
            },
        )
        notebook.add(channels_frame, text="Channels (read-only experimental)")

    def _record_table(self, parent: ttk.Notebook) -> ttk.Treeview:
        frame = ttk.Frame(parent, padding=4)
        return self._tree_with_scrollbars(
            frame,
            columns=("slot", "offset", "id", "name", "empty"),
            headings={
                "slot": "Slot",
                "offset": "Offset",
                "id": "ID",
                "name": "Name",
                "empty": "Empty",
            },
        )

    def _tree_with_scrollbars(
        self,
        parent: ttk.Frame,
        columns: tuple[str, ...],
        headings: dict[str, str],
    ) -> ttk.Treeview:
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        y_scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        x_scroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        for column in columns:
            tree.heading(column, text=headings[column])
            width = 220 if column == "name" else 110
            tree.column(column, width=width, anchor=tk.W)

        tree.grid(row=0, column=0, sticky=tk.NSEW)
        y_scroll.grid(row=0, column=1, sticky=tk.NS)
        x_scroll.grid(row=1, column=0, sticky=tk.EW)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.pack(fill=tk.BOTH, expand=True)
        return tree

    def open_dat(self) -> None:
        if filedialog is None or messagebox is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        filename = filedialog.askopenfilename(
            title="Open DAT",
            filetypes=(("DAT files", "*.dat"), ("All files", "*.*")),
        )
        if not filename:
            return

        path = Path(filename)
        try:
            project = self.backend.load_dat(path)
            raw_bytes = self.backend.raw_bytes()
        except Exception as exc:  # pragma: no cover - GUI error path
            messagebox.showerror("Open DAT failed", str(exc))
            return

        self.path_var.set(str(path))
        self.size_var.set(f"{len(raw_bytes)} bytes")
        self._populate_records(self.talk_groups_table, project.talkgroups)
        self._populate_records(self.individual_ids_table, project.contacts)
        self._populate_channels(extract_channel_records(raw_bytes))

    def _clear_table(self, tree: ttk.Treeview) -> None:
        tree.delete(*tree.get_children())

    def _populate_records(self, tree: ttk.Treeview, records: Iterable[object]) -> None:
        self._clear_table(tree)
        for record in records:
            tree.insert(
                "",
                tk.END,
                values=(
                    getattr(record, "slot"),
                    format_offset(getattr(record, "source_offset")),
                    getattr(record, "numeric_id"),
                    getattr(record, "name"),
                    "yes" if getattr(record, "empty") else "no",
                ),
            )

    def _populate_channels(self, rows: list[ChannelRecordRow]) -> None:
        self._clear_table(self.channels_table)
        for row in rows:
            self.channels_table.insert(
                "",
                tk.END,
                values=(row.channel, format_offset(row.offset), row.rx_bytes, row.tx_bytes),
            )


def main() -> int:
    if tk is None:
        raise RuntimeError("tkinter is not available in this Python installation")
    root = tk.Tk()
    root.geometry("900x600")
    OpenKPGTkApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
