"""Search input widget."""

from __future__ import annotations

from openkpg.ui.qt import QtWidgets, require_qt


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class SearchBox(QtWidgets.QLineEdit):
        def __init__(self) -> None:
            super().__init__()
            self.setPlaceholderText("Search")

else:

    class SearchBox:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
