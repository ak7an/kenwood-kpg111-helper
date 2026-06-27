from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from kpg111.decoder import NAME_LENGTH, NUMERIC_LENGTH, TALK_GROUP_TABLE_START, decode_table
from tools.import_dvref_talkgroups import load_dvref_rows, normalize_name


FIXTURE = Path("research/dattest/Dattest/AK7AN_Travel.dat")
TOOL = Path("tools/import_dvref_talkgroups.py")
DECODE_KEY = 0x5B


class ImportDvrefTalkgroupsTests(unittest.TestCase):
    def test_load_dvref_rows_normalizes_sorts_and_dedupes_tg_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "nxdn-reflectors.csv"
            csv_path.write_text(
                "\n".join(
                    [
                        '"Reflector/TG Number","Name/Description","DMR2NXDN TG #"',
                        '"149","HS3TDI","7000149"',
                        '"11","HELLAS Zone Net!  By SA7SVR","7000011"',
                        '"149","DUPLICATE","7000149"',
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            rows = load_dvref_rows(csv_path)

            self.assertEqual([row.tg_id for row in rows], [11, 149])
            self.assertEqual(rows[0].name, "11 HELLAS ZONE")
            self.assertEqual(rows[1].name, "149 HS3TDI")

    def test_normalize_name_is_ascii_printable_and_14_chars(self) -> None:
        name = normalize_name(12345, "Café / Long reflector name!!!")

        self.assertLessEqual(len(name), NAME_LENGTH)
        self.assertEqual(name, "12345 CAFE / L")
        self.assertTrue(all(32 <= ord(char) <= 126 for char in name))

    def test_cli_imports_new_talk_groups_without_touching_other_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "nxdn-reflectors.csv"
            output = Path(tmp) / "AK7AN_Travel_DVREF.dat"
            csv_path.write_text(
                "\n".join(
                    [
                        '"Reflector/TG Number","Name/Description","DMR2NXDN TG #"',
                        '"111","Alpha Reflector","7000111"',
                        '"222","Beta Reflector","7000222"',
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    "--input",
                    str(csv_path),
                    "--baseline",
                    str(FIXTURE),
                    "--output",
                    str(output),
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("New talk groups: 2", result.stdout)
            original = FIXTURE.read_bytes()
            patched = output.read_bytes()
            changed_offsets = {index for index, (left, right) in enumerate(zip(original, patched)) if left != right}
            expected_offsets = set()
            for slot in (17, 18):
                offset = TALK_GROUP_TABLE_START + slot * 32
                expected_offsets.update(range(offset + 1, offset + 1 + NAME_LENGTH))
                expected_offsets.update(range(offset + 19, offset + 19 + NUMERIC_LENGTH))
            self.assertTrue(changed_offsets)
            self.assertLessEqual(changed_offsets, expected_offsets)

            records = decode_table(
                patched,
                "talk_groups",
                "Talk Groups",
                TALK_GROUP_TABLE_START,
                DECODE_KEY,
                include_empty=True,
                max_records=24,
            )
            by_id = {record.numeric_id: record.name for record in records if record.name}
            self.assertEqual(by_id[111], "111 ALPHA REFL")
            self.assertEqual(by_id[222], "222 BETA REFLE")


if __name__ == "__main__":
    unittest.main()
