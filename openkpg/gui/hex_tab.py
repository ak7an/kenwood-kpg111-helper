"""Hex/raw viewer tab for the OpenKPG tkinter GUI."""

from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    ttk = None

from .helpers import HEX_VIEW_DEFAULT_LENGTH, format_offset, make_hexdump_rows, parse_offset


class HexRawTab:
    tab_title = "Hex / Raw"

    def __init__(
        self,
        notebook: ttk.Notebook,
        root: tk.Tk,
        set_text: object,
        show_error: object,
        show_info: object,
        status_callback: object,
    ) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.root = root
        self.set_text = set_text
        self.show_error = show_error
        self.show_info = show_info
        self.status_callback = status_callback
        self.raw_bytes = b""
        self.visible_hex_text = ""
        self.jump_var = tk.StringVar(value="0x0")

        self.frame = ttk.Frame(notebook, padding=4)
        self._build()
        notebook.add(self.frame, text=self.tab_title)

    def _build(self) -> None:
        controls = ttk.Frame(self.frame)
        controls.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(controls, text="Jump to offset:").pack(side=tk.LEFT)
        ttk.Entry(controls, textvariable=self.jump_var, width=12).pack(side=tk.LEFT, padx=(4, 8))
        ttk.Button(controls, text="Jump", command=self.jump).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(controls, text="Copy visible hex", command=self.copy_visible_hex).pack(side=tk.LEFT)

        self.text = tk.Text(self.frame, wrap=tk.NONE, state=tk.DISABLED, font=("Courier", 10))
        y_scroll = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.text.yview)
        x_scroll = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.text.xview)
        self.text.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    def load_file(self, raw_bytes: bytes) -> None:
        self.raw_bytes = raw_bytes
        self.render(0)

    def refresh(self) -> None:
        self.jump()

    def jump(self) -> None:
        if not self.raw_bytes:
            self.show_info("Hex view", "No DAT file is currently loaded.")
            return
        try:
            offset = parse_offset(self.jump_var.get())
        except ValueError as exc:
            self.show_error("Invalid offset", str(exc))
            return
        self.render(offset)
        self.status_callback(None, f"Hex view at {format_offset(offset)}")

    def render(self, offset: int) -> None:
        rows = make_hexdump_rows(self.raw_bytes, start=offset, length=HEX_VIEW_DEFAULT_LENGTH)
        self.visible_hex_text = "\n".join(rows)
        self.set_text(self.text, self.visible_hex_text)

    def copy_visible_hex(self) -> None:
        self.root.clipboard_clear()
        self.root.clipboard_append(self.visible_hex_text)
        self.status_callback(None, "Copied visible hex")
