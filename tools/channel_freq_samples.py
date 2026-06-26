#!/usr/bin/env python3
"""Explore experimental channel frequency byte samples without inferring fields."""

from __future__ import annotations

from dataclasses import dataclass


SAMPLES = (
    ("146.12000", bytes.fromhex("01 dc f4")),
    ("146.51000", bytes.fromhex("f1 d1 fa")),
    ("146.52000", bytes.fromhex("81 f6 fa")),
    ("146.53000", bytes.fromhex("91 9f fa")),
    ("146.72000", bytes.fromhex("41 84 ff")),
    ("147.00000", bytes.fromhex("81 4b 82")),
)
MODULI = (10, 16, 25, 50, 100, 125, 200, 250, 500, 1000, 5000, 10000)


@dataclass(frozen=True)
class FrequencySample:
    frequency_text: str
    frequency_hz: int
    raw: bytes

    @property
    def raw_big(self) -> int:
        return int.from_bytes(self.raw, "big")

    @property
    def raw_little(self) -> int:
        return int.from_bytes(self.raw, "little")

    @property
    def xor_ff(self) -> bytes:
        return bytes(byte ^ 0xFF for byte in self.raw)

    @property
    def xor_ff_big(self) -> int:
        return int.from_bytes(self.xor_ff, "big")

    @property
    def xor_ff_little(self) -> int:
        return int.from_bytes(self.xor_ff, "little")


def parse_frequency_hz(value: str) -> int:
    whole, fractional = value.split(".", 1)
    fractional = (fractional + "00000")[:5]
    return int(whole) * 1_000_000 + int(fractional) * 10


def samples() -> list[FrequencySample]:
    return [
        FrequencySample(frequency_text, parse_frequency_hz(frequency_text), raw)
        for frequency_text, raw in SAMPLES
    ]


def markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        print("| " + " | ".join("none" for _ in headers) + " |")
        return
    for row in rows:
        print("| " + " | ".join(row) + " |")


def fmt_delta(value: int | None) -> str:
    if value is None:
        return ""
    return f"{value:+d}"


def render_samples(rows: list[FrequencySample]) -> None:
    table_rows: list[list[str]] = []
    previous: FrequencySample | None = None
    for sample in rows:
        table_rows.append(
            [
                sample.frequency_text,
                sample.raw.hex(" "),
                str(sample.raw_big),
                str(sample.raw_little),
                sample.xor_ff.hex(" "),
                str(sample.xor_ff_big),
                str(sample.xor_ff_little),
                fmt_delta(None if previous is None else sample.frequency_hz - previous.frequency_hz),
                fmt_delta(None if previous is None else sample.raw_big - previous.raw_big),
                fmt_delta(None if previous is None else sample.raw_little - previous.raw_little),
                fmt_delta(None if previous is None else sample.xor_ff_big - previous.xor_ff_big),
                fmt_delta(None if previous is None else sample.xor_ff_little - previous.xor_ff_little),
            ]
        )
        previous = sample

    markdown_table(
        [
            "frequency",
            "bytes",
            "big endian integer",
            "little endian integer",
            "xor_ff bytes",
            "xor_ff big endian",
            "xor_ff little endian",
            "delta hz",
            "raw big delta",
            "raw little delta",
            "xor_ff big delta",
            "xor_ff little delta",
        ],
        table_rows,
    )


def modulo_pattern(values: list[int], modulus: int) -> str:
    return ", ".join(str(value % modulus) for value in values)


def render_modulo_patterns(rows: list[FrequencySample]) -> None:
    series = [
        ("raw little endian", [sample.raw_little for sample in rows]),
        ("raw big endian", [sample.raw_big for sample in rows]),
        ("xor_ff little endian", [sample.xor_ff_little for sample in rows]),
        ("xor_ff big endian", [sample.xor_ff_big for sample in rows]),
    ]
    table_rows = []
    for label, values in series:
        for modulus in MODULI:
            table_rows.append([label, str(modulus), modulo_pattern(values, modulus)])
    markdown_table(["series", "modulus", "remainders"], table_rows)


def main() -> int:
    rows = samples()
    print("# Channel Frequency Sample Byte Analysis")
    print()
    print("Read-only helper using hard-coded experimental samples. No final encoding formula is inferred.")
    print()
    print("## Samples")
    render_samples(rows)
    print()
    print("## Simple Modulo Transforms")
    render_modulo_patterns(rows)
    print()
    print("Observation: these transforms are exploratory only. Treat any apparent pattern as a hypothesis until more controlled samples confirm it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
