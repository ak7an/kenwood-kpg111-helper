from pathlib import Path
import importlib
import unittest


FIXTURE = Path("research/dattest/Dattest/AK7AN_Travel.dat")


class OpenKPGGuiTests(unittest.TestCase):
    def test_module_import_does_not_start_gui(self) -> None:
        module = importlib.import_module("openkpg_gui")

        self.assertTrue(hasattr(module, "OpenKPGTkApp"))

    def test_extract_channel_records_reads_experimental_raw_fields(self) -> None:
        module = importlib.import_module("openkpg_gui")
        data = bytearray(b"\x00" * 0x100)
        data[0x45:0x48] = b"\x01\x02\x03"
        data[0x49:0x4C] = b"\x04\x05\x06"
        data[0x85:0x88] = b"\x07\x08\x09"
        data[0x89:0x8C] = b"\x0a\x0b\x0c"

        rows = module.extract_channel_records(bytes(data), start=0x40, stride=0x40, count=2)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].channel, 1)
        self.assertEqual(rows[0].offset, 0x40)
        self.assertEqual(rows[0].rx_bytes, "01 02 03")
        self.assertEqual(rows[0].tx_bytes, "04 05 06")
        self.assertEqual(rows[1].channel, 2)
        self.assertEqual(rows[1].offset, 0x80)
        self.assertEqual(rows[1].rx_bytes, "07 08 09")
        self.assertEqual(rows[1].tx_bytes, "0a 0b 0c")

    def test_extract_channel_records_stops_before_incomplete_record(self) -> None:
        module = importlib.import_module("openkpg_gui")

        rows = module.extract_channel_records(b"\x00" * 0x7F, start=0x40, stride=0x40, count=2)

        self.assertEqual(rows, [])

    def test_backend_load_path_used_by_gui_can_load_fixture(self) -> None:
        module = importlib.import_module("openkpg_gui")
        backend = module.OpenKPGProjectBackend()

        project = backend.load_dat(FIXTURE)

        self.assertGreaterEqual(len(project.talkgroups), 1)
        self.assertGreaterEqual(len(project.contacts), 1)
        self.assertEqual(project.radio.source_file, str(FIXTURE))


if __name__ == "__main__":
    unittest.main()
