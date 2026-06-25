# KPG111 Allocation Analysis

This report is read-only. It analyzes existing `.dat` variants under `research/` and does not write or modify `Program.dat`.

## Inputs

| Experiment | Baseline | Modified | Baseline Key | Modified Key | Source |
| --- | --- | --- | --- | --- | --- |
| dattest | research/dattest/Dattest/AK7AN_Travel.dat | research/dattest/Dattest/Program_1TG.dat | 0x5b | 0x65 | research/dattest/reports/xor_analysis.json |
| dattest | research/dattest/Dattest/AK7AN_Travel.dat | research/dattest/Dattest/Program_1ID.dat | 0x5b | 0x57 | research/dattest/reports/xor_analysis.json |
| dattest | research/dattest/Dattest/AK7AN_Travel.dat | research/dattest/Dattest/Program_Rename.dat | 0x5b | 0x3c | research/dattest/reports/xor_analysis.json |
| dattest | research/dattest/Dattest/AK7AN_Travel.dat | research/dattest/Dattest/Program_Delete.dat | 0x5b | 0x45 | research/dattest/reports/xor_analysis.json |
| dattest2 | research/dattest2/Dattest2/Program_Nochange1.dat | research/dattest2/Dattest2/Program_Nochange2.dat | 0x34 | 0x40 | research/dattest2/reports/xor_analysis.json |
| dattest2 | research/dattest2/Dattest2/Program_Nochange1.dat | research/dattest2/Dattest2/Program_Nochange3.dat | 0x34 | 0x48 | research/dattest2/reports/xor_analysis.json |
| dattest2 | research/dattest2/Dattest2/Program_Nochange1.dat | research/dattest2/Dattest2/Program_TG_00001.dat | 0x34 | 0x4c | research/dattest2/reports/xor_analysis.json |
| dattest2 | research/dattest2/Dattest2/Program_Nochange1.dat | research/dattest2/Dattest2/Program_TG_00100.dat | 0x34 | 0x3f | research/dattest2/reports/xor_analysis.json |
| dattest2 | research/dattest2/Dattest2/Program_Nochange1.dat | research/dattest2/Dattest2/Program_TG_12345.dat | 0x34 | 0x2c | research/dattest2/reports/xor_analysis.json |
| dattest2 | research/dattest2/Dattest2/Program_Nochange1.dat | research/dattest2/Dattest2/Program_TG_65516.dat | 0x34 | 0x27 | research/dattest2/reports/xor_analysis.json |
| dattest2 | research/dattest2/Dattest2/Program_Nochange1.dat | research/dattest2/Dattest2/Program_ID_00001.dat | 0x34 | 0x51 | research/dattest2/reports/xor_analysis.json |
| dattest2 | research/dattest2/Dattest2/Program_Nochange1.dat | research/dattest2/Dattest2/Program_ID_00100.dat | 0x34 | 0x3e | research/dattest2/reports/xor_analysis.json |
| dattest2 | research/dattest2/Dattest2/Program_Nochange1.dat | research/dattest2/Dattest2/Program_ID_12345.dat | 0x34 | 0x2c | research/dattest2/reports/xor_analysis.json |
| dattest2 | research/dattest2/Dattest2/Program_Nochange1.dat | research/dattest2/Dattest2/Program_ID_65519.dat | 0x34 | 0x56 | research/dattest2/reports/xor_analysis.json |
| dattest3 | research/dattest3/Dattest3/Program.dat | research/dattest3/Dattest3/Program1.dat | 0x1f | 0x30 | research/dattest3/reports/xor_analysis.json |
| dattest3 | research/dattest3/Dattest3/Program.dat | research/dattest3/Dattest3/Program2.dat | 0x1f | 0x34 | research/dattest3/reports/xor_analysis.json |
| dattest3 | research/dattest3/Dattest3/Program.dat | research/dattest3/Dattest3/Program3.dat | 0x1f | 0x1e | research/dattest3/reports/xor_analysis.json |
| dattest3 | research/dattest3/Dattest3/Program.dat | research/dattest3/Dattest3/Program4.dat | 0x1f | 0x1f | research/dattest3/reports/xor_analysis.json |
| dattest4 | research/dattest4/Dattest4/Program3.dat | research/dattest4/Dattest4/Program5.dat | 0x1e | 0x58 | research/dattest4/reports/xor_analysis.json |
| dattest4 | research/dattest4/Dattest4/Program3.dat | research/dattest4/Dattest4/Program6.dat | 0x1e | 0x54 | research/dattest4/reports/xor_analysis.json |
| dattest4 | research/dattest4/Dattest4/Program5.dat | research/dattest4/Dattest4/Program6.dat | 0x58 | 0x54 | research/dattest4/README.md sequential Program5-to-Program6 observation |

