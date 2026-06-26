import unittest

from tools.frequency_transform_search import (
    FrequencySample,
    bit_reverse_byte,
    gray_decode,
    gray_encode,
    nibble_swap_byte,
    parse_frequency_hz,
    rotate_left,
    rotate_right,
    search_transforms,
    verified_samples,
)


class FrequencyTransformSearchTests(unittest.TestCase):
    def test_bit_reverse(self) -> None:
        self.assertEqual(bit_reverse_byte(0b00010010), 0b01001000)
        self.assertEqual(bit_reverse_byte(0x80), 0x01)
        self.assertEqual(bit_reverse_byte(0x00), 0x00)

    def test_nibble_swap(self) -> None:
        self.assertEqual(nibble_swap_byte(0xAB), 0xBA)
        self.assertEqual(nibble_swap_byte(0x01), 0x10)
        self.assertEqual(nibble_swap_byte(0xF0), 0x0F)

    def test_gray_encode_decode(self) -> None:
        for value in (0, 1, 2, 3, 0x123456, 0xFFFFFF):
            encoded = gray_encode(value)

            self.assertEqual(gray_decode(encoded), value & 0xFFFFFF)

    def test_rotate(self) -> None:
        self.assertEqual(rotate_left(0x000001, 1), 0x000002)
        self.assertEqual(rotate_left(0x800000, 1), 0x000001)
        self.assertEqual(rotate_right(0x000001, 1), 0x800000)
        self.assertEqual(rotate_right(0x000002, 1), 0x000001)

    def test_known_exact_simple_transform_on_synthetic_samples(self) -> None:
        samples = []
        for frequency_text in ("146.000", "146.100", "146.200"):
            hz = parse_frequency_hz(frequency_text)
            encoded = bytes(byte ^ 0xAA for byte in (hz & 0xFFFFFF).to_bytes(3, "little"))
            samples.append(FrequencySample(frequency_text, hz, encoded))

        exact, near = search_transforms(samples, near_threshold=len(samples))

        self.assertTrue(
            any(
                match.source_label == "Hz"
                and "raw 24-bit little endian" in match.name
                and "byte permutation 012" in match.name
                and "XOR 0xaa repeated" in match.name
                and match.matched == len(samples)
                for match in exact
            )
        )
        self.assertEqual(near, [])

    def test_current_samples_full_matches_are_actual_matches(self) -> None:
        samples = verified_samples()
        exact, _near = search_transforms(samples)

        self.assertTrue(exact)
        for match in exact:
            self.assertEqual(match.matched, len(samples))
            self.assertEqual(match.failed, ())

    def test_current_samples_include_verified_exact_candidate(self) -> None:
        exact, _near = search_transforms(verified_samples())

        self.assertTrue(
            any(
                match.source_label == "Hz"
                and match.name
                == "identity; raw 24-bit little endian; byte permutation 012; XOR 0x41 repeated"
                for match in exact
            )
        )


if __name__ == "__main__":
    unittest.main()
