from pathlib import Path
import tempfile
import unittest

from kpg111 import Codeplug
from openkpg import BuildProject as ExportedBuildProject
from openkpg.project_builder import BuildLimits, BuildProject, BuildResult


FIXTURE = Path("data/normalized/dattest/Dattest/AK7AN_Travel.dat")


class ProjectBuilderTests(unittest.TestCase):
    def test_project_builder_is_exported_from_package(self) -> None:
        self.assertIs(ExportedBuildProject, BuildProject)

    def test_builds_complete_plan_from_multiple_csv_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "colorado.csv"
            second = Path(tmp) / "utah.csv"
            first.write_text(
                "name,rx_frequency,tx_frequency,mode,zone\n"
                "Denver 1,146.940,146.340,FM,Colorado\n",
                encoding="utf-8",
            )
            second.write_text(
                "name,rx_frequency,mode,zone\n"
                "Utah Simplex,446.000,NXDN,Utah\n",
                encoding="utf-8",
            )

            result = BuildProject().import_csv(first).import_csv(second).build()

            self.assertIsInstance(result, BuildResult)
            self.assertEqual([channel.name for channel in result.accepted_channels], ["Denver 1", "Utah Simplex"])
            self.assertEqual([zone.name for zone in result.zones], ["Colorado", "Utah"])
            self.assertEqual(result.statistics.csv_files, 2)
            self.assertEqual(result.statistics.channels_imported, 2)
            self.assertEqual(result.statistics.channels_accepted, 2)
            self.assertEqual(result.statistics.channels_rejected, 0)
            self.assertEqual(result.statistics.zones_created, 2)
            self.assertEqual(result.statistics.errors, 0)
            self.assertEqual(result.accepted_count, 2)
            self.assertEqual(result.rejected_count, 0)
            self.assertEqual(result.zone_count, 2)
            self.assertEqual(result.warning_count, 0)
            self.assertEqual(result.error_count, 0)

    def test_supports_repeaterbook_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "repeaterbook.csv"
            path.write_text(
                "Name,Output,Input,Mode,Nearest City,State,County,Callsign\n"
                "Metro,449.500,444.500,FM,Denver,CO,Denver,W0XYZ\n",
                encoding="utf-8",
            )

            result = BuildProject().import_csv(path, profile="repeaterbook").build()

            self.assertEqual(len(result.accepted_channels), 1)
            channel = result.accepted_channels[0]
            self.assertEqual(channel.name, "Metro")
            self.assertEqual(channel.rx_frequency, "449.500")
            self.assertEqual(channel.tx_frequency, "444.500")
            self.assertEqual(channel.city, "Denver")
            self.assertEqual(channel.callsign, "W0XYZ")

    def test_removes_exact_duplicates_before_channel_build(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first.csv"
            second = Path(tmp) / "second.csv"
            contents = "name,rx_frequency,mode,zone\nShared,146.520,FM,Local\n"
            first.write_text(contents, encoding="utf-8")
            second.write_text(contents, encoding="utf-8")

            result = BuildProject().import_csv(first).import_csv(second).build()

            self.assertEqual([channel.name for channel in result.accepted_channels], ["Shared"])
            self.assertEqual(result.statistics.duplicate_channels_removed, 1)
            self.assertEqual(result.statistics.warnings, 1)
            self.assertEqual(result.validation_issues[0].code, "exact_duplicate_channel_removed")

    def test_conflicting_duplicate_names_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "channels.csv"
            path.write_text(
                "name,rx_frequency,mode,zone\n"
                "Shared,146.520,FM,Local\n"
                "shared,446.000,FM,Local\n",
                encoding="utf-8",
            )

            result = BuildProject().import_csv(path).build()

            self.assertEqual([channel.name for channel in result.accepted_channels], ["Shared"])
            self.assertEqual(result.statistics.channels_rejected, 1)
            self.assertEqual(result.statistics.errors, 1)
            self.assertEqual(result.rejected_channels[0].code, "conflicting_duplicate_channel")

    def test_invalid_import_and_channel_rows_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "channels.csv"
            path.write_text(
                "name,rx_frequency,mode\n"
                ",146.520,FM\n"
                "Bad Mode,446.000,DMR\n"
                "Valid,147.000,FM\n",
                encoding="utf-8",
            )

            result = BuildProject().import_csv(path).build()

            self.assertEqual([channel.name for channel in result.accepted_channels], ["Valid"])
            self.assertEqual(result.statistics.channels_imported, 3)
            self.assertEqual(result.statistics.channels_rejected, 2)
            self.assertEqual([issue.code for issue in result.rejected_channels], ["csv_row_rejected", "channel_rejected"])

    def test_project_limits_are_configurable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "channels.csv"
            path.write_text(
                "name,rx_frequency,mode,zone\n"
                "One,146.520,FM,A\n"
                "Two,446.000,FM,B\n",
                encoding="utf-8",
            )

            result = BuildProject(limits=BuildLimits(max_channels=1, max_zones=1)).import_csv(path).build()

            self.assertEqual(result.statistics.channels_accepted, 2)
            self.assertEqual(result.statistics.channels_rejected, 0)
            self.assertEqual(
                [issue.code for issue in result.validation_issues if issue.severity == "error"],
                ["max_channels_exceeded", "max_zones_exceeded"],
            )

    def test_duplicate_names_and_frequencies_are_project_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "channels.csv"
            path.write_text(
                "name,rx_frequency,mode,zone\n"
                "Shared,146.520,FM,A\n"
                "shared,146.520,FM,B\n",
                encoding="utf-8",
            )

            result = BuildProject().import_csv(path).build()

            self.assertEqual(result.statistics.channels_accepted, 2)
            self.assertEqual(
                [issue.code for issue in result.validation_issues],
                ["duplicate_channel_name", "duplicate_frequency"],
            )
            self.assertEqual(result.statistics.warnings, 2)
            self.assertEqual(result.statistics.channels_rejected, 0)

    def test_duplicate_frequencies_are_project_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "channels.csv"
            path.write_text(
                "name,rx_frequency,mode,zone\n"
                "One,146.520,FM,A\n"
                "Two,146.520,FM,B\n",
                encoding="utf-8",
            )

            result = BuildProject().import_csv(path).build()

            self.assertEqual(result.statistics.channels_accepted, 2)
            self.assertEqual([issue.code for issue in result.validation_issues], ["duplicate_frequency"])
            self.assertEqual(result.statistics.warnings, 1)

    def test_build_does_not_modify_codeplug_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "channels.csv"
            path.write_text("name,rx_frequency,mode\nSimplex,146.520,FM\n", encoding="utf-8")
            codeplug = Codeplug.load(FIXTURE)
            original = codeplug.to_bytes()

            result = BuildProject().import_csv(path).build(codeplug=codeplug)

            self.assertEqual(result.statistics.channels_accepted, 1)
            self.assertEqual(codeplug.to_bytes(), original)


if __name__ == "__main__":
    unittest.main()