## Observed Allocation Sequence

Rows are ordered by experiment comparison and slot. When one modified file contains multiple newly occupied records, the file does not prove the UI creation order.

| Experiment | Modified | Table | Slot | Offset | Name | Numeric ID | Previous Slot State | Previous Neighbor | Next Neighbor | Distance From Previous Occupied | Distance From Next Occupied | Candidate Policies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dattest | Program_1TG.dat | Talk Groups | 17 | 0x000151a0 | GPTTest1 | 65001 | empty | slot 16 occupied AK7AN TG (21277) | slot 18 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest | Program_1ID.dat | Individual IDs | 14 | 0x00010640 | Bradley | 7497 | empty | slot 13 occupied NX4DX BitbyBit (10417) | slot 15 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest | Program_1ID.dat | Talk Groups | 17 | 0x000151a0 | GPTTest1 | 65001 | empty | slot 16 occupied AK7AN TG (21277) | slot 18 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest2 | Program_TG_00001.dat | Talk Groups | 17 | 0x000151a0 | TG Test 00001 | 1 | empty | slot 16 occupied AK7AN TG (21277) | slot 18 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest2 | Program_TG_00100.dat | Talk Groups | 17 | 0x000151a0 | TG Test 00100 | 100 | empty | slot 16 occupied AK7AN TG (21277) | slot 18 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest2 | Program_TG_12345.dat | Talk Groups | 17 | 0x000151a0 | TG Test 12345 | 12345 | empty | slot 16 occupied AK7AN TG (21277) | slot 18 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest2 | Program_TG_65516.dat | Talk Groups | 17 | 0x000151a0 | TG Test 65519 | 65519 | empty | slot 16 occupied AK7AN TG (21277) | slot 18 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest2 | Program_ID_00001.dat | Individual IDs | 14 | 0x00010640 | ID_Test_00001 | 1 | empty | slot 13 occupied NX4DX BitbyBit (10417) | slot 15 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest2 | Program_ID_00100.dat | Individual IDs | 14 | 0x00010640 | ID_Test_00100 | 100 | empty | slot 13 occupied NX4DX BitbyBit (10417) | slot 15 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest2 | Program_ID_12345.dat | Individual IDs | 14 | 0x00010640 | ID_Test_12345 | 12345 | empty | slot 13 occupied NX4DX BitbyBit (10417) | slot 15 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest2 | Program_ID_65519.dat | Individual IDs | 14 | 0x00010640 | ID_Test_65519 | 65519 | empty | slot 13 occupied NX4DX BitbyBit (10417) | slot 15 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest4 | Program5.dat | Individual IDs | 9 | 0x000105a0 | Hello | 23654 | empty | slot 8 occupied Doug, W4DBG (1044) | slot 10 occupied Randy, W8EJC (39828) | 1 | 1 | lowest available slot, first empty slot |
| dattest4 | Program5.dat | Individual IDs | 30 | 0x00010840 |  UNIT ID 0031 | 43521 | empty | slot 29 occupied  UNIT ID 0030 (54345) | slot 31 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest4 | Program5.dat | Talk Groups | 9 | 0x000150a0 | Goodbye | 16432 | empty | slot 8 occupied NXDN N America (10200) | slot 10 occupied Utah DRN 01 (31491) | 1 | 1 | lowest available slot, first empty slot |
| dattest4 | Program6.dat | Individual IDs | 9 | 0x000105a0 | Hello | 23654 | empty | slot 8 occupied Doug, W4DBG (1044) | slot 10 occupied Randy, W8EJC (39828) | 1 | 1 | lowest available slot, first empty slot |
| dattest4 | Program6.dat | Individual IDs | 30 | 0x00010840 |  UNIT ID 0031 | 43521 | empty | slot 29 occupied  UNIT ID 0030 (54345) | slot 31 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest4 | Program6.dat | Talk Groups | 9 | 0x000150a0 | Goodbye | 16432 | empty | slot 8 occupied NXDN N America (10200) | slot 10 occupied Utah DRN 01 (31491) | 1 | 1 | lowest available slot, first empty slot |
| dattest4 | Program6.dat | Talk Groups | 30 | 0x00015340 | GROUP ID 0031 | 15432 | empty | slot 29 occupied GROUP ID 0030 (64421) | slot 31 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |
| dattest4 | Program6.dat | Talk Groups | 30 | 0x00015340 | GROUP ID 0031 | 15432 | empty | slot 29 occupied GROUP ID 0030 (64421) | slot 31 empty | 1 | none | lowest available slot, first empty slot, append after last occupied |

