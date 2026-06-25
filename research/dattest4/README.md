# Dattest4 Slot Reuse Analysis

## Inputs

`research/Dattest4.zip` was extracted to `research/dattest4/Dattest4/`.

Files:

- `Program3.dat`
- `Program5.dat`
- `Program6.dat`

This report treats `Program3.dat` as the baseline.

All files are `168257` bytes.

## Baseline Context

`Program3.dat` is the Dattest3 file where one Individual ID record and one Talk Group record had been cleared.

The active decode key for this baseline is `0x1e`. This follows from the prior Dattest3 baseline key `0x1f` and the Dattest4 baseline being one payload XOR step from that file.

Target slots checked:

| Purpose | Offset |
| --- | ---: |
| Previously emptied Individual ID slot | `0x105a0` |
| Individual ID first append slot | `0x10840` |
| Previously emptied Talk Group slot | `0x150a0` |
| Talk Group first append slot | `0x15340` |

## Direct And XOR-Normalized Diff Summary

| File | Direct Changed Bytes | Direct Regions | Dominant XOR | Normalized Changed Bytes | Normalized Regions |
| --- | ---: | ---: | ---: | ---: | ---: |
| `Program5.dat` | 168193 | 1 | `0x46` | 48 | 6 |
| `Program6.dat` | 168193 | 1 | `0x4a` | 64 | 8 |

After applying the dominant payload XOR value, all residual changes are inside the four target table slots. No residual outside-table changes were observed.

## Slot Results

| File | Slot | Baseline State | Modified State | Conclusion |
| --- | ---: | --- | --- | --- |
| `Program5.dat` | `0x105a0` ID reused slot | empty | `Hello`, ID 23654 | Reused cleared Individual ID slot. |
| `Program5.dat` | `0x10840` ID append slot | empty | ` UNIT ID 0031`, ID 43521 | Also appended a new Individual ID record. |
| `Program5.dat` | `0x150a0` TG reused slot | empty | `Goodbye`, TG 16432 | Reused cleared Talk Group slot. |
| `Program5.dat` | `0x15340` TG append slot | empty | empty | Did not append a TG record. |
| `Program6.dat` | `0x105a0` ID reused slot | empty | `Hello`, ID 23654 | Reused cleared Individual ID slot. |
| `Program6.dat` | `0x10840` ID append slot | empty | ` UNIT ID 0031`, ID 43521 | Appended Individual ID record remains present. |
| `Program6.dat` | `0x150a0` TG reused slot | empty | `Goodbye`, TG 16432 | Reused cleared Talk Group slot. |
| `Program6.dat` | `0x15340` TG append slot | empty | `GROUP ID 0031`, TG 15432 | Also appended a new Talk Group record. |

Plain-English answer:

- The new Individual ID reused the deleted empty slot at `0x105a0`.
- `Program5.dat` also contains an additional Individual ID at the append slot `0x10840`.
- The new Talk Group reused the deleted empty slot at `0x150a0`.
- `Program6.dat` also contains an additional Talk Group at the append slot `0x15340`.

This experiment shows that KPG111 can reuse deleted slots and can also append when another new record is added after the gap has been filled.

## Hex Evidence

All hex below is after payload-XOR normalization and uses decode key `0x1e`.

### Individual ID Reused Slot `0x105a0`

Baseline `Program3.dat`:

```text
e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1
e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1

Name: empty/non-printable
Numeric +19/+20 XOR 0x1e: ff ff, little-endian 65535
```

`Program5.dat` and `Program6.dat`:

```text
e1 56 7b 72 72 71 1e 1e 1e 1e 1e 1e 1e 1e 1e e1
e1 e1 e1 78 42 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1

Name +1..+14 XOR 0x1e: Hello
Numeric +19/+20 XOR 0x1e: 66 5c, little-endian 23654
```

### Individual ID Append Slot `0x10840`

Baseline `Program3.dat`:

```text
e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1
e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1
```

`Program5.dat` and `Program6.dat`:

```text
e1 3e 4b 50 57 4a 3e 57 5a 3e 2e 2e 2d 2f 1e e1
e1 e1 e1 1f b4 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1

Name +1..+14 XOR 0x1e:  UNIT ID 0031
Numeric +19/+20 XOR 0x1e: 01 aa, little-endian 43521
```

### Talk Group Reused Slot `0x150a0`

Baseline `Program3.dat`:

```text
e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1
e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1
```

`Program5.dat` and `Program6.dat`:

```text
e1 59 71 71 7a 7c 67 7b 1e 1e 1e 1e 1e 1e 1e e1
e1 e1 e1 2e 5e e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1

Name +1..+14 XOR 0x1e: Goodbye
Numeric +19/+20 XOR 0x1e: 30 40, little-endian 16432
```

### Talk Group Append Slot `0x15340`

Baseline `Program3.dat` and `Program5.dat`:

```text
e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1
e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1
```

`Program6.dat`:

```text
e1 59 4c 51 4b 4e 3e 57 5a 3e 2e 2e 2d 2f 1e e1
e1 e1 e1 56 22 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1

Name +1..+14 XOR 0x1e: GROUP ID 0031
Numeric +19/+20 XOR 0x1e: 48 3c, little-endian 15432
```

## Table Map Effects

Candidate table-map summaries:

| File | Individual ID Runs | Talk Group Runs |
| --- | --- | --- |
| `Program3.dat` baseline | `0x10480-0x1059f`, empty gap at `0x105a0`, then `0x105c0-0x1083f` | `0x14f80-0x1509f`, empty gap at `0x150a0`, then `0x150c0-0x1533f` |
| `Program5.dat` | `0x10480-0x1085f`, 31 occupied records | `0x14f80-0x1533f`, 30 occupied records |
| `Program6.dat` | `0x10480-0x1085f`, 31 occupied records | `0x14f80-0x1535f`, 31 occupied records |

Interpretation:

- Filling `0x105a0` merges the split Individual ID runs.
- Filling `0x10840` extends the Individual ID run by one record.
- Filling `0x150a0` merges the split Talk Group runs.
- Filling `0x15340` extends the Talk Group run by one record.

## Count, Index, Checksum-Like, Or Outside-Table Fields

No residual normalized changes were observed outside the target table records:

- `Program5.dat` residual ranges:
  - `0x105a1-0x105ae`, `0x105b3-0x105b4`
  - `0x10841-0x1084e`, `0x10853-0x10854`
  - `0x150a1-0x150ae`, `0x150b3-0x150b4`

- `Program6.dat` residual ranges:
  - all Program5 ranges
  - plus `0x15341-0x1534e`, `0x15353-0x15354`

These are exactly the name field `+1..+14` and numeric field `+19/+20` inside the target records. No separate count, index, checksum-like, header, tail, or outside-table field changed in these comparisons after XOR normalization.

This does not prove such fields do not exist; it only means this experiment did not produce observed changes in them.

## Generated Evidence Files

- `reports/xor_analysis.md`
- `reports/session_report.md`
- `reports/offset_spacing.md`
- `reports/Program5.target_slots.md`
- `reports/Program6.target_slots.md`
- `table_map.md`
- `reports/Program5.table_map.md`
- `reports/Program6.table_map.md`

No Program.dat files were generated or modified, and no writer was built.
