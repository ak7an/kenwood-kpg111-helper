from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.dat_xor_relation import xor_relation


TOOL = Path("tools/dat_xor_relation.py")


class DatXorRelationTests(unittest.TestCase):
    def test_constant_payload_xor_is_reported(self) -> None:
        left = b"H" * 0x40 + bytes([0x00, 0x11, 0x22])
        right = b"h" * 0x40 + bytes(byte ^ 0x5B for byte in [0x00, 0x11, 0x22])

        relation = xor_relation(left, right)

        self.assertEqual(relation.header_differing_bytes, 0x40)
        self.assertEqual(relation.payload_compared_bytes, 3)
        self.assertTrue(relation.constant)
        self.assertEqual(relation.xor_value, 0x5B)
        self.assertEqual(relation.dominant_xor_value, 0x5B)
        self.assertEqual(relation.dominant_xor_count, 3)
        self.assertEqual(relation.dominant_xor_percent, 100.0)
        self.assertEqual(relation.mismatches, [])

    def test_mismatches_are_reported_when_not_constant(self) -> None:
        left = b"H" * 0x40 + bytes([0x00, 0x11, 0x22])
        right = b"H" * 0x40 + bytes([0x5B, 0x4A, 0x22])

        relation = xor_relation(left, right)

        self.assertFalse(relation.constant)
        self.assertIsNone(relation.xor_value)
        self.assertEqual(relation.dominant_xor_value, 0x5B)
        self.assertEqual(relation.dominant_xor_count, 2)
        self.assertAlmostEqual(relation.dominant_xor_percent, 66.66666666666666)
        self.assertEqual(len(relation.mismatches), 1)
        self.assertEqual(relation.mismatches[0].offset, 0x42)
        self.assertEqual(relation.mismatches[0].xor_value, 0x00)

    def test_dominant_xor_with_a_few_edited_bytes(self) -> None:
        left_payload = bytes(range(10))
        right_payload = bytearray(byte ^ 0x5B for byte in left_payload)
        right_payload[3] = left_payload[3] ^ 0x11
        right_payload[7] = left_payload[7] ^ 0x22
        left = b"H" * 0x40 + left_payload
        right = b"H" * 0x40 + bytes(right_payload)

        relation = xor_relation(left, right)

        self.assertFalse(relation.constant)
        self.assertEqual(relation.dominant_xor_value, 0x5B)
        self.assertEqual(relation.dominant_xor_count, 8)
        self.assertEqual(relation.dominant_xor_percent, 80.0)
        self.assertEqual([mismatch.offset for mismatch in relation.mismatches], [0x43, 0x47])
        self.assertEqual([mismatch.xor_value for mismatch in relation.mismatches], [0x11, 0x22])

    def test_header_is_compared_separately_from_payload(self) -> None:
        left = bytearray(b"H" * 0x40 + b"\x01")
        right = bytearray(left)
        right[0] = 0x00
        right[0x40] = 0x5A

        relation = xor_relation(bytes(left), bytes(right))

        self.assertEqual(relation.header_differing_bytes, 1)
        self.assertTrue(relation.constant)
        self.assertEqual(relation.xor_value, 0x5B)

    def test_cli_reports_constant_xor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            left = self._write_bytes(Path(tmp) / "left.dat", b"H" * 0x40 + b"\x00\x01")
            right = self._write_bytes(Path(tmp) / "right.dat", b"H" * 0x40 + b"\x5b\x5a")

            result = self._run_tool(left, right)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Dominant payload XOR: 0x5b (2/2, 100.00%)", result.stdout)
            self.assertIn("Payload XOR relation: constant 0x5b", result.stdout)

    def test_cli_reports_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            left = self._write_bytes(Path(tmp) / "left.dat", b"H" * 0x40 + b"\x00\x01")
            right = self._write_bytes(Path(tmp) / "right.dat", b"H" * 0x40 + b"\x5b\x01")

            result = self._run_tool(left, right)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Dominant payload XOR: 0x5b (1/2, 50.00%)", result.stdout)
            self.assertIn("Payload XOR relation: not constant", result.stdout)
            self.assertIn("Mismatches relative to dominant XOR: 1", result.stdout)
            self.assertIn("0x00000041", result.stdout)

    def test_size_mismatch_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            left = self._write_bytes(Path(tmp) / "left.dat", b"H" * 0x40)
            right = self._write_bytes(Path(tmp) / "right.dat", b"H" * 0x41)

            result = self._run_tool(left, right)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("files must be the same size", result.stderr)

    def test_does_not_mutate_files(self) -> None:
        left_data = b"H" * 0x40 + b"\x00\x01"
        right_data = b"H" * 0x40 + b"\x5b\x5a"
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
