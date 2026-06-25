# KPG111 Writer Design Specification

This document is an architecture and validation specification only. It does not implement a writer, does not write `Program.dat`, and does not modify research files.

The current evidence base supports read-only decoding, comparison, planning, and CSV workflows. Binary writing remains blocked until the unknown metadata, checksum, table-capacity, and validation requirements are resolved.

## Pipeline Overview

```text
Program.dat
  |
  v
Decode
  |
  v
Validate
  |
  v
Import CSV
  |
  v
Plan Merge
  |
  v
Allocate Records
  |
  v
Encode Records
  |
  v
Rebuild Binary
  |
  v
Internal Validation
  |
  v
KPG111 Validation
  |
  v
Radio Validation
```

The intended production behavior is fail-closed. If any stage fails, the process aborts and no `Program.dat` is emitted.

## Stage Specifications

### Program.dat Input

- Purpose: Accept one known-good source codeplug file as the immutable baseline.
- Inputs: Existing `Program.dat` path, expected file size if known, expected KPG111 version/layout profile if known.
- Outputs: Read-only byte buffer plus file metadata such as path, size, hash, and header observations.
- Failure conditions: Missing file, unreadable file, unexpected size, unsupported header/version, unsupported model/layout, mutable output path equal to input path.
- Safety checks: Open read-only; hash before processing; reject in-place output; reject unknown KPG111 versions until layout compatibility is proven.

### Decode

- Purpose: Convert supported table regions into structured records without changing bytes.
- Inputs: Read-only byte buffer, table map, active XOR/decode profile, record layout definition.
- Outputs: Decoded Individual ID records, Talk Group records, empty-slot observations, and raw record byte references.
- Failure conditions: Unknown decode key, unexpected table offset, malformed record, undecodable name, numeric field outside expected range, ambiguous occupied/empty state.
- Safety checks: Keep raw bytes attached to each decoded record; preserve unknown bytes unchanged; reject records outside proven table regions.

### Validate

- Purpose: Establish that the source file is internally consistent before any merge is planned.
- Inputs: Decoded records, raw byte buffer, table map, evidence profile, optional expected counts.
- Outputs: Validation report and a pass/fail decision.
- Failure conditions: Duplicate numeric IDs, duplicate names when not explicitly allowed, table overlap, record outside candidate boundaries, unknown metadata changes, unsupported table size, decode mismatch.
- Safety checks: Validate table alignment, 32-byte record boundaries, name field `+1..+14`, numeric field `+19/+20`, empty-slot representation, and source-file hash stability.

### Import CSV

- Purpose: Load requested user changes from CSV into typed records.
- Inputs: CSV files for Individual IDs and Talk Groups, import schema, duplicate-name policy.
- Outputs: Parsed import rows and row-level validation diagnostics.
- Failure conditions: Missing required columns, malformed numeric ID, invalid table name, invalid name length, unsupported characters, duplicate rows, duplicate numeric IDs, duplicate names when not explicitly allowed.
- Safety checks: Treat CSV as desired state or patch input only after explicit mode selection; normalize whitespace consistently; preserve source line numbers in diagnostics.

### Plan Merge

- Purpose: Compare decoded source records with imported rows and produce a deterministic merge plan.
- Inputs: Decoded source tables, parsed CSV rows, merge mode, duplicate policy.
- Outputs: Add, update, keep, delete, and conflict actions with target table and logical key.
- Failure conditions: Conflicting changes, duplicate numeric IDs, duplicate names when disallowed, delete requested for unknown record, update requested for multiple matching records, planner output depends on unstable ordering.
- Safety checks: Plan before allocation; show every action; require zero conflicts; ensure planner output can be replayed deterministically against the same source hash.

### Allocate Records

- Purpose: Assign planned additions to safe table slots.
- Inputs: Merge plan, decoded table occupancy, candidate empty slots, append slots, capacity limits.
- Outputs: Allocation map from planned additions to record offsets.
- Failure conditions: No proven empty slot, ambiguous empty slot, table at unknown capacity, append would cross proven boundary, allocation would overwrite occupied slot, allocation policy not supported by evidence.
- Safety checks: Never overwrite an occupied slot; prefer only allocation rules supported by current target layout evidence; reject multiple possible policies unless explicitly resolved; keep allocation separate from encoding.

### Encode Records

