# KPG111 `Program.dat` Reverse Engineering Plan

This plan is for read-only format research. It must not be used to generate,
modify, repair, or merge `Program.dat` files.

## Safety Rules

- Keep original exports untouched.
- Work from copies in named experiment folders.
- Change exactly one thing per experiment.
- Record every experiment, even when the diff looks unhelpful.
- Treat every result as provisional until repeated across multiple exports.
- Do not write binary files until every relevant structure has been proven.

## Standard Workflow

1. Export a baseline `Program.dat` from KPG111.
2. Run read-only baseline inspection and table discovery.
3. Change exactly one thing in KPG111.
4. Export again as a new `Program.dat`.
5. Compare the baseline and modified files.
6. Record observations, changed offsets, changed regions, and notes.
7. Repeat with one new controlled change.
8. After several sessions, aggregate reports and spacing analysis.

## Recommended Directory Layout

```text
research/
  000_baseline/
    Program.dat
    notes.md
  001_change_one_tg_name/
    Program.dat
    notes.md
    session.json
  002_change_one_tg_id/
    Program.dat
    notes.md
    session.json
```

## Per-Experiment Commands

Inspect the baseline:

```bash
python3 tools/dat_inspect.py research/000_baseline/Program.dat
```

Look for possible fixed-width table regions before experiments:

```bash
python3 tools/dat_tables.py research/000_baseline/Program.dat \
  --json research/000_baseline/tables.json \
  > research/000_baseline/tables.md
```

Search for a known name or ID:

```bash
python3 tools/dat_search.py research/000_baseline/Program.dat Dispatch
python3 tools/dat_search.py research/000_baseline/Program.dat 1200
```

Create a read-only comparison session:

```bash
python3 tools/dat_compare_session.py \
  research/000_baseline/Program.dat \
  research/001_change_one_tg_name/Program.dat \
  --output research/001_change_one_tg_name/session.json
```

Generate an aggregate markdown report:

```bash
python3 tools/session_report.py research/*/session.json > research/report.md
```

Analyze offset and region spacing after several sessions:

```bash
python3 tools/offset_spacing.py research/*/session.json > research/spacing.md
```

## Table Discovery Workflow

Use `dat_tables.py` before controlled edits. It can highlight regions that have
statistical features often seen in fixed-width tables:

- repeated candidate record widths
- zero-filled or FF-filled slots
- printable string density by block
- entropy by block
- repeated padding-like patterns
- possible starts and ends based on alignment and repetition

These are only search aids. A high score does not prove that a region is a
Talk Group table, an Individual ID table, or any other specific structure.

After several `session.json` files exist, use `offset_spacing.py` to compare
where changes occur. Common spacing, shared divisors, repeated region lengths,
and alignment histograms can suggest candidate record sizes. They still do not
prove field meanings or write safety.

## What To Record

- KPG111 version.
- Radio model and codeplug context, if known.
- Exact UI field changed.
- Old value and new value.
- Whether file size changed.
- Changed offsets and changed regions.
- Strings added or removed.
- Search hits for known names and numeric IDs.
- Table-discovery candidate regions and candidate record sizes.
- Offset-spacing observations after several sessions.
- Any repeated offset or region patterns seen across sessions.

## Interpreting Results Conservatively

Use cautious language:

- "offset changed in 4 of 5 sessions"
- "region start often aligns to 16 bytes"
- "changed-region starts commonly differ by 32 bytes"
- "candidate table region has many zero-filled slots"
- "short recurring change could be a count, index, or checksum input"
- "tail-end recurring change could be checksum-like"

Avoid certainty:

- Do not claim a field meaning from one experiment.
- Do not claim an offset is a checksum only because it changes often.
- Do not claim a record size until repeated additions or edits support it.
- Do not claim table boundaries from one `dat_tables.py` report.
- Do not treat common divisors from `offset_spacing.py` as confirmed record
  sizes.
- Do not assume text encoding from a single visible string.

## Writing Readiness Gate

No binary writer should be implemented until all of these have repeatable
evidence for the target KPG111 version:

- Talk Group record boundaries.
- Individual ID record boundaries.
- Record field order and byte order.
- Text encoding, null termination, and padding.
- Numeric ID range and byte width.
- Table count fields, indexes, and capacities.
- Empty slot representation.
- Table starts, ends, and record sizes.
- Checksum, CRC, hash, or other integrity fields, or proof that none exist.
- Behavior when entries are added, deleted, renamed, and reordered.
