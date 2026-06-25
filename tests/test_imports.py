from pathlib import Path
import unittest

from kpg111.imports import load_import_csv


def write_tmp(name: str, content: str) -> Path:
    path = Path("/tmp") / name
    path.write_text(content, encoding="utf-8")
    return path


class ImportTests(unittest.TestCase):
    def test_valid_csv_loads_records(self) -> None:
        path = write_tmp(
            "kpg111_test_valid.csv",
            "type,name,id\nTG,Parrot,10\nINDIVIDUAL,Curtis AE4BT,16042\n",
        )
        records = load_import_csv(path)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].record_type, "talk_groups")
        self.assertEqual(records[0].name, "Parrot")
        self.assertEqual(records[0].numeric_id, 10)
        self.assertEqual(records[1].record_type, "individual_ids")

    def test_invalid_type_raises(self) -> None:
        path = write_tmp("kpg111_test_bad_type.csv", "type,name,id\nZONE,Test,1\n")
        with self.assertRaises(ValueError):
            load_import_csv(path)

    def test_blank_name_raises(self) -> None:
        path = write_tmp("kpg111_test_blank_name.csv", "type,name,id\nTG,,1\n")
        with self.assertRaises(ValueError):
            load_import_csv(path)

    def test_bad_id_raises(self) -> None:
        path = write_tmp("kpg111_test_bad_id.csv", "type,name,id\nTG,Test,abc\n")
        with self.assertRaises(ValueError):
            load_import_csv(path)


if __name__ == "__main__":
    unittest.main()
