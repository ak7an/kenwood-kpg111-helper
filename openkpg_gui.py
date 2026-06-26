#!/usr/bin/env python3
"""Read-only tkinter GUI for OpenKPG."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
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


DAT_HEADER_SIZE = 0x40
HEX_VIEW_DEFAULT_LENGTH = 4096
HEXDUMP_WIDTH = 16

CHANNEL_TABLE_START = 0x5E80
CHANNEL_RECORD_STRIDE = 0x40
CHANNEL_RECORD_SIZE = 0x40
CHANNEL_RECORD_COUNT = 128
CHANNEL_RX_OFFSET = 0x05
CHANNEL_TX_OFFSET = 0x09
CHANNEL_MARKER_08_OFFSET = 0x08
CHANNEL_MARKER_0C_OFFSET = 0x0C
CHANNEL_FREQUENCY_SIZE = 3


@dataclass(frozen=True)
class ChannelRecordRow:
    channel: int
    offset: int
    rx_bytes: str
    tx_bytes: str
    marker_08: str
    marker_0c: str
    ascii_preview: str
    raw_record: bytes
    normalized_record: bytes


@dataclass(frozen=True)
class LoadedDatSummary:
    path: Path
    size: int
    talk_group_count: int
    individual_id_count: int
    channel_count: int


def parse_int_auto_base(value: str | int) -> int:
    """Parse decimal or 0x-prefixed hexadecimal integers."""
    if isinstance(value, int):
        return value
    return int(value.strip(), 0)


def parse_offset(value: str | int) -> int:
    parsed = parse_int_auto_base(value)
    if parsed < 0:
        raise ValueError("offset must be >= 0")
    return parsed


def format_offset(offset: int | None) -> str:
    if offset is None:
        return ""
    return f"0x{offset:08x}"


def format_hex_bytes(data: bytes) -> str:
    return data.hex(" ")


def format_bytes(data: bytes) -> str:
    """Compatibility alias for older tests and callers."""
    return format_hex_bytes(data)


def ascii_safe(data: bytes) -> str:
    return "".join(chr(byte) if 0x20 <= byte <= 0x7E else "." for byte in data)


def format_record_hex(data: bytes) -> str:
    return "\n".join(
        format_hex_bytes(data[offset : offset + HEXDUMP_WIDTH])
        for offset in range(0, len(data), HEXDUMP_WIDTH)
    )


def make_hexdump_rows(
    data: bytes,
    start: int | str = 0,
    length: int | str | None = HEX_VIEW_DEFAULT_LENGTH,
    width: int = HEXDUMP_WIDTH,
) -> list[str]:
    start_offset = parse_offset(start)
    if width <= 0:
        raise ValueError("width must be > 0")
    if length is None:
        end = len(data)
    else:
        parsed_length = parse_int_auto_base(length)
        if parsed_length < 0:
            raise ValueError("length must be >= 0")
        end = min(len(data), start_offset + parsed_length)

    rows: list[str] = []
    for offset in range(start_offset, end, width):
        chunk = data[offset : offset + width]
        hex_part = format_hex_bytes(chunk).ljust((width * 3) - 1)
        rows.append(f"{offset:08x}  {hex_part}  |{ascii_safe(chunk)}|")
    return rows


def detect_self_payload_xor_mask(data: bytes) -> int:
    """Placeholder mask detection for a DAT compared with itself."""
    return 0x00


def normalize_record(record: bytes, xor_mask: int) -> bytes:
    return bytes(byte ^ xor_mask for byte in record)


def extract_channel_records(
    data: bytes,
    start: int | str = CHANNEL_TABLE_START,
    stride: int | str = CHANNEL_RECORD_STRIDE,
    count: int = CHANNEL_RECORD_COUNT,
    xor_mask: int = 0x00,
) -> list[ChannelRecordRow]:
    """Return raw experimental channel record fields without decoding frequency."""
    return channel_row_model(data, start=start, stride=stride, count=count, xor_mask=xor_mask)


def channel_row_model(
    data: bytes,
    start: int | str = CHANNEL_TABLE_START,
    stride: int | str = CHANNEL_RECORD_STRIDE,
    count: int = CHANNEL_RECORD_COUNT,
    xor_mask: int = 0x00,
) -> list[ChannelRecordRow]:
    """Build read-only channel table rows from raw DAT bytes."""
    start_offset = parse_offset(start)
    record_stride = parse_offset(stride)
    if record_stride <= 0:
        raise ValueError("stride must be > 0")
    if count < 0:
        raise ValueError("count must be >= 0")

    rows: list[ChannelRecordRow] = []
    for index in range(count):
        offset = start_offset + (index * record_stride)
        record = data[offset : offset + CHANNEL_RECORD_SIZE]
        if len(record) < CHANNEL_RECORD_SIZE:
            break
        normalized_record = normalize_record(record, xor_mask)
        rows.append(
            ChannelRecordRow(
                channel=index + 1,
                offset=offset,
                rx_bytes=format_hex_bytes(record[CHANNEL_RX_OFFSET : CHANNEL_RX_OFFSET + CHANNEL_FREQUENCY_SIZE]),
                tx_bytes=format_hex_bytes(record[CHANNEL_TX_OFFSET : CHANNEL_TX_OFFSET + CHANNEL_FREQUENCY_SIZE]),
                marker_08=format_hex_bytes(record[CHANNEL_MARKER_08_OFFSET : CHANNEL_MARKER_08_OFFSET + 1]),
                marker_0c=format_hex_bytes(record[CHANNEL_MARKER_0C_OFFSET : CHANNEL_MARKER_0C_OFFSET + 1]),
                ascii_preview=ascii_safe(record[:16]),
                raw_record=record,
                normalized_record=normalized_record,
            )
        )
    return rows


def record_table_values(record: object) -> tuple[object, ...]:
    return (
        getattr(record, "slot"),
        format_offset(getattr(record, "source_offset")),
        getattr(record, "numeric_id"),
        getattr(record, "name"),
        "yes" if getattr(record, "empty") else "no",
        getattr(record, "confidence"),
    )


def filter_table_rows(rows: Iterable[object], query: str) -> list[object]:
    needle = query.strip().lower()
    row_list = list(rows)
    if not needle:
        return row_list

    filtered: list[object] = []
    for row in row_list:
        if isinstance(row, dict):
            values = row.values()
        elif isinstance(row, Sequence) and not isinstance(row, (str, bytes, bytearray)):
            values = row
        else:
            values = record_table_values(row)
        haystack = " ".join(str(value).lower() for value in values)
        if needle in haystack:
            filtered.append(row)
    return filtered


class OpenKPGTkApp:
    def __init__(self, root: tk.Tk) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.root = root
        self.root.title("OpenKPG")
        self.backend = OpenKPGProjectBackend()

        self.current_path: Path | None = None
        self.raw_bytes: bytes = b""
        self.xor_mask = 0x00
        self.all_talkgroups: list[object] = []
        self.all_contacts: list[object] = []
        self.channel_rows_by_item: dict[str, ChannelRecordRow] = {}
        self.visible_hex_text = ""

        self.path_var = tk.StringVar(value="No DAT loaded")
        self.size_var = tk.StringVar(value="")
        self.header_preview_var = tk.StringVar(value="")
        self.payload_size_var = tk.StringVar(value="")
        self.xor_status_var = tk.StringVar(value="Assumed payload XOR mask: 0x00 (self comparison placeholder)")
        self.readonly_note_var = tk.StringVar(value="Read-only GUI: no DAT writing, save, or save-as functionality.")

        self.talk_group_count_var = tk.StringVar(value="Talk Group rows: 0")
        self.individual_id_count_var = tk.StringVar(value="Individual ID rows: 0")
        self.channel_record_count_var = tk.StringVar(value="Channel records: 0")
        self.talk_group_search_var = tk.StringVar(value="")
        self.individual_id_search_var = tk.StringVar(value="")

        self.channel_start_var = tk.StringVar(value=f"0x{CHANNEL_TABLE_START:x}")
        self.channel_stride_var = tk.StringVar(value=f"0x{CHANNEL_RECORD_STRIDE:x}")
        self.channel_count_entry_var = tk.StringVar(value=str(CHANNEL_RECORD_COUNT))
        self.channel_detail_offset_var = tk.StringVar(value="")
        self.channel_detail_index_var = tk.StringVar(value="")
        self.channel_detail_rx_var = tk.StringVar(value="")
        self.channel_detail_tx_var = tk.StringVar(value="")

        self.hex_jump_var = tk.StringVar(value="0x0")

        self.status_path_var = tk.StringVar(value="File: none")
        self.status_size_var = tk.StringVar(value="Size: 0")
        self.status_tg_var = tk.StringVar(value="TG: 0")
        self.status_id_var = tk.StringVar(value="Individual IDs: 0")
        self.status_channel_var = tk.StringVar(value="Channels: 0")
        self.status_message_var = tk.StringVar(value="Ready")

        self._build_menu()
        self._build_layout()

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Open DAT", command=self.open_dat)
        file_menu.add_command(label="Reload", command=self.reload_dat)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menu_bar, tearoff=False)
        view_menu.add_command(label="Refresh current tab", command=self.refresh_current_tab)
        menu_bar.add_cascade(label="View", menu=view_menu)

        tools_menu = tk.Menu(menu_bar, tearoff=False)
        tools_menu.add_command(label="Run DAT Summary", command=self.run_dat_summary)
        tools_menu.add_command(label="Run Channel Layout Summary", command=self.run_channel_layout_summary)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)

        help_menu = tk.Menu(menu_bar, tearoff=False)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def _build_layout(self) -> None:
        self._build_summary_panel()
        self._build_status_bar()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        self._build_talk_groups_tab()
        self._build_individual_ids_tab()
        self._build_channels_tab()
        self._build_hex_tab()

    def _build_summary_panel(self) -> None:
        summary = ttk.LabelFrame(self.root, text="Loaded file summary", padding=8)
        summary.pack(fill=tk.X, padx=8, pady=8)

        ttk.Label(summary, text="File path:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.path_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(summary, text="File size:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.size_var).grid(row=1, column=1, sticky=tk.W)
        ttk.Label(summary, text="Header preview:").grid(row=2, column=0, sticky=tk.NW)
        ttk.Label(summary, textvariable=self.header_preview_var, wraplength=900).grid(row=2, column=1, sticky=tk.W)
        ttk.Label(summary, text="Payload size:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.payload_size_var).grid(row=3, column=1, sticky=tk.W)
        ttk.Label(summary, text="XOR mask:").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.xor_status_var).grid(row=4, column=1, sticky=tk.W)
        ttk.Label(summary, text="Notes:").grid(row=5, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.readonly_note_var).grid(row=5, column=1, sticky=tk.W)
        summary.columnconfigure(1, weight=1)

    def _build_status_bar(self) -> None:
        status = ttk.Frame(self.root, relief=tk.SUNKEN, padding=(6, 2))
        status.pack(side=tk.BOTTOM, fill=tk.X)
        for variable in (
            self.status_path_var,
            self.status_size_var,
            self.status_tg_var,
            self.status_id_var,
            self.status_channel_var,
            self.status_message_var,
        ):
            ttk.Label(status, textvariable=variable).pack(side=tk.LEFT, padx=(0, 12))

    def _build_talk_groups_tab(self) -> None:
        frame = ttk.Frame(self.notebook, padding=4)
        self._build_record_tab_controls(
            frame,
            "Read-only decoded Talk Group records",
            self.talk_group_search_var,
            self.talk_group_count_var,
            lambda _event=None: self._populate_talk_groups(),
            lambda: self._copy_selected_record(self.talk_groups_table),
        )
        self.talk_groups_table = self._record_table(frame)
        self.notebook.add(frame, text="Talk Groups")

    def _build_individual_ids_tab(self) -> None:
        frame = ttk.Frame(self.notebook, padding=4)
        self._build_record_tab_controls(
            frame,
            "Read-only decoded Individual ID records",
            self.individual_id_search_var,
            self.individual_id_count_var,
            lambda _event=None: self._populate_individual_ids(),
            lambda: self._copy_selected_record(self.individual_ids_table),
        )
        self.individual_ids_table = self._record_table(frame)
        self.notebook.add(frame, text="Individual IDs")

    def _build_record_tab_controls(
        self,
        parent: ttk.Frame,
        label: str,
        search_var: tk.StringVar,
        count_var: tk.StringVar,
        filter_callback: object,
        copy_callback: object,
    ) -> None:
        ttk.Label(parent, text=label).pack(anchor=tk.W, pady=(0, 4))
        controls = ttk.Frame(parent)
        controls.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(controls, text="Search:").pack(side=tk.LEFT)
        entry = ttk.Entry(controls, textvariable=search_var, width=32)
        entry.pack(side=tk.LEFT, padx=(4, 8))
        entry.bind("<KeyRelease>", filter_callback)
        ttk.Button(controls, text="Copy selected row", command=copy_callback).pack(side=tk.LEFT)
        ttk.Label(parent, textvariable=count_var).pack(anchor=tk.W, pady=(0, 4))

    def _build_channels_tab(self) -> None:
        channels_frame = ttk.Frame(self.notebook, padding=4)
        ttk.Label(
            channels_frame,
            text=(
                "Experimental / read-only channel record view. "
                "Frequency is not decoded yet."
            ),
        ).pack(anchor=tk.W, pady=(0, 4))

        controls = ttk.Frame(channels_frame)
        controls.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(controls, text="Start offset:").pack(side=tk.LEFT)
        ttk.Entry(controls, textvariable=self.channel_start_var, width=10).pack(side=tk.LEFT, padx=(4, 8))
        ttk.Label(controls, text="Stride:").pack(side=tk.LEFT)
        ttk.Entry(controls, textvariable=self.channel_stride_var, width=8).pack(side=tk.LEFT, padx=(4, 8))
        ttk.Label(controls, text="Count:").pack(side=tk.LEFT)
        ttk.Entry(controls, textvariable=self.channel_count_entry_var, width=6).pack(side=tk.LEFT, padx=(4, 8))
        ttk.Button(controls, text="Reload channel view", command=self.reload_channel_view).pack(side=tk.LEFT)

        ttk.Label(channels_frame, textvariable=self.channel_record_count_var).pack(anchor=tk.W, pady=(0, 4))

        channel_pane = ttk.PanedWindow(channels_frame, orient=tk.HORIZONTAL)
        channel_pane.pack(fill=tk.BOTH, expand=True)

        channel_table_frame = ttk.Frame(channel_pane, padding=(0, 0, 4, 0))
        channel_detail_frame = ttk.Frame(channel_pane, padding=(4, 0, 0, 0))
        channel_pane.add(channel_table_frame, weight=1)
        channel_pane.add(channel_detail_frame, weight=2)

        self.channels_table = self._tree_with_scrollbars(
            channel_table_frame,
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
            manage_parent=False,
        )
        self.channels_table.bind("<<TreeviewSelect>>", self._on_channel_selected)
        self._build_channel_details(channel_detail_frame)
        self.notebook.add(channels_frame, text="Channels")

    def _build_channel_details(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Selected channel details").grid(row=0, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(parent, text="Record index:").grid(row=1, column=0, sticky=tk.W, pady=(6, 0))
        ttk.Label(parent, textvariable=self.channel_detail_index_var).grid(row=1, column=1, sticky=tk.W, pady=(6, 0))
        ttk.Label(parent, text="Record offset:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(parent, textvariable=self.channel_detail_offset_var).grid(row=2, column=1, sticky=tk.W)
        ttk.Label(parent, text="RX bytes:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(parent, textvariable=self.channel_detail_rx_var).grid(row=3, column=1, sticky=tk.W)
        ttk.Label(parent, text="TX bytes:").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(parent, textvariable=self.channel_detail_tx_var).grid(row=4, column=1, sticky=tk.W)

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

    def _build_hex_tab(self) -> None:
        frame = ttk.Frame(self.notebook, padding=4)
        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(controls, text="Jump to offset:").pack(side=tk.LEFT)
        ttk.Entry(controls, textvariable=self.hex_jump_var, width=12).pack(side=tk.LEFT, padx=(4, 8))
        ttk.Button(controls, text="Jump", command=self.jump_hex_view).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(controls, text="Copy visible hex", command=self.copy_visible_hex).pack(side=tk.LEFT)

        self.hex_text = tk.Text(frame, wrap=tk.NONE, state=tk.DISABLED, font=("Courier", 10))
        y_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.hex_text.yview)
        x_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.hex_text.xview)
        self.hex_text.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.hex_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.notebook.add(frame, text="Hex / Raw")

    def _record_table(self, parent: ttk.Frame) -> ttk.Treeview:
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        return self._tree_with_scrollbars(
            frame,
            columns=("slot", "offset", "id", "name", "empty", "confidence"),
            headings={
                "slot": "Slot",
                "offset": "Offset",
                "id": "ID",
                "name": "Name",
                "empty": "Empty",
                "confidence": "Confidence",
            },
            manage_parent=False,
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
            if column == "name":
                width = 220
            elif column == "ascii_preview":
                width = 150
            else:
                width = 110
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
        if filedialog is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        filename = filedialog.askopenfilename(
            title="Open DAT",
            filetypes=(("DAT files", "*.dat"), ("All files", "*.*")),
        )
        if filename:
            self.load_dat_path(Path(filename))

    def reload_dat(self) -> None:
        if self.current_path is None:
            self._show_info("Reload", "No DAT file is currently loaded.")
            return
        self.load_dat_path(self.current_path)

    def load_dat_path(self, path: Path) -> None:
        if not path.is_file():
            self._show_error("Open DAT failed", f"File does not exist: {path}")
            return

        self._set_status_message("Loading DAT...")
        self.root.configure(cursor="watch")
        self.root.update_idletasks()
        try:
            project = self.backend.load_dat(path)
            raw_bytes = self.backend.raw_bytes()
            xor_mask = detect_self_payload_xor_mask(raw_bytes)
            channel_rows = self._build_channel_rows(raw_bytes, xor_mask)
        except Exception as exc:  # pragma: no cover - GUI error path
            self._show_error("Open DAT failed", str(exc))
            return
        finally:
            self.root.configure(cursor="")

        self.current_path = path
        self.raw_bytes = raw_bytes
        self.xor_mask = xor_mask
        self.all_talkgroups = list(project.talkgroups)
        self.all_contacts = list(project.contacts)

        self.path_var.set(str(path))
        self.size_var.set(f"{len(raw_bytes)} bytes")
        self.header_preview_var.set(format_hex_bytes(raw_bytes[:DAT_HEADER_SIZE]))
        self.payload_size_var.set(f"{max(0, len(raw_bytes) - DAT_HEADER_SIZE)} bytes")
        self.xor_status_var.set(f"Assumed payload XOR mask: 0x{xor_mask:02x} (self comparison placeholder)")

        self._populate_talk_groups()
        self._populate_individual_ids()
        self._populate_channels(channel_rows)
        self._render_hex_view(0)
        self._set_loaded_status(
            LoadedDatSummary(
                path=path,
                size=len(raw_bytes),
                talk_group_count=len(self.all_talkgroups),
                individual_id_count=len(self.all_contacts),
                channel_count=len(channel_rows),
            )
        )
        self._set_status_message("Loaded DAT")

    def _build_channel_rows(self, raw_bytes: bytes, xor_mask: int) -> list[ChannelRecordRow]:
        count = parse_int_auto_base(self.channel_count_entry_var.get())
        return extract_channel_records(
            raw_bytes,
            start=self.channel_start_var.get(),
            stride=self.channel_stride_var.get(),
            count=count,
            xor_mask=xor_mask,
        )

    def reload_channel_view(self) -> None:
        if not self.raw_bytes:
            self._show_info("Reload channel view", "No DAT file is currently loaded.")
            return
        try:
            channel_rows = self._build_channel_rows(self.raw_bytes, self.xor_mask)
        except ValueError as exc:
            self._show_error("Invalid channel layout", str(exc))
            return
        self._populate_channels(channel_rows)
        self.status_channel_var.set(f"Channels: {len(channel_rows)}")
        self._set_status_message("Channel view refreshed")

    def refresh_current_tab(self) -> None:
        tab_text = self.notebook.tab(self.notebook.select(), "text")
        if tab_text == "Talk Groups":
            self._populate_talk_groups()
        elif tab_text == "Individual IDs":
            self._populate_individual_ids()
        elif tab_text == "Channels":
            self.reload_channel_view()
        elif tab_text == "Hex / Raw":
            self.jump_hex_view()
        self._set_status_message(f"Refreshed {tab_text}")

    def run_dat_summary(self) -> None:
        if self.current_path is None:
            self._show_info("DAT Summary", "No DAT file is currently loaded.")
            return
        self._show_info(
            "DAT Summary",
            "\n".join(
                (
                    f"File: {self.current_path}",
                    f"Size: {len(self.raw_bytes)} bytes",
                    f"Payload size: {max(0, len(self.raw_bytes) - DAT_HEADER_SIZE)} bytes",
                    f"Assumed XOR mask: 0x{self.xor_mask:02x}",
                    f"Talk Groups: {len(self.all_talkgroups)}",
                    f"Individual IDs: {len(self.all_contacts)}",
                    "Read-only GUI: no writing enabled.",
                )
            ),
        )

    def run_channel_layout_summary(self) -> None:
        if self.current_path is None:
            self._show_info("Channel Layout Summary", "No DAT file is currently loaded.")
            return
        self._show_info(
            "Channel Layout Summary",
            "\n".join(
                (
                    "Experimental channel layout",
                    f"Start offset: {self.channel_start_var.get()}",
                    f"Stride: {self.channel_stride_var.get()}",
                    f"Requested count: {self.channel_count_entry_var.get()}",
                    f"Loaded channel records: {len(self.channel_rows_by_item)}",
                    "RX bytes: record +0x05 length 3",
                    "TX bytes: record +0x09 length 3",
                    "Frequency is not decoded yet.",
                )
            ),
        )

    def show_about(self) -> None:
        self._show_info(
            "About OpenKPG",
            "OpenKPG tkinter GUI\n\nRead-only DAT browser.\nNo file writing is enabled.",
        )

    def _populate_talk_groups(self) -> None:
        rows = filter_table_rows(self.all_talkgroups, self.talk_group_search_var.get())
        self._populate_records(self.talk_groups_table, rows)
        self.talk_group_count_var.set(f"Talk Group rows: {len(rows)} of {len(self.all_talkgroups)}")

    def _populate_individual_ids(self) -> None:
        rows = filter_table_rows(self.all_contacts, self.individual_id_search_var.get())
        self._populate_records(self.individual_ids_table, rows)
        self.individual_id_count_var.set(f"Individual ID rows: {len(rows)} of {len(self.all_contacts)}")

    def _clear_table(self, tree: ttk.Treeview) -> None:
        tree.delete(*tree.get_children())

    def _populate_records(self, tree: ttk.Treeview, records: Iterable[object]) -> None:
        self._clear_table(tree)
        for record in records:
            tree.insert("", tk.END, values=record_table_values(record))

    def _populate_channels(self, rows: list[ChannelRecordRow]) -> None:
        self._clear_table(self.channels_table)
        self.channel_rows_by_item.clear()
        self._clear_channel_details()
        self.channel_record_count_var.set(f"Channel records: {len(rows)}")
        for row in rows:
            item = self.channels_table.insert(
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
        self.channel_detail_index_var.set("")
        self.channel_detail_offset_var.set("")
        self.channel_detail_rx_var.set("")
        self.channel_detail_tx_var.set("")
        self._set_text(self.raw_record_text, "")
        self._set_text(self.normalized_record_text, "")

    def _show_channel_details(self, row: ChannelRecordRow) -> None:
        self.channel_detail_index_var.set(str(row.channel))
        self.channel_detail_offset_var.set(format_offset(row.offset))
        self.channel_detail_rx_var.set(row.rx_bytes)
        self.channel_detail_tx_var.set(row.tx_bytes)
        self._set_text(self.raw_record_text, format_record_hex(row.raw_record))
        self._set_text(self.normalized_record_text, format_record_hex(row.normalized_record))

    def jump_hex_view(self) -> None:
        if not self.raw_bytes:
            self._show_info("Hex view", "No DAT file is currently loaded.")
            return
        try:
            offset = parse_offset(self.hex_jump_var.get())
        except ValueError as exc:
            self._show_error("Invalid offset", str(exc))
            return
        self._render_hex_view(offset)
        self._set_status_message(f"Hex view at {format_offset(offset)}")

    def _render_hex_view(self, offset: int) -> None:
        rows = make_hexdump_rows(self.raw_bytes, start=offset, length=HEX_VIEW_DEFAULT_LENGTH)
        self.visible_hex_text = "\n".join(rows)
        self._set_text(self.hex_text, self.visible_hex_text)

    def copy_visible_hex(self) -> None:
        self.root.clipboard_clear()
        self.root.clipboard_append(self.visible_hex_text)
        self._set_status_message("Copied visible hex")

    def _copy_selected_record(self, tree: ttk.Treeview) -> None:
        selection = tree.selection()
        if not selection:
            self._set_status_message("No row selected")
            return
        values = tree.item(selection[0], "values")
        self.root.clipboard_clear()
        self.root.clipboard_append("\t".join(str(value) for value in values))
        self._set_status_message("Copied selected row")

    def _set_loaded_status(self, summary: LoadedDatSummary) -> None:
        self.status_path_var.set(f"File: {summary.path}")
        self.status_size_var.set(f"Size: {summary.size} bytes")
        self.status_tg_var.set(f"TG: {summary.talk_group_count}")
        self.status_id_var.set(f"Individual IDs: {summary.individual_id_count}")
        self.status_channel_var.set(f"Channels: {summary.channel_count}")

    def _set_status_message(self, message: str) -> None:
        self.status_message_var.set(message)

    def _set_text(self, widget: tk.Text, value: str) -> None:
        widget.configure(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
        widget.configure(state=tk.DISABLED)

    def _show_error(self, title: str, message: str) -> None:
        if messagebox is None:
            raise RuntimeError(message)
        messagebox.showerror(title, message)
        self._set_status_message(message)

    def _show_info(self, title: str, message: str) -> None:
        if messagebox is None:
            raise RuntimeError(message)
        messagebox.showinfo(title, message)
        self._set_status_message(title)


def main() -> int:
    if tk is None:
        raise RuntimeError("tkinter is not available in this Python installation")
    root = tk.Tk()
    root.geometry("1200x800")
    OpenKPGTkApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
