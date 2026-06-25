"""Main OpenKPG application window."""

from __future__ import annotations

from openkpg.core.workspace import Workspace
from openkpg.ui.qt import QtCore, QtWidgets, require_qt
from openkpg.ui.views.hex_view import HexView
from openkpg.ui.views.navigation import NavigationView
from openkpg.ui.views.output_view import OutputView
from openkpg.ui.views.overview import OverviewPage
from openkpg.ui.views.validation_view import ValidationView
from openkpg.ui.widgets.property_panel import PropertyPanel


if QtWidgets is not None and QtCore is not None:  # pragma: no cover - requires Qt

    class MainWindow(QtWidgets.QMainWindow):
        """Dockable workspace shell for the modern CPS architecture."""

        def __init__(self, workspace: Workspace | None = None) -> None:
            super().__init__()
            self.workspace = workspace or Workspace()
            self.setWindowTitle("OpenKPG")

            self.tabs = QtWidgets.QTabWidget()
            self.overview_page = OverviewPage()
            self.tabs.addTab(self.overview_page, "Overview")
            self.setCentralWidget(self.tabs)

            self.navigation = NavigationView()
            self.properties = PropertyPanel()
            self.hex_view = HexView()
            self.validation = ValidationView()
            self.output = OutputView()

            self._add_dock("Navigation", self.navigation, QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)
            self._add_dock("Properties", self.properties, QtCore.Qt.DockWidgetArea.RightDockWidgetArea)
            self._add_dock("Hex View", self.hex_view, QtCore.Qt.DockWidgetArea.BottomDockWidgetArea)
            self._add_dock("Validation", self.validation, QtCore.Qt.DockWidgetArea.BottomDockWidgetArea)
            self._add_dock("Output", self.output, QtCore.Qt.DockWidgetArea.BottomDockWidgetArea)

        def _add_dock(self, title: str, widget: object, area: object) -> None:
            dock = QtWidgets.QDockWidget(title, self)
            dock.setObjectName(title.replace(" ", ""))
            dock.setWidget(widget)
            self.addDockWidget(area, dock)

else:

    class MainWindow:  # pragma: no cover - simple dependency guard
        def __init__(self, workspace: Workspace | None = None) -> None:
            require_qt()
