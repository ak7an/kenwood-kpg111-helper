#!/usr/bin/env python3
"""Application entry point for the OpenKPG GUI scaffold."""

from __future__ import annotations

import sys

from .core.workspace import Workspace
from .ui.qt import QtWidgets, require_qt
from .ui.windows.main_window import MainWindow


def main(argv: list[str] | None = None) -> int:
    """Start the GUI if a supported Qt binding is installed."""
    require_qt()
    app = QtWidgets.QApplication(sys.argv if argv is None else argv)
    window = MainWindow(Workspace())
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
