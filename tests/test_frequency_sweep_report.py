from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.frequency_sweep_report import (
    CHANNEL_TABLE_START,
    analyze_sweep,
    parse_frequency_from_filename,
    render_report,
)


TOOL = Path("tools/frequency_sweep_report.py")


class FrequencySweepReportTests(unittest.TestCase):
    def test_parse_frequency_uses_last_numeric_token(self) -> None:
        text, hz = parse_frequency_from_filename(Path("Line2_RX_146400.dat"))

        self.assertEqual(text, "146.400")
        self.assertEqual(hz, 146_400_000)

    def test_parse_decimal_frequency(self) -> None:
        text, hz = parse_frequency_from_filename(Path("Line2_RX_146.5125.dat"))

        self.assertEqual(text, "146.5125")
        self.assertEqual(hz, 146_512_500)

    def test_analyze_sweep_normalizes_payload_and_extracts_channel_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline = root / "baseline.dat"
            first = root / "Line2_RX_146000.dat"
            second = root / "Line2_RX_146100.dat"

            baseline_data = bytearray(b"H" * CHANNEL_TABLE_START + b"\x00" * 0x80)
            channel2 = CHANNEL_TABLE_START + 0x40
            baseline_data[channel2 + 0x05 : channel2 + 0x08] = bytes.fromhex("10 20 30")
            baseline_data[channel2 + 0x09 : channel2 + 0x0c] = bytes.fromhex("40 50 60")
            baseline.write_bytes(bytes(baseline_data))

            first_data = bytearray(byte ^ 0x5B if offset >= 0x40 else byte for offset, byte in enumerate(baseline_data))
            first_data[channel2 + 0x05 : channel2 + 0x08] = bytes(
                byte ^ 0x5B for byte in bytes.fromhex("11 20 30")
            )
            first.write_bytes(bytes(first_data))

            second_data = bytearray(byte ^ 0x5B if offset >= 0x40 else byte for offset, byte in enumerate(baseline_data))
            second_data[channel2 + 0x05 : channel2 + 0x08] = bytes(
                byte ^ 0x5B for byte in bytes.fromhex("21 22 30")
            )
            second_data[channel2 + 0x09 : channel2 + 0x0c] = bytes(
                byte ^ 0x5B for byte in bytes.fromhex("40 51 60")
            )
            second.write_bytes(bytes(second_data))

            samples = analyze_sweep(baseline, [second, first])

            self.assertEqual([sample.frequency_text for sample in samples], ["146.000", "146.100"])
            self.assertEqual(samples[0].xor_mask, 0x5B)
            self.assertEqual(samples[0].rx_bytes, bytes.fromhex("11 20 30"))
            self.assertEqual(samples[0].tx_bytes, bytes.fromhex("40 50 60"))
            self.assertEqual(samples[1].rx_bytes, bytes.fromhex("21 22 30"))
            self.assertEqual(samples[1].tx_bytes, bytes.fromhex("40 51 60"))

            report = render_report(baseline, samples)
            self.assertIn("| 146.000 | 11 20 30 | 40 50 60 |  |  |", report)
            self.assertIn("| 146.100 | 21 22 30 | 40 51 60 | 30 02 00 | 00 01 00 |", report)
            self.assertIn("| byte0 | start, +16 | start, +0 |", report)
            self.assertIn("- byte2: values 0x30, 0x30; deltas +0; constant yes", report)

    def test_cli_is_read_only_and_reports_no_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            baseline = Path(tmp) / "baseline.dat"
            baseline.write_bytes(b"H" * 0x40)

            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    "--baseline",
                    str(baseline),
                    "--input-glob",
                    str(Path(tmp) / "Line2_RX_*.dat"),
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no input DAT files matched", result.stderr)
            self.assertEqual(baseline.read_bytes(), b"H" * 0x40)


if __name__ == "__main__":
    unittest.main()
