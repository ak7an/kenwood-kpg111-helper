from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.dat_normalized_diff import normalized_diff


TOOL = Path("tools/dat_normalized_diff.py")


class DatNormalizedDiffTests(unittest.TestCase):
    def test_pure_xor_shifted_files_produce_zero_normalized_diffs(self) -> None:
        left = b"H" * 0x40 + bytes([0x00, 0x11, 0x22, 0x33])
        right = b"H" * 0x40 + bytes(byte ^ 0x5B for byte in [0x00, 0x11, 0x22, 0x33])

        result = normalized_diff(left, right)

        self.assertEqual(result.header_differing_bytes, 0)
        self.assertEqual(result.payload_compared_bytes, 4)
        self.assertEqual(result.dominant_xor_mask, 0x5B)
        self.assertEqual(result.normalized_differing_bytes, 0)
        self.assertEqual(result.differences, [])

    def test_one_real_edited_byte_reports_one_normalized_diff(self) -> None:
        left = b"H" * 0x40 + bytes([0x00, 0x11, 0x22, 0x33])
        right_payload = bytearray(byte ^ 0x5B for byte in [0x00, 0x11, 0x22, 0x33])
        right_payload[2] = 0x99
        right = b"H" * 0x40 + bytes(right_payload)

        result = normalized_diff(left, right)

        self.assertEqual(result.dominant_xor_mask, 0x5B)
        self.assertEqual(result.normalized_differing_bytes, 1)
        self.assertEqual(result.differences[0].offset, 0x42)
        self.assertEqual(result.differences[0].left, 0x22)
        self.assertEqual(result.differences[0].right_raw, 0x99)
        self.assertEqual(result.differences[0].right_normalized, 0xC2)

    def test_header_differences_reported_separately(self) -> None:
        left = bytearray(b"H" * 0x40 + b"\x00")
        right = bytearray(b"H" * 0x40 + b"\x5b")
        right[0] = 0x00

        result = normalized_diff(bytes(left), bytes(right))

        self.assertEqual(result.header_differing_bytes, 1)
        self.assertEqual(result.normalized_differing_bytes, 0)

    def test_limit_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            left = self._write_bytes(Path(tmp) / "left.dat", b"H" * 0x40 + b"\x00\x01\x02\x03\x04")
            right = self._write_bytes(Path(tmp) / "right.dat", b"H" * 0x40 + b"\x5b\x5a\x59\x99\x88")
            result = self._run_tool(left, right, "--limit", "1")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Normalized differing bytes: 2", result.stdout)
            self.assertIn("| 0x00000043 |", result.stdout)
            self.assertNotIn("| 0x00000044 |", result.stdout)
            self.assertIn("... 1 more normalized diffs not shown", result.stdout)

    def test_invalid_size_mismatch_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            left = self._write_bytes(Path(tmp) / "left.dat", b"H" * 0x40)
            right = self._write_bytes(Path(tmp) / "right.dat", b"H" * 0x41)

            result = self._run_tool(left, right)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("files must be the same size", result.stderr)

    def test_input_files_are_not_mutated(self) -> None:
        left_data = b"H" * 0x40 + b"\x00\x11"
        right_data = b"H" * 0x40 + b"\x5b\x4a"
        with tempfile.TemporaryDirectory() as tmp:
            left = self._write_bytes(Path(tmp) / "left.dat", left_data)
            right = self._write_bytes(Path(tmp) / "right.dat", right_data)

            result = self._run_tool(left, right)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(left.read_bytes(), left_data)
            self.assertEqual(right.read_bytes(), right_data)

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