- Purpose: Convert planned logical records into byte-level record payloads.
- Inputs: Allocation map, update actions, record layout, active XOR/decode profile, source raw records.
- Outputs: Candidate encoded 32-byte records and a byte-change manifest.
- Failure conditions: Name too long, unsupported character, numeric ID outside supported range, unknown padding rule, unknown bytes would need synthesis, encoding does not round-trip through decoder.
- Safety checks: Modify only proven field bytes; preserve untouched bytes from source records; encode name field and numeric field only when layout is proven; decode encoded records immediately and compare to planned values.

### Rebuild Binary

- Purpose: Produce a candidate byte buffer by applying the byte-change manifest to a copy of the source buffer.
- Inputs: Source byte buffer, byte-change manifest, allowed write regions, metadata/checksum strategy.
- Outputs: Candidate byte buffer and binary diff report.
- Failure conditions: Any write outside proven regions, unknown metadata update required, unknown checksum required, file size change, header change, overlapping writes, unaccounted byte changes.
- Safety checks: Allowed-region enforcement; exact file-size preservation; all non-target bytes identical unless a metadata rule is proven; reject if metadata/checksum behavior is UNKNOWN.

### Internal Validation

- Purpose: Prove the candidate buffer matches the plan before it can leave the tool.
- Inputs: Candidate byte buffer, source hash, merge plan, allocation map, expected table counts, decoder.
- Outputs: Internal validation report and pass/fail decision.
- Failure conditions: Candidate does not decode, decoded records do not match plan, unexpected record count, unexpected diff outside manifest, duplicate IDs/names, unknown metadata changes, checksum validation unavailable.
- Safety checks: Decode candidate independently; compare decoded tables to planner output; verify record counts and empty slots; compare binary diff to manifest; reject if any warning remains unresolved.

### KPG111 Validation

- Purpose: Verify the candidate file with Kenwood KPG111 software before any radio use.
- Inputs: Candidate file in an isolated validation location, KPG111 version/profile, expected visible records.
- Outputs: Human or automated validation record: opens successfully, no warnings, expected rows visible.
- Failure conditions: KPG111 refuses file, reports warnings, changes unexpected fields, displays wrong records, crashes, silently rewrites unexpected bytes on save.
- Safety checks: Use a copy only; never replace a working codeplug; record KPG111 version; optionally save a no-change export and compare normalized output to expected bytes.

### Radio Validation

- Purpose: Verify the generated file behaves safely on target radio hardware after KPG111 accepts it.
- Inputs: KPG111-accepted file, test radio, backup of current radio programming, rollback procedure.
- Outputs: Radio validation result and observed behavior.
- Failure conditions: Load failure, warning, missing records, wrong IDs/TGs, radio behavior differs from expected, inability to restore backup.
- Safety checks: Use non-critical test radio first; back up existing radio state; validate receive/transmit behavior only within legal and operational constraints; stop on any warning.

## Required Invariants

- Never overwrite an occupied slot.
- Never duplicate numeric IDs within the same table.
- Never duplicate names within the same table unless explicitly allowed by policy.
- Never modify bytes outside proven regions.
- Never write if unknown metadata changes are detected.
- Never write if checksum behavior is unknown for the target layout.
- Never write if pointer or index behavior is unknown and could be affected.
- Never change file size.
- Never change the source file in place.
- Never emit a candidate if validation fails.
- Never treat absence of observed metadata changes as proof that metadata does not exist.
- Preserve all bytes not explicitly covered by the byte-change manifest.
- All planned logical changes must be visible in the decoded candidate.
- All decoded candidate records must match the planner output exactly.

## Allocation Rules

### Current Evidence

- Candidate first empty slots have been observed for Individual IDs and Talk Groups.
- Dattest4 shows a cleared Individual ID slot at `0x105a0` can be reused.
- Dattest4 shows a cleared Talk Group slot at `0x150a0` can be reused.
- Dattest4 shows an Individual ID append slot at `0x10840` can be populated.
- Dattest4 shows a Talk Group append slot at `0x15340` can be populated.
- Current reports did not observe separate normalized count, index, checksum-like, header, tail, or outside-table metadata changes in these controlled cases.

### Proposed Production Policy

