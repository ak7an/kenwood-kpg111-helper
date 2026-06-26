import unittest

from openkpg.dat.frequency import (
    DEFAULT_FREQUENCY_CANDIDATES,
    decode_frequency_low24,
    encode_frequency_hz,
    format_frequency_mhz,
    reconstruct_frequency,
)


VERIFIED_SAMPLES = (
    (145_675_000, "b9 93 ef"),
    (146_000_000, "c1 89 f2"),
    (146_100_000, "61 0e f4"),
    (146_120_000, "01 dc f4"),
    (146_200_000, "81 94 f7"),
    (146_300_000, "21 1d f9"),
    (146_400_000, "41 a2 f8"),
    (146_500_000, "e1 28 fa"),
    (146_510_000, "f1 d1 fa"),
    (146_520_000, "81 f6 fa"),
    (146_530_000, "91 9f fa"),
    (146_600_000, "01 b1 fd"),
    (146_700_000, "a1 37 ff"),
    (146_720_000, "41 84 ff"),
    (146_800_000, "c1 bc fe"),
    (146_900_000, "61 c5 80"),
    (147_000_000, "81 4b 82"),
)


class FrequencyEncodingTests(unittest.TestCase):
    def test_encode_frequency_hz_matches_verified_samples(self) -> None:
        for hz, raw_hex in VERIFIED_SAMPLES:
            with self.subTest(hz=hz):
                self.assertEqual(encode_frequency_hz(hz), bytes.fromhex(raw_hex))

    def test_decode_frequency_low24_returns_low_24_bits_for_verified_samples(self) -> None:
        for hz, raw_hex in VERIFIED_SAMPLES:
            with self.subTest(hz=hz):
                self.assertEqual(decode_frequency_low24(bytes.fromhex(raw_hex)), hz & 0xFFFFFF)

    def test_decode_reconstruct_display_for_verified_samples(self) -> None:
        for hz, raw_hex in VERIFIED_SAMPLES:
            with self.subTest(hz=hz):
                low24 = decode_frequency_low24(bytes.fromhex(raw_hex))
                reconstructed = reconstruct_frequency(low24, ((144_000_000, 148_000_000),))

                self.assertEqual(reconstructed, hz)
                self.assertTrue(format_frequency_mhz(reconstructed).startswith("14"))

    def test_reconstruct_frequency_returns_none_for_ambiguous_broad_bands(self) -> None:
        low24 = decode_frequency_low24(bytes.fromhex("81 f6 fa"))

        self.assertIsNone(reconstruct_frequency(low24, DEFAULT_FREQUENCY_CANDIDATES))

    def test_reconstruct_frequency_returns_none_for_no_candidate_match(self) -> None:
        self.assertIsNone(reconstruct_frequency(0x123456, ((144_000_000, 148_000_000),)))

    def test_encode_masks_to_low_24_bits(self) -> None:
        self.assertEqual(encode_frequency_hz(0x1123456), encode_frequency_hz(0x123456))

    def test_decode_rejects_wrong_length(self) -> None:
        with self.assertRaises(ValueError):
            decode_frequency_low24(b"\x00\x01")
        with self.assertRaises(ValueError):
            decode_frequency_low24(b"\x00\x01\x02\x03")

    def test_encode_rejects_negative_frequency(self) -> None:
        with self.assertRaises(ValueError):
            encode_frequency_hz(-1)

    def test_encode_rejects_non_int_frequency(self) -> None:
        with self.assertRaises(TypeError):
            encode_frequency_hz(146.52)  # type: ignore[arg-type]

    def test_format_frequency_mhz(self) -> None:
        self.assertEqual(format_frequency_mhz(146_000_000), "146.000")
        self.assertEqual(format_frequency_mhz(146_520_000), "146.520")
        self.assertEqual(format_frequency_mhz(146_512_500), "146.5125")

    def test_kpg111_compatibility_aliases(self) -> None:
        from kpg111.frequency import decode_frequency_bytes, decode_frequency_low24 as compat_low24

        raw = bytes.fromhex("81 f6 fa")
        self.assertEqual(decode_frequency_bytes(raw), decode_frequency_low24(raw))
        self.assertEqual(compat_low24(raw), decode_frequency_low24(raw))


if __name__ == "__main__":
    unittest.main()
