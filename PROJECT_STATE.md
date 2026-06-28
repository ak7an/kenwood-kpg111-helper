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

