from pathlib import Path
import unittest

from kpg111.record_spec import record_spec


ROOTS = [
    Path("data/normalized/dattest"),
    Path("data/normalized/dattest2"),
    Path("data/normalized/dattest3"),
    Path("data/normalized/dattest4"),
]


class RecordSpecificationTests(unittest.TestCase):
    def test_record_summary_counts_known_bytes_conservatively(self) -> None:
        spec = record_spec(ROOTS)

        self.assertEqual(spec.talk_group.record_size, 32)
        self.assertEqual(spec.individual_id.record_size, 32)
        self.assertEqual(spec.talk_group.known_bytes, 16)
        self.assertEqual(spec.individual_id.known_bytes, 16)
        self.assertEqual(spec.talk_group.unknown_bytes, 16)
        self.assertEqual(spec.individual_id.unknown_bytes, 16)

    def test_unknown_bytes_remain_reserved_candidates(self) -> None:
        spec = record_spec(ROOTS)
        unknown_offsets = {
            byte.offset
            for byte in spec.talk_group.bytes
            if byte.meaning.startswith("UNKNOWN")
        }

        self.assertIn(0, unknown_offsets)
        self.assertIn(15, unknown_offsets)
        self.assertIn(31, unknown_offsets)
        self.assertNotIn(1, unknown_offsets)
        self.assertNotIn(19, unknown_offsets)


if __name__ == "__main__":
    unittest.main()
