from pathlib import Path
import csv
import re
import subprocess
import sys
import tempfile
import unittest

from tools.dat_export_channels import FIELDNAMES


FIXTURE = Path("research/dattest/Dattest/AK7AN_Travel.dat")
TOOL = Path("tools/dat_export_channels.py")
HEX_RE = re.compile(r"^0x[0-9a-fA-F]{8}$")


class ChannelExportTests(unittest.TestCase):
    def test_tool_runs_on_ak7an_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "channels.csv"

            result = self._run_tool(output)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(output.exists())

    def test_csv_header_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "channels.csv"

            result = self._run_tool(output)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with output.open(newline="", encoding="utf-8") as handle:
                reader = csv.reader(handle)
                self.assertEqual(next(reader), FIELDNAMES)

    def test_record_offsets_are_valid_hex_or_blank(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "channels.csv"

            result = self._run_tool(output, "--limit", "10")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for row in self._read_rows(output):
                offset = row["record_offset"]
                self.assertTrue(offset == "" or HEX_RE.match(offset), offset)

    def test_confidence_column_is_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "channels.csv"

            result = self._run_tool(output, "--limit", "5")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            rows = self._read_rows(output)
            self.assertIn("confidence", rows[0])
            self.assertTrue(rows[0]["confidence"])

    def test_no_dat_output_file_is_written_or_modified(self) -> None:
        original = FIXTURE.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "channels.csv"

            result = self._run_tool(output, "--limit", "5")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(FIXTURE.read_bytes(), original)
            self.assertEqual(
                {path.name for path in Path(tmp).iterdir()},
                {"channels.csv"},
            )

    @staticmethod
    def _run_tool(output: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(TOOL),
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
    def _read_rows(path: Path) -> list[dict[str, str]]:
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
