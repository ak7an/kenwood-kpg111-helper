# OpenKPG

OpenKPG is an open-source codeplug builder and maintenance toolkit for Kenwood NX-series radios.

Its purpose is to eliminate repetitive manual data entry by automating the creation and maintenance of KPG111D-compatible codeplugs while preserving complete compatibility with the official Kenwood programming software.

OpenKPG builds and maintains codeplugs.

Kenwood KPG111D remains the official application used to write those codeplugs to supported radios.

---

## Mission

The goal of OpenKPG is to simplify the creation and maintenance of Kenwood NX-series codeplugs.

Rather than replacing the Kenwood Customer Programming Software (CPS), OpenKPG complements it by providing modern tools for constructing, importing, validating, and maintaining codeplugs before they are opened in KPG111D.

The resulting DAT files are intended to:

- Open correctly in KPG111D.
- Remain editable in KPG111D.
- Program successfully into supported radios using the official Kenwood software.

---

## What OpenKPG Is

OpenKPG is designed to automate repetitive codeplug maintenance including:

- Building complete KPG111D-compatible DAT files.
- Importing RepeaterBook CSV files.
- Importing DVREF Talk Group lists.
- Importing Individual ID lists.
- Building channels.
- Building zones.
- Managing Talk Groups.
- Managing Individual IDs.
- Merge operations.
- Replace operations.
- Sorting.
- Name normalization.
- Validation.
- Report generation.

Every feature should reduce manual editing inside KPG111D.

---

## What OpenKPG Is Not

OpenKPG is NOT:

- a replacement for Kenwood KPG111D
- a clone of the Kenwood CPS
- a radio programming application

Programming radios remains the responsibility of the official Kenwood software.

---

## Supported Platforms

The OpenKPG engine is intended to support:

- Windows
- Debian Linux
- Ubuntu
- Raspberry Pi OS

A single code base should support every platform.

The graphical user interface shall use the same underlying OpenKPG engine regardless of operating system.

---

## Project Philosophy

Never guess.

Protect the user's existing codeplug.

Preserve compatibility with KPG111D.

Implement write support only after controlled experiments prove the file format.

Diagnostics precede implementation.

Safety, compatibility, and correctness are more important than feature count.

---

## Reverse Engineering Policy

Reverse engineering is performed only as necessary to safely implement OpenKPG codeplug builder features.

Reverse engineering supports implementation.

It is not the deliverable.

The deliverable is a practical, reliable, cross-platform codeplug builder.

---

## Development Priorities

1. Stable DAT reader.
2. Stable DAT writer.
3. Talk Group Manager.
4. Individual ID Manager.
5. RepeaterBook CSV Import.
6. Channel Builder.
7. Zone Builder.
8. Cross-platform GUI.
9. Additional reverse engineering only when required to implement the above features.

---

## Decision Filter

Before beginning any development work ask:

Does this directly improve OpenKPG's ability to build or maintain KPG111D-compatible codeplugs?

If YES:

Proceed.

If NO:

Do not implement it unless it directly supports one of the project's primary builder features.

---

## Current Status

OpenKPG is under active development.

The project has already proven numerous portions of the KPG111D DAT format through controlled experimentation.

Current development focuses on implementing practical codeplug-builder functionality using only verified knowledge of the file format.


Project Rules

Every feature implemented in OpenKPG shall satisfy the following principles:

1. Never guess.
2. Protect the user's existing codeplug.
3. Preserve compatibility with KPG111D.
4. Implement only behavior supported by controlled experiments.
5. Diagnostics precede implementation.
6. Builder functionality always takes priority over curiosity-driven reverse engineering.

OpenKPG exists to solve real programming problems.

---

Current Reverse Engineering Status

Much of the KPG111D DAT format has already been reverse engineered through controlled experimentation.

Confirmed discoveries include, but are not limited to:

- Talk Group record layout
- Individual ID record layout
- Multiple channel record fields
- Numerous allocation behaviors
- Header normalization behavior
- XOR normalization
- Controlled write validation
- Safe merge behavior
- Reserved record identification

Additional reverse engineering will be performed only when required to implement a builder feature.

---

Development Workflow

Every new feature follows the same workflow:

1. Identify a builder requirement.
2. Determine whether existing knowledge is sufficient.
3. Perform controlled experiments if additional information is required.
4. Implement the feature.
5. Validate against KPG111D.
6. Validate with automated tests.
7. Validate with actual radios whenever practical.

---

Contributing

Contributions are welcome.

Before implementing write support for undocumented portions of the DAT format:

- Create controlled experiments.
- Document findings.
- Validate conclusions.
- Avoid speculation.

Evidence always takes precedence over assumptions.

---

License

OpenKPG is released under the GNU General Public License Version 3 (GPLv3).

See the LICENSE file for details.


Roadmap

Near-Term Goals

- Complete stable DAT reader.
- Complete stable DAT writer.
- Finish Talk Group Manager.
- Finish Individual ID Manager.
- Finish RepeaterBook CSV importer.
- Finish Channel Builder.
- Finish Zone Builder.
- Complete validation framework.

Mid-Term Goals

- Cross-platform graphical user interface.
- Codeplug templates.
- Batch codeplug generation.
- Import/export profiles.
- Comprehensive reporting.
- Additional supported Kenwood models where practical.

Long-Term Goals

Provide an open-source toolkit capable of building and maintaining Kenwood codeplugs using a modern workflow while remaining compatible with the official Kenwood programming software.

