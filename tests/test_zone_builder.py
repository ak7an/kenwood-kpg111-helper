from pathlib import Path
import unittest

from kpg111 import Codeplug
from openkpg.channel_builder import ChannelDefinition
from openkpg.zone_builder import DEFAULT_ZONE_NAME, ZoneBuilder, ZoneDefinition


FIXTURE = Path("data/normalized/dattest/Dattest/AK7AN_Travel.dat")


def channel(name: str, zone: str | None = None, row: int = 2) -> ChannelDefinition:
    return ChannelDefinition(
        name=name,
        rx_frequency="146.520",
        tx_frequency="146.520",
        mode="FM",
        channel_type="analog",
        operation="simplex",
        zone=zone,
        source="channels.csv",
        source_row=row,
    )


class ZoneBuilderTests(unittest.TestCase):
    def test_groups_channels_by_zone_and_preserves_zone_order(self) -> None:
        plan = ZoneBuilder().build(
            [
                channel("A", "North", 2),
                channel("B", "South", 3),
                channel("C", "North", 4),
            ]
        )

        self.assertEqual(plan.rejected_count, 0)
        self.assertEqual([zone.name for zone in plan.zones], ["North", "South"])
        self.assertEqual([item.name for item in plan.zones[0].channels], ["A", "C"])
        self.assertEqual([item.name for item in plan.zones[1].channels], ["B"])

    def test_default_zone_handles_missing_and_blank_zone_names(self) -> None:
        plan = ZoneBuilder().build([channel("A"), channel("B", "  ")])

        self.assertEqual(len(plan.zones), 1)
        self.assertEqual(plan.zones[0].name, DEFAULT_ZONE_NAME)
        self.assertEqual([item.name for item in plan.zones[0].channels], ["A", "B"])

    def test_preserves_channel_order_within_each_zone(self) -> None:
        plan = ZoneBuilder().build(
            [
                channel("First", "Local"),
                channel("Second", "Local"),
                channel("Third", "Local"),
            ]
        )

        self.assertEqual([item.name for item in plan.zones[0].channels], ["First", "Second", "Third"])

    def test_duplicate_channel_names_rejected_only_within_same_zone(self) -> None:
        plan = ZoneBuilder().build(
            [
                channel("Shared", "North", 2),
                channel("Shared", "South", 3),
                channel("shared", "North", 4),
            ]
        )

        self.assertEqual(plan.accepted_count, 2)
        self.assertEqual(plan.rejected_count, 1)
        self.assertEqual([zone.name for zone in plan.zones], ["North", "South"])
        self.assertEqual(plan.rejected[0].source_row, 4)
        self.assertIn("duplicate channel name", plan.rejected[0].reason)

    def test_rejects_blank_channel_names_with_report_context(self) -> None:
        plan = ZoneBuilder().build([channel(" ", "Local", 9), channel("Valid", "Local", 10)])

        self.assertEqual(plan.accepted_count, 1)
        self.assertEqual(plan.rejected_count, 1)
        self.assertEqual(plan.rejected[0].source, "channels.csv")
        self.assertEqual(plan.rejected[0].source_row, 9)
        self.assertEqual(plan.rejected[0].zone, "Local")
        self.assertIn("channel name is required", plan.rejected[0].reason)

    def test_zone_builder_does_not_modify_codeplug_bytes(self) -> None:
        codeplug = Codeplug.load(FIXTURE)
        original = codeplug.to_bytes()

        plan = ZoneBuilder().build([channel("A", "Local")])

        self.assertIsInstance(plan.zones[0], ZoneDefinition)
        self.assertEqual(codeplug.to_bytes(), original)

    def test_blank_default_zone_name_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ZoneBuilder(default_zone=" ")


if __name__ == "__main__":
    unittest.main()
