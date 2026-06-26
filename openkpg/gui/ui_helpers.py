"""Generic UI helpers for the OpenKPG tkinter GUI."""

from __future__ import annotations

import re
from typing import Any

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    ttk = None


def natural_sort_key(value: object) -> tuple[Any, ...]:
    text = str(value)
    parts = re.split(r"(\d+)", text.lower())
    return tuple(int(part) if part.isdigit() else part for part in parts)


def sorted_table_rows(rows: list[tuple[object, ...]], column_index: int, reverse: bool = False) -> list[tuple[object, ...]]:
    return sorted(rows, key=lambda row: natural_sort_key(row[column_index]), reverse=reverse)


def row_to_clipboard_text(values: object) -> str:
    if isinstance(values, (list, tuple)):
        return "\t".join(str(value) for value in values)
    return str(values)


def hex_values_from_row(values: object) -> str:
    if not isinstance(values, (list, tuple)):
        return ""
    hex_re = re.compile(r"^(?:[0-9a-fA-F]{2})(?: [0-9a-fA-F]{2})*$")
    return " ".join(str(value) for value in values if hex_re.match(str(value)))


def valid_window_geometry(value: object) -> str:
    if not isinstance(value, str):
        return ""
    if re.match(r"^\d+x\d+(?:[+-]\d+[+-]\d+)?$", value):
        return value
    return ""


def coerce_pane_position(value: object) -> int | None:
    if isinstance(value, int) and value >= 0:
        return value
    return None


def create_tree_with_scrollbars(
    parent: ttk.Frame,
    columns: tuple[str, ...],
    headings: dict[str, str],
    widths: dict[str, int] | None = None,
) -> ttk.Treeview:
    if tk is None or ttk is None:
        raise RuntimeError("tkinter is not available in this Python installation")
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    y_scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
    x_scroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
    for column in columns:
        tree.heading(column, text=headings[column])
        tree.column(column, width=(widths or {}).get(column, 110), anchor=tk.W, stretch=True)
    tree.tag_configure("odd", background="#f7f7f7")
    tree.tag_configure("even", background="#ffffff")
    tree.grid(row=0, column=0, sticky=tk.NSEW)
    y_scroll.grid(row=0, column=1, sticky=tk.NS)
    x_scroll.grid(row=1, column=0, sticky=tk.EW)
    parent.rowconfigure(0, weight=1)
    parent.columnconfigure(0, weight=1)
    install_sortable_columns(tree)
    return tree


def install_sortable_columns(tree: ttk.Treeview) -> None:
    if tk is None or ttk is None:
        raise RuntimeError("tkinter is not available in this Python installation")
    for column in tree["columns"]:
        tree.heading(column, command=lambda selected=column: sort_treeview_column(tree, selected, False))


def sort_treeview_column(tree: ttk.Treeview, column: str, reverse: bool) -> None:
    rows = [(tree.set(item, column), item) for item in tree.get_children("")]
    rows.sort(key=lambda item: natural_sort_key(item[0]), reverse=reverse)
    for index, (_value, item) in enumerate(rows):
        tree.move(item, "", index)
        tree.item(item, tags=("even" if index % 2 == 0 else "odd",))
    tree.heading(column, command=lambda: sort_treeview_column(tree, column, not reverse))


def insert_tree_rows(tree: ttk.Treeview, rows: list[tuple[object, ...]]) -> None:
    tree.delete(*tree.get_children())
    for index, row in enumerate(rows):
        tree.insert("", tk.END, values=row, tags=("even" if index % 2 == 0 else "odd",))


def install_tree_context_menu(tree: ttk.Treeview, root: tk.Tk, status_callback: object) -> None:
    if tk is None or ttk is None:
        raise RuntimeError("tkinter is not available in this Python installation")

    menu = tk.Menu(tree, tearoff=False)

    def selected_values() -> tuple[object, ...]:
        selection = tree.selection()
        if not selection:
            return ()
        return tuple(tree.item(selection[0], "values"))

    def copy_text(text: str, message: str) -> None:
        root.clipboard_clear()
        root.clipboard_append(text)
        status_callback(message)

    def copy_value() -> None:
        item = tree.focus()
        column = tree.identify_column(getattr(tree, "_openkpg_menu_x", 0))
        if not item or not column.startswith("#"):
            return
        values = tree.item(item, "values")
        index = int(column[1:]) - 1
        if 0 <= index < len(values):
            copy_text(str(values[index]), "Copied value")

    def copy_row() -> None:
        values = selected_values()
        if values:
            copy_text(row_to_clipboard_text(values), "Copied row")

    def copy_hex() -> None:
        text = hex_values_from_row(selected_values())
        if text:
            copy_text(text, "Copied selected hex")

    menu.add_command(label="Copy value", command=copy_value)
    menu.add_command(label="Copy row", command=copy_row)
    menu.add_command(label="Copy selected hex", command=copy_hex)

    def open_menu(event: object) -> None:
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
            tree.focus(item)
        tree._openkpg_menu_x = event.x
        menu.tk_popup(event.x_root, event.y_root)

    tree.bind("<Button-3>", open_menu)
