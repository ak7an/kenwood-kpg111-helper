from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.dat_payload_runs import find_byte_runs, first_non_long_filler_offset, filtered_runs


TOOL = Path("tools/dat_payload_runs.py")


class DatPayloadRunsTests(unittest.TestCase):
    def test_simple_artificial_payload_with_repeated_runs(self) -> None:
        data = b"H" * 0x40 + b"\xaa" * 16 + b"\x01\x02" + b"\xbb" * 20

        runs = filtered_runs(data, min_run=16)

        self.assertEqual(
            [(run.start, run.end, run.length, run.value) for run in runs],
            [(0x40, 0x4F, 16, 0xAA), (0x52, 0x65, 20, 0xBB)],
        )
        self.assertEqual(first_non_long_filler_offset(data, min_run=16), 0x50)

    def test_min_run_filtering(self) -> None:
        data = b"H" * 0x40 + b"\xaa" * 8 + b"\xbb" * 16

        self.assertEqual([(run.length, run.value) for run in filtered_runs(data, 16)], [(16, 0xBB)])
        self.assertEqual(
            [(run.length, run.value) for run in find_byte_runs(data)],
            [(8, 0xAA), (16, 0xBB)],
        )

    def test_multiple_file_support(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = self._write_bytes(Path(tmp) / "first.dat", b"H" * 0x40 + b"\xaa" * 16)
            second = self._write_bytes(Path(tmp) / "second.dat", b"H" * 0x40 + b"\xbb" * 16)

            result = self._run_tool(first, second)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(f"## `{first}`", result.stdout)
            self.assertIn(f"## `{second}`", result.stdout)
            self.assertIn("0xaa", result.stdout)
            self.assertIn("0xbb", result.stdout)

    def test_no_mutation_of_input_files(self) -> None:
        original = b"H" * 0x40 + b"\xaa" * 16 + b"\x01\x02"
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_bytes(Path(tmp) / "input.dat", original)

            result = self._run_tool(path)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(path.read_bytes(), original)

    @staticmethod
    def _write_bytes(path: Path, data: bytes) -> Path:
        path.write_bytes(data)
        return path

    @staticmethod
    def _run_tool(*paths: Path, extra_args: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        args = [sys.executable, str(TOOL), *(str(path) for path in paths)]
        if extra_args:
            args.extend(extra_args)
        return subprocess.run(
            args,
            check=False,
            text=True,
            capture_output=True,
        )


if __name__ == "__main__":
    unittest.main()
