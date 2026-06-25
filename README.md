# Kenwood KPG111 Helper

Safe analysis tools for researching Kenwood KPG111 `Program.dat` files.

This project is intentionally read-only for KPG111 fields inside binary `.dat`
files. It does not patch, merge, or generate edited KPG111 data files yet. The
first goal is to collect evidence about the file format before any field-level
writer is implemented.

## Tools

- `tools/dat_inspect.py` reports size, hashes, hex summaries, printable
  strings, likely table-like regions, and repeated byte structures.
- `tools/dat_diff.py` compares two `.dat` files byte-by-byte and summarizes
  changed offsets and contiguous changed regions.
- `tools/dat_search.py` searches for ASCII strings, UTF-16LE strings, decimal
  text, and common integer encodings.
- `tools/dat_compare_session.py` compares a baseline and modified `.dat` file
  and writes read-only evidence to `session.json`.
- `tools/session_report.py` reads one or more session files and produces a
  markdown report of recurring statistical observations.
- `tools/dat_tables.py` analyzes one `.dat` file for possible fixed-width table
  regions, unused slots, entropy, printable density, and repeated padding.
- `tools/offset_spacing.py` analyzes one or more session files for spacing,
  divisors, alignment histograms, and record-size candidates.
- `tools/csv_validate.py` validates Talk Group and Individual ID CSV files with
  the required columns `type,name,id`.
- `tools/dat_roundtrip_check.py` parses a `.dat` file with the existing project
  code, writes an unchanged byte-preserving copy, and verifies that the copy is
  byte-for-byte identical to the input.

## CSV Format

Input CSV files must include this header:

```csv
type,name,id
TG,Dispatch,1001
INDIVIDUAL,Radio 42,42042
```

Rules:

- `type` must be exactly `TG` or `INDIVIDUAL`.
- `name` must not be blank.
- `id` must be a positive decimal integer.

## Usage

Inspect one KPG111 data file:

```bash
python3 tools/dat_inspect.py Program.dat
```

Look for possible fixed-width table regions before running experiments:

```bash
python3 tools/dat_tables.py Program.dat
python3 tools/dat_tables.py Program.dat --json tables.json
```

Compare two KPG111 data files:

```bash
python3 tools/dat_diff.py before/Program.dat after/Program.dat
```

Search for a known name or ID:

```bash
python3 tools/dat_search.py Program.dat 1200
python3 tools/dat_search.py Program.dat Dispatch
```

Create a comparison session:

```bash
python3 tools/dat_compare_session.py baseline.dat modified.dat
```

Generate a markdown report from one or more sessions:

```bash
python3 tools/session_report.py session.json other/session.json > report.md
```

Analyze spacing after several comparison sessions:

```bash
python3 tools/offset_spacing.py research/*/session.json > spacing.md
```

Validate one or more CSV files:

```bash
python3 tools/csv_validate.py talkgroups.csv individual_ids.csv
```

Optional stricter duplicate checks:

```bash
python3 tools/csv_validate.py --unique-ids talkgroups.csv individual_ids.csv
python3 tools/csv_validate.py --unique-names talkgroups.csv individual_ids.csv
```

Run a byte-for-byte round-trip safety check:

```bash
python3 tools/dat_roundtrip_check.py Program.dat --decode-key 0x5b
python3 tools/dat_roundtrip_check.py Program.dat --decode-key 0x5b --output roundtrip.dat
```

Round-trip validation is the safety foundation before any future field-level
editing. An unchanged file must parse, serialize through the project, and match
the original bytes exactly before edited output can be considered.

## Research Workflow

1. Export a baseline `Program.dat`.
2. Change exactly one thing in KPG111.
3. Export again as a new `Program.dat`.
4. Compare the baseline and modified files with `dat_diff.py` or
   `dat_compare_session.py`.
5. Record observations in `docs/FORMAT_RESEARCH.md`.
6. Repeat with one new controlled change.
7. After several sessions, use `session_report.py` and `offset_spacing.py` to
   look for recurring statistical patterns.

See `docs/REVERSE_ENGINEERING_PLAN.md` for the complete safe workflow.

Do not implement binary writing until the relevant record layout, checksums,
padding, encoding, and version-specific behavior are proven from repeatable
test files.
