from pathlib import Path
import unittest

from kpg111 import Codeplug, IndividualIDChange, IndividualIDManager, WriterError
from kpg111.decoder import (
    INDIVIDUAL_ID_TABLE_START,
    NAME_LENGTH,
    NAME_START,
    NUMERIC_LENGTH,
    NUMERIC_START,
    RECORD_SIZE,
    decode_table,
)


FIXTURE = Path("data/normalized/dattest/Dattest/AK7AN_Travel.dat")
DECODE_KEY = 0x5B


class IndividualIDManagerTests(unittest.TestCase):
    def test_add_uses_first_empty_slot_and_preserves_unknown_bytes(self) -> None:
        original = FIXTURE.read_bytes()
        codeplug = Codeplug.load(FIXTURE)

        updated = IndividualIDManager(codeplug).add("NEW ID", 4242)

        self.assertIsNot(updated, codeplug)
        self.assertEqual(codeplug.to_bytes(), original)
        changed_offsets = self._changed_offsets(original, updated.to_bytes())
        slot_offset = INDIVIDUAL_ID_TABLE_START + 14 * RECORD_SIZE
        expected = set(range(slot_offset + NAME_START, slot_offset + NAME_START + NAME_LENGTH))
        expected.update(range(slot_offset + NUMERIC_START, slot_offset + NUMERIC_START + NUMERIC_LENGTH))
        self.assertTrue(changed_offsets)
        self.assertLessEqual(changed_offsets, expected)
        self.assertEqual(updated.changed_ranges[0].start, slot_offset + NAME_START)

        records = self._individual_ids(updated)
        by_id = {record.numeric_id: record for record in records if record.name}
        self.assertEqual(by_id[4242].slot, 14)
        self.assertEqual(by_id[4242].name, "NEW ID")

    def test_update_reuses_verified_codeplug_edit(self) -> None:
        original = FIXTURE.read_bytes()
        updated = IndividualIDManager(Codeplug.load(FIXTURE)).update(1, name="FRANK2")

        changed_offsets = self._changed_offsets(original, updated.to_bytes())
        slot_offset = INDIVIDUAL_ID_TABLE_START + RECORD_SIZE
        expected = set(range(slot_offset + NAME_START, slot_offset + NAME_START + NAME_LENGTH))
        self.assertTrue(changed_offsets)
        self.assertLessEqual(changed_offsets, expected)

    def test_merge_adds_new_records_and_updates_existing_id(self) -> None:
        codeplug = Codeplug.load(FIXTURE)
        updated = IndividualIDManager(codeplug).merge(
            [
                IndividualIDChange("FRANK2", 1571),
                IndividualIDChange("NEW ID", 4242),
            ]
        )

        records = self._individual_ids(updated)
        by_id = {record.numeric_id: record for record in records if record.name}
        self.assertEqual(by_id[1571].name, "FRANK2")
        self.assertEqual(by_id[4242].slot, 14)
        self.assertEqual(by_id[4242].name, "NEW ID")

    def test_replace_rejects_when_existing_records_would_need_delete(self) -> None:
        with self.assertRaisesRegex(WriterError, "would require delete support"):
            IndividualIDManager(Codeplug.load(FIXTURE)).replace([IndividualIDChange("FRANK2", 1571)])

    def test_delete_fails_closed_until_safe_clearing_is_supported(self) -> None:
        with self.assertRaisesRegex(WriterError, "delete is not write-supported"):
            IndividualIDManager(Codeplug.load(FIXTURE)).delete(1)

    def test_sort_fails_closed_without_mutating_codeplug(self) -> None:
        codeplug = Codeplug.load(FIXTURE)
        original = codeplug.to_bytes()

        with self.assertRaisesRegex(WriterError, "physical sort is not write-supported"):
            IndividualIDManager(codeplug).sort()

        self.assertEqual(codeplug.to_bytes(), original)

    def test_sort_rejects_unknown_key(self) -> None:
        codeplug = Codeplug.load(FIXTURE)

        with self.assertRaisesRegex(WriterError, "unsupported Individual ID sort key"):
            IndividualIDManager(codeplug).sort(key="slot")

        self.assertEqual(codeplug.to_bytes(), FIXTURE.read_bytes())

    def test_sort_noops_when_records_are_already_ordered_by_name(self) -> None:
        codeplug = Codeplug.load(FIXTURE)
        manager = IndividualIDManager(codeplug)
        if [record.name for record in manager.records()] != sorted(record.name for record in manager.records()):
            self.skipTest("fixture is not name-sorted")
        self.assertIs(manager.sort(key="name"), codeplug)

    @staticmethod
    def _changed_offsets(original: bytes, candidate: bytes) -> set[int]:
        return {
            offset
            for offset, (left, right) in enumerate(zip(original, candidate))
            if left != right
        }

    @staticmethod
    def _individual_ids(codeplug: Codeplug):
        return decode_table(
            codeplug.to_bytes(),
            "individual_ids",
            "Individual IDs",
            INDIVIDUAL_ID_TABLE_START,
            DECODE_KEY,
            include_empty=True,
            max_records=40,
        )


if __name__ == "__main__":
    unittest.main()
