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
CHANNEL_RECORD_COUNT = 64
CHANNEL_RX_OFFSET = 0x05
CHANNEL_TX_OFFSET = 0x09
CHANNEL_FREQUENCY_SIZE = 3


@dataclass(frozen=True)
class ChannelRecordRow:
    channel: int
    offset: int
    rx_bytes: str
    tx_bytes: str
    raw_record: bytes
    normalized_record: bytes


def format_offset(offset: int | None) -> str:
    if offset is None:
        return ""
    return f"0x{offset:08x}"


def format_bytes(data: bytes) -> str:
    return data.hex(" ")


def format_record_hex(data: bytes) -> str:
    return "\n".join(
        data[offset : offset + 16].hex(" ") for offset in range(0, len(data), 16)
    )


def detect_self_payload_xor_mask(data: bytes) -> int:
    """Placeholder mask detection for a DAT compared with itself."""
    return 0x00


def normalize_record(record: bytes, xor_mask: int) -> bytes:
    return bytes(byte ^ xor_mask for byte in record)


def extract_channel_records(
    data: bytes,
    start: int = CHANNEL_TABLE_START,
    stride: int = CHANNEL_RECORD_STRIDE,
    count: int = CHANNEL_RECORD_COUNT,
    xor_mask: int = 0x00,
) -> list[ChannelRecordRow]:
    """Return raw experimental channel record fields without decoding frequency."""
    rows: list[ChannelRecordRow] = []
    for index in range(count):
        offset = start + (index * stride)
        record = data[offset : offset + CHANNEL_RECORD_SIZE]
        if len(record) < CHANNEL_RECORD_SIZE:
            break
        normalized_record = normalize_record(record, xor_mask)
        rows.append(
            ChannelRecordRow(
                channel=index + 1,
                offset=offset,
                rx_bytes=format_bytes(record[CHANNEL_RX_OFFSET : CHANNEL_RX_OFFSET + CHANNEL_FREQUENCY_SIZE]),
                tx_bytes=format_bytes(record[CHANNEL_TX_OFFSET : CHANNEL_TX_OFFSET + CHANNEL_FREQUENCY_SIZE]),
                raw_record=record,
                normalized_record=normalized_record,
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
        self.channel_rows_by_item: dict[str, ChannelRecordRow] = {}

        self.path_var = tk.StringVar(value="No DAT loaded")
        self.size_var = tk.StringVar(value="")
        self.channel_record_count_var = tk.StringVar(value="Channel records: 0")
        self.status_var = tk.StringVar(value="No DAT loaded")
        self.channel_detail_offset_var = tk.StringVar(value="")
        self.channel_detail_rx_var = tk.StringVar(value="")
        self.channel_detail_tx_var = tk.StringVar(value="")

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

        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(6, 2),
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

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
        ttk.Label(channels_frame, textvariable=self.channel_record_count_var).pack(anchor=tk.W, pady=(0, 4))

        channel_pane = ttk.PanedWindow(channels_frame, orient=tk.HORIZONTAL)
        channel_pane.pack(fill=tk.BOTH, expand=True)

        channel_table_frame = ttk.Frame(channel_pane, padding=(0, 0, 4, 0))
        channel_detail_frame = ttk.Frame(channel_pane, padding=(4, 0, 0, 0))
        channel_pane.add(channel_table_frame, weight=1)
        channel_pane.add(channel_detail_frame, weight=2)

        self.channels_table = self._tree_with_scrollbars(
            channel_table_frame,
            columns=("channel", "offset", "rx_bytes", "tx_bytes"),
            headings={
                "channel": "Channel",
                "offset": "Offset",
                "rx_bytes": "RX bytes",
                "tx_bytes": "TX bytes",
            },
            manage_parent=False,
        )
        self.channels_table.bind("<<TreeviewSelect>>", self._on_channel_selected)
        self._build_channel_details(channel_detail_frame)
        notebook.add(channels_frame, text="Channels (read-only experimental)")

    def _build_channel_details(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Selected channel details").grid(row=0, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(parent, text="Record offset:").grid(row=1, column=0, sticky=tk.W, pady=(6, 0))
        ttk.Label(parent, textvariable=self.channel_detail_offset_var).grid(row=1, column=1, sticky=tk.W, pady=(6, 0))
        ttk.Label(parent, text="RX bytes:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(parent, textvariable=self.channel_detail_rx_var).grid(row=2, column=1, sticky=tk.W)
        ttk.Label(parent, text="TX bytes:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(parent, textvariable=self.channel_detail_tx_var).grid(row=3, column=1, sticky=tk.W)

        ttk.Label(parent, text="Raw 64-byte record hex:").grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(8, 0))
        self.raw_record_text = tk.Text(parent, height=5, width=58, wrap=tk.NONE, state=tk.DISABLED)
        self.raw_record_text.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW)

        ttk.Label(parent, text="Normalized 64-byte record hex:").grid(
            row=6, column=0, columnspan=2, sticky=tk.W, pady=(8, 0)
        )
        self.normalized_record_text = tk.Text(parent, height=5, width=58, wrap=tk.NONE, state=tk.DISABLED)
        self.normalized_record_text.grid(row=7, column=0, columnspan=2, sticky=tk.NSEW)

        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(5, weight=1)
        parent.rowconfigure(7, weight=1)

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
        manage_parent: bool = True,
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
        if manage_parent:
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
            xor_mask = detect_self_payload_xor_mask(raw_bytes)
            channel_rows = extract_channel_records(raw_bytes, xor_mask=xor_mask)
        except Exception as exc:  # pragma: no cover - GUI error path
            messagebox.showerror("Open DAT failed", str(exc))
            return

        self.path_var.set(str(path))
        self.size_var.set(f"{len(raw_bytes)} bytes")
        self._populate_records(self.talk_groups_table, project.talkgroups)
        self._populate_records(self.individual_ids_table, project.contacts)
        self._populate_channels(channel_rows)
        self.status_var.set(f"Loaded {path} ({len(raw_bytes)} bytes), {len(channel_rows)} channel records")

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
        self.channel_rows_by_item.clear()
        self._clear_channel_details()
        self.channel_record_count_var.set(f"Channel records: {len(rows)}")
        for row in rows:
            item = self.channels_table.insert(
                "",
                tk.END,
                values=(row.channel, format_offset(row.offset), row.rx_bytes, row.tx_bytes),
            )
            self.channel_rows_by_item[item] = row

    def _on_channel_selected(self, _event: object) -> None:
        selection = self.channels_table.selection()
        if not selection:
            self._clear_channel_details()
            return
        row = self.channel_rows_by_item.get(selection[0])
        if row is None:
            self._clear_channel_details()
            return
        self._show_channel_details(row)

    def _clear_channel_details(self) -> None:
        self.channel_detail_offset_var.set("")
        self.channel_detail_rx_var.set("")
        self.channel_detail_tx_var.set("")
        self._set_text(self.raw_record_text, "")
        self._set_text(self.normalized_record_text, "")

    def _show_channel_details(self, row: ChannelRecordRow) -> None:
        self.channel_detail_offset_var.set(format_offset(row.offset))
        self.channel_detail_rx_var.set(row.rx_bytes)
        self.channel_detail_tx_var.set(row.tx_bytes)
        self._set_text(self.raw_record_text, format_record_hex(row.raw_record))
        self._set_text(self.normalized_record_text, format_record_hex(row.normalized_record))

    def _set_text(self, widget: tk.Text, value: str) -> None:
        widget.configure(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
        widget.configure(state=tk.DISABLED)


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
