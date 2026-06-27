from pathlib import Path
import tempfile
import unittest

from tools.frequency_dataset_analysis import (
    analyze_dataset,
    bit_transition_summary,
    hamming_distance,
    parse_frequency_from_filename,
    render_report,
    render_rx_step_analysis,
    write_csv,
)


class FrequencyDatasetAnalysisTests(unittest.TestCase):
    def test_parse_frequency_from_filename_uses_last_numeric_token(self) -> None:
        text, hz = parse_frequency_from_filename(Path("AK7AN_Channel_Line2_RXOnly_146520.dat"))

        self.assertEqual(text, "146.520")
        self.assertEqual(hz, 146_520_000)

    def test_analyze_dataset_normalizes_and_extracts_channel_two(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline = root / "Line2_RX_146000.dat"
            modified = root / "Line2_RX_146100.dat"
            baseline_data = bytearray(b"H" * 0x40 + b"\x00" * 0x80)
            channel2 = 0x40
            baseline_data[channel2 + 0x05 : channel2 + 0x08] = bytes.fromhex("10 20 30")
            baseline_data[channel2 + 0x09 : channel2 + 0x0c] = bytes.fromhex("40 50 60")
            baseline.write_bytes(bytes(baseline_data))

            modified_data = bytearray(
                byte ^ 0x5B if offset >= 0x40 else byte
                for offset, byte in enumerate(baseline_data)
            )
            modified_data[channel2 + 0x05 : channel2 + 0x08] = bytes(
                byte ^ 0x5B for byte in bytes.fromhex("11 22 33")
            )
            modified_data[channel2 + 0x09 : channel2 + 0x0c] = bytes(
                byte ^ 0x5B for byte in bytes.fromhex("44 55 66")
            )
            modified.write_bytes(bytes(modified_data))

            samples = analyze_dataset([baseline, modified], baseline_path=baseline, start=0, stride=0x40)

            self.assertEqual([sample.frequency_text for sample in samples], ["146.000", "146.100"])
            self.assertEqual(samples[0].xor_mask, 0x00)
            self.assertEqual(samples[1].xor_mask, 0x5B)
            self.assertEqual(samples[1].rx.raw, bytes.fromhex("11 22 33"))
            self.assertEqual(samples[1].tx.raw, bytes.fromhex("44 55 66"))
            self.assertEqual(samples[1].rx.big_endian, 0x112233)
            self.assertEqual(samples[1].rx.little_endian, 0x332211)
            self.assertEqual(samples[1].rx.ones_complement, bytes.fromhex("ee dd cc"))

    def test_write_csv_and_render_report_are_observational(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dat_file = root / "Line2_RX_146520.dat"
            data = bytearray(b"H" * 0x40 + b"\x00" * 0x80)
            data[0x45:0x48] = bytes.fromhex("81 f6 fa")
            data[0x49:0x4c] = bytes.fromhex("01 dc f4")
            dat_file.write_bytes(bytes(data))
            samples = analyze_dataset([dat_file], baseline_path=dat_file, start=0, stride=0x40)
            csv_path = root / "frequency_dataset.csv"

            write_csv(csv_path, samples)
            report = render_report(samples, dat_file, channel=2, start=0, stride=0x40)

            csv_text = csv_path.read_text(encoding="utf-8")
            header = csv_text.splitlines()[0].split(",")
            for column in ("frequency", "rx0", "rx1", "rx2", "tx0", "tx1", "tx2"):
                self.assertIn(column, header)
            self.assertIn("146.520", csv_text)
            self.assertIn("81 f6 fa", report)
            self.assertIn("No encoding formula determined.", report)

    def test_transition_helpers(self) -> None:
        self.assertEqual(hamming_distance(bytes.fromhex("00 ff 55"), bytes.fromhex("ff ff 50")), 10)
        self.assertEqual(
            bit_transition_summary(bytes.fromhex("00 01 03"), bytes.fromhex("01 03 02")),
            "byte0: 0; byte1: 1; byte2: 0",
        )

    def test_rx_step_analysis_uses_selected_dataset_samples_and_10khz_subset(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            samples = []
            for text, rx_hex in (
                ("146000", "c1 89 f2"),
                ("146500", "e1 28 fa"),
                ("146510", "f1 d1 fa"),
                ("146520", "81 f6 fa"),
                ("146530", "91 9f fa"),
            ):
                dat_file = root / f"Line2_RX_{text}.dat"
                data = bytearray(b"H" * 0x40 + b"\x00" * 0x80)
                data[0x45:0x48] = bytes.fromhex(rx_hex)
                data[0x49:0x4c] = bytes.fromhex("01 dc f4")
                dat_file.write_bytes(bytes(data))
                samples.append(dat_file)

            duplicate = root / "duplicate_Line2_RX_146520.dat"
            duplicate.write_bytes(samples[3].read_bytes())
            samples.append(duplicate)

            analyzed = analyze_dataset(samples, baseline_path=samples[0], start=0, stride=0x40)
            rendered = "\n".join(render_rx_step_analysis(analyzed))

            self.assertIn("| 146.000 |", rendered)
            self.assertIn("| 146.510 | +10 | f1 d1 fa | 10 f9 00 |", rendered)
            self.assertIn("### 10 kHz Samples", rendered)
            self.assertEqual(rendered.count("| 146.520 |"), 2)


if __name__ == "__main__":
    unittest.main()
