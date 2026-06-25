from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.dat_diff import ascii_preview, find_changed_ranges, hex_preview


TOOL = Path("tools/dat_diff.py")


class DatDiffTests(unittest.TestCase):
    def test_find_changed_ranges_groups_contiguous_offsets(self) -> None:
        ranges = find_changed_ranges(b"abcdefghi", b"abXYefZhi")

        self.assertEqual([(changed.start, changed.end) for changed in ranges], [(2, 3), (6, 6)])
        self.assertEqual([changed.length for changed in ranges], [2, 1])

    def test_find_changed_ranges_reports_size_growth(self) -> None:
        ranges = find_changed_ranges(b"abc", b"abcde")

        self.assertEqual([(changed.start, changed.end) for changed in ranges], [(3, 4)])

    def test_find_changed_ranges_reports_size_shrink(self) -> None:
        ranges = find_changed_ranges(b"abcde", b"abc")

        self.assertEqual([(changed.start, changed.end) for changed in ranges], [(3, 4)])

    def test_preview_helpers(self) -> None:
        data = b"AB\x00\xffZ"

        self.assertEqual(hex_preview(data), "41 42 00 ff 5a")
        self.assertEqual(hex_preview(data, 1, 4), "42 00 ff")
        self.assertEqual(ascii_preview(data), "AB..Z")
        self.assertEqual(ascii_preview(data, 1, 4), "B..")

    def test_cli_markdown_report_limits_ranges(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            baseline = Path(tmp) / "baseline.dat"
            modified = Path(tmp) / "modified.dat"
            baseline.write_bytes(b"abcdefghi")
            modified.write_bytes(b"abXYefZhi")

            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    str(baseline),
                    str(modified),
                    "--context",
                    "1",
                    "--max-ranges",
                    "1",
                    "--markdown",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("# DAT Binary Difference Report", result.stdout)
            self.assertIn("- Total changed bytes: 3", result.stdout)
            self.assertIn("- Changed ranges: 2", result.stdout)
            self.assertIn("### 0x00000002-0x00000003 length=2", result.stdout)
            self.assertIn("... 1 more ranges not shown", result.stdout)

    def test_cli_reports_identical_files_as_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            baseline = Path(tmp) / "baseline.dat"
            modified = Path(tmp) / "modified.dat"
            baseline.write_bytes(b"abc")
            modified.write_bytes(b"abc")

            result = subprocess.run(
                [sys.executable, str(TOOL), str(baseline), str(modified)],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Files are identical.", result.stdout)


if __name__ == "__main__":
    unittest.main()
