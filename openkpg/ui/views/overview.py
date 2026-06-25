"""Overview workspace page."""

from __future__ import annotations

from openkpg.core.project import OpenKPGProject
from openkpg.ui.qt import QtWidgets, require_qt


OVERVIEW_CARDS = (
    "Radio",
    "Channels",
    "Zones",
    "Talkgroups",
    "Individual IDs",
    "Scan Lists",
    "Memory Usage",
    "Validation Status",
)


if QtWidgets is not None:  # pragma: no cover - requires Qt

    class OverviewCard(QtWidgets.QFrame):
        def __init__(self, title: str, value: str = "Not decoded") -> None:
            super().__init__()
            self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            layout = QtWidgets.QVBoxLayout(self)
            self.title_label = QtWidgets.QLabel(title)
            self.value_label = QtWidgets.QLabel(value)
            layout.addWidget(self.title_label)
            layout.addWidget(self.value_label)

        def set_value(self, value: str) -> None:
            self.value_label.setText(value)


    class OverviewPage(QtWidgets.QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.cards: dict[str, OverviewCard] = {}
            layout = QtWidgets.QGridLayout(self)
            for index, title in enumerate(OVERVIEW_CARDS):
                card = OverviewCard(title)
                self.cards[title] = card
                layout.addWidget(card, index // 4, index % 4)

        def set_project(self, project: OpenKPGProject) -> None:
            self.cards["Radio"].set_value(project.radio.model)
            self.cards["Channels"].set_value(str(len(project.channels)))
            self.cards["Zones"].set_value(str(len(project.zones)))
            self.cards["Talkgroups"].set_value(str(len([tg for tg in project.talkgroups if not tg.empty])))
            self.cards["Individual IDs"].set_value(str(len([contact for contact in project.contacts if not contact.empty])))
            self.cards["Scan Lists"].set_value(str(len(project.scan_lists)))
            self.cards["Memory Usage"].set_value("Known limits pending")
            self.cards["Validation Status"].set_value("Not run")

        def set_validation_status(self, warning_count: int) -> None:
            if warning_count:
                self.cards["Validation Status"].set_value(f"{warning_count} warnings")
            else:
                self.cards["Validation Status"].set_value("No warnings")

else:

    class OverviewPage:  # pragma: no cover - simple dependency guard
        def __init__(self) -> None:
            require_qt()
