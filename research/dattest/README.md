# Dattest Controlled Experiment Report

## Inputs

- Archive extracted to `research/dattest/Dattest/`.
- Baseline: `AK7AN_Travel.dat`
- Modified files: `Program_1TG.dat`, `Program_1ID.dat`, `Program_Rename.dat`, `Program_Delete.dat`
- Every file is exactly `168257` bytes.
- Baseline SHA-256: `aa20a84b5cb76e5fd58a691eb26fdc4140e7d75fb3bd6b28fc156f3ec4144cce`

Supporting generated reports:

- `reports/session_report.md`
- `reports/offset_spacing.md`
- `reports/xor_analysis.md`
- `reports/*.records.md`
- `reports/*.inspect.md`
- `reports/*.tables.md`

## Direct Binary Comparison

All four modified files have the same direct comparison shape against the baseline:

| File | Size Delta | Direct Changed Bytes | Direct Changed Regions |
| --- | ---: | ---: | ---: |
| `Program_1TG.dat` | 0 | 168193 | 1 |
| `Program_1ID.dat` | 0 | 168193 | 1 |
| `Program_Rename.dat` | 0 | 168193 | 1 |
| `Program_Delete.dat` | 0 | 168193 | 1 |

The unchanged prefix is exactly `0x40` bytes. The changed region is:

- `0x00000040-0x00029140`
- length `168193`

The first `0x40` bytes contain the visible header:

- `KPG111D`
- `V5.20`
- `MNX 0700`

No direct comparison exposed a localized checksum region, short count field, or tail-only update. The whole payload after `0x40` is rewritten.

## Dominant XOR Rewrite Evidence

The payload rewrite is almost entirely explained by one file-level XOR delta per modified file. This is derived from `baseline_byte ^ modified_byte` for every payload byte from `0x40` to EOF.

| File | Dominant XOR Delta | Count | Ratio | Exceptions |
| --- | ---: | ---: | ---: | ---: |
| `Program_1TG.dat` | `0x3e` | 168177 | 99.9905% | 16 |
| `Program_1ID.dat` | `0x0c` | 168161 | 99.9810% | 32 |
| `Program_Rename.dat` | `0x67` | 168181 | 99.9929% | 12 |
| `Program_Delete.dat` | `0x1e` | 168165 | 99.9834% | 28 |

Example evidence from the first payload bytes:

- Baseline filler byte `0xa4` becomes `0x9a` in `Program_1TG.dat`.
- `0xa4 ^ 0x9a = 0x3e`.
- Baseline byte `0x5b` becomes `0x65` in the same file.
- `0x5b ^ 0x65 = 0x3e`.

After applying each file's dominant XOR delta back to its payload, the logical diffs collapse to small localized ranges:

| File | Normalized Changed Bytes | Normalized Changed Regions |
| --- | ---: | ---: |
| `Program_1TG.dat` | 16 | 2 |
| `Program_1ID.dat` | 32 | 4 |
| `Program_Rename.dat` | 12 | 1 |
| `Program_Delete.dat` | 28 | 3 |

Conclusion supported by this evidence:

- The payload is not completely different logical data.
- The save operation changes a whole-payload single-byte XOR mask, then writes localized logical edits underneath that mask.
- This is evidence for XOR obfuscation or a trivial single-byte stream transform in these files. No supporting evidence for block encryption was observed.

## Compression, Encryption, Checksum, And Determinism

Evidence not supporting compression in this experiment:

- File size is constant across all saves.
- The encoded payload contains massive repetition: the baseline has `0xa4` 146542 times and `0x5b` 5210 times.
- After XOR normalization, logical edits are small fixed records, not shifted or recompressed byte streams.

Evidence not supporting block encryption in this experiment:

- The observed one-byte XOR relation over more than 99.98% of the payload is not supporting evidence for block encryption.
- Logical changes after normalization are not block-sized. They are 12, 14, and 2 byte field changes inside 32-byte records.

Evidence about stream encryption in this experiment:

- The observed behavior is compatible with only a trivial single-byte XOR mask over the payload.
- No evidence was observed here for a position-dependent keystream.

Evidence about checksums in this experiment:

- Direct comparison changed the entire payload, so a checksum could be hidden by the XOR rewrite.
- After XOR normalization, no extra tail field, header field, or independent checksum-like changed region remains.
- This experiment therefore gives no positive evidence for checksum regeneration.

Evidence about deterministic rewriting:

