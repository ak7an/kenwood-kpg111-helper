"""Property dock panel."""

from __future__ import annotations

from openkpg.ui.qt import QtWidgets, require_qt


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class PropertyPanel(QtWidgets.QTableWidget):
        def __init__(self) -> None:
            super().__init__(0, 2)
            self.setHorizontalHeaderLabels(["Property", "Value"])

else:

    class PropertyPanel:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
