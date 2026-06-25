import unittest

from tools.dat_channel_analysis import analyze_candidates
from tools.dat_channel_analysis import bcd_value, feature_hints, looks_like_frequency


class ChannelAnalysisTests(unittest.TestCase):
    def test_frequency_helpers_are_conservative(self) -> None:
        self.assertTrue(looks_like_frequency(146_520_000))
        self.assertFalse(looks_like_frequency(1234))
        self.assertFalse(looks_like_frequency(1_234_567))

    def test_bcd_value_decodes_low_nibble_first(self) -> None:
        self.assertEqual(bcd_value(bytes([0x21, 0x43])), 1234)
        self.assertIsNone(bcd_value(bytes([0x2A])))

    def test_feature_hints_find_literal_terms(self) -> None:
        hints = feature_hints(("Analog Wide",), ("High Power", "RAN"))
        self.assertIn("WIDE", hints)
        self.assertIn("POWER", hints)
        self.assertIn("HIGH", hints)
        self.assertIn("RAN", hints)

    def test_candidate_analysis_does_not_claim_high_confidence(self) -> None:
        data = bytearray(b"\x5b" * 512)
        data[0x40 : 0x40 + 14] = bytes(byte ^ 0x5B for byte in b"CALL CHANNEL\x00\x00")
        candidates = analyze_candidates(bytes(data), 0x5B, top=5)

        self.assertTrue(candidates)
        self.assertNotIn("HIGH", {candidate.confidence for candidate in candidates})


if __name__ == "__main__":
    unittest.main()
