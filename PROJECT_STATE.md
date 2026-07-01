# OpenKPG / Kenwood KPG111 Reverse Engineering Project

Repository:
    ~/dev/kenwood-kpg111-helper

GitHub:
    https://github.com/ak7an/kenwood-kpg111-helper

Branch:
    main

Project Goal
------------

Develop an open-source library and tools capable of reading, modifying, and eventually writing valid Kenwood KPG111 (.DAT) codeplugs.

The original goal was bulk importing DVREF NXDN Talk Groups.

The project has evolved into complete reverse engineering of the KPG111 DAT format.

Project Philosophy
------------------

Never guess.

Every modification must be supported by controlled KPG111-generated DAT experiments.

Read-only diagnostics are preferred over speculative importer changes.


Current Proven Facts
--------------------

Talk Group Table

Confirmed:

- Physical partition contains 400 records.
- Record size is 32 bytes.
- Physical table begins at 0x14F80.

Physical layout:

    0-199      Occupied
    200-299    Empty
    300-342    Occupied
    343-350    Empty
    351-353    Reserved / Invalid
    354-399    Empty

Safe insertion slots:

    200-299
    343-350
    354-399

Never write:

    300-342
    351-353


DVREF Import Status
-------------------

Merge importer now:

- Preserves existing TGs
- Inserts only into safe empty slots
- Never overwrites reserved slots
- Removes TG-number prefixes from imported names

Replace mode is disabled unless explicitly enabled as experimental.

Validation:

- Codeplug opens correctly in KPG111.
- Loads into radio successfully.
- Radio functions correctly.

Remaining work:

- Normalize existing TG names to current DVREF naming.
- Understand logical TG ordering.
- Design a safe rebuild/replace mode.


Frequency Reverse Engineering
-----------------------------

Known:

Channel table:

    Start  : 0x5E80
    Stride : 0x40

Zone 1 Channel 2:

    Record : 0x5EC0

RX Frequency Field:

    Offset : +0x05
    Length : 3 bytes

Controlled experiments prove:

Only bytes

    0x5EC5
    0x5EC6
    0x5EC7

change when RX frequency changes.

No other normalized bytes in the DAT file change.


Frequency Hypotheses Eliminated
-------------------------------

The following have been disproven:

- Big-endian integer
- Little-endian integer
- Scaled integer
- BCD
- Decimal nibble encoding
- Direct frequency-step index
- Direct Gray code
- Reflected Gray code
- Binary bit permutation
- Gray bit permutation
- Simple XOR whitening
- Simple LFSR
- Simple affine GF(2)

Still plausible:

- Proprietary packed 24-bit encoding
- Lookup/index encoding
- Multi-stage transform
- Non-linear bit transformation

No proven frequency formula currently exists.


Diagnostic Tools
----------------

Read-only diagnostics:

tools/frequency_lookup_hypothesis.py

tools/frequency_full_diff_ladder.py

tools/frequency_bit_dependency.py

tools/diagnose_tg_table.py

These tools exist only for reverse engineering.

Project Rules
-------------

Before changing code:

1. Create controlled DAT files.
2. Compare against baseline.
3. Write a diagnostic.
4. Prove or disprove the hypothesis.
5. Only then modify importer behavior.

Do not restart already disproven investigations.

Read this file before beginning a new ChatGPT session.


Reverse Engineering Method
--------------------------

Every unknown field follows the same workflow:

1. Create baseline DAT.
2. Modify exactly one CPS setting.
3. Save new DAT.
4. Normalize changing metadata.
5. Diff against baseline.
6. Identify changed bytes.
7. Build read-only diagnostic.
8. Prove or disprove hypotheses.
9. Never implement write support until proven.

The repository values reproducible experiments over speculation.


Talk Group Numeric ID Encoding Discovery
----------------------------------------

Confirmed by controlled KPG111 experiment:

File pair:

- AK7AN_Travel_400TG_Normalized.dat
- AK7AN_Travel_400TG_Edit_31490_to_31491.dat

Procedure:

- Opened normalized DAT in KPG111.
- Changed exactly one visible Talk Group number:
  31490 -> 31491
