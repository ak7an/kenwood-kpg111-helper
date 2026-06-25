"""Main OpenKPG application window."""

from __future__ import annotations

from pathlib import Path

from openkpg.backend import OpenKPGProjectBackend
from openkpg.core.recent import RecentProjects
from openkpg.core.validation import validate_project
from openkpg.core.workspace import Workspace
from openkpg.ui.qt import QtCore, QtWidgets, require_qt
from openkpg.ui.views.hex_view import HexView
from openkpg.ui.views.navigation import NavigationView
from openkpg.ui.views.output_view import OutputView
from openkpg.ui.views.overview import OverviewPage
from openkpg.ui.views.validation_view import ValidationView
from openkpg.ui.views.welcome import WelcomePage
from openkpg.ui.widgets.property_panel import PropertyPanel


if QtWidgets is not None and QtCore is not None:  # pragma: no cover - requires Qt

    class MainWindow(QtWidgets.QMainWindow):
        """Dockable workspace shell for the modern CPS architecture."""

        def __init__(
            self,
            workspace: Workspace | None = None,
            backend: OpenKPGProjectBackend | None = None,
            recent_projects: RecentProjects | None = None,
        ) -> None:
            super().__init__()
            self.workspace = workspace or Workspace()
            self.backend = backend or OpenKPGProjectBackend()
            self.recent_projects = recent_projects or RecentProjects()
            self.setWindowTitle("OpenKPG")

            self._build_file_menu()
            self.tabs = QtWidgets.QTabWidget()
            self.welcome_page = WelcomePage()
            self.overview_page = OverviewPage()
            self.tabs.addTab(self.welcome_page, "Welcome")
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

        def _build_file_menu(self) -> None:
            file_menu = self.menuBar().addMenu("File")
            self.open_dat_action = file_menu.addAction("Open DAT")
            self.open_dat_action.triggered.connect(self.open_dat)
            file_menu.addSeparator()
            self.exit_action = file_menu.addAction("Exit")
            self.exit_action.triggered.connect(self.close)

        def _add_dock(self, title: str, widget: object, area: object) -> None:
            dock = QtWidgets.QDockWidget(title, self)
            dock.setObjectName(title.replace(" ", ""))
            dock.setWidget(widget)
            self.addDockWidget(area, dock)

        def open_dat(self) -> None:
            path, _selected_filter = QtWidgets.QFileDialog.getOpenFileName(
                self,
                "Open KPG111 DAT",
                "",
                "KPG111 DAT Files (*.dat);;All Files (*)",
            )
            if path:
                self.open_dat_path(Path(path))

        def open_dat_path(self, path: Path | str) -> None:
            dat_path = Path(path)
            project = self.backend.load_dat(dat_path)
            self.workspace.open_project(project, dat_path)
            self.recent_projects.add(dat_path)
            self.overview_page.set_project(project)
            if project.raw_bytes is not None:
                self.hex_view.set_bytes(project.raw_bytes)
            warnings = validate_project(project)
            self.validation.set_warnings(warnings)
            self.overview_page.set_validation_status(len(warnings))
            self.output.write_message(f"Opened DAT read-only: {dat_path}")
            self.tabs.setCurrentWidget(self.overview_page)

else:

    class MainWindow:  # pragma: no cover - simple dependency guard
        def __init__(
            self,
            workspace: Workspace | None = None,
            backend: OpenKPGProjectBackend | None = None,
            recent_projects: RecentProjects | None = None,
        ) -> None:
            require_qt()

        def open_dat(self) -> None:
            require_qt()

        def open_dat_path(self, path: Path | str) -> None:
            require_qt()
