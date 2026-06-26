"""Read-only DAT compare tab for the OpenKPG tkinter GUI."""

from __future__ import annotations

from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    ttk = None

from .helpers import (
    NormalizedDiffResult,
    NormalizedDifference,
    format_hex_bytes,
    format_offset,
    normalized_differences,
)
from .ui_helpers import create_tree_with_scrollbars, insert_tree_rows, install_tree_context_menu


COMPARE_DEFAULT_LIMIT = 500


class CompareTab:
    tab_title = "Compare"

    def __init__(
        self,
        notebook: ttk.Notebook,
        root: tk.Tk,
        show_error: object,
        show_info: object,
        status_callback: object,
        result_callback: object | None = None,
    ) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.show_error = show_error
        self.root = root
        self.show_info = show_info
        self.status_callback = status_callback
        self.result_callback = result_callback
        self.baseline_path: Path | None = None
        self.modified_path: Path | None = None
        self.baseline_bytes: bytes | None = None
        self.modified_bytes: bytes | None = None
        self.latest_result: NormalizedDiffResult | None = None

        self.baseline_path_var = tk.StringVar(value="No baseline DAT loaded")
        self.modified_path_var = tk.StringVar(value="No modified DAT loaded")
        self.mask_var = tk.StringVar(value="")
        self.payload_compared_var = tk.StringVar(value="")
        self.diff_count_var = tk.StringVar(value="")
        self.limit_var = tk.StringVar(value=str(COMPARE_DEFAULT_LIMIT))

        self.frame = ttk.Frame(notebook, padding=4)
        self._build()
        notebook.add(self.frame, text=self.tab_title)

    def _build(self) -> None:
        ttk.Label(self.frame, text="Read-only DAT compare. Payload XOR differences are normalized.").pack(
            anchor=tk.W, pady=(0, 4)
        )

        summary = ttk.Frame(self.frame)
        summary.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(summary, text="Baseline:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.baseline_path_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(summary, text="Modified:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.modified_path_var).grid(row=1, column=1, sticky=tk.W)
        ttk.Label(summary, text="Dominant XOR mask:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.mask_var).grid(row=2, column=1, sticky=tk.W)
        ttk.Label(summary, text="Payload bytes compared:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.payload_compared_var).grid(row=3, column=1, sticky=tk.W)
        ttk.Label(summary, text="Normalized differing bytes:").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(summary, textvariable=self.diff_count_var).grid(row=4, column=1, sticky=tk.W)
        summary.columnconfigure(1, weight=1)

        controls = ttk.Frame(self.frame)
        controls.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(controls, text="Show first N differences:").pack(side=tk.LEFT)
        self.limit_entry = ttk.Entry(controls, textvariable=self.limit_var, width=8)
        self.limit_entry.pack(side=tk.LEFT, padx=(4, 8))

        self.table = self._tree_with_scrollbars(
            self.frame,
            columns=(
                "offset",
                "left_byte",
                "right_raw_byte",
                "right_normalized_byte",
                "channel",
                "channel_relative_offset",
                "label",
            ),
            headings={
                "offset": "Offset",
                "left_byte": "Left byte",
                "right_raw_byte": "Right raw byte",
                "right_normalized_byte": "Right normalized byte",
                "channel": "Channel",
                "channel_relative_offset": "Channel offset",
                "label": "Region",
            },
        )
        install_tree_context_menu(self.table, self.root, self.status_callback)

    def _tree_with_scrollbars(
        self,
        parent: ttk.Frame,
        columns: tuple[str, ...],
        headings: dict[str, str],
    ) -> ttk.Treeview:
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        return create_tree_with_scrollbars(frame, columns, headings, widths={"label": 150})

    def load_baseline(self, path: Path) -> None:
        self.baseline_path, self.baseline_bytes = self._read_dat(path)
        self.baseline_path_var.set(str(path))
        self.status_callback("Loaded compare baseline")

    def load_modified(self, path: Path) -> None:
        self.modified_path, self.modified_bytes = self._read_dat(path)
        self.modified_path_var.set(str(path))
        self.status_callback("Loaded compare modified DAT")

    def _read_dat(self, path: Path) -> tuple[Path, bytes]:
        if not path.is_file():
            raise ValueError(f"File does not exist: {path}")
        return path, path.read_bytes()

    def run_compare(self) -> None:
        if self.baseline_bytes is None:
            self.show_info("Run Compare", "No baseline DAT is loaded.")
            return
        if self.modified_bytes is None:
            self.show_info("Run Compare", "No modified DAT is loaded.")
            return
        try:
            limit = int(self.limit_var.get(), 0)
            if limit < 0:
                raise ValueError("limit must be >= 0")
            result = normalized_differences(self.baseline_bytes, self.modified_bytes, limit=limit)
        except ValueError as exc:
            self.show_error("Compare failed", str(exc))
            return

        self.latest_result = result
        self.populate(result)
        if self.result_callback is not None:
            self.result_callback(result)
        self.status_callback("Compare complete")

    def populate(self, result: NormalizedDiffResult) -> None:
        self.mask_var.set(f"0x{result.dominant_xor_mask:02x}")
        self.payload_compared_var.set(str(result.payload_bytes_compared))
        self.diff_count_var.set(str(result.normalized_differing_byte_count))
        insert_tree_rows(self.table, [self._row_values(difference) for difference in result.differences])

    def _row_values(self, difference: NormalizedDifference) -> tuple[str, str, str, str, str, str, str]:
        location = difference.channel_location
        if location is None:
            channel = ""
            relative_offset = ""
            label = ""
        else:
            channel = str(location.channel)
            relative_offset = f"+0x{location.relative_offset:02x}"
            label = location.label
        return (
            format_offset(difference.offset),
            format_hex_bytes(bytes([difference.left_byte])),
            format_hex_bytes(bytes([difference.right_raw_byte])),
            format_hex_bytes(bytes([difference.right_normalized_byte])),
            channel,
            relative_offset,
            label,
        )

    def refresh(self) -> None:
        if self.latest_result is not None:
            self.populate(self.latest_result)

    def focus_search(self) -> None:
        self.limit_entry.focus_set()
