"""Memory usage widget."""

from __future__ import annotations

from openkpg.ui.qt import QtWidgets, require_qt


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class MemoryBar(QtWidgets.QProgressBar):
        def __init__(self) -> None:
            super().__init__()
            self.setRange(0, 100)
            self.setValue(0)

else:

    class MemoryBar:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
