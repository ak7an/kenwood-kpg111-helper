"""Validation dock view."""

from __future__ import annotations

from openkpg.core.validation import ValidationWarning
from openkpg.ui.qt import QtWidgets, require_qt


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class ValidationView(QtWidgets.QTableWidget):
        def __init__(self) -> None:
            super().__init__(0, 3)
            self.setHorizontalHeaderLabels(["Severity", "Code", "Message"])

        def set_warnings(self, warnings: list[ValidationWarning]) -> None:
            self.setRowCount(len(warnings))
            for row, warning in enumerate(warnings):
                self.setItem(row, 0, QtWidgets.QTableWidgetItem(warning.severity))
                self.setItem(row, 1, QtWidgets.QTableWidgetItem(warning.code))
                self.setItem(row, 2, QtWidgets.QTableWidgetItem(warning.message))

else:

    class ValidationView:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
