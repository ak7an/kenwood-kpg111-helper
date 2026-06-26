from pathlib import Path
import csv
import subprocess
import sys
import tempfile
import unittest

from kpg111.decoder import NAME_LENGTH, NAME_START, NUMERIC_LENGTH, NUMERIC_START


FIXTURE = Path("research/dattest/Dattest/AK7AN_Travel.dat")
EXPORT_TOOL = Path("tools/dat_export_records.py")
IMPORT_TOOL = Path("tools/dat_import_records.py")


class CsvRecordToolTests(unittest.TestCase):
    def test_export_talk_groups_csv_includes_row_slot_id_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "talkgroups.csv"

            result = self._run_export(output, "--table", "talk_groups")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            rows = self._read_csv(output)
            self.assertEqual(list(rows[0].keys()), ["row", "slot", "id", "name"])
            self.assertEqual(rows[0]["row"], "1")
            self.assertEqual(rows[0]["slot"], "0")
            self.assertEqual(rows[0]["id"], "65000")
            self.assertEqual(rows[0]["name"], "World Wide TG")

    def test_export_individual_ids_csv_includes_row_slot_id_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "ids.csv"

            result = self._run_export(output, "--table", "individual_ids")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            rows = self._read_csv(output)
            self.assertEqual(list(rows[0].keys()), ["row", "slot", "id", "name"])
            self.assertEqual(rows[0]["row"], "1")
            self.assertEqual(rows[0]["slot"], "0")
            self.assertEqual(rows[0]["id"], "16042")
            self.assertEqual(rows[0]["name"], "Curtis, AE4BT")

    def test_import_one_talk_group_name_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = self._write_csv(Path(tmp) / "tg.csv", "row,name\n2,TEST TG\n")
            output = Path(tmp) / "out.dat"

            result = self._run_import(output, "--table", "talk_groups", "--csv", str(csv_path))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            changed = self._changed_offsets(FIXTURE.read_bytes(), output.read_bytes())
            self.assertTrue(changed)
            self.assertLessEqual(changed, self._tg_name_offsets(1))

    def test_import_one_talk_group_id_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = self._write_csv(Path(tmp) / "tg.csv", "row,id\n2,12345\n")
            output = Path(tmp) / "out.dat"

            result = self._run_import(output, "--table", "talk_groups", "--csv", str(csv_path))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            changed = self._changed_offsets(FIXTURE.read_bytes(), output.read_bytes())
            self.assertTrue(changed)
            self.assertLessEqual(changed, self._tg_id_offsets(1))

    def test_import_combined_talk_group_name_and_id_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = self._write_csv(Path(tmp) / "tg.csv", "row,id,name\n2,12345,TEST TG\n")
            output = Path(tmp) / "out.dat"

            result = self._run_import(output, "--table", "talk_groups", "--csv", str(csv_path))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            changed = self._changed_offsets(FIXTURE.read_bytes(), output.read_bytes())
            self.assertTrue(changed)
            self.assertLessEqual(changed, self._tg_name_offsets(1) | self._tg_id_offsets(1))
            self.assertTrue(changed & self._tg_name_offsets(1))
            self.assertTrue(changed & self._tg_id_offsets(1))

    def test_import_one_individual_id_name_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = self._write_csv(Path(tmp) / "ids.csv", "row,name\n2,TEST ID\n")
            output = Path(tmp) / "out.dat"

            result = self._run_import(output, "--table", "individual_ids", "--csv", str(csv_path))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            changed = self._changed_offsets(FIXTURE.read_bytes(), output.read_bytes())
            self.assertTrue(changed)
            self.assertLessEqual(changed, self._id_name_offsets(1))

    def test_duplicate_row_targets_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = self._write_csv(Path(tmp) / "tg.csv", "row,name\n2,TEST TG\n2,OTHER TG\n")
            output = Path(tmp) / "out.dat"

            result = self._run_import(output, "--table", "talk_groups", "--csv", str(csv_path))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate target", result.stderr)

    def test_out_of_range_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = self._write_csv(Path(tmp) / "tg.csv", "row,id\n2,65520\n")
            output = Path(tmp) / "out.dat"

            result = self._run_import(output, "--table", "talk_groups", "--csv", str(csv_path))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("numeric ID must be between 1 and 65519", result.stderr)

    def test_missing_row_and_slot_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = self._write_csv(Path(tmp) / "tg.csv", "id,name\n12345,TEST TG\n")
            output = Path(tmp) / "out.dat"

            result = self._run_import(output, "--table", "talk_groups", "--csv", str(csv_path))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required row or slot column", result.stderr)

    def test_input_overwrite_is_rejected_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "input.dat"
            input_path.write_bytes(FIXTURE.read_bytes())
            csv_path = self._write_csv(Path(tmp) / "tg.csv", "row,name\n2,TEST TG\n")

            result = subprocess.run(
                [
                    sys.executable,
                    str(IMPORT_TOOL),
                    str(input_path),
                    str(input_path),
                    "--table",
                    "talk_groups",
                    "--csv",
                    str(csv_path),
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing to overwrite input file", result.stderr)
            self.assertEqual(input_path.read_bytes(), FIXTURE.read_bytes())

    @staticmethod
    def _run_export(output: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(EXPORT_TOOL),
                str(FIXTURE),
                "--output",
                str(output),
                *args,
            ],
            check=False,
            text=True,
            capture_output=True,
        )

    @staticmethod
    def _run_import(output: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(IMPORT_TOOL),
                str(FIXTURE),
                str(output),
                *args,
            ],
            check=False,
            text=True,
            capture_output=True,
        )

    @staticmethod
    def _write_csv(path: Path, content: str) -> Path:
        path.write_text(content, encoding="utf-8")
        return path

    @staticmethod
    def _read_csv(path: Path) -> list[dict[str, str]]:
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    @staticmethod
    def _changed_offsets(original: bytes, candidate: bytes) -> set[int]:
        return {
            offset
            for offset, (left, right) in enumerate(zip(original, candidate))
            if left != right
        }

    @staticmethod
    def _tg_name_offsets(slot: int) -> set[int]:
        start = 0x14F80 + slot * 32 + NAME_START
        return set(range(start, start + NAME_LENGTH))

    @staticmethod
    def _tg_id_offsets(slot: int) -> set[int]:
        start = 0x14F80 + slot * 32 + NUMERIC_START
        return set(range(start, start + NUMERIC_LENGTH))

    @staticmethod
    def _id_name_offsets(slot: int) -> set[int]:
        start = 0x10480 + slot * 32 + NAME_START
        return set(range(start, start + NAME_LENGTH))


if __name__ == "__main__":
    unittest.main()
