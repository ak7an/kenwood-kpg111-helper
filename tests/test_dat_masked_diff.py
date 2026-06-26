from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.dat_masked_diff import masked_diff, parse_ignore_pair


TOOL = Path("tools/dat_masked_diff.py")


class DatMaskedDiffTests(unittest.TestCase):
    def test_identical_files(self) -> None:
        data = b"H" * 0x40 + b"\x00\x01\x02"
        result = masked_diff(data, data)

        self.assertEqual(result.total_compared, 3)
        self.assertEqual(result.raw_differing, 0)
        self.assertEqual(result.ignored_filler_substitutions, 0)
        self.assertEqual(result.meaningful_differing, 0)

    def test_one_ignored_filler_substitution(self) -> None:
        left = b"H" * 0x40 + bytes([0xBE])
        right = b"H" * 0x40 + bytes([0xC6])
        result = masked_diff(left, right)

        self.assertEqual(result.raw_differing, 1)
        self.assertEqual(result.ignored_filler_substitutions, 1)
        self.assertEqual(result.meaningful_differing, 0)

    def test_one_meaningful_difference(self) -> None:
        left = b"H" * 0x40 + bytes([0x11])
        right = b"H" * 0x40 + bytes([0x22])
        result = masked_diff(left, right)

        self.assertEqual(result.raw_differing, 1)
        self.assertEqual(result.ignored_filler_substitutions, 0)
        self.assertEqual(result.meaningful_differing, 1)
        self.assertEqual(result.meaningful_differences[0].offset, 0x40)
        self.assertEqual(result.meaningful_differences[0].left, 0x11)
        self.assertEqual(result.meaningful_differences[0].right, 0x22)

    def test_header_skipped(self) -> None:
        left = bytearray(b"H" * 0x40 + b"\x00")
        right = bytearray(left)
        right[0] = 0x00
        result = masked_diff(bytes(left), bytes(right))

        self.assertEqual(result.total_compared, 1)
        self.assertEqual(result.raw_differing, 0)
        self.assertEqual(result.meaningful_differing, 0)

    def test_limit_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            left = self._write_bytes(Path(tmp) / "left.dat", b"H" * 0x40 + b"\x00\x00\x00")
            right = self._write_bytes(Path(tmp) / "right.dat", b"H" * 0x40 + b"\x01\x02\x03")

            result = self._run_tool(left, right, "--limit", "1")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Meaningful differing bytes: 3", result.stdout)
            self.assertIn("| 0x00000040 | 0x00 | 0x01 |", result.stdout)
            self.assertNotIn("| 0x00000041 | 0x00 | 0x02 |", result.stdout)
            self.assertIn("... 2 more meaningful diffs not shown", result.stdout)

    def test_invalid_argument_handling(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            left = self._write_bytes(Path(tmp) / "left.dat", b"H" * 0x40)
            right = self._write_bytes(Path(tmp) / "right.dat", b"H" * 0x40)

            bad_pair = self._run_tool(left, right, "--ignore-pair", "BE")
            bad_limit = self._run_tool(left, right, "--limit", "-1")
            bad_header = self._run_tool(left, right, "--header-size", "-1")

            self.assertNotEqual(bad_pair.returncode, 0)
            self.assertIn("--ignore-pair must be A:B", bad_pair.stderr)
            self.assertNotEqual(bad_limit.returncode, 0)
            self.assertIn("--limit must be >= 0", bad_limit.stderr)
            self.assertNotEqual(bad_header.returncode, 0)
            self.assertIn("--header-size must be >= 0", bad_header.stderr)

    def test_ignore_pair_accepts_prefixed_and_unprefixed_hex(self) -> None:
        self.assertEqual(parse_ignore_pair("BE:C6"), (0xBE, 0xC6))
        self.assertEqual(parse_ignore_pair("0xBE:0xC6"), (0xBE, 0xC6))

    @staticmethod
    def _write_bytes(path: Path, data: bytes) -> Path:
        path.write_bytes(data)
        return path

    @staticmethod
    def _run_tool(left: Path, right: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(TOOL),
                str(left),
                str(right),
                *args,
            ],
            check=False,
            text=True,
            capture_output=True,
        )


if __name__ == "__main__":
    unittest.main()