- The same logical edit normalizes to the same bytes across files. `Program_1TG.dat` and `Program_1ID.dat` both contain the added record at `0x151a0` with identical normalized bytes.
- `Program_Rename.dat` and `Program_Delete.dat` both contain the rename at `0x15180` with identical normalized bytes.
- The per-save dominant XOR delta changes, but normalized logical records are stable.

Conclusion: in these observed files, the logical payload appears deterministic after removing the file-level XOR delta.

## Candidate Fixed-Length Records

All normalized logical changes align to 32-byte record bases:

| Logical Change | Changed Range(s) | Candidate Record Base | Offset Within Record |
| --- | --- | ---: | --- |
| Add TG | `0x151a1-0x151ae`, `0x151b3-0x151b4` | `0x151a0` | `+1..+14`, `+19..+20` |
| Add ID | `0x10641-0x1064e`, `0x10653-0x10654` | `0x10640` | `+1..+14`, `+19..+20` |
| Rename TG | `0x15181-0x1518c` | `0x15180` | `+1..+12` |
| Delete TG | `0x15121-0x1512e`, `0x15133-0x15134` | `0x15120` | `+1..+14`, `+19..+20` |

The candidate record size is 32 bytes because all candidate bases are 32-byte aligned and the changed fields recur at the same intra-record offsets.

Observed record layout evidence:

- Byte `+0` is `0xa4` in occupied and empty candidate records observed here.
- Bytes `+1..+14` are a fixed 14-byte name field.
- Bytes `+15..+18` are `0xa4 a4 a4 a4` in the observed records.
- Bytes `+19..+20` change during add/delete and remain stable during rename. This is a candidate numeric ID field, but the integer encoding is not identified from this experiment.
- Bytes `+21..+31` are `0xa4` in the observed records.

## Text Encoding Evidence

Within normalized candidate records, bytes `+1..+14` XOR `0x5b` decode as ASCII text with `0x5b` acting as zero padding in the encoded form.

Examples:

| File / Record | Normalized Bytes `+1..+14` | XOR `0x5b` Text |
| --- | --- | --- |
| `Program_1TG.dat` at `0x151a0` | `1c 0b 0f 0f 3e 28 2f 6a 5b 5b 5b 5b 5b 5b` | `GPTTest1` |
| `Program_1ID.dat` at `0x10640` | `19 29 3a 3f 37 3e 22 5b 5b 5b 5b 5b 5b 5b` | `Bradley` |
| `Program_Rename.dat` at `0x15180` | `19 32 2f 19 22 19 32 2f 13 3a 36 28 5b 5b` | `BitByBitHams` |
| Baseline at `0x15180` | `1a 10 6c 1a 15 7b 0f 1c 5b 5b 5b 5b 5b 5b` | `AK7AN TG` |
| Baseline at `0x15120` | `1f 32 28 38 34 35 35 3e 38 2f 7b 0f 1c 5b` | `Disconnect TG` |

No UTF-16 evidence was found for these changed names. The strings are not visible as plain ASCII until the payload is normalized and the record text bytes are XORed with `0x5b`.

## Candidate Individual ID Table

The baseline contains a run of occupied 32-byte records matching the observed layout:

- `0x10480-0x10620`
- 14 occupied records in the scanned run
- The add-ID experiment writes the next 32-byte slot at `0x10640`

Evidence from the nearby baseline scan:

| Record Base | Decoded Name From `+1..+14 ^ 0x5b` | Bytes `+19..+20` |
| ---: | --- | --- |
| `0x10480` | `Curtis, AE4BT` | `f1 65` |
| `0x104a0` | `Frank, KF4CLO` | `78 5d` |
| `0x104c0` | `Ed, AK7AN` | `19 6b` |
| `0x104e0` | `Kelli, KD0CVD` | `1a 6b` |
| `0x10500` | `Chris, K4DKK` | `94 74` |
| `0x10520` | `DVNET` | `54 7c` |
| `0x10540` | `No NXDN ID` | `20 22` |
| `0x10560` | `Bjorn, SA7AUX` | `e9 65` |
| `0x10580` | `Doug, W4DBG` | `4f 5f` |
| `0x105a0` | `Jamie, KQ1USA` | `d1 4d` |
| `0x105c0` | `Randy, W8EJC` | `cf c0` |
| `0x105e0` | `BitByBit Hams` | `62 6b` |
| `0x10600` | `Tom, K4TH` | `c5 7e` |
| `0x10620` | `NX4DX BitbyBit` | `ea 73` |
| `0x10640` in `Program_1ID.dat` | `Bradley` | `12 46` |

Conclusion: `0x10480` is a supported candidate start for an Individual ID record run in this file, and `0x10640` is the observed add slot. The full table boundary is not proven by this experiment.

