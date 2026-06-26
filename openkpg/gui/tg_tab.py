"""Talk Group tab for the OpenKPG tkinter GUI."""

from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    ttk = None

from .helpers import filter_table_rows, record_table_values
from .ui_helpers import create_tree_with_scrollbars, insert_tree_rows, install_tree_context_menu


class RecordTableTab:
    tab_title = "Records"
    description = "Read-only decoded records"
    count_label = "Rows"

    def __init__(self, notebook: ttk.Notebook, root: tk.Tk, copy_callback: object, status_callback: object) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.copy_callback = copy_callback
        self.status_callback = status_callback
        self.root = root
        self.records: list[object] = []
        self.search_var = tk.StringVar(value="")
        self.count_var = tk.StringVar(value=f"{self.count_label}: 0")

        self.frame = ttk.Frame(notebook, padding=4)
        self._build_controls()
        self.table = self._record_table(self.frame)
        install_tree_context_menu(self.table, self.root, self.status_callback)
        notebook.add(self.frame, text=self.tab_title)

    def _build_controls(self) -> None:
        ttk.Label(self.frame, text=self.description).pack(anchor=tk.W, pady=(0, 4))
        controls = ttk.Frame(self.frame)
        controls.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(controls, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(controls, textvariable=self.search_var, width=32)
        self.search_entry.pack(side=tk.LEFT, padx=(4, 8))
        self.search_entry.bind("<KeyRelease>", lambda _event=None: self.refresh())
        ttk.Button(controls, text="Copy selected row", command=self.copy_selected_row).pack(side=tk.LEFT)
        ttk.Label(self.frame, textvariable=self.count_var).pack(anchor=tk.W, pady=(0, 4))

    def _record_table(self, parent: ttk.Frame) -> ttk.Treeview:
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        return create_tree_with_scrollbars(
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
            widths={"name": 220},
        )

    def load_records(self, records: list[object]) -> None:
        self.records = list(records)
        self.refresh()

    def refresh(self) -> None:
        rows = filter_table_rows(self.records, self.search_var.get())
        insert_tree_rows(self.table, [record_table_values(record) for record in rows])
        self.count_var.set(f"{self.count_label}: {len(rows)} of {len(self.records)}")

    def copy_selected_row(self) -> None:
        self.copy_callback(self.table)

    def focus_search(self) -> None:
        self.search_entry.focus_set()


class TalkGroupsTab(RecordTableTab):
    tab_title = "Talk Groups"
    description = "Read-only decoded Talk Group records"
    count_label = "Talk Group rows"
