"""Output dock view."""

from __future__ import annotations

from openkpg.ui.qt import QtWidgets, require_qt


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class OutputView(QtWidgets.QPlainTextEdit):
        def __init__(self) -> None:
            super().__init__()
            self.setReadOnly(True)

        def write_message(self, message: str) -> None:
            self.appendPlainText(message)

else:

    class OutputView:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
