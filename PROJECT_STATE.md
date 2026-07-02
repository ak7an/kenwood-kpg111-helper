# OpenKPG Project State

Repository

    ~/dev/kenwood-kpg111-helper

GitHub

    https://github.com/ak7an/kenwood-kpg111-helper

Branch

    main

Project Mission
---------------

OpenKPG is an open-source codeplug builder and maintenance toolkit for Kenwood NX-series radios.

The purpose of OpenKPG is to eliminate repetitive manual data entry by automating the creation and maintenance of KPG111D-compatible codeplugs while preserving complete compatibility with the official Kenwood programming software.

OpenKPG builds and maintains codeplugs.

Kenwood KPG111D remains the official application used to write those codeplugs into supported radios.

Project Objectives
------------------

Primary objectives are:

- Build KPG111D-compatible DAT codeplugs.
- Import RepeaterBook CSV files.
- Import DVREF Talk Group lists.
- Import Individual ID lists.
- Build channels.
- Build zones.
- Merge existing programming.
- Replace programming when requested.
- Normalize imported data.
- Validate generated codeplugs.
- Produce useful reports.

Every implemented feature should reduce manual editing inside KPG111D.

What OpenKPG Is Not
-------------------

OpenKPG is NOT:

- A replacement for Kenwood KPG111D.
- A clone of the Kenwood CPS.
- A radio programming application.

Programming radios remains the responsibility of the official Kenwood software.

Supported Platforms
-------------------

The OpenKPG engine shall support:

- Windows
- Debian Linux
- Ubuntu
- Raspberry Pi OS

One code base shall support every operating system.

The GUI shall use the same builder engine on every supported platform.

Project Philosophy
------------------

Never guess.

Protect the user's existing codeplug.

Preserve compatibility with KPG111D.

Diagnostics precede implementation.

Builder functionality always has priority over curiosity-driven reverse engineering.

Safety, compatibility, and correctness are more important than feature count.

Reverse Engineering Policy
--------------------------

Reverse engineering is performed only as necessary to safely implement OpenKPG codeplug builder features.

Every write operation shall be supported by controlled experiments.

Only proven discoveries shall be implemented.


Decision Filter
---------------

Before beginning any development work ask:

    Does this directly improve OpenKPG's ability to build or maintain
    KPG111D-compatible codeplugs?

If YES:

    Proceed.

If NO:

    Defer the work unless it directly supports a required builder feature.

Development Priorities
----------------------

Current priorities are:

1. Stable DAT reader.

2. Stable DAT writer.

3. Talk Group Manager.

4. Individual ID Manager.

5. RepeaterBook CSV Import.

6. Channel Builder.

7. Zone Builder.

8. Cross-platform GUI.

9. Additional reverse engineering only when required to implement one
   of the above builder features.

Current Status
--------------

OpenKPG is under active development.

The repository has evolved from a collection of reverse-engineering
utilities into the foundation of a practical codeplug builder.

Reverse engineering continues only when additional knowledge is required
to safely implement builder functionality.

Current development is focused on producing reliable
KPG111D-compatible DAT files that can be opened, edited, and programmed
using the official Kenwood software.

Repository Organization
-----------------------

Primary repository layout:

    data/
        baseline/
        experiments/
        imports/
        normalized/

    docs/

    kpg111/

    tests/

    tools/

Supporting directories contain controlled experiments, diagnostics,
builder utilities, and automated tests.


Current Proven Discoveries
--------------------------

The following discoveries have been verified through controlled
experiments and may be safely relied upon by OpenKPG.

Talk Group Records

Confirmed:

- Fixed record size.
- Verified record layout.
- Verified numeric field location.
- Verified Talk Group numeric encoding.
- Verified name field location.
- Verified controlled write behavior.

Individual ID Records

Confirmed:

- Fixed record size.
- Verified record layout.
- Verified numeric field location.
- Verified name field location.
- Controlled edits affect only expected fields.

Channel Records

Confirmed:

- Fixed record layout.
- Multiple frequency field locations identified.
- Numerous channel attributes mapped.
- Controlled edits modify only expected bytes.

General DAT Behavior

Confirmed:

- Payload normalization behavior.
- Header stability.
- XOR normalization techniques.
- Controlled write validation.
- Safe merge behavior.
- Reserved record identification.
- Multiple allocation behaviors.

