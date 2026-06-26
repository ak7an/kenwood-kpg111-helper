from dataclasses import dataclass
from pathlib import Path
import importlib
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

    def test_backend_load_path_used_by_gui_can_load_fixture(self) -> None:
        module = importlib.import_module("openkpg.backend")
        backend = module.OpenKPGProjectBackend()

        project = backend.load_dat(FIXTURE)

        self.assertGreaterEqual(len(project.talkgroups), 1)
        self.assertGreaterEqual(len(project.contacts), 1)
        self.assertEqual(project.radio.source_file, str(FIXTURE))


if __name__ == "__main__":
    unittest.main()
