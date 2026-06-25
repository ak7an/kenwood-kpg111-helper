# Channel Record Analysis

This document starts the evidence trail for KPG111 channel records. The current state is read-only and exploratory. No DAT editing, channel encoder, or writer is implemented.

## Current Evidence

- Known Talk Group and Individual ID records are decoded separately and are not channel records.
- Existing reports identify 32-byte TG/ID records, but that does not prove channel records use the same size.
- No controlled channel-specific before/after experiment is currently present under `research/`.
- `tools/dat_channel_analysis.py` provides a heuristic scan for candidate channel-like blocks. Its output is hypothesis-generating only.
- The first heuristic pass over `research/dattest/Dattest/AK7AN_Travel.dat` surfaces low-confidence blocks containing decoded menu/configuration-like strings such as `CALL`, `AUDIO/TONES`, `Power`, and `HORN ALERT`. These are not confirmed channel records.

## Candidate Record Offsets

No channel record offset is confirmed yet.

Current low-confidence heuristic candidates from `AK7AN_Travel.dat` with decode key `0x5b` include:

| Offset | Candidate Size | Confidence | Notes |
| --- | ---: | --- | --- |
| `0x00000c30` | 128 | LOW | Contains decoded string windows and frequency-like integer values; likely may be UI/config text rather than a channel record. |
| `0x00000c40` | 128 | LOW | Contains `CALL`, `AUDIO/TONES`, `Power`, and `QT` text hints; not confirmed as channel data. |
| `0x00001820` | 128 | LOW | Contains configuration-like strings and feature words; not confirmed. |
| `0x00001830` | 128 | LOW | Contains configuration-like strings and feature words; not confirmed. |
| `0x00001840` | 96 | LOW | Contains configuration-like strings and feature words; not confirmed. |

These offsets should be treated as scan results, not as field-map evidence.

## Candidate Record Size

No channel record size is confirmed yet.

The new analysis tool scans candidate sizes:

```text
32, 44, 48, 64, 80, 96, 128
```

This range intentionally includes sizes outside the known TG/ID 32-byte record size. Channel records may have a different stride, may be grouped with zone or scan-list structures, or may require a different decode key or layout.

## Known Unknowns

- Channel table start offset.
- Channel record size.
- Channel name encoding and offset.
- RX frequency encoding and offset.
- TX frequency encoding and offset.
- Spacing/channel step representation.
- Analog vs NXDN mode representation.
- Wide/narrow bandwidth field.
- High/low power field.
- QT/DQT encoding.
- NXDN RAN encoding.
- Zone membership or zone reference structure.
- Channel count fields, indexes, pointers, checksums, and metadata.
- Whether channel records are contiguous or referenced indirectly.

## Tool Usage

Run a heuristic scan:

```bash
python3 tools/dat_channel_analysis.py research/dattest/Dattest/AK7AN_Travel.dat --decode-key 0x5b
```

The report separates confirmed parser facts from candidate channel-like blocks. Treat every candidate row as a hypothesis until a controlled channel edit changes that offset predictably.

## Recommended Controlled Experiments

Run these in KPG-111D with one change per export:

1. Blank codeplug vs one analog channel.
2. One analog channel vs same channel with changed RX frequency.
3. Changed TX frequency only.
4. Changed channel name only.
5. Changed wide/narrow only.
6. Changed high/low power only.
7. Changed QT/DQT only.
8. Changed NXDN RAN only.
9. One channel vs two channels.
10. Same channels in different zones.

For each experiment:

- Preserve the original DAT export.
- Compare before/after bytes.
- Normalize any whole-payload XOR behavior before interpreting changes.
- Record changed offsets, changed ranges, and candidate field meanings.
- Add tests only after the observed offset and encoding are repeatable.

## Field Map Status

| Field | Status | Confidence | Notes |
| --- | --- | --- | --- |
| Channel record start | UNKNOWN | LOW | No controlled channel experiment yet. |
| Channel record size | UNKNOWN | LOW | Candidate sizes are scan parameters only. |
| Channel name | HYPOTHESIS ONLY | LOW | Name-like strings exist, but not tied to channel UI changes. |
| RX frequency | HYPOTHESIS ONLY | LOW | Frequency-like integers can be false positives. |
| TX frequency | HYPOTHESIS ONLY | LOW | No TX-only experiment yet. |
| Mode | UNKNOWN | LOW | No analog/NXDN controlled change yet. |
| Bandwidth | UNKNOWN | LOW | No wide/narrow controlled change yet. |
| Power | UNKNOWN | LOW | Feature text appears in scans, but no field is identified. |
| QT/DQT | UNKNOWN | LOW | No controlled tone/code change yet. |
| RAN | UNKNOWN | LOW | No controlled NXDN RAN change yet. |
| Zone reference | UNKNOWN | LOW | No same-channel different-zone experiment yet. |
