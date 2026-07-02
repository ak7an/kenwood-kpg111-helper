from pathlib import Path
import tempfile
import unittest

from openkpg.csv_import import (
    ImportedChannel,
    import_channel_csv,
    normalize_header,
)


class CSVImportTests(unittest.TestCase):
    def test_openkpg_profile_imports_standard_channel_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "channels.csv"
            path.write_text(
                "name,rx_frequency,tx_frequency,mode,bandwidth,tone,ran,color_code,nac,zone,city,state,county,callsign\n"
                "Local 1,146.940,146.340,FM,12.5,100.0,1,2,293,Home,Denver,CO,Denver,W0ABC\n",
                encoding="utf-8",
            )

            report = import_channel_csv(path, profile="openkpg")

            self.assertEqual(report.accepted_count, 1)
            self.assertEqual(report.rejected_count, 0)
            channel = report.accepted[0]
            self.assertIsInstance(channel, ImportedChannel)
            self.assertEqual(channel.name, "Local 1")
            self.assertEqual(channel.rx_frequency, "146.940")
            self.assertEqual(channel.tx_frequency, "146.340")
            self.assertEqual(channel.mode, "FM")
            self.assertEqual(channel.bandwidth, "12.5")
            self.assertEqual(channel.tone, "100.0")
            self.assertEqual(channel.ran, "1")
            self.assertEqual(channel.color_code, "2")
            self.assertEqual(channel.nac, "293")
            self.assertEqual(channel.zone, "Home")
            self.assertEqual(channel.city, "Denver")
            self.assertEqual(channel.state, "CO")
            self.assertEqual(channel.county, "Denver")
            self.assertEqual(channel.callsign, "W0ABC")
            self.assertEqual(channel.source, str(path))
            self.assertEqual(channel.source_row, 2)

    def test_repeaterbook_profile_maps_common_headers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "repeaterbook.csv"
            path.write_text(
                "Name,Output,Input,Offset,Uplink Tone,Mode,Nearest City,State,County,Callsign\n"
                "Metro Repeater,449.500,444.500,-5.000,123.0,FM,Denver,CO,Denver,W0XYZ\n",
                encoding="utf-8",
            )

            report = import_channel_csv(path, profile="repeaterbook")

            self.assertEqual(report.accepted_count, 1)
            channel = report.accepted[0]
            self.assertEqual(channel.name, "Metro Repeater")
            self.assertEqual(channel.rx_frequency, "449.500")
            self.assertEqual(channel.tx_frequency, "444.500")
            self.assertEqual(channel.offset, "-5.000")
            self.assertEqual(channel.tone, "123.0")
            self.assertEqual(channel.city, "Denver")
            self.assertEqual(channel.callsign, "W0XYZ")

    def test_rejected_rows_include_row_number_and_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "channels.csv"
            path.write_text(
                "name,rx_frequency,mode\n"
                ",146.520,FM\n"
                "Simplex,,FM\n"
                "Valid,446.000,FM\n",
                encoding="utf-8",
            )

            report = import_channel_csv(path)

            self.assertEqual(report.accepted_count, 1)
            self.assertEqual(report.accepted[0].name, "Valid")
            self.assertEqual(report.rejected_count, 2)
            self.assertEqual(report.rejected[0].source_row, 2)
            self.assertIn("name is required", report.rejected[0].reason)
            self.assertEqual(report.rejected[1].source_row, 3)
            self.assertIn("rx_frequency is required", report.rejected[1].reason)

    def test_missing_required_columns_rejects_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "channels.csv"
            path.write_text("name,mode\nLocal,FM\n", encoding="utf-8")

            report = import_channel_csv(path)

            self.assertEqual(report.accepted_count, 0)
            self.assertEqual(report.rejected_count, 1)
            self.assertEqual(report.rejected[0].source_row, 1)
            self.assertIn("rx_frequency", report.rejected[0].reason)

    def test_custom_column_mapping_can_override_profile_headers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "custom.csv"
            path.write_text("Channel Label,Receive MHz,Kind\nLocal,147.000,FM\n", encoding="utf-8")

            report = import_channel_csv(
                path,
                column_mapping={
                    "Channel Label": "name",
                    "Receive MHz": "rx_frequency",
                    "Kind": "mode",
                },
            )

            self.assertEqual(report.accepted_count, 1)
            self.assertEqual(report.accepted[0].name, "Local")
            self.assertEqual(report.accepted[0].rx_frequency, "147.000")
            self.assertEqual(report.accepted[0].mode, "FM")

    def test_unknown_profile_and_bad_custom_field_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            import_channel_csv(Path("unused.csv"), profile="unknown")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "custom.csv"
            path.write_text("name,rx_frequency\nLocal,147.000\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                import_channel_csv(path, column_mapping={"name": "not_a_field"})

    def test_header_normalization_ignores_case_and_punctuation(self) -> None:
        self.assertEqual(normalize_header(" RX Frequency "), "rxfrequency")
        self.assertEqual(normalize_header("Nearest-City"), "nearestcity")


if __name__ == "__main__":
    unittest.main()
