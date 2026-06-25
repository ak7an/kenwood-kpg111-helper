from pathlib import Path
import unittest

from kpg111.decoder import decode_program_tables


FIXTURE = Path("research/dattest/Dattest/AK7AN_Travel.dat")


class DecoderTests(unittest.TestCase):
    def test_decodes_first_individual_id(self) -> None:
        tables = decode_program_tables(FIXTURE, 0x5B)
        first = tables.individual_ids[0]
        self.assertEqual(first.name, "Curtis, AE4BT")
        self.assertEqual(first.numeric_id, 16042)

    def test_decodes_talk_group_parrot(self) -> None:
        tables = decode_program_tables(FIXTURE, 0x5B)
        parrot = next(record for record in tables.talk_groups if record.name == "Parrot")
        self.assertEqual(parrot.numeric_id, 10)


if __name__ == "__main__":
    unittest.main()
