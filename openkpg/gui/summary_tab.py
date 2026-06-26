"""Loaded DAT summary panel for the OpenKPG tkinter GUI."""

from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    ttk = None

from .helpers import DAT_HEADER_SIZE, format_hex_bytes


class SummaryPanel:
    def __init__(self, root: tk.Tk) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.path_var = tk.StringVar(value="No DAT loaded")
        self.size_var = tk.StringVar(value="")
        self.header_preview_var = tk.StringVar(value="")
        self.payload_size_var = tk.StringVar(value="")
        self.xor_status_var = tk.StringVar(value="Assumed payload XOR mask: 0x00 (self comparison placeholder)")
        self.readonly_note_var = tk.StringVar(value="Read-only GUI: no DAT writing, save, or save-as functionality.")

        summary = ttk.LabelFrame(root, text="Loaded file summary", padding=8)
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

    def load_file(self, path: object, raw_bytes: bytes, xor_mask: int) -> None:
        self.path_var.set(str(path))
        self.size_var.set(f"{len(raw_bytes)} bytes")
        self.header_preview_var.set(format_hex_bytes(raw_bytes[:DAT_HEADER_SIZE]))
        self.payload_size_var.set(f"{max(0, len(raw_bytes) - DAT_HEADER_SIZE)} bytes")
        self.xor_status_var.set(f"Assumed payload XOR mask: 0x{xor_mask:02x} (self comparison placeholder)")
