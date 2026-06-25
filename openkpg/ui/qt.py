"""Optional Qt binding loader for the OpenKPG UI layer."""

from __future__ import annotations


QT_BINDING: str | None

try:  # pragma: no cover - depends on local developer environment
    from PySide6 import QtCore, QtGui, QtWidgets

    QT_BINDING = "PySide6"
except ImportError:  # pragma: no cover - depends on local developer environment
    try:
        from PyQt6 import QtCore, QtGui, QtWidgets

        QT_BINDING = "PyQt6"
    except ImportError:
        QtCore = QtGui = QtWidgets = None  # type: ignore[assignment]
        QT_BINDING = None


def require_qt() -> None:
    if QT_BINDING is None:
        raise RuntimeError("OpenKPG GUI requires PySide6 or PyQt6 to be installed")
