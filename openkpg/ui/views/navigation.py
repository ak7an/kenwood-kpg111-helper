"""Navigation dock view."""

from __future__ import annotations

from openkpg.ui.qt import QtWidgets, require_qt


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class NavigationView(QtWidgets.QTreeWidget):
        def __init__(self) -> None:
            super().__init__()
            self.setHeaderLabels(["Workspace"])
            for label in ("Overview", "Channels", "Zones", "Talkgroups", "Individual IDs", "Scan Lists"):
                QtWidgets.QTreeWidgetItem(self, [label])

else:

    class NavigationView:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