---

Repository Organization

The repository is organized as follows:

    data/
        baseline/
        experiments/
        imports/
        normalized/

    docs/

    kpg111/

    tests/

    tools/

    README.md

    PROJECT_STATE.md

The data directory contains controlled experiments and reference datasets.

The tools directory contains diagnostics and builder utilities.

The tests directory contains automated validation.

---

Project Scope

OpenKPG focuses exclusively on building and maintaining compatible codeplugs.

The project intentionally avoids replacing the official Kenwood CPS.

Programming radios, firmware management, and radio servicing remain outside the scope of this project.

---

Acknowledgements

This project exists because of many hours of controlled experimentation, validation, and real-world testing using Kenwood NX-series radios.

Every verified discovery improves the reliability of the OpenKPG codeplug builder.


Frequently Asked Questions

Q: Does OpenKPG replace KPG111D?

A: No.

OpenKPG complements KPG111D.

OpenKPG builds and maintains compatible codeplugs.

KPG111D remains the official application used to write those codeplugs into supported radios.

---

Q: Will OpenKPG communicate directly with radios?

A: Not as a project objective.

The project's primary goal is reliable generation and maintenance of KPG111D-compatible DAT files.

---

Q: Why is reverse engineering included?

A: Because portions of the DAT format are undocumented.

Reverse engineering is performed only when necessary to safely implement a builder feature.

Every documented discovery is verified through controlled experimentation.

---

Q: Will additional Kenwood CPS formats be supported?

A: Possibly.

The long-term architecture is intended to separate the builder engine from individual CPS file formats.

Support for additional Kenwood formats will be considered after OpenKPG provides a mature implementation for KPG111D.

---

Design Principles

The OpenKPG engine should be modular.

Individual components should remain independent whenever practical.

Examples include:

    DAT Reader

    DAT Writer

    Builder Engine

    Validation Engine

    RepeaterBook Import

    Talk Group Import

    Individual ID Import

    Channel Builder

    Zone Builder

    Report Generator

    Cross-platform GUI

Keeping these components independent improves testing, maintainability, and future expansion.

---

Project Success Criteria

OpenKPG will be considered successful when a user can:

    Import a RepeaterBook CSV.

    Import a Talk Group list.

    Import an Individual ID list.

    Build a complete codeplug.

    Open the generated DAT in KPG111D.

    Make optional manual edits.

    Successfully program a supported Kenwood radio.

without repetitive manual data entry.

---

Thank you for supporting OpenKPG.

73,

AK7AN


Future Builder Modules

The OpenKPG architecture is intended to support additional builder modules over time.

Potential modules include:

    Contact Manager

    Scan List Manager

    FleetSync Manager

    MDC-1200 Manager

    Signaling Manager

    Conventional Personality Builder

    NXDN Personality Builder

    Fleet Mapping Utilities

    Batch Codeplug Builder

    Template Manager

These modules will be developed only after the core builder engine is considered stable.

---

Engineering Philosophy

OpenKPG favors correctness over speed.

Every builder feature should be:

    Predictable

    Reproducible

    Testable

    Backward compatible whenever practical

Builder code should be understandable by future contributors without requiring knowledge of undocumented behavior.

Whenever possible:

    Discover

    Verify

    Implement

    Test

    Document

in that order.

---

Testing Requirements

Builder features should include:

    Unit tests

    Integration tests

    Controlled DAT comparisons

    Validation against KPG111D

    Validation on physical radios whenever practical

The objective is confidence rather than assumptions.

---

Repository Standards

Source code should remain portable.

Avoid operating-system-specific implementations whenever practical.

Builder logic should remain independent of the graphical interface.

The GUI is a client of the OpenKPG engine.

The command-line tools are also clients of the OpenKPG engine.

There should be a single implementation of the builder logic.

---

Versioning

OpenKPG follows semantic versioning whenever practical.

Major versions represent significant builder capability.

Minor versions add compatible functionality.

Patch releases correct defects without changing intended behavior.

---

Closing Statement

OpenKPG exists to make maintaining Kenwood NX-series codeplugs easier, safer, faster, and more reliable while remaining fully compatible with the official Kenwood programming software.

The project values verified engineering over speculation and practical builder functionality over unnecessary complexity.


Appendix A - Guiding Principles

OpenKPG shall always favor:

    Verified behavior over assumed behavior.

    Builder functionality over unnecessary complexity.

    Compatibility over convenience.

    Safety over speed.

Every modification to a DAT file should be explainable, repeatable, and supported by documented evidence.

---

Appendix B - Supported Builder Inputs

Planned supported input formats include:

    RepeaterBook CSV

    DVREF Talk Group CSV

    Individual ID CSV

    OpenKPG project files

    Existing KPG111D DAT files

Additional import formats may be added as practical without compromising the primary project goals.

---

Appendix C - Supported Builder Outputs

Primary output:

    KPG111D-compatible DAT files

Additional reports may include:

    Validation reports

    Duplicate reports

    Import summaries

    Merge summaries

    Builder statistics

---

Final Statement

OpenKPG is an engineering project with a practical objective.

The measure of success is not how much of the KPG111D file format has been reverse engineered.

The measure of success is whether OpenKPG can reliably build and maintain KPG111D-compatible codeplugs that open correctly in KPG111D and can be successfully programmed into supported Kenwood NX-series radios.

The project will remain focused on delivering practical builder capabilities while preserving compatibility, reliability, and user confidence.