- Allocate only into slots decoded as empty and inside proven table capacity.
- Prefer reuse of an explicitly empty slot when the merge plan is replacing a deleted logical position and the slot is proven empty.
- Use append only when the append slot is inside proven capacity and all intermediate occupancy rules are known.
- Reject allocation if there is more than one plausible policy and no target-layout rule selects one deterministically.
- Reject allocation if any count field, index, bitmap, checksum, or pointer update would be required but is not implemented from proven evidence.

### Unknowns

- Maximum table capacity is not established.
- Absolute table boundaries are not fully proven.
- Allocation bitmap behavior is not observed in current experiments.
- Count fields are not observed in current experiments.
- Pointer/index table behavior is not observed in current experiments.
- Empty-slot selection order is only partially observed.
- Behavior with multiple gaps, reordered entries, and full tables is unknown.

### Confidence

- Reusing the specific observed cleared slots: PARTIAL to HIGH for the observed files, not generalized to all layouts.
- Appending to the specific observed first append slots: PARTIAL to HIGH for the observed files, not generalized to all capacities.
- General allocation algorithm: PARTIAL.
- Full production allocation safety: UNKNOWN until table capacity, metadata, and checksum behavior are resolved.

## Rollback Strategy

This design uses abort-before-emit as the primary rollback strategy.

- If any stage fails, abort immediately.
- Do not emit `Program.dat`.
- Do not overwrite the source file.
- Do not keep a partially rebuilt binary as a success artifact.
- Preserve diagnostic reports only if they contain no binary output and no source-file mutation.
- Require the user to continue using the original known-good KPG111 export.

If a future implementation ever emits candidate files, it must write to a new, clearly named validation path and never to the input path. Promotion to operational use can happen only after KPG111 and radio validation both pass.

## Required Verification

Generated candidate output, if a future writer is ever implemented, must:

- Decode successfully with the project decoder.
- Match the merge planner exactly.
- Match expected Individual ID and Talk Group record counts.
- Contain no duplicate numeric IDs.
- Contain no duplicate names unless explicitly allowed.
- Have no binary changes outside the approved byte-change manifest.
- Preserve file size.
- Preserve all unknown bytes.
- Open in KPG111.
- Load in KPG111 without warnings.
- Display the expected records in KPG111.
- Optionally round-trip through KPG111 with no unexpected logical changes.
- Load onto a test radio without warnings.
- Preserve a known-good rollback path for radio programming.

## Unsupported Scenarios

The writer design must reject these scenarios:

- Unknown metadata behavior.
- Unknown KPG111 versions or layouts.
- Unexpected table sizes.
- Unknown checksums, CRCs, hashes, or integrity fields.
- Unknown pointer structures.
- Unknown index structures.
- Unknown allocation bitmap behavior.
- Ambiguous empty-slot allocation.
- Tables at or near unknown capacity.
- Reordered tables.
- Files with unexpected size or header.
- Files where normalized comparison shows changes outside supported record fields.
- Any request requiring modification outside proven TG/ID record regions.

## Final Checklist

| Item | Status | Notes |
| --- | --- | --- |
| Record layout | PARTIAL | 32-byte candidate records, name `+1..+14`, and numeric `+19/+20` are supported for observed TG/ID records. |
| Numeric encoding | PARTIAL | 16-bit little-endian after active XOR is supported for observed records. |
| Text encoding | PARTIAL | XOR-decoded name field behavior is supported in observed byte spaces; full character policy is not production-proven. |
| Table boundaries | PARTIAL | Candidate starts and occupied runs are mapped; maximum capacity and absolute boundaries are unresolved. |
| Allocation | PARTIAL | Specific reuse and append behavior is observed; general policy remains incomplete. |
| Empty slot representation | PARTIAL | Empty records are observed in current datasets; all layout/version cases are not proven. |
| Count fields | UNKNOWN | Not observed in current experiments. |
| Checksums | UNKNOWN | No positive evidence; not proven absent. |
| Metadata | PARTIAL | Separate metadata changes were not observed after normalization in current experiments, but metadata is not proven absent. |
| Pointer/index structures | UNKNOWN | Not observed in current experiments. |
| Validation | PARTIAL | Internal read-only validation exists; KPG111 and radio validation of generated files cannot exist until a writer exists. |
| Writer | NOT STARTED | This document intentionally does not implement binary writing. |
| KPG111 validation | UNKNOWN | No generated file exists to validate. |
| Radio validation | UNKNOWN | No generated file exists to validate on hardware. |
