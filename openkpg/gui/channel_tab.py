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
    NormalizedDiffResult,
    extract_channel_records,
    format_offset,
    parse_int_auto_base,
)
from .property_inspector import PropertyInspector, build_channel_inspector_model
from .ui_helpers import create_tree_with_scrollbars, insert_tree_rows, install_tree_context_menu


class ChannelTab:
    tab_title = "Channels"

    def __init__(
        self,
        notebook: ttk.Notebook,
        root: tk.Tk,
        set_text: object,
        show_error: object,
        show_info: object,
        status_callback: object,
        initial_start: str = f"0x{CHANNEL_TABLE_START:x}",
        initial_stride: str = f"0x{CHANNEL_RECORD_STRIDE:x}",
        initial_count: int = CHANNEL_RECORD_COUNT,
        preferences_callback: object | None = None,
    ) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.set_text = set_text
        self.root = root
        self.show_error = show_error
        self.show_info = show_info
        self.status_callback = status_callback
        self.preferences_callback = preferences_callback
        self.raw_bytes = b""
        self.xor_mask = 0x00
        self.rows_by_item: dict[str, ChannelRecordRow] = {}
        self.compare_result: NormalizedDiffResult | None = None
        self.selected_row: ChannelRecordRow | None = None

        self.start_var = tk.StringVar(value=initial_start)
        self.stride_var = tk.StringVar(value=initial_stride)
        self.count_entry_var = tk.StringVar(value=str(initial_count))
        self.record_count_var = tk.StringVar(value="Channel records: 0")

        self.frame = ttk.Frame(notebook, padding=4)
        self._build()
        notebook.add(self.frame, text=self.tab_title)

    def _build(self) -> None:
        ttk.Label(
            self.frame,
            text="Experimental / read-only channel record view. Full MHz reconstruction pending band context.",
        ).pack(anchor=tk.W, pady=(0, 4))

        controls = ttk.Frame(self.frame)
        controls.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(controls, text="Start offset:").pack(side=tk.LEFT)
        self.start_entry = ttk.Entry(controls, textvariable=self.start_var, width=10)
        self.start_entry.pack(side=tk.LEFT, padx=(4, 8))
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
            columns=("channel", "offset", "rx_frequency", "tx_frequency", "marker_08", "marker_0c", "ascii_preview"),
            headings={
                "channel": "Channel",
                "offset": "Record offset",
                "rx_frequency": "RX Frequency",
                "tx_frequency": "TX Frequency",
                "marker_08": "Marker +0x08",
                "marker_0c": "Marker +0x0C",
                "ascii_preview": "ASCII preview",
            },
        )
        self.table.bind("<<TreeviewSelect>>", self._on_selected)
        install_tree_context_menu(self.table, self.root, lambda message: self.status_callback(None, message))
        self.inspector = PropertyInspector(detail_frame)

    def _tree_with_scrollbars(
        self,
        parent: ttk.Frame,
        columns: tuple[str, ...],
        headings: dict[str, str],
    ) -> ttk.Treeview:
        return create_tree_with_scrollbars(parent, columns, headings, widths={"ascii_preview": 150})

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
        self.save_preferences()
        self.status_callback(f"Channels: {len(rows)}", "Channel view refreshed")

    def refresh(self) -> None:
        self.reload()

    def populate(self, rows: list[ChannelRecordRow]) -> None:
        self.rows_by_item.clear()
        self.clear_details()
        self.record_count_var.set(f"Channel records: {len(rows)}")
        table_rows = [
            (
                row.channel,
                format_offset(row.offset),
                row.rx_frequency,
                row.tx_frequency,
                row.marker_08,
                row.marker_0c,
                row.ascii_preview,
            )
            for row in rows
        ]
        insert_tree_rows(self.table, table_rows)
        for item, row in zip(self.table.get_children(), rows):
            self.rows_by_item[item] = row

    def focus_search(self) -> None:
        self.start_entry.focus_set()

    def save_preferences(self) -> None:
        if self.preferences_callback is None:
            return
        count = parse_int_auto_base(self.count_entry_var.get())
        self.preferences_callback(self.start_var.get(), self.stride_var.get(), count)

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
        self.selected_row = None
        self.inspector.render(build_channel_inspector_model(None, self.compare_result))

    def show_details(self, row: ChannelRecordRow) -> None:
        self.selected_row = row
        self.inspector.render(build_channel_inspector_model(row, self.compare_result))
        self.status_callback(f"Channel: {row.channel}", f"Selected channel {row.channel}")

    def select_channel(self, channel_number: int) -> None:
        for item, row in self.rows_by_item.items():
            if row.channel == channel_number:
                self.table.selection_set(item)
                self.table.focus(item)
                self.table.see(item)
                self.show_details(row)
                return

    def set_compare_result(self, compare_result: NormalizedDiffResult | None) -> None:
        self.compare_result = compare_result
        self.inspector.render(build_channel_inspector_model(self.selected_row, self.compare_result))

    def layout_summary(self) -> str:
        return "\n".join(
            (
                "Experimental channel layout",
                f"Start offset: {self.start_var.get()}",
                f"Stride: {self.stride_var.get()}",
                f"Requested count: {self.count_entry_var.get()}",
                f"Loaded channel records: {len(self.rows_by_item)}",
                "RX Frequency: record +0x05 length 3",
                "TX Frequency: record +0x09 length 3",
                "Inspector retains raw bytes for reverse engineering.",
            )
        )
