# Channel Reverse Engineering

This document records experimentally verified observations only.

## Verified facts

- The DAT header is the first `0x40` bytes.
- The payload uses a variable single-byte XOR mask.
- KPG Save As may change the payload XOR mask while preserving the normalized
  payload.
- `tools/dat_normalized_diff.py` is the canonical comparison tool.
- Channel records appear to start at `0x5E80`.
- Channel record stride appears to be `0x40` bytes.
- Channel 1 RX frequency field is at record offset `+0x05`, with length 3
  bytes.
- Channel 1 TX frequency field is at record offset `+0x09`, with length 3
  bytes.
- Channel 2 RX frequency field is at record offset `+0x05`, with length 3
  bytes.
- Channel 2 TX frequency field is at record offset `+0x09`, with length 3
  bytes.

## Verified frequency encodings

| Frequency | Encoded bytes |
| --- | --- |
| `146.12000` | `01 dc f4` |
| `146.51000` | `f1 d1 fa` |
| `146.52000` | `81 f6 fa` |
| `146.53000` | `91 9f fa` |
| `146.72000` | `41 84 ff` |
| `147.00000` | `81 4b 82` |

The frequency-encoding formula is not known.

## Unknowns

- The frequency-encoding formula.
- Whether the apparent channel record start and stride apply to every channel
  and every DAT file.
- The meanings of all other bytes in each apparent channel record.
- Channel record count, bounds, empty-record representation, and indexing.
- Whether additional channel-related metadata, checksums, or references change
  when a channel is edited.

## Do not assume

- Do not assume the apparent channel record start or stride is a complete,
  universally valid record specification.
- Do not assume that a byte sequence for one verified frequency can be derived
  for any other frequency.
- Do not assume RX and TX fields share a known encoding formula merely because
  they have the same observed field length and offsets in Channels 1 and 2.
- Do not assume a raw DAT byte diff is meaningful without normalizing the
  payload XOR mask first.
- Do not assume that changing only a channel frequency is sufficient to create
  a valid DAT file.

## Next recommended controlled experiments

1. For one channel, change only RX frequency across several values and compare
   normalized payloads with `tools/dat_normalized_diff.py`.
2. Repeat the same single-variable experiment for TX frequency.
3. Repeat RX and TX experiments on additional channel numbers to test the
   apparent `0x40`-byte stride.
4. Perform a KPG Save As with no channel edits, then verify that normalization
   removes any payload XOR-mask-only difference.
5. Add, delete, and reorder one channel at a time to identify channel bounds,
   record count behavior, and related metadata.
