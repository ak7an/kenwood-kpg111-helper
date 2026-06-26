"""Talk Group tab for the OpenKPG tkinter GUI."""

from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    ttk = None

from .helpers import filter_table_rows, record_table_values


class RecordTableTab:
    tab_title = "Records"
    description = "Read-only decoded records"
    count_label = "Rows"

    def __init__(self, notebook: ttk.Notebook, copy_callback: object, status_callback: object) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.copy_callback = copy_callback
        self.status_callback = status_callback
        self.records: list[object] = []
        self.search_var = tk.StringVar(value="")
        self.count_var = tk.StringVar(value=f"{self.count_label}: 0")

        self.frame = ttk.Frame(notebook, padding=4)
        self._build_controls()
        self.table = self._record_table(self.frame)
        notebook.add(self.frame, text=self.tab_title)

    def _build_controls(self) -> None:
        ttk.Label(self.frame, text=self.description).pack(anchor=tk.W, pady=(0, 4))
        controls = ttk.Frame(self.frame)
        controls.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(controls, text="Search:").pack(side=tk.LEFT)
        entry = ttk.Entry(controls, textvariable=self.search_var, width=32)
        entry.pack(side=tk.LEFT, padx=(4, 8))
        entry.bind("<KeyRelease>", lambda _event=None: self.refresh())
        ttk.Button(controls, text="Copy selected row", command=self.copy_selected_row).pack(side=tk.LEFT)
        ttk.Label(self.frame, textvariable=self.count_var).pack(anchor=tk.W, pady=(0, 4))

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
            tree.column(column, width=220 if column == "name" else 110, anchor=tk.W)
        tree.grid(row=0, column=0, sticky=tk.NSEW)
        y_scroll.grid(row=0, column=1, sticky=tk.NS)
        x_scroll.grid(row=1, column=0, sticky=tk.EW)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        return tree

    def load_records(self, records: list[object]) -> None:
        self.records = list(records)
        self.refresh()

    def refresh(self) -> None:
        rows = filter_table_rows(self.records, self.search_var.get())
        self.table.delete(*self.table.get_children())
        for record in rows:
            self.table.insert("", tk.END, values=record_table_values(record))
        self.count_var.set(f"{self.count_label}: {len(rows)} of {len(self.records)}")

    def copy_selected_row(self) -> None:
        self.copy_callback(self.table)


class TalkGroupsTab(RecordTableTab):
    tab_title = "Talk Groups"
    description = "Read-only decoded Talk Group records"
    count_label = "Talk Group rows"
