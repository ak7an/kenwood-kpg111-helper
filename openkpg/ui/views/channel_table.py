"""Channel table view."""

from __future__ import annotations

from openkpg.ui.qt import QtWidgets, require_qt


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class ChannelTableView(QtWidgets.QTableWidget):
        def __init__(self) -> None:
            super().__init__(0, 8)
            self.setHorizontalHeaderLabels(
                ["Slot", "Name", "RX", "TX", "Bandwidth", "Power", "Mode", "Confidence"]
            )

else:

    class ChannelTableView:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
