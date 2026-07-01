# Dattest2 Controlled Experiment Report

## Inputs And Baseline

The archive `research/Dattest2.zip` was extracted to `research/dattest2/Dattest2/`.

The archive does not contain a literal `Program.dat` file. It contains three no-change saves, so this report uses `Program_Nochange1.dat` as the comparison baseline for Dattest2.

All files are `168257` bytes.

Important filename note: the task text refers to `Program_TG_65535.dat` and `Program_ID_65535.dat`, but the archive contains `Program_TG_65516.dat` and `Program_ID_65519.dat`. The bytes in both max-value experiments decode to `65519`, not `65535`.

Generated supporting reports are under `data/normalized/dattest2/reports/`.

## Direct Byte Comparison Against `Program_Nochange1.dat`

Every non-baseline file has the same direct diff shape:

- Size delta: `0`
- Changed bytes: `168193`
- Changed regions: `1`
- Changed region: `0x00000040-0x00029140`

The common unchanged prefix is `0x40` bytes. The visible header in that prefix is unchanged:

```text
00000000  4b 50 47 31 31 31 44 ff ff ff 56 35 2e 32 30 ff  KPG111D...V5.20.
00000010  4d 4e 58 20 30 37 30 30 ff ff 00 04 ff ff ff ff  MNX 0700........
00000020  44 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff  D...............
00000030  ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff  ................
```

Direct byte comparison alone is therefore not sufficient to locate logical edits.

## Payload XOR Keys

For each file, `baseline_byte ^ modified_byte` over the payload from `0x40` to EOF has one dominant value.

| File | Dominant XOR | Dominant Count | Ratio | XOR Exceptions | Normalized Changed Bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| `Program_Nochange2.dat` | `0x74` | 168193 | 100.0000% | 0 | 0 |
| `Program_Nochange3.dat` | `0x7c` | 168193 | 100.0000% | 0 | 0 |
| `Program_TG_00001.dat` | `0x78` | 168177 | 99.9905% | 16 | 16 |
| `Program_TG_00100.dat` | `0x0b` | 168177 | 99.9905% | 16 | 16 |
| `Program_TG_12345.dat` | `0x18` | 168177 | 99.9905% | 16 | 16 |
| `Program_TG_65516.dat` | `0x13` | 168178 | 99.9911% | 15 | 15 |
| `Program_ID_00001.dat` | `0x65` | 168177 | 99.9905% | 16 | 16 |
| `Program_ID_00100.dat` | `0x0a` | 168177 | 99.9905% | 16 | 16 |
| `Program_ID_12345.dat` | `0x18` | 168177 | 99.9905% | 16 | 16 |
| `Program_ID_65519.dat` | `0x62` | 168178 | 99.9911% | 15 | 15 |

Evidence:

- No-change saves differ by exactly one constant XOR byte over all `168193` payload bytes.
- TG/ID saves differ by one constant XOR byte everywhere except the logical record bytes changed by the experiment.
- The XOR mask is constant over the payload for a given save. It is not position dependent in these samples.
- The XOR key changes between saves.

## No-Change Saves

The no-change saves are not byte-identical:

- `Program_Nochange2.dat` uses payload XOR delta `0x74` versus `Program_Nochange1.dat`.
- `Program_Nochange3.dat` uses payload XOR delta `0x7c` versus `Program_Nochange1.dat`.

After applying the dominant XOR delta back to the payload:

- `Program_Nochange2.dat` has `0` changed logical bytes.
- `Program_Nochange3.dat` has `0` changed logical bytes.

Conclusion: no-change saves produce identical logical records while changing the whole-payload XOR key.

## Encoding, Compression, And Rewrite Evidence

Compression: no supporting evidence was observed in this evidence set.

- Files keep identical size.
- No-change saves normalize to exactly identical payloads.
- Controlled edits normalize to only 15 or 16 changed bytes.
- A compressed payload would not usually preserve a constant whole-payload XOR relationship and tiny fixed-offset residual edits.

Block encryption: no supporting evidence was observed in this evidence set.

- The observed single constant byte-wise XOR delta over 100% of no-change payload bytes is not supporting evidence for block encryption.
- The residual logical changes are not block-sized; they are name and numeric fields inside 32-byte records.

Position-dependent stream encryption: no supporting evidence was observed in this evidence set.

