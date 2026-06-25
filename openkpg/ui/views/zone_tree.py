"""Zone tree view."""

from __future__ import annotations

from openkpg.ui.qt import QtWidgets, require_qt


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class ZoneTreeView(QtWidgets.QTreeWidget):
        def __init__(self) -> None:
            super().__init__()
            self.setHeaderLabels(["Zone", "Channels"])

else:

    class ZoneTreeView:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