Current Reverse Engineering Status
----------------------------------

The repository contains numerous controlled experiments documenting the
current understanding of the KPG111D DAT format.

Reverse engineering efforts shall remain narrowly focused on supporting
builder features.

No investigation shall be undertaken solely because it is interesting.

Unknown portions of the DAT format shall remain undocumented until
supported by controlled experimentation.

Builder Features In Progress
----------------------------

Current builder work includes:

- DAT reader refinement.
- DAT writer implementation.
- Talk Group Manager.
- Individual ID Manager.
- RepeaterBook CSV importer.
- Channel Builder.
- Zone Builder.
- Validation framework.
- Cross-platform GUI planning.


Diagnostic Tools
----------------

Diagnostic tools exist to support builder development.

Their purpose is to verify hypotheses before implementation.

Current diagnostics include:

    tools/layout_diff_analysis.py

    tools/layout_trigger_check.py

    tools/diagnose_tg_table.py

    tools/diagnose_individual_id.py

    tools/dat_allocation_analysis.py

    tools/frequency_full_diff_ladder.py

    tools/frequency_bit_dependency.py

    tools/frequency_lookup_hypothesis.py

These tools are intended to remain read-only whenever practical.

Builder implementation should consume verified results rather than
performing experimental analysis during normal operation.

Controlled Experiment Workflow
------------------------------

Every unknown field shall follow the same workflow.

1. Create a baseline DAT.

2. Modify exactly one CPS setting.

3. Save the modified DAT.

4. Normalize metadata changes.

5. Compare against the baseline.

6. Identify changed bytes.

7. Develop a read-only diagnostic.

8. Confirm or reject the hypothesis.

9. Implement builder support only after the behavior has been proven.

This workflow has produced the current verified understanding of the
KPG111D DAT format and remains the standard for future investigations.

Development Rules
-----------------

Before implementing any builder feature:

- Verify the required DAT structures.
- Preserve existing programming whenever possible.
- Never overwrite unknown data.
- Never rely on assumptions.
- Validate generated DAT files using KPG111D.
- Validate on actual radios whenever practical.

Builder functionality shall never depend upon undocumented behavior
unless that behavior has first been verified through controlled
experimentation.


Outstanding Work
----------------

The following work remains before OpenKPG reaches its primary objectives.

DAT Engine

- Complete stable DAT reader.
- Complete stable DAT writer.
- Preserve unknown records during write operations.
- Validate generated DAT files against KPG111D.

Builder Modules

- Complete Talk Group Manager.
- Complete Individual ID Manager.
- Complete RepeaterBook CSV importer.
- Complete Channel Builder.
- Complete Zone Builder.

Validation

- Expand automated test coverage.
- Increase controlled experiment coverage.
- Validate builder output against multiple codeplug layouts.
- Validate builder output on supported radios.

Graphical User Interface

The GUI shall remain a client of the OpenKPG engine.

The GUI shall provide:

- Open DAT
- Save DAT
- Import RepeaterBook CSV
- Import Talk Groups
- Import Individual IDs
- Channel Builder
- Zone Builder
- Merge
- Replace
- Sort
- Normalize
- Validation
- Report generation

The GUI shall not duplicate builder logic.

All builder functionality shall remain inside the OpenKPG engine.

Future Direction
----------------

The long-term objective is to provide an open-source toolkit capable of
building and maintaining Kenwood NX-series codeplugs while remaining
fully compatible with the official Kenwood programming software.

Future support for additional Kenwood CPS formats may be considered
after the KPG111D implementation is mature.

Success Criteria
----------------

OpenKPG will be considered successful when a user can:

- Import a RepeaterBook CSV.
- Import a Talk Group list.
- Import an Individual ID list.
- Build a complete KPG111D-compatible codeplug.
- Open the generated DAT in KPG111D.
- Optionally make manual edits in KPG111D.
- Successfully program a supported Kenwood radio.

without repetitive manual data entry.

Closing Statement
-----------------

OpenKPG is a practical engineering project.

Its success will not be measured by the amount of reverse engineering
performed.

Its success will be measured by its ability to reliably build and
maintain KPG111D-compatible codeplugs that reduce manual effort while
preserving compatibility with the official Kenwood programming software.