## Evidence Table

| Assessment | Matching Events | Counterexamples | Confidence | Notes |
| --- | --- | --- | --- | --- |
| observed first available empty record in slot order | 19 | 0 | HIGH | Observed behavior is consistent with selecting the first available empty record in slot order. |
| sequential scan implementation | 19 | 0 | MODERATE | Current experiments do not distinguish this mechanism from other implementations that produce the same observable result. |
| lowest-available-slot implementation | 19 | 0 | MODERATE | Current experiments do not distinguish this mechanism from other implementations that produce the same observable result. |
| append after last occupied | 15 | 4 | MODERATE | Some observed allocations are consistent with this policy, but counterexamples exist. |
| bitmap allocation | 0 | 19 | LOW | No current experiment identifies evidence for this policy. |
| free list | 0 | 19 | LOW | No current experiment identifies evidence for this policy. |
| unknown | 0 | 19 | LOW | Used only when an allocation does not match first-empty/lowest-available/append evidence. |

## Candidate Allocation Policy

Observed behavior is consistent with selecting the first available empty record in slot order. Current experiments do not distinguish between a sequential scan, a lowest-available-slot rule, or another implementation that produces the same observable result. Append-after-last-occupied is observed when the selected slot is immediately after the occupied run, but Dattest4 provides counterexamples to an append-only explanation because cleared interior slots are reused. No bitmap or free-list structure has been identified in current evidence.

## Counterexamples

| Policy | Experiment | Modified | Table | Slot | Offset | Observed Candidate Policies |
| --- | --- | --- | --- | --- | --- | --- |
| append after last occupied | dattest4 | Program5.dat | Individual IDs | 9 | 0x000105a0 | lowest available slot, first empty slot |
| append after last occupied | dattest4 | Program5.dat | Talk Groups | 9 | 0x000150a0 | lowest available slot, first empty slot |
| append after last occupied | dattest4 | Program6.dat | Individual IDs | 9 | 0x000105a0 | lowest available slot, first empty slot |
| append after last occupied | dattest4 | Program6.dat | Talk Groups | 9 | 0x000150a0 | lowest available slot, first empty slot |

## Unknowns

- Program files do not prove UI operation order when multiple records appear in one modified file.
- No allocation bitmap, free list, count field, or pointer table has been identified.
- Maximum table capacity and complete table boundaries remain unresolved.
- The current evidence cannot distinguish lowest-available from first-empty scanning when they select the same slot.
- Append behavior is observed, but not enough to prove the general rule for full tables or multiple gaps.

## Conclusion

The observed newly occupied records are consistent with selecting the first available empty record in slot order. Observed behavior confidence is HIGH for the current events because every newly occupied slot matches that result. Implementation mechanism confidence remains MODERATE because the experiments do not prove whether KPG111 uses a sequential scan, a lowest-available-slot rule, or another mechanism with the same visible output. General production confidence remains limited by unresolved table capacity, metadata, pointer/index structures, and multi-gap behavior.