- The observed mask is constant over the payload for each save.
- No position-dependent keystream is needed to explain any observed byte.

Deterministic logical rewriting: supported.

- No-change saves normalize to identical logical bytes.
- Controlled TG saves all edit the same record at `0x151a0`.
- Controlled ID saves all edit the same record at `0x10640`.
- Equal numeric values in TG and ID experiments produce equal encoded numeric bytes after normalization.

## Relationship To Previous Dattest Report

`Program_Nochange1.dat` is logically identical to the previous `AK7AN_Travel.dat` after applying a payload XOR delta of `0x6f`:

| Baseline | Modified | Dominant XOR | Normalized Changed Bytes |
| --- | --- | ---: | ---: |
| `research/dattest/Dattest/AK7AN_Travel.dat` | `Program_Nochange1.dat` | `0x6f` | 0 |

That relationship explains the apparent change in text decode key:

- In previous `AK7AN_Travel.dat` byte space, record text decodes with XOR `0x5b`.
- In Dattest2 `Program_Nochange1.dat` byte space, the same logical text decodes with XOR `0x34`.
- `0x5b ^ 0x6f = 0x34`.

Conclusion: the previous `XOR 0x5b` string hypothesis is supported when records are viewed in the previous canonical byte space. Within any saved file's current byte space, the effective text XOR key shifts with the file-level payload mask.

## Observed Record Structure Evidence

Both TG and ID add experiments support 32-byte records for the observed add slots.

Observed changed fields:

| Experiment Type | Record Base | Name Field | Numeric Field |
| --- | ---: | --- | --- |
| Talk Group | `0x151a0` | `+1..+14` = `0x151a1-0x151ae` | `+19..+20` = `0x151b3-0x151b4` |
| Individual ID | `0x10640` | `+1..+14` = `0x10641-0x1064e` | `+19..+20` = `0x10653-0x10654` |

The baseline slots at those record bases are empty in `Program_Nochange1.dat` byte space:

```text
TG empty slot at 0x151a0:
cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb
cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb

ID empty slot at 0x10640:
cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb
cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb
```

After normalization, add experiments change only the name field and numeric field. No count field, index field, or checksum-like side field changes in these comparisons.

## Talk Group Numeric Field

The Talk Group numeric ID is stored at record bytes `+19/+20`, absolute offsets `0x151b3-0x151b4` for the add slot used in this experiment.

In `Program_Nochange1.dat` byte space:

- Decode bytes `+19/+20` with XOR `0x34`.
- Interpret the two decoded bytes as little-endian unsigned 16-bit.

Evidence:

| File | Label / Observed Name | Encoded `+19/+20` | XOR `0x34` | Little-Endian | Big-Endian |
| --- | --- | --- | --- | ---: | ---: |
| `Program_TG_00001.dat` | `TG Test 00001` | `35 34` | `01 00` | 1 | 256 |
| `Program_TG_00100.dat` | `TG Test 00100` | `50 34` | `64 00` | 100 | 25600 |
| `Program_TG_12345.dat` | `TG Test 12345` | `0d 04` | `39 30` | 12345 | 14640 |
| `Program_TG_65516.dat` | `TG Test 65519` | `db cb` | `ef ff` | 65519 | 61439 |

The big-endian interpretation fails all controlled values. Little-endian matches every observed value.

Hex evidence for `Program_TG_12345.dat` normalized against `Program_Nochange1.dat`:

```text
Record 0x151a0:
cb 60 73 14 60 51 47 40 14 05 06 07 00 01 34 cb
cb cb cb 0d 04 cb cb cb cb cb cb cb cb cb cb cb

Name bytes +1..+14 XOR 0x34:
54 47 20 54 65 73 74 20 31 32 33 34 35 00 = "TG Test 12345"

Numeric bytes +19/+20:
0d 04 XOR 0x34 = 39 30
0x3039 little-endian = 12345
```

## Individual ID Numeric Field

The Individual ID numeric ID is stored at record bytes `+19/+20`, absolute offsets `0x10653-0x10654` for the add slot used in this experiment.

In `Program_Nochange1.dat` byte space:

- Decode bytes `+19/+20` with XOR `0x34`.
- Interpret the two decoded bytes as little-endian unsigned 16-bit.

Evidence:

