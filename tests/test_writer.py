from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from kpg111.decoder import NAME_LENGTH, NAME_START, NUMERIC_LENGTH, NUMERIC_START
from kpg111.writer import WriterError, edit_record, rename_record


FIXTURE = Path("data/normalized/dattest/Dattest/AK7AN_Travel.dat")
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

    def test_talk_group_numeric_id_edit_changes_only_expected_id_bytes(self) -> None:
        original = FIXTURE.read_bytes()
        result = edit_record(original, DECODE_KEY, "talk_groups", 1, numeric_id=12345)

        changed_offsets = self._changed_offsets(original, result.data)
        id_offsets = set(range(0x14FA0 + NUMERIC_START, 0x14FA0 + NUMERIC_START + NUMERIC_LENGTH))

        self.assertTrue(changed_offsets)
        self.assertLessEqual(changed_offsets, id_offsets)
        self.assertEqual(
            result.data[0x14FA0 + NUMERIC_START : 0x14FA0 + NUMERIC_START + NUMERIC_LENGTH],
            bytes(byte ^ DECODE_KEY for byte in (12345).to_bytes(NUMERIC_LENGTH, "little")),
        )

    def test_individual_id_numeric_id_edit_changes_only_expected_id_bytes(self) -> None:
        original = FIXTURE.read_bytes()
        result = edit_record(original, DECODE_KEY, "individual_ids", 1, numeric_id=12345)

        changed_offsets = self._changed_offsets(original, result.data)
        id_offsets = set(range(0x104A0 + NUMERIC_START, 0x104A0 + NUMERIC_START + NUMERIC_LENGTH))

        self.assertTrue(changed_offsets)
        self.assertLessEqual(changed_offsets, id_offsets)

    def test_combined_name_and_id_edit_changes_only_expected_bytes(self) -> None:
        original = FIXTURE.read_bytes()
        result = edit_record(
            original,
            DECODE_KEY,
            "talk_groups",
            1,
            name="TEST TG",
            numeric_id=12345,
        )

        changed_offsets = self._changed_offsets(original, result.data)
        name_offsets = set(range(0x14FA0 + NAME_START, 0x14FA0 + NAME_START + NAME_LENGTH))
        id_offsets = set(range(0x14FA0 + NUMERIC_START, 0x14FA0 + NUMERIC_START + NUMERIC_LENGTH))

        self.assertTrue(changed_offsets)
        self.assertLessEqual(changed_offsets, name_offsets | id_offsets)
        self.assertTrue(changed_offsets & name_offsets)
        self.assertTrue(changed_offsets & id_offsets)

    def test_talk_group_id_65519_is_accepted(self) -> None:
        original = FIXTURE.read_bytes()
        result = edit_record(original, DECODE_KEY, "talk_groups", 1, numeric_id=65519)

        self.assertNotEqual(result.data, original)

    def test_talk_group_id_65520_is_rejected(self) -> None:
        original = FIXTURE.read_bytes()
        with self.assertRaises(WriterError):
            edit_record(original, DECODE_KEY, "talk_groups", 1, numeric_id=65520)

    def test_talk_group_id_zero_is_rejected(self) -> None:
        original = FIXTURE.read_bytes()
        with self.assertRaises(WriterError):
            edit_record(original, DECODE_KEY, "talk_groups", 1, numeric_id=0)

    def test_individual_id_range_enforcement_works(self) -> None:
        original = FIXTURE.read_bytes()
        edit_record(original, DECODE_KEY, "individual_ids", 1, numeric_id=65519)
        with self.assertRaises(WriterError):
            edit_record(original, DECODE_KEY, "individual_ids", 1, numeric_id=65520)
        with self.assertRaises(WriterError):
            edit_record(original, DECODE_KEY, "individual_ids", 1, numeric_id=0)

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

    def test_edit_requires_name_or_id(self) -> None:
        original = FIXTURE.read_bytes()
        with self.assertRaises(WriterError):
            edit_record(original, DECODE_KEY, "talk_groups", 1)

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

    def test_cli_row_2_edits_same_bytes_as_slot_1(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            slot_output = Path(tmp) / "slot.dat"
            row_output = Path(tmp) / "row.dat"

            slot_result = self._run_cli(
                slot_output,
                "--table",
                "talk_groups",
                "--slot",
                "1",
                "--name",
                "TEST TG",
            )
            row_result = self._run_cli(
                row_output,
                "--table",
                "talk_groups",
                "--row",
                "2",
                "--name",
                "TEST TG",
            )

            self.assertEqual(slot_result.returncode, 0, slot_result.stdout + slot_result.stderr)
            self.assertEqual(row_result.returncode, 0, row_result.stdout + row_result.stderr)
            self.assertEqual(row_output.read_bytes(), slot_output.read_bytes())
            self.assertIn("Row: 2", row_result.stdout)
            self.assertIn("Slot: 1", row_result.stdout)

    def test_cli_row_1_maps_to_slot_0(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "row1.dat"

            result = self._run_cli(
                output,
                "--table",
                "talk_groups",
                "--row",
                "1",
                "--name",
                "TEST TG",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Row: 1", result.stdout)
            self.assertIn("Slot: 0", result.stdout)
            self.assertIn("Record offset: 0x00014f80", result.stdout)

    def test_cli_row_zero_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run_cli(
                Path(tmp) / "out.dat",
                "--table",
                "talk_groups",
                "--row",
                "0",
                "--name",
                "TEST TG",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--row must be >= 1", result.stderr)

    def test_cli_using_both_row_and_slot_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run_cli(
                Path(tmp) / "out.dat",
                "--table",
                "talk_groups",
                "--row",
                "2",
                "--slot",
                "1",
                "--name",
                "TEST TG",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("provide exactly one of --slot or --row, not both", result.stderr)

    def test_cli_using_neither_row_nor_slot_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run_cli(
                Path(tmp) / "out.dat",
                "--table",
                "talk_groups",
                "--name",
                "TEST TG",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("provide exactly one of --slot or --row", result.stderr)

    def test_cli_existing_slot_behavior_still_works(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "slot.dat"

            result = self._run_cli(
                output,
                "--table",
                "talk_groups",
                "--slot",
                "1",
                "--id",
                "12345",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(output.exists())
            self.assertIn("Row: 2", result.stdout)
            self.assertIn("Slot: 1", result.stdout)

    @staticmethod
    def _changed_offsets(original: bytes, candidate: bytes) -> set[int]:
        return {
            offset
            for offset, (left, right) in enumerate(zip(original, candidate))
            if left != right
        }

    @staticmethod
    def _run_cli(output: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(TOOL),
                str(FIXTURE),
                str(output),
                *args,
            ],
            check=False,
            text=True,
            capture_output=True,
        )


if __name__ == "__main__":
    unittest.main()
