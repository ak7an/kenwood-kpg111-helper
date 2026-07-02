from pathlib import Path
import unittest

from kpg111 import Codeplug, TalkGroupChange, TalkGroupManager, WriterError
from kpg111.decoder import (
    NAME_LENGTH,
    NAME_START,
    NUMERIC_LENGTH,
    NUMERIC_START,
    RECORD_SIZE,
    TALK_GROUP_TABLE_START,
    decode_table,
)


FIXTURE = Path("data/normalized/dattest/Dattest/AK7AN_Travel.dat")
DECODE_KEY = 0x5B


class TalkGroupManagerTests(unittest.TestCase):
    def test_add_uses_safe_empty_slot_and_preserves_unknown_bytes(self) -> None:
        original = FIXTURE.read_bytes()
        codeplug = Codeplug.load(FIXTURE)

        updated = TalkGroupManager(codeplug).add("NEW TG", 4242)

        self.assertIsNot(updated, codeplug)
        self.assertEqual(codeplug.to_bytes(), original)
        changed_offsets = self._changed_offsets(original, updated.to_bytes())
        slot_offset = TALK_GROUP_TABLE_START + 200 * RECORD_SIZE
        expected = set(range(slot_offset + NAME_START, slot_offset + NAME_START + NAME_LENGTH))
        expected.update(range(slot_offset + NUMERIC_START, slot_offset + NUMERIC_START + NUMERIC_LENGTH))
        self.assertTrue(changed_offsets)
        self.assertLessEqual(changed_offsets, expected)
        self.assertEqual(updated.changed_ranges[0].start, slot_offset + NAME_START)

        records = self._talk_groups(updated)
        by_id = {record.numeric_id: record for record in records if record.name}
        self.assertEqual(by_id[4242].slot, 200)
        self.assertEqual(by_id[4242].name, "NEW TG")

    def test_update_reuses_verified_codeplug_edit(self) -> None:
        original = FIXTURE.read_bytes()
        updated = TalkGroupManager(Codeplug.load(FIXTURE)).update(1, name="PARROT2")

        changed_offsets = self._changed_offsets(original, updated.to_bytes())
        slot_offset = TALK_GROUP_TABLE_START + RECORD_SIZE
        expected = set(range(slot_offset + NAME_START, slot_offset + NAME_START + NAME_LENGTH))
        self.assertTrue(changed_offsets)
        self.assertLessEqual(changed_offsets, expected)

    def test_merge_adds_new_records_and_updates_existing_id(self) -> None:
        codeplug = Codeplug.load(FIXTURE)
        updated = TalkGroupManager(codeplug).merge(
            [
                TalkGroupChange("PARROT2", 10),
                TalkGroupChange("NEW TG", 4242),
            ]
        )

        records = self._talk_groups(updated)
        by_id = {record.numeric_id: record for record in records if record.name}
        self.assertEqual(by_id[10].name, "PARROT2")
        self.assertEqual(by_id[4242].slot, 200)
        self.assertEqual(by_id[4242].name, "NEW TG")

    def test_replace_rejects_when_existing_records_would_need_delete(self) -> None:
        with self.assertRaisesRegex(WriterError, "would require delete support"):
            TalkGroupManager(Codeplug.load(FIXTURE)).replace([TalkGroupChange("PARROT2", 10)])

    def test_delete_fails_closed_until_safe_clearing_is_supported(self) -> None:
        with self.assertRaisesRegex(WriterError, "delete is not write-supported"):
            TalkGroupManager(Codeplug.load(FIXTURE)).delete(1)

    def test_sort_fails_closed_without_mutating_codeplug(self) -> None:
        codeplug = Codeplug.load(FIXTURE)
        original = codeplug.to_bytes()

        with self.assertRaisesRegex(WriterError, "physical sort is not write-supported"):
            TalkGroupManager(codeplug).sort()

        self.assertEqual(codeplug.to_bytes(), original)

    def test_sort_rejects_unknown_key(self) -> None:
        codeplug = Codeplug.load(FIXTURE)

        with self.assertRaisesRegex(WriterError, "unsupported Talk Group sort key"):
            TalkGroupManager(codeplug).sort(key="slot")

        self.assertEqual(codeplug.to_bytes(), FIXTURE.read_bytes())

    def test_sort_noops_when_records_are_already_ordered_by_name(self) -> None:
        codeplug = Codeplug.load(FIXTURE)
        manager = TalkGroupManager(codeplug)
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
    def _talk_groups(codeplug: Codeplug):
        return decode_table(
            codeplug.to_bytes(),
            "talk_groups",
            "Talk Groups",
            TALK_GROUP_TABLE_START,
            DECODE_KEY,
            include_empty=True,
            max_records=400,
        )


if __name__ == "__main__":
    unittest.main()
