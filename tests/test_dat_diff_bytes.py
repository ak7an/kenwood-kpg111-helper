from pathlib import Path
import csv
import subprocess
import sys
import tempfile
import unittest

from kpg111.decoder import TALK_GROUP_TABLE_START
from tools.dat_diff_bytes import CSV_FIELDNAMES, find_changed_ranges


TOOL = Path("tools/dat_diff_bytes.py")


class DatDiffBytesTests(unittest.TestCase):
    def test_identical_files_report_no_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            before = self._write_bytes(Path(tmp) / "before.dat", b"abcdef")
            after = self._write_bytes(Path(tmp) / "after.dat", b"abcdef")

            result = self._run_tool(before, after)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("No byte changes.", result.stdout)

    def test_one_byte_change_reports_one_range(self) -> None:
        ranges = find_changed_ranges(b"abc", b"aXc")

        self.assertEqual([(changed.start, changed.end, changed.length) for changed in ranges], [(1, 1, 1)])

    def test_adjacent_byte_changes_group_into_one_range(self) -> None:
        ranges = find_changed_ranges(b"abcdef", b"abXYef")

        self.assertEqual([(changed.start, changed.end, changed.length) for changed in ranges], [(2, 3, 2)])

    def test_separated_changes_produce_multiple_ranges(self) -> None:
        ranges = find_changed_ranges(b"abcdef", b"aXcYeZ")

        self.assertEqual(
            [(changed.start, changed.end, changed.length) for changed in ranges],
            [(1, 1, 1), (3, 3, 1), (5, 5, 1)],
        )

    def test_size_mismatch_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            before = self._write_bytes(Path(tmp) / "before.dat", b"abc")
            after = self._write_bytes(Path(tmp) / "after.dat", b"abcd")

            result = self._run_tool(before, after)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("files must be the same size", result.stderr)

    def test_csv_output_has_stable_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            before = self._write_bytes(Path(tmp) / "before.dat", b"abcdef")
            after = self._write_bytes(Path(tmp) / "after.dat", b"abcXef")
            output = Path(tmp) / "diff.csv"

            result = self._run_tool(before, after, "--csv", str(output))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with output.open(newline="", encoding="utf-8") as handle:
                reader = csv.reader(handle)
                self.assertEqual(next(reader), CSV_FIELDNAMES)

    def test_known_tg_table_overlap_is_identified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data = bytearray(b"\x5b" * (TALK_GROUP_TABLE_START + 64))
            before = self._write_bytes(Path(tmp) / "before.dat", bytes(data))
            data[TALK_GROUP_TABLE_START + 1] ^= 0x01
            after = self._write_bytes(Path(tmp) / "after.dat", bytes(data))

            result = self._run_tool(before, after, "--context", "0")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("known Talk Group table", result.stdout)

    @staticmethod
    def _write_bytes(path: Path, data: bytes) -> Path:
        path.write_bytes(data)
        return path

    @staticmethod
    def _run_tool(before: Path, after: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(TOOL),
                str(before),
                str(after),
                *args,
            ],
            check=False,
            text=True,
            capture_output=True,
        )


if __name__ == "__main__":
    unittest.main()
