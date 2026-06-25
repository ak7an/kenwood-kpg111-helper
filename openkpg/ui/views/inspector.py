"""Inspector view for selected project entities."""

from __future__ import annotations

from openkpg.ui.qt import QtWidgets, require_qt


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class InspectorView(QtWidgets.QTableWidget):
        def __init__(self) -> None:
            super().__init__(0, 3)
            self.setHorizontalHeaderLabels(["Field", "Value", "Confidence"])

else:

    class InspectorView:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