## Candidate Talk Group Table

The baseline contains a run of occupied 32-byte records matching the observed layout:

- `0x14f80-0x15180`
- 17 occupied records in the scanned run
- The add-TG experiment writes the next 32-byte slot at `0x151a0`

Evidence from the nearby baseline scan:

| Record Base | Decoded Name From `+1..+14 ^ 0x5b` | Bytes `+19..+20` |
| ---: | --- | --- |
| `0x14f80` | `World Wide TG` | `b3 a6` |
| `0x15000` | `AlabamaLink TG` | `79 22` |
| `0x15020` | `SW Missouri TG` | `60 21` |
| `0x15040` | `PiStar TG` | `e3 20` |
| `0x15060` | `VK Radio TG` | `3c 9e` |
| `0x15080` | `NXDN N America` | `83 7c` |
| `0x150a0` | `Scotland TG` | `a4 00` |
| `0x150c0` | `Utah DRN 01` | `58 20` |
| `0x150e0` | `Utah DRN 05` | `5c 20` |
| `0x15100` | `PA7LIM TG` | `93 14` |
| `0x15120` | `Disconnect TG` | `54 7c` |
| `0x15140` | `Utah DRN 00` | `59 20` |
| `0x15160` | `Lookout Mtn TG` | `26 f2` |
| `0x15180` | `AK7AN TG` | `46 08` |
| `0x151a0` in `Program_1TG.dat` | `GPTTest1` | `b2 a6` |

Conclusion: `0x14f80` is a supported candidate start for a Talk Group record run in this file, and `0x151a0` is the observed add slot. The full table boundary is not proven by this experiment.

## Indexes, Counts, And Integer Patterns

Indexes and counts:

- No separate count field changed in normalized comparisons.
- Adds only changed the new record slot.
- Rename only changed the name bytes in an existing record.
- Delete changed the deleted record slot to all `0xa4`.
- Therefore this experiment does not identify a table count, index table, free-list, or sorted index.

Integer-like field:

- Bytes `+19..+20` are consistently populated in occupied records and are cleared to `a4 a4` when a record is deleted.
- Add-TG writes `b2 a6`; add-ID writes `12 46`.
- Rename leaves `+19..+20` unchanged (`46 08` before and after at `0x15180`).
- This supports `+19..+20` as a candidate numeric field, but the integer encoding is not determined.

Tested transforms that are not sufficient from this experiment alone:

- Plain little-endian and big-endian interpretation of `+19..+20`
- XOR with the file-level dominant payload delta
- XOR with the text transform `0x5b`
- Treating `a4 a4` as a simple null value for this field

More known ID values are required before assigning integer meaning.

## Changed Byte Ranges Summary

Direct changed range in every modified file:

- `0x00000040-0x00029140`

Normalized logical changed ranges:

| File | Ranges |
| --- | --- |
| `Program_1TG.dat` | `0x151a1-0x151ae`, `0x151b3-0x151b4` |
| `Program_1ID.dat` | `0x10641-0x1064e`, `0x10653-0x10654`, `0x151a1-0x151ae`, `0x151b3-0x151b4` |
| `Program_Rename.dat` | `0x15181-0x1518c` |
| `Program_Delete.dat` | `0x15121-0x1512e`, `0x15133-0x15134`, `0x15181-0x1518c` |

## Tooling Changes

Two read-only analysis tools were added:

- `tools/dat_xor_analysis.py`
  - derives the dominant payload XOR delta per modified file
  - normalizes modified files into baseline XOR space
  - reports the remaining logical changed ranges

- `tools/dat_record_probe.py`
  - probes specified 32-byte candidate records after dominant-XOR normalization
  - shows raw record bytes
  - decodes bytes `+1..+14` with the observed `^ 0x5b` text transform

No Program.dat editor work was started.

## Recommended Next Controlled Experiment

Run two independent one-change experiments with known numeric values and no cumulative edits:

1. Start from the same `AK7AN_Travel.dat` baseline.
2. Add exactly one Talk Group with a distinctive 14-character-or-shorter name and a known numeric TG value, for example name `TG00012345A` and TG value `12345`.
3. Add exactly one Individual ID with a distinctive 14-character-or-shorter name and a known numeric ID value, for example name `ID00023456A` and ID value `23456`.
4. Save each as a separate file directly from the baseline.
5. Also make a rename-only file for one existing TG and one existing ID, changing only the name and not the numeric value.

This should identify whether bytes `+19..+20` encode the visible TG/ID number, whether the same numeric encoding is used in both tables, and whether any count/index field changes when experiments are not cumulative.
