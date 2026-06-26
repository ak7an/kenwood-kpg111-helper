"""Experimental channel browser tab for the OpenKPG tkinter GUI."""

from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    ttk = None

from .helpers import (
    CHANNEL_RECORD_COUNT,
    CHANNEL_RECORD_STRIDE,
    CHANNEL_TABLE_START,
    ChannelRecordRow,
    extract_channel_records,
    format_offset,
    format_record_hex,
    parse_int_auto_base,
)


class ChannelTab:
    tab_title = "Channels"

    def __init__(
        self,
        notebook: ttk.Notebook,
        set_text: object,
        show_error: object,
        show_info: object,
        status_callback: object,
    ) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.set_text = set_text
        self.show_error = show_error
        self.show_info = show_info
        self.status_callback = status_callback
        self.raw_bytes = b""
        self.xor_mask = 0x00
        self.rows_by_item: dict[str, ChannelRecordRow] = {}

        self.start_var = tk.StringVar(value=f"0x{CHANNEL_TABLE_START:x}")
        self.stride_var = tk.StringVar(value=f"0x{CHANNEL_RECORD_STRIDE:x}")
        self.count_entry_var = tk.StringVar(value=str(CHANNEL_RECORD_COUNT))
        self.record_count_var = tk.StringVar(value="Channel records: 0")
        self.detail_offset_var = tk.StringVar(value="")
        self.detail_index_var = tk.StringVar(value="")
        self.detail_rx_var = tk.StringVar(value="")
        self.detail_tx_var = tk.StringVar(value="")

        self.frame = ttk.Frame(notebook, padding=4)
        self._build()
        notebook.add(self.frame, text=self.tab_title)

    def _build(self) -> None:
        ttk.Label(
            self.frame,
            text="Experimental / read-only channel record view. Frequency is not decoded yet.",
        ).pack(anchor=tk.W, pady=(0, 4))

        controls = ttk.Frame(self.frame)
        controls.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(controls, text="Start offset:").pack(side=tk.LEFT)
        ttk.Entry(controls, textvariable=self.start_var, width=10).pack(side=tk.LEFT, padx=(4, 8))
        ttk.Label(controls, text="Stride:").pack(side=tk.LEFT)
        ttk.Entry(controls, textvariable=self.stride_var, width=8).pack(side=tk.LEFT, padx=(4, 8))
        ttk.Label(controls, text="Count:").pack(side=tk.LEFT)
        ttk.Entry(controls, textvariable=self.count_entry_var, width=6).pack(side=tk.LEFT, padx=(4, 8))
        ttk.Button(controls, text="Reload channel view", command=self.reload).pack(side=tk.LEFT)

        ttk.Label(self.frame, textvariable=self.record_count_var).pack(anchor=tk.W, pady=(0, 4))

        pane = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)
        table_frame = ttk.Frame(pane, padding=(0, 0, 4, 0))
        detail_frame = ttk.Frame(pane, padding=(4, 0, 0, 0))
        pane.add(table_frame, weight=1)
        pane.add(detail_frame, weight=2)

        self.table = self._tree_with_scrollbars(
            table_frame,
            columns=("channel", "offset", "rx_bytes", "tx_bytes", "marker_08", "marker_0c", "ascii_preview"),
            headings={
                "channel": "Channel",
                "offset": "Record offset",
                "rx_bytes": "RX bytes",
                "tx_bytes": "TX bytes",
                "marker_08": "Marker +0x08",
                "marker_0c": "Marker +0x0C",
                "ascii_preview": "ASCII preview",
            },
        )
        self.table.bind("<<TreeviewSelect>>", self._on_selected)
        self._build_details(detail_frame)

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
            tree.column(column, width=150 if column == "ascii_preview" else 110, anchor=tk.W)
        tree.grid(row=0, column=0, sticky=tk.NSEW)
        y_scroll.grid(row=0, column=1, sticky=tk.NS)
        x_scroll.grid(row=1, column=0, sticky=tk.EW)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        return tree

    def _build_details(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Selected channel details").grid(row=0, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(parent, text="Record index:").grid(row=1, column=0, sticky=tk.W, pady=(6, 0))
        ttk.Label(parent, textvariable=self.detail_index_var).grid(row=1, column=1, sticky=tk.W, pady=(6, 0))
        ttk.Label(parent, text="Record offset:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(parent, textvariable=self.detail_offset_var).grid(row=2, column=1, sticky=tk.W)
        ttk.Label(parent, text="RX bytes:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(parent, textvariable=self.detail_rx_var).grid(row=3, column=1, sticky=tk.W)
        ttk.Label(parent, text="TX bytes:").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(parent, textvariable=self.detail_tx_var).grid(row=4, column=1, sticky=tk.W)

        ttk.Label(parent, text="Raw 64-byte record hex:").grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(8, 0))
        self.raw_record_text = tk.Text(parent, height=5, width=62, wrap=tk.NONE, state=tk.DISABLED)
        self.raw_record_text.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW)

        ttk.Label(parent, text="Normalized 64-byte record hex:").grid(
            row=7, column=0, columnspan=2, sticky=tk.W, pady=(8, 0)
        )
        self.normalized_record_text = tk.Text(parent, height=5, width=62, wrap=tk.NONE, state=tk.DISABLED)
        self.normalized_record_text.grid(row=8, column=0, columnspan=2, sticky=tk.NSEW)

        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(6, weight=1)
        parent.rowconfigure(8, weight=1)

    def build_rows(self, raw_bytes: bytes, xor_mask: int) -> list[ChannelRecordRow]:
        count = parse_int_auto_base(self.count_entry_var.get())
        return extract_channel_records(
            raw_bytes,
            start=self.start_var.get(),
            stride=self.stride_var.get(),
            count=count,
            xor_mask=xor_mask,
        )

    def load_file(self, raw_bytes: bytes, xor_mask: int) -> list[ChannelRecordRow]:
        self.raw_bytes = raw_bytes
        self.xor_mask = xor_mask
        rows = self.build_rows(raw_bytes, xor_mask)
        self.populate(rows)
        return rows

    def reload(self) -> None:
        if not self.raw_bytes:
            self.show_info("Reload channel view", "No DAT file is currently loaded.")
            return
        try:
            rows = self.build_rows(self.raw_bytes, self.xor_mask)
        except ValueError as exc:
            self.show_error("Invalid channel layout", str(exc))
            return
        self.populate(rows)
        self.status_callback(f"Channels: {len(rows)}", "Channel view refreshed")

    def refresh(self) -> None:
        self.reload()

    def populate(self, rows: list[ChannelRecordRow]) -> None:
        self.table.delete(*self.table.get_children())
        self.rows_by_item.clear()
        self.clear_details()
        self.record_count_var.set(f"Channel records: {len(rows)}")
        for row in rows:
            item = self.table.insert(
                "",
                tk.END,
                values=(
                    row.channel,
                    format_offset(row.offset),
                    row.rx_bytes,
                    row.tx_bytes,
                    row.marker_08,
                    row.marker_0c,
                    row.ascii_preview,
                ),
            )
            self.rows_by_item[item] = row

    def _on_selected(self, _event: object) -> None:
        selection = self.table.selection()
        if not selection:
            self.clear_details()
            return
        row = self.rows_by_item.get(selection[0])
        if row is None:
            self.clear_details()
            return
        self.show_details(row)

    def clear_details(self) -> None:
        self.detail_index_var.set("")
        self.detail_offset_var.set("")
        self.detail_rx_var.set("")
        self.detail_tx_var.set("")
        self.set_text(self.raw_record_text, "")
        self.set_text(self.normalized_record_text, "")

    def show_details(self, row: ChannelRecordRow) -> None:
        self.detail_index_var.set(str(row.channel))
        self.detail_offset_var.set(format_offset(row.offset))
        self.detail_rx_var.set(row.rx_bytes)
        self.detail_tx_var.set(row.tx_bytes)
        self.set_text(self.raw_record_text, format_record_hex(row.raw_record))
        self.set_text(self.normalized_record_text, format_record_hex(row.normalized_record))

    def layout_summary(self) -> str:
        return "\n".join(
            (
                "Experimental channel layout",
                f"Start offset: {self.start_var.get()}",
                f"Stride: {self.stride_var.get()}",
                f"Requested count: {self.count_entry_var.get()}",
                f"Loaded channel records: {len(self.rows_by_item)}",
                "RX bytes: record +0x05 length 3",
                "TX bytes: record +0x09 length 3",
                "Frequency is not decoded yet.",
            )
        )
