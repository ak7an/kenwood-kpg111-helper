"""Startup welcome page for OpenKPG."""

from __future__ import annotations

from openkpg.ui.qt import QtWidgets, require_qt


WELCOME_ACTIONS = (
    "Open DAT",
    "Recent Projects",
    "New Project",
    "Import CSV",
    "Import RepeaterBook",
    "Documentation",
    "About OpenKPG",
)


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class WelcomePage(QtWidgets.QWidget):
        def __init__(self) -> None:
            super().__init__()
            layout = QtWidgets.QVBoxLayout(self)
            title = QtWidgets.QLabel("OpenKPG")
            layout.addWidget(title)
            for action in WELCOME_ACTIONS:
                button = QtWidgets.QPushButton(action)
                button.setEnabled(action in {"Open DAT", "Documentation", "About OpenKPG"})
                layout.addWidget(button)
            layout.addStretch()

else:

    class WelcomePage:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