| File | Label / Observed Name | Encoded `+19/+20` | XOR `0x34` | Little-Endian | Big-Endian |
| --- | --- | --- | --- | ---: | ---: |
| `Program_ID_00001.dat` | `ID_Test_00001` | `35 34` | `01 00` | 1 | 256 |
| `Program_ID_00100.dat` | `ID_Test_00100` | `50 34` | `64 00` | 100 | 25600 |
| `Program_ID_12345.dat` | `ID_Test_12345` | `0d 04` | `39 30` | 12345 | 14640 |
| `Program_ID_65519.dat` | `ID_Test_65519` | `db cb` | `ef ff` | 65519 | 61439 |

The same encoding is used for TG and ID records in this experiment.

Hex evidence for `Program_ID_12345.dat` normalized against `Program_Nochange1.dat`:

```text
Record 0x10640:
cb 7d 70 6b 60 51 47 40 6b 05 06 07 00 01 34 cb
cb cb cb 0d 04 cb cb cb cb cb cb cb cb cb cb cb

Name bytes +1..+14 XOR 0x34:
49 44 5f 54 65 73 74 5f 31 32 33 34 35 00 = "ID_Test_12345"

Numeric bytes +19/+20:
0d 04 XOR 0x34 = 39 30
0x3039 little-endian = 12345
```

## String Field Evidence

In Dattest2 `Program_Nochange1.dat` byte space, the added record names decode with XOR `0x34`:

| File | Name Bytes `+1..+14` | Decoded Text |
| --- | --- | --- |
| `Program_TG_00001.dat` | `60 73 14 60 51 47 40 14 04 04 04 04 05 34` | `TG Test 00001` |
| `Program_TG_00100.dat` | `60 73 14 60 51 47 40 14 04 04 05 04 04 34` | `TG Test 00100` |
| `Program_TG_12345.dat` | `60 73 14 60 51 47 40 14 05 06 07 00 01 34` | `TG Test 12345` |
| `Program_TG_65516.dat` | `60 73 14 60 51 47 40 14 02 01 01 05 0d 34` | `TG Test 65519` |
| `Program_ID_00001.dat` | `7d 70 6b 60 51 47 40 6b 04 04 04 04 05 34` | `ID_Test_00001` |
| `Program_ID_00100.dat` | `7d 70 6b 60 51 47 40 6b 04 04 05 04 04 34` | `ID_Test_00100` |
| `Program_ID_12345.dat` | `7d 70 6b 60 51 47 40 6b 05 06 07 00 01 34` | `ID_Test_12345` |
| `Program_ID_65519.dat` | `7d 70 6b 60 51 47 40 6b 02 01 01 05 0d 34` | `ID_Test_65519` |

The last byte of a 14-byte shorter-or-equal name is `0x34`, which decodes to `0x00`. This is consistent with null padding under the active text XOR key.

## Hypothesis Status

| Hypothesis | Status | Evidence |
| --- | --- | --- |
| 32-byte records | Supported for observed TG and ID add slots | All logical edits align to `0x10640` or `0x151a0`; fields recur at `+1..+14` and `+19..+20`. |
| XOR `0x5b` string decoding | Supported in previous canonical byte space; effective key is `0x34` in `Program_Nochange1.dat` byte space | `Program_Nochange1.dat` is previous baseline XOR `0x6f`; `0x5b ^ 0x6f = 0x34`. |
| Bytes `+19/+20` contain numeric IDs | Supported for observed TG and ID add records | Decoding `+19/+20` with the active XOR key and little-endian byte order matches 1, 100, 12345, and 65519. |
| Big-endian numeric byte order | Not supported for observed add records | Big-endian values are 256, 25600, 14640, and 61439 for the controlled rows. |
| Position-dependent XOR mask | No supporting evidence in observed saves | No-change saves are exactly one XOR value over the full payload. |
| Compression / block encryption / stream encryption | No supporting evidence in observed saves | Constant XOR plus tiny normalized record edits explains all observed bytes. |

## Tooling Changes

`tools/dat_record_probe.py` was improved to accept:

- `--text-xor`
- `--numeric-xor`

This keeps the tool read-only while allowing reports in either the previous `0x5b` canonical space or the Dattest2 `0x34` byte space.

No Program.dat generator or editor was created.
