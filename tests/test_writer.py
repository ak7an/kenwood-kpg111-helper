from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from kpg111.decoder import NAME_LENGTH, NAME_START
from kpg111.writer import WriterError, rename_record


FIXTURE = Path("research/dattest/Dattest/AK7AN_Travel.dat")
TOOL = Path("tools/dat_edit_record.py")
DECODE_KEY = 0x5B


class WriterTests(unittest.TestCase):
    def test_no_op_writer_output_is_byte_identical(self) -> None:
        original = FIXTURE.read_bytes()
        result = rename_record(original, DECODE_KEY, "talk_groups", 1, "Parrot")

        self.assertEqual(result.data, original)
        self.assertEqual(result.changed_ranges, [])

    def test_edit_talk_group_changes_only_expected_name_bytes(self) -> None:
        original = FIXTURE.read_bytes()
        result = rename_record(original, DECODE_KEY, "talk_groups", 1, "TEST TG")

        changed_offsets = self._changed_offsets(original, result.data)
        name_offsets = set(range(0x14FA0 + NAME_START, 0x14FA0 + NAME_START + NAME_LENGTH))

        self.assertTrue(changed_offsets)
        self.assertLessEqual(changed_offsets, name_offsets)
        self.assertEqual(
            result.data[0x14FA0 + NAME_START : 0x14FA0 + NAME_START + NAME_LENGTH],
            bytes(byte ^ DECODE_KEY for byte in b"TEST TG".ljust(NAME_LENGTH, b"\x00")),
        )

    def test_edit_individual_id_changes_only_expected_name_bytes(self) -> None:
        original = FIXTURE.read_bytes()
        result = rename_record(original, DECODE_KEY, "individual_ids", 1, "TEST ID")

        changed_offsets = self._changed_offsets(original, result.data)
        name_offsets = set(range(0x104A0 + NAME_START, 0x104A0 + NAME_START + NAME_LENGTH))

        self.assertTrue(changed_offsets)
        self.assertLessEqual(changed_offsets, name_offsets)

    def test_unknown_bytes_remain_unchanged(self) -> None:
        original = FIXTURE.read_bytes()
        result = rename_record(original, DECODE_KEY, "talk_groups", 1, "TEST TG")
        record_start = 0x14FA0
        unknown_offsets = (
            [record_start]
            + list(range(record_start + 15, record_start + 19))
            + list(range(record_start + 21, record_start + 32))
        )

        for offset in unknown_offsets:
            self.assertEqual(result.data[offset], original[offset], f"offset 0x{offset:08x}")

    def test_unsupported_table_names_are_rejected(self) -> None:
        original = FIXTURE.read_bytes()
        with self.assertRaises(WriterError):
            rename_record(original, DECODE_KEY, "channels", 1, "TEST")

    def test_out_of_range_slots_are_rejected(self) -> None:
        original = FIXTURE.read_bytes()
        with self.assertRaises(WriterError):
            rename_record(original, DECODE_KEY, "talk_groups", 9999, "TEST")

    def test_input_file_cannot_be_overwritten_by_accident(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "input.dat"
            input_path.write_bytes(FIXTURE.read_bytes())

            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    str(input_path),
                    str(input_path),
                    "--table",
                    "talk_groups",
                    "--slot",
                    "1",
                    "--name",
                    "TEST TG",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing to overwrite input file", result.stderr)
            self.assertEqual(input_path.read_bytes(), FIXTURE.read_bytes())

    @staticmethod
    def _changed_offsets(original: bytes, candidate: bytes) -> set[int]:
        return {
            offset
            for offset, (left, right) in enumerate(zip(original, candidate))
            if left != right
        }


if __name__ == "__main__":
    unittest.main()
