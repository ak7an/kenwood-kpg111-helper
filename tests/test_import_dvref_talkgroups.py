from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from kpg111.decoder import (
    NAME_LENGTH,
    NAME_START,
    NUMERIC_LENGTH,
    NUMERIC_START,
    RECORD_SIZE,
    TALK_GROUP_TABLE_START,
    decode_table,
)
from tools.import_dvref_talkgroups import load_dvref_rows, normalize_name


FIXTURE = Path("research/dattest/Dattest/AK7AN_Travel.dat")
TOOL = Path("tools/import_dvref_talkgroups.py")
DECODE_KEY = 0x5B


class ImportDvrefTalkgroupsTests(unittest.TestCase):
    def write_import_csv(self, csv_path: Path) -> None:
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
            self.assertEqual(rows[0].name, "HELLAS ZONE NE")
            self.assertEqual(rows[1].name, "HS3TDI")

    def test_normalize_name_is_ascii_printable_and_14_chars(self) -> None:
        name = normalize_name(12345, "Café / Long reflector name!!!")

        self.assertLessEqual(len(name), NAME_LENGTH)
        self.assertEqual(name, "CAFE / LONG RE")
        self.assertTrue(all(32 <= ord(char) <= 126 for char in name))

    def test_cli_imports_new_talk_groups_without_touching_other_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "nxdn-reflectors.csv"
            output = Path(tmp) / "AK7AN_Travel_DVREF.dat"
            self.write_import_csv(csv_path)

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
            self.assertEqual(by_id[111], "ALPHA REFLECTO")
            self.assertEqual(by_id[222], "BETA REFLECTOR")

    def test_cli_initializes_new_talk_group_from_existing_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "nxdn-reflectors.csv"
            baseline = Path(tmp) / "AK7AN_Travel_Template.dat"
            output = Path(tmp) / "AK7AN_Travel_DVREF.dat"
            self.write_import_csv(csv_path)

            data = bytearray(FIXTURE.read_bytes())
            template_offset = TALK_GROUP_TABLE_START
            data[template_offset + 16] = 0x12
            baseline.write_bytes(data)

            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    "--input",
                    str(csv_path),
                    "--baseline",
                    str(baseline),
                    "--output",
                    str(output),
                    "--talk-group-capacity",
                    "18",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            patched = output.read_bytes()
            new_record_offset = TALK_GROUP_TABLE_START + 17 * RECORD_SIZE
            self.assertEqual(patched[new_record_offset + 16], 0x12)
            name_offsets = set(range(NAME_START, NAME_START + NAME_LENGTH))
            id_offsets = set(range(NUMERIC_START, NUMERIC_START + NUMERIC_LENGTH))
            for relative_offset in range(RECORD_SIZE):
                if relative_offset in name_offsets or relative_offset in id_offsets:
                    continue
                self.assertEqual(
                    patched[new_record_offset + relative_offset],
                    patched[template_offset + relative_offset],
                )
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
            self.assertEqual(by_id[111], "ALPHA REFLECTO")

    def test_cli_uses_explicit_talk_group_capacity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "nxdn-reflectors.csv"
            output = Path(tmp) / "AK7AN_Travel_DVREF.dat"
            self.write_import_csv(csv_path)

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
                    "--talk-group-capacity",
                    "19",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Talk group capacity: 19", result.stdout)
            self.assertIn("New talk groups: 2", result.stdout)

    def test_cli_skips_new_talk_groups_when_explicit_capacity_is_full(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "nxdn-reflectors.csv"
            output = Path(tmp) / "AK7AN_Travel_DVREF.dat"
            self.write_import_csv(csv_path)

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
                    "--talk-group-capacity",
                    "18",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Talk group capacity: 18", result.stdout)
            self.assertIn("Imported: 1", result.stdout)
            self.assertIn("Skipped (table full): 1", result.stdout)
            self.assertIn("TG IDs skipped (table full): 222", result.stdout)
            self.assertTrue(output.exists())

            original = FIXTURE.read_bytes()
            patched = output.read_bytes()
            changed_offsets = {index for index, (left, right) in enumerate(zip(original, patched)) if left != right}
            expected_offsets = set()
            offset = TALK_GROUP_TABLE_START + 17 * 32
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
            self.assertEqual(by_id[111], "ALPHA REFLECTO")
            self.assertNotIn(222, by_id)

    def test_cli_applies_same_id_updates_when_explicit_capacity_is_full(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "nxdn-reflectors.csv"
            output = Path(tmp) / "AK7AN_Travel_DVREF.dat"
            csv_path.write_text(
                "\n".join(
                    [
                        '"Reflector/TG Number","Name/Description","DMR2NXDN TG #"',
                        '"43389","Lookout Mountain","7043389"',
                        '"111","Alpha Reflector","7000111"',
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
                    "--talk-group-capacity",
                    "17",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Empty slots: 0", result.stdout)
            self.assertIn("Imported: 0", result.stdout)
            self.assertIn("Updated: 1", result.stdout)
            self.assertIn("Skipped (table full): 1", result.stdout)
            self.assertIn("TG IDs skipped (table full): 111", result.stdout)

            original = FIXTURE.read_bytes()
            patched = output.read_bytes()
            changed_offsets = {index for index, (left, right) in enumerate(zip(original, patched)) if left != right}
            expected_offsets = set()
            offset = TALK_GROUP_TABLE_START + 15 * 32
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
            self.assertEqual(by_id[43389], "LOOKOUT MOUNTA")
            self.assertNotIn(111, by_id)

    def test_cli_replace_rebuilds_talk_group_table_from_slot_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "nxdn-reflectors.csv"
            baseline = Path(tmp) / "AK7AN_Travel_Template.dat"
            output = Path(tmp) / "AK7AN_Travel_DVREF.dat"
            self.write_import_csv(csv_path)

            data = bytearray(FIXTURE.read_bytes())
            template_offset = TALK_GROUP_TABLE_START
            data[template_offset + 16] = 0x12
            baseline.write_bytes(data)

            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    "--mode",
                    "replace",
                    "--input",
                    str(csv_path),
                    "--baseline",
                    str(baseline),
                    "--output",
                    str(output),
                    "--talk-group-capacity",
                    "4",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Mode: replace", result.stdout)
            self.assertIn("Imported: 2", result.stdout)
            self.assertIn("Skipped (table full): 0", result.stdout)

            original = baseline.read_bytes()
            patched = output.read_bytes()
            changed_offsets = {index for index, (left, right) in enumerate(zip(original, patched)) if left != right}
            allowed_offsets = set(
                range(TALK_GROUP_TABLE_START, TALK_GROUP_TABLE_START + 4 * RECORD_SIZE)
            )
            self.assertTrue(changed_offsets)
            self.assertLessEqual(changed_offsets, allowed_offsets)

            records = decode_table(
                patched,
                "talk_groups",
                "Talk Groups",
                TALK_GROUP_TABLE_START,
                DECODE_KEY,
                include_empty=True,
                max_records=6,
            )
            by_slot = {record.slot: record for record in records}
            self.assertEqual(by_slot[0].numeric_id, 111)
            self.assertEqual(by_slot[0].name, "ALPHA REFLECTO")
            self.assertEqual(by_slot[1].numeric_id, 222)
            self.assertEqual(by_slot[1].name, "BETA REFLECTOR")
            self.assertTrue(by_slot[2].empty)
            self.assertTrue(by_slot[3].empty)
            self.assertEqual(patched[TALK_GROUP_TABLE_START + 16], 0x12)
            self.assertEqual(patched[TALK_GROUP_TABLE_START + RECORD_SIZE + 16], 0x12)

    def test_cli_replace_reports_skipped_rows_beyond_capacity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "nxdn-reflectors.csv"
            output = Path(tmp) / "AK7AN_Travel_DVREF.dat"
            self.write_import_csv(csv_path)

            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    "--mode",
                    "replace",
                    "--input",
                    str(csv_path),
                    "--baseline",
                    str(FIXTURE),
                    "--output",
                    str(output),
                    "--talk-group-capacity",
                    "1",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Imported: 1", result.stdout)
            self.assertIn("Skipped (table full): 1", result.stdout)
            self.assertIn("TG IDs skipped (table full): 222", result.stdout)


if __name__ == "__main__":
    unittest.main()
