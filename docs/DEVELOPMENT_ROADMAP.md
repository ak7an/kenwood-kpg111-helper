# Development Roadmap

This roadmap describes the intended path from the current read-only research toolkit toward safe edited DAT output. Each phase must preserve existing round-trip guarantees and keep unknown bytes untouched.

## Phase 1: Golden DAT Corpus

- Collect known-good DAT fixtures from controlled KPG-111D exports.
- Record source context for each fixture: KPG-111D version, radio model, and exact UI state when known.
- Keep original fixtures immutable.
- Require every fixture to pass byte-identical no-op round-trip validation.

## Phase 2: Primitive Field Decoding

- Decode one primitive field at a time from controlled before/after experiments.
- Document byte offsets, lengths, encoding, observed values, and confidence.
- Prefer additive decoding that leaves all unknown bytes preserved.
- Add tests for each decoded field before using it in higher-level models.

## Phase 3: Channel Record Dataclasses

- Introduce dataclasses for channel-like records only after field boundaries are supported by evidence.
- Keep raw byte slices attached to decoded records so unknown bytes remain preservable.
- Separate decoded semantic fields from raw storage.
- Treat partially decoded records as read-only until all write-relevant fields are proven.

## Phase 4: Field Encoders

- Build encoders only for fields with matching decoder tests and controlled evidence.
- Every encoder must round-trip known values and reject unsupported values.
- Encoders must preserve unknown bytes by construction.
- No encoder should imply that a full writer is safe.

## Phase 5: Safe Edited Write-Back

- Start with the existing no-op byte-identical round-trip path.
- Permit edited output only when the target bytes are proven safe and covered by tests.
- Validate that only intended bytes changed.
- Reject writes when checksums, counts, indexes, metadata, or capacity behavior are unknown for the requested edit.

## Phase 6: CSV/Import Tooling

- Expand CSV import only after decoded models and field encoders are stable.
- Validate duplicate IDs, duplicate names, ranges, table capacity, and unsupported fields before planning edits.
- Produce merge plans that are inspectable before any write-back.
- Keep KPG-111D validation mandatory for generated edited files.

## Phase 7: GUI/CPS-Style Application

- Build a GUI only after the command-line decode, validate, plan, encode, and write-back workflow is proven.
- Keep advanced controls visible for validation status, unsupported fields, and unknown bytes.
- Do not hide safety warnings behind convenience workflows.
- Treat the application as an assistant to KPG-111D until KPG-111D and radio validation coverage is broad.

## Cross-Phase Gates

- No edited DAT output without byte-identical no-op round-trip tests.
- No field encoder without decoder tests and fixture coverage.
- No radio use without KPG-111D opening the generated file without warnings.
- No destructive rewrite strategy while unknown bytes remain.
