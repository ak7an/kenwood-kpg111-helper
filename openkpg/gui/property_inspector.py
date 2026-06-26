"""Structured read-only property inspector for channel records."""

from __future__ import annotations

from dataclasses import dataclass

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    ttk = None

from .helpers import CHANNEL_RECORD_SIZE, ChannelRecordRow, NormalizedDiffResult, ascii_safe, format_hex_bytes, format_offset


@dataclass(frozen=True)
class InspectorSection:
    title: str
    properties: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class ChannelInspectorModel:
    sections: tuple[InspectorSection, ...]


def build_compare_properties(
    row: ChannelRecordRow,
    compare_result: NormalizedDiffResult | None = None,
) -> tuple[tuple[str, str], ...]:
    if compare_result is None:
        return (
            ("Changed fields", "No compare file loaded"),
            ("Changed byte count", "0"),
            ("Changed offsets", ""),
        )

    record_start = row.offset
    record_end = row.offset + CHANNEL_RECORD_SIZE
    in_record = [
        diff for diff in compare_result.differences if record_start <= diff.offset < record_end
    ]
    labels = sorted(
        {
            diff.channel_location.label
            for diff in in_record
            if diff.channel_location is not None and diff.channel_location.label
        }
    )
    offsets = ", ".join(f"+0x{diff.offset - record_start:02x}" for diff in in_record)
    return (
        ("Changed fields", ", ".join(labels) if labels else ""),
        ("Changed byte count", str(len(in_record))),
        ("Changed offsets", offsets),
    )


def build_channel_inspector_model(
    row: ChannelRecordRow | None,
    compare_result: NormalizedDiffResult | None = None,
) -> ChannelInspectorModel:
    if row is None:
        return ChannelInspectorModel(
            sections=(
                InspectorSection("General", (("Status", "No channel selected"),)),
                InspectorSection("Compare", build_compare_properties_for_empty(compare_result)),
            )
        )

    return ChannelInspectorModel(
        sections=(
            InspectorSection(
                "General",
                (
                    ("Channel number", str(row.channel)),
                    ("Record offset", format_offset(row.offset)),
                    ("Record size", f"{CHANNEL_RECORD_SIZE} bytes"),
                    ("Table index", str(row.channel - 1)),
                ),
            ),
            InspectorSection(
                "Frequency (Experimental)",
                (
                    ("RX bytes", row.rx_bytes),
                    ("TX bytes", row.tx_bytes),
                    ("Status", "Encoding not yet decoded"),
                ),
            ),
            InspectorSection(
                "Record Structure",
                (
                    ("Marker byte +0x08", row.marker_08),
                    ("Marker byte +0x0C", row.marker_0c),
                    ("Raw bytes (hex)", format_hex_bytes(row.raw_record)),
                    ("ASCII preview", ascii_safe(row.raw_record)),
                ),
            ),
            InspectorSection("Compare", build_compare_properties(row, compare_result)),
        )
    )


def build_compare_properties_for_empty(
    compare_result: NormalizedDiffResult | None = None,
) -> tuple[tuple[str, str], ...]:
    if compare_result is None:
        return (
            ("Changed fields", "No compare file loaded"),
            ("Changed byte count", "0"),
            ("Changed offsets", ""),
        )
    return (
        ("Changed fields", "No channel selected"),
        ("Changed byte count", "0"),
        ("Changed offsets", ""),
    )


class PropertyInspector:
    def __init__(self, parent: ttk.Frame) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.canvas = tk.Canvas(parent, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.canvas.yview)
        self.frame = ttk.Frame(self.canvas)
        self.window = self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.render(build_channel_inspector_model(None))

    def _on_frame_configure(self, _event: object) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event: object) -> None:
        self.canvas.itemconfigure(self.window, width=event.width)

    def render(self, model: ChannelInspectorModel) -> None:
        for child in self.frame.winfo_children():
            child.destroy()

        for section_index, section in enumerate(model.sections):
            section_frame = ttk.LabelFrame(self.frame, text=section.title, padding=6)
            section_frame.pack(fill=tk.X, padx=4, pady=(4 if section_index == 0 else 8, 0))
            for row_index, (name, value) in enumerate(section.properties):
                ttk.Label(section_frame, text=f"{name}:").grid(row=row_index, column=0, sticky=tk.NW, padx=(0, 8))
                ttk.Label(section_frame, text=value, wraplength=420, justify=tk.LEFT).grid(
                    row=row_index, column=1, sticky=tk.W
                )
            section_frame.columnconfigure(1, weight=1)