- Saved as a new DAT.
- Normalized payload XOR before diffing.

Result:

Only one byte changed after normalization:

- TG physical slot: 289
- Absolute offset: 0x173b3
- Record-relative offset: +0x13
- Before: 0x53
- After:  0x52

The record's +0x13/+0x14 field changed from:

- 0x2a53 little-endian for TG 31490
- 0x2a52 little-endian for TG 31491

Derived encoding:

    stored_tg_id = tg_id ^ 0x5151
    tg_id = stored_tg_id ^ 0x5151

Field location:

    record +0x13..+0x14
    little-endian uint16 XOR 0x5151

Full-file validation:

All numeric-prefixed Talk Group names in AK7AN_Travel_400TG_Normalized.dat
matched this encoding with zero mismatches.

Important consequence:

A byte value of 0xAE inside the numeric field is valid encoded data.
It must not be interpreted as an empty byte by itself.

Example:

    TG 23551
    23551 ^ 0x5151 = 0x0aae
    stored little-endian = ae 0a

Therefore slot 285 is a valid Talk Group record, not malformed.

Do not generalize this rule to Individual IDs yet.
The controlled experiment only proves Talk Group numeric encoding for this KPG111 DAT format.


Talk Group Table Start / Capacity Discovery
-------------------------------------------

New controlled ladder experiment:

Starting file:

- AK7AN_Blank.dat

KPG111-created ladder files:

- AK7AN_TG_Ladder_001.dat
- AK7AN_TG_Ladder_002.dat
- AK7AN_TG_Ladder_003.dat
- AK7AN_TG_Ladder_010.dat

Procedure:

- Created 1, 2, 3, and 10 Talk Groups in KPG111.
- Used default KPG111 Talk Group names.
- Normalized payload XOR before diffing each ladder file against blank.

Result:

Each added Talk Group changed exactly:

- 14 name bytes at record +0x01..+0x0e
- 2 numeric bytes at record +0x13..+0x14

The first ladder TG appears at:

    0x14940

Record spacing is:

    0x20 bytes

Therefore for the blank/default ladder DAT, KPG111 writes the Talk Group table at:

    0x14940

This disproves the assumption that the Talk Group table always begins at:

    0x14f80

Important consequence:

Talk Group table start is DAT-layout dependent and must not be hardcoded.

The earlier AK7AN travel/imported DAT contains a long contiguous sequence of valid
Talk Group records that can be recognized at many shifted 32-byte-aligned windows.
Record-shape scanning alone cannot prove the true table start, because any shifted
window inside a dense TG table also appears valid.

A metadata/partition descriptor likely determines actual logical table start and
capacity, but direct searches for raw little-endian values 0x14940, 0x14f80,
397, 400, 340, 400*32, and 340*32 did not find an obvious plaintext descriptor.

Current proven record layout remains:

    record +0x01..+0x0e : encoded name
    record +0x13..+0x14 : TG numeric ID, uint16 little-endian XOR 0x5151

OpenKPG next direction:

- Stop treating TALK_GROUP_TABLE_START as a universal constant.
- Add diagnostics to infer or discover table locations from DAT structure.
- Do not modify importer write behavior until table-start discovery is proven.


Individual ID Table Discovery
-----------------------------

Controlled experiments:

- AK7AN_Blank.dat
- AK7AN_Blank_OneIndividualID.dat
- AK7AN_Blank_OneIndividualID_EditNumber.dat
- AK7AN_Blank_TwoIndividualIDs.dat

Confirmed:

- First Individual ID record begins at:

      0x11D80

  in the blank-layout DAT.

- Record size:

      32 bytes

- Adding a second Individual ID creates the next record exactly
  one record later:

      0x11DA0

- Record layout matches the Talk Group record structure:

      +0x01..+0x0E   Name
      +0x13..+0x14   Numeric Individual ID

Controlled edit of only the Individual ID number changed only:

      +0x13..+0x14

Strong evidence indicates the numeric field uses the same
little-endian XOR 0x5151 encoding as Talk Groups.

A final controlled increment/decrement experiment should be
performed before declaring the encoding fully proven.

