# OpenKPG Next Steps

## Current Status

Current milestone: v0.5.0

The project has a working DAT reverse-engineering framework.

## Verified Facts

- DAT header is first 0x40 bytes.
- Payload uses a variable single-byte XOR mask.
- KPG Save As can change the payload XOR mask without changing normalized payload.
- `tools/dat_normalized_diff.py` is the canonical comparison tool.
- Channel table appears to start at 0x5E80.
- Channel record stride appears to be 0x40 bytes.
- RX frequency field is record + 0x05, length 3.
- TX frequency field is record + 0x09, length 3.

## Verified Frequency Samples

| Frequency | Encoded bytes |
| ---: | --- |
| 146.12000 | 01 dc f4 |
| 146.51000 | f1 d1 fa |
| 146.52000 | 81 f6 fa |
| 146.53000 | 91 9f fa |
| 146.72000 | 41 84 ff |
| 147.00000 | 81 4b 82 |

## Important Unknowns

- Exact 3-byte frequency encoding formula.
- Whether frequency encoding is packed integer, scrambled integer, lookup-like, or derived.
- Adjacent channel fields: bandwidth, power, mode, signaling, scan, zone/index behavior.

## Next Controlled KPG111 Experiments

Use Line 2 RX-only unless otherwise noted.

Recommended samples:

- 146.00000
- 146.10000
- 146.20000
- 146.30000
- 146.40000
- 146.50000
- 146.90000
- 146.99000
- 146.99500 if supported
- 147.00500 if supported
- 147.01000
- 147.10000

For each saved DAT:

1. Copy DAT to OptiPlex.
2. Run `dat_normalized_diff.py` against baseline.
3. Confirm only 3 normalized bytes changed at channel 2 RX field.
4. Record encoding in frequency sample table.

## Do Not Assume

- Do not assume BCD frequency encoding.
- Do not assume TK-8180 memory layout applies to KPG111 DAT.
- Do not map additional fields without controlled edits.
- Do not compare raw DAT payloads without XOR normalization.
