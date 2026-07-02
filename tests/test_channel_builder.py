from pathlib import Path
import unittest

from kpg111 import Codeplug
from openkpg.channel_builder import ChannelBuilder, ChannelDefinition
from openkpg.csv_import import ImportedChannel


FIXTURE = Path("data/normalized/dattest/Dattest/AK7AN_Travel.dat")


class ChannelBuilderTests(unittest.TestCase):
    def test_builds_analog_simplex_channel_without_mutating_codeplug(self) -> None:
        codeplug = Codeplug.load(FIXTURE)
        original = codeplug.to_bytes()
        imported = ImportedChannel(
            name="Simplex",
            rx_frequency="146.520",
            mode="FM",
            tone="100.0",
            zone="Local",
            source="channels.csv",
            source_row=2,
        )

        plan = ChannelBuilder(codeplug).build([imported])

        self.assertIs(plan.codeplug, codeplug)
        self.assertEqual(codeplug.to_bytes(), original)
        self.assertEqual(plan.accepted_count, 1)
        self.assertEqual(plan.rejected_count, 0)
        channel = plan.channels[0]
        self.assertIsInstance(channel, ChannelDefinition)
        self.assertEqual(channel.name, "Simplex")
        self.assertEqual(channel.rx_frequency, "146.520")
        self.assertEqual(channel.tx_frequency, "146.520")
        self.assertEqual(channel.mode, "FM")
        self.assertEqual(channel.channel_type, "analog")
        self.assertEqual(channel.operation, "simplex")
        self.assertEqual(channel.tone, "100.0")
        self.assertEqual(channel.zone, "Local")

    def test_builds_repeater_channel_from_offset(self) -> None:
        imported = ImportedChannel(
            name="UHF Repeater",
            rx_frequency="449.500",
            offset="-5.000",
            mode="analog",
        )

        plan = ChannelBuilder(Codeplug.load(FIXTURE)).build([imported])

        self.assertEqual(plan.accepted_count, 1)
        channel = plan.channels[0]
        self.assertEqual(channel.tx_frequency, "444.500")
        self.assertEqual(channel.operation, "repeater")
        self.assertEqual(channel.mode, "FM")

    def test_tx_frequency_takes_precedence_over_offset(self) -> None:
        imported = ImportedChannel(
            name="Explicit TX",
            rx_frequency="146.940",
            tx_frequency="146.340",
            offset="-0.600",
            mode="FM",
        )

        channel = ChannelBuilder(Codeplug.load(FIXTURE)).build([imported]).channels[0]

        self.assertEqual(channel.tx_frequency, "146.340")
        self.assertEqual(channel.operation, "repeater")

    def test_builds_nxdn_channel_and_preserves_optional_future_fields(self) -> None:
        imported = ImportedChannel(
            name="NXDN Site",
            rx_frequency="453.100",
            tx_frequency="458.100",
            mode="NXDN",
            ran="12",
            color_code="3",
            nac="293",
            callsign="W0NXD",
        )

        channel = ChannelBuilder(Codeplug.load(FIXTURE)).build([imported]).channels[0]

        self.assertEqual(channel.mode, "NXDN")
        self.assertEqual(channel.channel_type, "nxdn")
        self.assertEqual(channel.operation, "repeater")
        self.assertEqual(channel.ran, "12")
        self.assertEqual(channel.color_code, "3")
        self.assertEqual(channel.nac, "293")
        self.assertEqual(channel.callsign, "W0NXD")

    def test_invalid_rows_are_rejected_with_reasons(self) -> None:
        imports = [
            ImportedChannel(name="", rx_frequency="146.520"),
            ImportedChannel(name="Bad RX", rx_frequency="not-a-frequency"),
            ImportedChannel(name="Bad Mode", rx_frequency="146.520", mode="DMR"),
            ImportedChannel(name="Valid", rx_frequency="446.000"),
        ]

        plan = ChannelBuilder(Codeplug.load(FIXTURE)).build(imports)

        self.assertEqual(plan.accepted_count, 1)
        self.assertEqual(plan.channels[0].name, "Valid")
        self.assertEqual(plan.rejected_count, 3)
        self.assertIn("name is required", plan.rejected[0].reason)
        self.assertIn("rx_frequency is not a valid frequency", plan.rejected[1].reason)
        self.assertIn("unsupported channel mode", plan.rejected[2].reason)

    def test_bad_offset_rejects_row(self) -> None:
        imported = ImportedChannel(name="Bad Offset", rx_frequency="146.520", offset="minus")

        plan = ChannelBuilder(Codeplug.load(FIXTURE)).build([imported])

        self.assertEqual(plan.accepted_count, 0)
        self.assertEqual(plan.rejected_count, 1)
        self.assertIn("offset is not a valid frequency offset", plan.rejected[0].reason)


if __name__ == "__main__":
    unittest.main()
