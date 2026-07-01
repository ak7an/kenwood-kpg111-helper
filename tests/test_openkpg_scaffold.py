from dataclasses import is_dataclass
from pathlib import Path
import unittest

from openkpg.backend import OpenKPGProjectBackend
from openkpg.core.commands import AddChannel, DeleteChannel, EditChannel
from openkpg.core.project import OpenKPGProject
from openkpg.core.recent import RecentProjects
from openkpg.core.validation import (
    validate_duplicate_channels,
    validate_duplicate_talkgroups,
    validate_memory_limits,
)
from openkpg.core.workspace import Workspace
from openkpg.entities import Channel, Contact, Radio, ScanList, TalkGroup, UnknownRecord, Zone
from openkpg.ui.qt import QT_BINDING
from openkpg.ui.views.overview import OVERVIEW_CARDS
from openkpg.ui.views.welcome import WELCOME_ACTIONS
from openkpg.ui.windows.main_window import MainWindow


FIXTURE = Path("data/normalized/dattest/Dattest/AK7AN_Travel.dat")


class OpenKPGScaffoldTests(unittest.TestCase):
    def test_entities_are_pure_dataclasses(self) -> None:
        for entity_type in (Radio, Channel, Zone, TalkGroup, Contact, ScanList, UnknownRecord):
            self.assertTrue(is_dataclass(entity_type))
            self.assertNotIn("Qt", getattr(entity_type, "__module__", ""))

    def test_project_owns_domain_collections(self) -> None:
        project = OpenKPGProject(
            radio=Radio(model="NX-5000"),
            channels=[Channel(slot=1, name="Analog 1")],
            zones=[Zone(name="Zone 1", channel_slots=(1,))],
            talkgroups=[TalkGroup(slot=1, name="Dispatch", numeric_id=1001)],
            contacts=[Contact(slot=1, name="Unit 1", numeric_id=2001)],
            scan_lists=[ScanList(name="Main", channel_slots=(1,))],
            unknown_records=[UnknownRecord(source="test", offset=0, length=4)],
        )

        self.assertEqual(project.memory_usage_summary()["channels"], 1)
        self.assertEqual(project.memory_usage_summary()["talkgroups"], 1)
        self.assertEqual(project.memory_usage_summary()["contacts"], 1)
        self.assertEqual(project.memory_usage_summary()["unknown_records"], 1)

    def test_validation_returns_structured_warnings(self) -> None:
        project = OpenKPGProject(
            channels=[Channel(slot=1, name="A"), Channel(slot=2, name="a")],
            talkgroups=[
                TalkGroup(slot=1, name="TG1", numeric_id=100),
                TalkGroup(slot=2, name="TG2", numeric_id=100),
            ],
        )

        channel_warnings = validate_duplicate_channels(project)
        talkgroup_warnings = validate_duplicate_talkgroups(project)
        memory_warnings = validate_memory_limits(project)

        self.assertEqual(channel_warnings[0].code, "duplicate_channel_name")
        self.assertEqual(talkgroup_warnings[0].code, "duplicate_talkgroup_id")
        self.assertEqual(memory_warnings[0].code, "memory_limits_unknown")

    def test_workspace_tracks_project_filename_dirty_and_undo(self) -> None:
        workspace = Workspace()
        project = OpenKPGProject()

        workspace.open_project(project, "example.dat")
        workspace.undo_stack.append(AddChannel())
        workspace.mark_dirty()

        self.assertIs(workspace.current_project, project)
        self.assertEqual(workspace.open_filename, Path("example.dat"))
        self.assertTrue(workspace.dirty)
        self.assertEqual(workspace.undo_stack[0].label, "Add Channel")

    def test_workspace_open_resets_dirty_and_undo(self) -> None:
        workspace = Workspace(dirty=True)
        workspace.undo_stack.append(AddChannel())

        workspace.open_project(OpenKPGProject(), "fresh.dat")

        self.assertFalse(workspace.dirty)
        self.assertEqual(workspace.open_filename, Path("fresh.dat"))
        self.assertEqual(workspace.undo_stack, [])

    def test_recent_projects_add_list_deduplicate_and_limit(self) -> None:
        recent = RecentProjects(max_items=2)
        first = recent.add("first.dat")
        second = recent.add("second.dat", label="Second")
        recent.add("first.dat")
        recent.add("third.dat")

        items = recent.list()
        self.assertEqual(first.display_name, "first.dat")
        self.assertEqual(second.display_name, "Second")
        self.assertEqual([item.path for item in items], [Path("third.dat"), Path("first.dat")])

    def test_command_placeholders_do_not_edit(self) -> None:
        for command in (AddChannel(), DeleteChannel(), EditChannel()):
            with self.assertRaises(NotImplementedError):
                command.execute()
            with self.assertRaises(NotImplementedError):
                command.undo()

    def test_backend_loads_dat_into_application_project(self) -> None:
        backend = OpenKPGProjectBackend()
        project = backend.load_dat(FIXTURE)

        self.assertIs(project, backend.current_project)
        self.assertEqual(backend.raw_bytes(), FIXTURE.read_bytes())
        self.assertGreaterEqual(len(project.talkgroups), 1)
        self.assertGreaterEqual(len(project.contacts), 1)
        self.assertIn("talk_groups", backend.table_summary())
        self.assertIsInstance(project, OpenKPGProject)

    def test_ui_modules_import_without_instantiating_qt(self) -> None:
        import openkpg.app
        import openkpg.ui.views.channel_table
        import openkpg.ui.views.hex_view
        import openkpg.ui.views.inspector
        import openkpg.ui.views.navigation
        import openkpg.ui.views.output_view
        import openkpg.ui.views.validation_view
        import openkpg.ui.views.welcome
        import openkpg.ui.views.zone_tree
        import openkpg.ui.widgets.memory_bar
        import openkpg.ui.widgets.property_panel
        import openkpg.ui.widgets.search_box
        import openkpg.ui.windows.main_window

        self.assertIn(QT_BINDING, {None, "PySide6", "PyQt6"})

    def test_overview_cards_cover_requested_sections(self) -> None:
        self.assertEqual(
            set(OVERVIEW_CARDS),
            {
                "Radio",
                "Channels",
                "Zones",
                "Talkgroups",
                "Individual IDs",
                "Scan Lists",
                "Memory Usage",
                "Validation Status",
            },
        )

    def test_welcome_actions_cover_startup_placeholders(self) -> None:
        self.assertEqual(
            set(WELCOME_ACTIONS),
            {
                "Open DAT",
                "Recent Projects",
                "New Project",
                "Import CSV",
                "Import RepeaterBook",
                "Documentation",
                "About OpenKPG",
            },
        )

    def test_file_open_workflow_methods_exist_without_qt_execution(self) -> None:
        self.assertTrue(hasattr(MainWindow, "open_dat"))
        self.assertTrue(hasattr(MainWindow, "open_dat_path"))


if __name__ == "__main__":
    unittest.main()
