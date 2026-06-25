# Dattest3 Program.dat Analysis

## Inputs

`research/Dattest3.zip` was extracted to `research/dattest3/Dattest3/`.

The prompt listed `Program_1.dat`, `Program_2.dat`, and `Program_3.dat`, but the archive contains:

- `Program.dat`
- `Program1.dat`
- `Program2.dat`
- `Program3.dat`
- `Program4.dat`

This report treats `Program.dat` as the baseline and analyzes all four modified files present in the archive.

All files are `168257` bytes.

## Baseline Decode Context

Comparing Dattest3 `Program.dat` to the earlier Dattest baseline shows a dominant payload XOR relationship of `0x44`. Using the previous working text key `0x5b`, the active decode key for this Dattest3 baseline is:

```text
0x5b ^ 0x44 = 0x1f
```

`tools/dat_table_map.py` was run on `Program.dat` with `--decode-xor 0x1f`.

## Candidate Table Boundaries In Baseline

The Dattest3 baseline has more occupied records than the earlier experiments.

| Candidate Table | Occupied Start | Occupied End | Occupied Records | First Empty Slot | Empty Slots After |
| --- | ---: | ---: | ---: | ---: | ---: |
| Individual ID | `0x00010480` | `0x0001083f` | 30 | `0x00010840` | 570 |
| Talk Group | `0x00014f80` | `0x0001533f` | 30 | `0x00015340` | 321 |

Supporting map:

- `research/dattest3/table_map.md`
- `research/dattest3/table_map.json`

## Direct Diff Summary

| File | Direct Changed Bytes | Direct Changed Regions | Size Delta |
| --- | ---: | ---: | ---: |
| `Program1.dat` | 168193 | 1 | 0 |
| `Program2.dat` | 168191 | 3 | 0 |
| `Program3.dat` | 168190 | 4 | 0 |
| `Program4.dat` | 53 | 9 | 0 |

`Program1.dat`, `Program2.dat`, and `Program3.dat` mostly differ because their payload XOR key changed. `Program4.dat` keeps the same payload XOR key as the baseline and only has localized record changes.

## Payload XOR Summary

| File | Dominant XOR vs Baseline | Dominant Ratio | Normalized Changed Bytes | Normalized Regions |
| --- | ---: | ---: | ---: | ---: |
| `Program1.dat` | `0x2f` | 99.9857% | 24 | 2 |
| `Program2.dat` | `0x2b` | 99.9845% | 26 | 4 |
| `Program3.dat` | `0x01` | 99.9661% | 57 | 8 |
| `Program4.dat` | `0x00` | 99.9685% | 53 | 9 |

After normalizing with the dominant XOR value, all residual changed ranges fall inside candidate Individual ID or Talk Group records. No residual changed ranges were observed in separate count, index, or checksum-like locations.

## Plain-English Changes

| File | Table | Record | Before Name | After Name | Before Decoded ID | After Decoded ID | Interpretation |
| --- | --- | ---: | --- | --- | ---: | ---: | --- |
| `Program1.dat` | Individual ID | `0x10640` | `ID_Test_65519` | `Long Gone` | 65519 | 65519 | Renamed ID record. |
| `Program1.dat` | Talk Group | `0x15140` | `Utah DRN 00` | `Hot n Sexy` | 31490 | 31490 | Renamed TG record. |
| `Program2.dat` | Individual ID | `0x10640` | `ID_Test_65519` | `Long Gone` | 65519 | 65518 | Renamed ID record and changed numeric ID by -1. |
| `Program2.dat` | Talk Group | `0x15140` | `Utah DRN 00` | `Hot n Sexy` | 31490 | 31491 | Renamed TG record and changed numeric TG by +1. |
| `Program3.dat` | Individual ID | `0x105a0` | `Jamie, KQ1USA` | empty | 5770 | 65535 | Cleared an occupied ID record. |
| `Program3.dat` | Individual ID | `0x10640` | `ID_Test_65519` | `Long Gone` | 65519 | 65518 | Same ID rename/numeric change as Program2. |
| `Program3.dat` | Talk Group | `0x150a0` | `Scotland TG` | empty | 23551 | 65535 | Cleared an occupied TG record. |
| `Program3.dat` | Talk Group | `0x15140` | `Utah DRN 00` | `Hot n Sexy` | 31490 | 31491 | Same TG rename/numeric change as Program2. |
| `Program4.dat` | Individual ID | `0x105a0` | `Jamie, KQ1USA` | `Hello` | 5770 | 23654 | Changed name and numeric ID in an existing ID record. |
| `Program4.dat` | Individual ID | `0x10640` | `ID_Test_65519` | `Long Gone` | 65519 | 65518 | Same ID rename/numeric change as Program2. |
| `Program4.dat` | Talk Group | `0x150a0` | `Scotland TG` | `Goodbye` | 23551 | 16432 | Changed name and numeric TG in an existing TG record. |
| `Program4.dat` | Talk Group | `0x15140` | `Utah DRN 00` | `Hot n Sexy` | 31490 | 31491 | Same TG rename/numeric change as Program2. |

