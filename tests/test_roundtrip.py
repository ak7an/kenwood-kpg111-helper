from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from kpg111.project import KPG111Project
from tools.dat_roundtrip_check import first_difference


FIXTURE = Path("data/normalized/dattest/Dattest/AK7AN_Travel.dat")
TOOL = Path("tools/dat_roundtrip_check.py")


class RoundTripTests(unittest.TestCase):
    def test_project_to_bytes_preserves_input(self) -> None:
        original = FIXTURE.read_bytes()
        project = KPG111Project().load_program(FIXTURE, 0x5B)

        self.assertEqual(project.to_bytes(), original)

    def test_project_write_bytes_preserves_input(self) -> None:
        original = FIXTURE.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "roundtrip.dat"
            KPG111Project().load_program(FIXTURE, 0x5B).write_bytes(output)

            self.assertEqual(output.read_bytes(), original)

    def test_roundtrip_tool_passes_for_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "roundtrip.dat"
            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    str(FIXTURE),
                    "--decode-key",
                    "0x5b",
                    "--output",
                    str(output),
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS", result.stdout)
            self.assertEqual(output.read_bytes(), FIXTURE.read_bytes())

    def test_first_difference_reports_size_boundary(self) -> None:
        self.assertEqual(first_difference(b"abc", b"abd"), 2)
        self.assertEqual(first_difference(b"abc", b"abcd"), 3)
        self.assertIsNone(first_difference(b"abc", b"abc"))


if __name__ == "__main__":
    unittest.main()
