"""Hex view for DAT byte inspection."""

from __future__ import annotations

from openkpg.ui.qt import QtWidgets, require_qt


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class HexView(QtWidgets.QPlainTextEdit):
        def __init__(self) -> None:
            super().__init__()
            self.setReadOnly(True)

        def set_bytes(self, data: bytes) -> None:
            rows = []
            for offset in range(0, len(data), 16):
                chunk = data[offset : offset + 16]
                rows.append(f"{offset:08x}  {' '.join(f'{byte:02x}' for byte in chunk)}")
            self.setPlainText("\n".join(rows))

else:

    class HexView:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