## Hex Evidence Examples

The following record probes are after payload-XOR normalization and use decode key `0x1f`.

### `Program1.dat`: ID Rename

```text
Record 0x10640 before:
e0 56 5b 40 4b 7a 6c 6b 40 29 2a 2a 2e 26 1f e0
e0 e0 e0 f0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0

Name +1..+14 XOR 0x1f: ID_Test_65519
Numeric +19/+20 XOR 0x1f: ef ff, little-endian 65519

Record 0x10640 after:
e0 53 70 71 78 3f 58 70 71 7a 1f 1f 1f 1f 1f e0
e0 e0 e0 f0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0

Name +1..+14 XOR 0x1f: Long Gone
Numeric +19/+20 XOR 0x1f: ef ff, little-endian 65519
```

### `Program3.dat`: ID Record Cleared

```text
Record 0x105a0 before:
e0 55 7e 72 76 7a 33 3f 54 4e 2e 4a 4c 5e 1f e0
e0 e0 e0 95 09 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0

Name +1..+14 XOR 0x1f: Jamie, KQ1USA
Numeric +19/+20 XOR 0x1f: 8a 16, little-endian 5770

Record 0x105a0 after:
e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0
e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0

Name: empty/non-printable
Numeric +19/+20 XOR 0x1f: ff ff, little-endian 65535
```

### `Program4.dat`: TG Record Changed

```text
Record 0x150a0 before:
e0 4c 7c 70 6b 73 7e 71 7b 3f 4b 58 1f 1f 1f e0
e0 e0 e0 e0 44 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0

Name +1..+14 XOR 0x1f: Scotland TG
Numeric +19/+20 XOR 0x1f: ff 5b, little-endian 23551

Record 0x150a0 after:
e0 58 70 70 7b 7d 66 7a 1f 1f 1f 1f 1f 1f 1f e0
e0 e0 e0 2f 5f e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0

Name +1..+14 XOR 0x1f: Goodbye
Numeric +19/+20 XOR 0x1f: 30 40, little-endian 16432
```

## Effect On Tables And Empty Slots

Baseline table maps:

- Individual ID table candidate run: `0x10480-0x1083f`, 30 occupied records, first empty slot `0x10840`.
- Talk Group table candidate run: `0x14f80-0x1533f`, 30 occupied records, first empty slot `0x15340`.

Modified table-map summaries:

| File | Individual ID Run(s) | Talk Group Run(s) |
| --- | --- | --- |
| `Program1.dat` | `0x10480-0x1083f` unchanged, 30 occupied | `0x14f80-0x1533f` unchanged, 30 occupied |
| `Program2.dat` | `0x10480-0x1083f` unchanged, 30 occupied | `0x14f80-0x1533f` unchanged, 30 occupied |
| `Program3.dat` | Split into `0x10480-0x1059f` and `0x105c0-0x1083f` because `0x105a0` was cleared | Split into `0x14f80-0x1509f` and `0x150c0-0x1533f` because `0x150a0` was cleared |
| `Program4.dat` | `0x10480-0x1083f` unchanged, 30 occupied | `0x14f80-0x1533f` unchanged, 30 occupied |

No modified file wrote to the first empty append slots `0x10840` or `0x15340`. Program3 created empty slots inside existing occupied runs by clearing records at `0x105a0` and `0x150a0`.

## Counts, Indexes, And Checksum-Like Fields

No separate count field, index table, or checksum-like field changed after XOR normalization in these comparisons.

Evidence:

- Every normalized residual changed range maps to one of these candidate table records:
  - ID records: `0x105a0`, `0x10640`
  - TG records: `0x150a0`, `0x15140`
- Changed intra-record offsets are the name field `+1..+14` and numeric field `+19/+20`.
- No residual normalized changes appear near the end of file, in the header, or outside the candidate TG/ID table records.

This does not prove count/index/checksum fields do not exist. It only means these experiments did not produce observed changes in such fields.

## Generated Evidence Files

- `reports/xor_analysis.md`
- `reports/session_report.md`
- `reports/offset_spacing.md`
- `table_map.md`
- `reports/Program1.records.md`
- `reports/Program2.records.md`
- `reports/Program3.records.md`
- `reports/Program4.records.md`
- `reports/change_summary_table.md`

No Program.dat files were generated or modified, and no writer was built.
