# KPG111 Helper Project Philosophy

This project exists to make KPG111 `Program.dat` research safer, more repeatable, and easier to audit. The project must not write `Program.dat`, build a writer, or modify research files until the evidence and validation gates support that work.

## Core Principles

- Evidence over assumptions: format claims must be backed by controlled experiments, reports, tests, or decoded artifacts.
- Read-only before read-write: inspection, decoding, validation, comparison, and planning come before any binary output work.
- Experiments before implementation: new format behavior should be observed and documented before code depends on it.
- Unknowns are documented, not ignored: unresolved metadata, count fields, checksums, pointers, and capacity rules remain explicit blockers.
- Never modify unknown bytes: any future binary output must preserve bytes that are not proven safe to change.
- Fail closed: uncertainty, validation errors, ambiguous allocation, or unexpected bytes must stop the workflow.
- KPG111 validation before radio validation: generated files, if a future writer ever exists, must pass KPG111 before they are considered for radio use.

## Project Safety Rules

- No generated file is trusted until it decodes correctly.
- No generated file is trusted until KPG111 opens it without warnings.
- No generated file goes to a radio until a rollback path exists.
- Original `Program.dat` files are never overwritten.
- Research inputs remain immutable.
- Writer work remains blocked while metadata, checksum, capacity, and KPG111/radio validation are unresolved.

## Development Workflow

1. Run experiment.
2. Update evidence matrix.
3. Update writer design if needed.
4. Add or adjust tests.
5. Only then modify implementation.

Implementation should follow the documented evidence rather than expand the supported format by guesswork. When new behavior is found, the evidence and design documents should move first so code changes have a clear safety boundary.

## Current Phase Summary

| Area | Status |
| --- | --- |
| Reverse engineering foundation | complete |
| Read-only toolkit | complete |
| Evidence matrix | complete |
| Writer design | complete |
| Writer implementation | not started |
| KPG111/radio validation | not started |

The current project state supports read-only analysis and planning. It does not support generating or modifying `Program.dat` files.
