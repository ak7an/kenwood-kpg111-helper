from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TOOL = Path("tools/channel_record_dump.py")


class ChannelRecordDumpTests(unittest.TestCase):
    def test_xor_mask_outputs_raw_and_normalized_fields(self) -> None:
        data = bytes(range(0x40))
        with tempfile.TemporaryDirectory() as tmp:
            dat_file = self._write_bytes(Path(tmp) / "sample.dat", data)

            result = self._run_tool(dat_file, "--start", "0", "--count", "1", "--xor-mask", "0xff")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("XOR mask: 0xff", result.stdout)
            self.assertIn("Raw bytes:", result.stdout)
            self.assertIn("Normalized bytes:", result.stdout)
            self.assertIn("  ff fe fd fc fb fa f9 f8 f7 f6 f5 f4 f3 f2 f1 f0", result.stdout)
            self.assertIn(
                "RX frequency bytes (+0x05, length 3): raw 05 06 07; normalized fa f9 f8",
                result.stdout,
            )
            self.assertIn(
                "TX frequency bytes (+0x09, length 3): raw 09 0a 0b; normalized f6 f5 f4",
                result.stdout,
            )
            self.assertIn("ASCII-safe raw:", result.stdout)
            self.assertIn("ASCII-safe normalized:", result.stdout)
            self.assertEqual(dat_file.read_bytes(), data)

    def test_without_xor_mask_keeps_original_output_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dat_file = self._write_bytes(Path(tmp) / "sample.dat", bytes(range(0x40)))

            result = self._run_tool(dat_file, "--start", "0", "--count", "1")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("RX frequency bytes (+0x05, length 3): 05 06 07", result.stdout)
            self.assertNotIn("Normalized bytes:", result.stdout)

    def test_invalid_xor_mask_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dat_file = self._write_bytes(Path(tmp) / "sample.dat", bytes(range(0x40)))

            result = self._run_tool(dat_file, "--start", "0", "--count", "1", "--xor-mask", "0x100")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--xor-mask must be between 0x00 and 0xff", result.stderr)

    @staticmethod
    def _write_bytes(path: Path, data: bytes) -> Path:
        path.write_bytes(data)
        return path

    @staticmethod
    def _run_tool(dat_file: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(TOOL),
                str(dat_file),
                *args,
            ],
            check=False,
            text=True,
            capture_output=True,
        )


if __name__ == "__main__":
    unittest.main()
