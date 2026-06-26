from dataclasses import dataclass
from pathlib import Path
import importlib
import tempfile
import unittest


FIXTURE = Path("research/dattest/Dattest/AK7AN_Travel.dat")


@dataclass(frozen=True)
class FakeRecord:
    slot: int
    source_offset: int
    numeric_id: int
    name: str
    empty: bool = False
    confidence: str = "HIGH"


class OpenKPGGuiTests(unittest.TestCase):
    def test_module_import_does_not_start_gui(self) -> None:
        module = importlib.import_module("openkpg_gui")

        self.assertTrue(hasattr(module, "main"))

    def test_parse_int_auto_base_accepts_decimal_and_hex(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        self.assertEqual(module.parse_int_auto_base("64"), 64)
        self.assertEqual(module.parse_int_auto_base("0x40"), 64)
        self.assertEqual(module.parse_int_auto_base(64), 64)

    def test_parse_offset_rejects_negative_values(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        with self.assertRaises(ValueError):
            module.parse_offset("-1")
        with self.assertRaises(ValueError):
            module.parse_offset(-1)

    def test_format_hex_bytes(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        self.assertEqual(module.format_hex_bytes(b"\x00\xab\xff"), "00 ab ff")

    def test_ascii_safe_replaces_nonprintable_bytes(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        self.assertEqual(module.ascii_safe(b"A\x00~\xff"), "A.~.")

    def test_make_hexdump_rows_includes_offset_hex_and_ascii(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        rows = module.make_hexdump_rows(b"ABCDEFGHIJKLMNOPQRST", start="0x10", length=4, width=4)

        self.assertEqual(rows, ["00000010  51 52 53 54  |QRST|"])

    def test_make_hexdump_rows_rejects_invalid_width_and_length(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        with self.assertRaises(ValueError):
            module.make_hexdump_rows(b"", width=0)
        with self.assertRaises(ValueError):
            module.make_hexdump_rows(b"", length=-1)

    def test_extract_channel_records_reads_experimental_raw_fields(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")
        data = bytearray(b"\x00" * 0x100)
        data[0x45:0x48] = b"\x01\x02\x03"
        data[0x48] = 0x99
        data[0x49:0x4C] = b"\x04\x05\x06"
        data[0x4C] = 0x88
        data[0x85:0x88] = b"\x07\x08\x09"
        data[0x89:0x8C] = b"\x0a\x0b\x0c"

        rows = module.extract_channel_records(bytes(data), start=0x40, stride=0x40, count=2)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].channel, 1)
        self.assertEqual(rows[0].offset, 0x40)
        self.assertEqual(rows[0].rx_bytes, "01 02 03")
        self.assertEqual(rows[0].tx_bytes, "04 05 06")
        self.assertEqual(rows[0].marker_08, "99")
        self.assertEqual(rows[0].marker_0c, "88")
        self.assertEqual(rows[0].raw_record, bytes(data[0x40:0x80]))
        self.assertEqual(rows[1].channel, 2)
        self.assertEqual(rows[1].offset, 0x80)
        self.assertEqual(rows[1].rx_bytes, "07 08 09")
        self.assertEqual(rows[1].tx_bytes, "0a 0b 0c")

    def test_extract_channel_records_stops_before_incomplete_record(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        rows = module.extract_channel_records(b"\x00" * 0x7F, start=0x40, stride=0x40, count=2)

        self.assertEqual(rows, [])

    def test_extract_channel_records_defaults_to_first_128_records(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")
        data = b"\x00" * (module.CHANNEL_TABLE_START + (128 * module.CHANNEL_RECORD_STRIDE))

        rows = module.extract_channel_records(data)

        self.assertEqual(len(rows), 128)
        self.assertEqual(rows[-1].channel, 128)
        self.assertEqual(rows[-1].offset, module.CHANNEL_TABLE_START + (127 * module.CHANNEL_RECORD_STRIDE))

    def test_channel_row_model_accepts_hex_start_and_stride(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")
        data = bytearray(b"\x00" * 0x100)
        data[0x45:0x48] = b"\xaa\xbb\xcc"

        rows = module.channel_row_model(bytes(data), start="0x40", stride="0x40", count=1)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].offset, 0x40)
        self.assertEqual(rows[0].rx_bytes, "aa bb cc")

    def test_channel_row_model_rejects_invalid_stride_and_count(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        with self.assertRaises(ValueError):
            module.channel_row_model(b"", stride=0)
        with self.assertRaises(ValueError):
            module.channel_row_model(b"", count=-1)

    def test_self_payload_xor_mask_is_placeholder_zero(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        self.assertEqual(module.detect_self_payload_xor_mask(b"abc"), 0x00)

    def test_channel_records_include_normalized_record_bytes(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")
        data = bytes(range(0x40))

        rows = module.extract_channel_records(data, start=0, stride=0x40, count=1, xor_mask=0xFF)

        self.assertEqual(rows[0].raw_record[:4], b"\x00\x01\x02\x03")
        self.assertEqual(rows[0].normalized_record[:4], b"\xff\xfe\xfd\xfc")

    def test_format_record_hex_uses_16_byte_rows(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        rendered = module.format_record_hex(bytes(range(0x20)))

        self.assertEqual(
            rendered,
            "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f\n"
            "10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f",
        )

    def test_filter_table_rows_matches_decoded_record_fields(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")
        rows = [
            FakeRecord(slot=1, source_offset=0x100, numeric_id=101, name="Dispatch"),
            FakeRecord(slot=2, source_offset=0x120, numeric_id=202, name="Tac"),
        ]

        self.assertEqual(module.filter_table_rows(rows, "dispatch"), [rows[0]])
        self.assertEqual(module.filter_table_rows(rows, "0x00000120"), [rows[1]])
        self.assertEqual(module.filter_table_rows(rows, ""), rows)

    def test_filter_table_rows_matches_dict_and_sequence_rows(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        self.assertEqual(module.filter_table_rows([{"name": "Alpha"}], "alp"), [{"name": "Alpha"}])
        self.assertEqual(module.filter_table_rows([(1, "Bravo")], "bravo"), [(1, "Bravo")])

    def test_dominant_xor_mask_detects_payload_shift(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        self.assertEqual(module.dominant_xor_mask(b"\x00\x11\x22", b"\x5b\x4a\x79"), 0x5B)

    def test_pure_xor_shifted_payload_has_zero_normalized_differences(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")
        left = b"H" * 0x40 + bytes([0x00, 0x11, 0x22, 0x33])
        right = b"H" * 0x40 + bytes(byte ^ 0x5B for byte in [0x00, 0x11, 0x22, 0x33])

        result = module.normalized_differences(left, right)

        self.assertEqual(result.dominant_xor_mask, 0x5B)
        self.assertEqual(result.payload_bytes_compared, 4)
        self.assertEqual(result.normalized_differing_byte_count, 0)
        self.assertEqual(result.differences, [])

    def test_one_edited_byte_is_reported_after_normalization(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")
        left = b"H" * 0x40 + bytes([0x00, 0x11, 0x22, 0x33])
        right_payload = bytearray(byte ^ 0x5B for byte in [0x00, 0x11, 0x22, 0x33])
        right_payload[2] = 0x99
        right = b"H" * 0x40 + bytes(right_payload)

        result = module.normalized_differences(left, right)

        self.assertEqual(result.normalized_differing_byte_count, 1)
        self.assertEqual(result.differences[0].offset, 0x42)
        self.assertEqual(result.differences[0].left_byte, 0x22)
        self.assertEqual(result.differences[0].right_raw_byte, 0x99)
        self.assertEqual(result.differences[0].right_normalized_byte, 0xC2)

    def test_normalized_differences_rejects_size_mismatch(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        with self.assertRaises(ValueError):
            module.normalized_differences(b"a", b"ab")

    def test_channel_location_maps_offset_to_channel_and_relative_offset(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        location = module.channel_location_for_offset(0x5E80 + 0x40 + 0x12)

        self.assertIsNotNone(location)
        self.assertEqual(location.channel, 2)
        self.assertEqual(location.relative_offset, 0x12)
        self.assertEqual(location.label, "channel record +0x12")

    def test_channel_location_detects_rx_and_tx_field_labels(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        rx = module.channel_location_for_offset(0x5E80 + 0x05)
        tx = module.channel_location_for_offset(0x5E80 + 0x09)

        self.assertEqual(rx.label, "RX frequency")
        self.assertEqual(tx.label, "TX frequency")

    def test_channel_location_returns_none_outside_known_table(self) -> None:
        module = importlib.import_module("openkpg.gui.helpers")

        self.assertIsNone(module.channel_location_for_offset(0x5E7F))
        self.assertIsNone(module.channel_location_for_offset(0x5E80 + 512 * 0x40))

    def test_no_dat_explorer_model(self) -> None:
        module = importlib.import_module("openkpg.gui.explorer")

        model = module.no_dat_explorer_model()

        self.assertEqual(model.label, "No DAT loaded")
        self.assertEqual(model.target, "none")
        self.assertEqual(model.children, ())

    def test_explorer_model_generation_from_counts(self) -> None:
        module = importlib.import_module("openkpg.gui.explorer")

        model = module.explorer_model_for_dat(Path("/tmp/example.dat"), 70, 17, 14)

        self.assertEqual(model.label, "example.dat")
        self.assertEqual([child.label for child in model.children], [
            "Summary",
            "Channels (70)",
            "Talk Groups (17)",
            "Individual IDs (14)",
            "Hex View",
            "Compare",
        ])
        channels = model.children[1]
        self.assertEqual(len(channels.children), 64)
        self.assertEqual(channels.children[0].label, "Channel 1")
        self.assertEqual(channels.children[-1].label, "Channel 64")
        self.assertEqual(channels.children[-1].channel_number, 64)

    def test_channel_number_to_offset_mapping(self) -> None:
        module = importlib.import_module("openkpg.gui.explorer")

        self.assertEqual(module.channel_number_to_offset(1), 0x5E80)
        self.assertEqual(module.channel_number_to_offset(2), 0x5EC0)
        self.assertEqual(module.channel_number_to_offset(64), 0x5E80 + 63 * 0x40)
        with self.assertRaises(ValueError):
            module.channel_number_to_offset(0)

    def test_loading_missing_preferences_uses_defaults(self) -> None:
        module = importlib.import_module("openkpg.gui.preferences")
        with tempfile.TemporaryDirectory() as tmp:
            prefs = module.Preferences.load(Path(tmp) / "missing.json")

        self.assertEqual(prefs.recent_files, [])
        self.assertEqual(prefs.last_open_dir, "")
        self.assertEqual(prefs.channel_start, "0x5E80")
        self.assertEqual(prefs.channel_stride, "0x40")
        self.assertEqual(prefs.channel_count, 128)

    def test_invalid_json_preferences_fallback_to_defaults(self) -> None:
        module = importlib.import_module("openkpg.gui.preferences")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "preferences.json"
            path.write_text("{not valid json", encoding="utf-8")

            prefs = module.Preferences.load(path)

        self.assertEqual(prefs.recent_files, [])
        self.assertEqual(prefs.channel_count, 128)

    def test_recent_file_add_dedupe_and_max_10(self) -> None:
        module = importlib.import_module("openkpg.gui.preferences")
        prefs = module.Preferences()

        for index in range(12):
            prefs.add_recent_file(f"/tmp/file{index}.dat")
        prefs.add_recent_file("/tmp/file5.dat")

        self.assertEqual(prefs.recent_files[0], "/tmp/file5.dat")
        self.assertEqual(len(prefs.recent_files), 10)
        self.assertEqual(prefs.recent_files.count("/tmp/file5.dat"), 1)
        self.assertEqual(prefs.last_open_dir, "/tmp")

    def test_clear_recent_files(self) -> None:
        module = importlib.import_module("openkpg.gui.preferences")
        prefs = module.Preferences(recent_files=["/tmp/a.dat", "/tmp/b.dat"])

        prefs.clear_recent_files()

        self.assertEqual(prefs.recent_files, [])

    def test_saving_and_loading_channel_defaults(self) -> None:
        module = importlib.import_module("openkpg.gui.preferences")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".config" / "openkpg" / "preferences.json"
            prefs = module.Preferences()
            prefs.set_channel_defaults("0x6000", "0x80", 64)
            prefs.save(path)

            loaded = module.Preferences.load(path)

        self.assertEqual(loaded.channel_start, "0x6000")
        self.assertEqual(loaded.channel_stride, "0x80")
        self.assertEqual(loaded.channel_count, 64)

    def test_backend_load_path_used_by_gui_can_load_fixture(self) -> None:
        module = importlib.import_module("openkpg.backend")
        backend = module.OpenKPGProjectBackend()

        project = backend.load_dat(FIXTURE)

        self.assertGreaterEqual(len(project.talkgroups), 1)
        self.assertGreaterEqual(len(project.contacts), 1)
        self.assertEqual(project.radio.source_file, str(FIXTURE))


if __name__ == "__main__":
    unittest.main()
