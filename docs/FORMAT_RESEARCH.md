# KPG111 `Program.dat` Format Research

This document tracks evidence about the KPG111 `Program.dat` binary format.

## Ground Rules

- Do not assume the binary format from a single file.
- Do not write output `.dat` files until the format is proven.
- Prefer controlled experiments: change exactly one thing in KPG111, export,
  diff, and record the result.
- Keep original files untouched and store generated exports separately.
- Treat all offsets as provisional until confirmed across multiple files.

## Known Facts

- File extension: `.dat`
- Producer: Kenwood KPG111 programming software
- Current project support: read-only inspection and comparison
- Structure discovery support: statistical table, spacing, and alignment reports
- Binary writing support: intentionally not implemented

## Open Questions

- What file header, magic values, or version fields exist?
- What text encoding is used for names?
- Where are Talk Group IDs stored?
- Where are Individual IDs stored?
- Are records fixed-width or variable-length?
- Are there checksums, CRCs, length fields, indexes, or internal offsets?
- Are records sorted by UI order, numeric ID, creation order, or another key?
- Does the file contain padding, deleted records, or unused table capacity?
- Do different KPG111 versions produce different layouts?

## Suggested Experiments

For the complete safe workflow, see `docs/REVERSE_ENGINEERING_PLAN.md`.

### Baseline Export

- Export a known-good untouched file.
- Run:

```bash
python3 tools/dat_inspect.py Program.dat
```

- Record file size, hashes, notable strings, and likely table regions.
- Run a table-discovery pass before changing anything:

```bash
python3 tools/dat_tables.py Program.dat > tables.md
```

- Search for known names and IDs:

```bash
python3 tools/dat_search.py Program.dat 1200
python3 tools/dat_search.py Program.dat Dispatch
```

### Single Talk Group Change

- Start from a baseline file.
- Change exactly one Talk Group name or ID.
- Export as a new file.
- Run:

```bash
python3 tools/dat_diff.py baseline/Program.dat changed_tg/Program.dat
```

- Record changed offsets and region lengths.
- Optionally create a structured session:

```bash
python3 tools/dat_compare_session.py baseline/Program.dat changed_tg/Program.dat \
  --output changed_tg/session.json
```

### Single Individual ID Change

- Start from a baseline file.
- Change exactly one Individual name or ID.
- Export as a new file.
- Run:

```bash
python3 tools/dat_diff.py baseline/Program.dat changed_individual/Program.dat
```

- Record changed offsets and region lengths.

### Add One Entry

- Start from a baseline file.
- Add exactly one Talk Group or Individual entry.
- Export as a new file.
- Compare with the baseline.
- Watch for record insertion, free-slot reuse, count fields, and checksum
  updates.

### Aggregate Sessions

After several controlled experiments, generate a markdown report:

```bash
python3 tools/session_report.py */session.json > report.md
```

Review recurring offsets, recurring regions, alignment patterns, short changed
regions, and tail-end changes as statistical observations only. Do not treat
them as confirmed field meanings.

Analyze changed-offset spacing after several sessions:

```bash
python3 tools/offset_spacing.py */session.json > spacing.md
```

Spacing, divisors, and alignment histograms can suggest candidate record sizes
or table layouts. They do not prove where records begin, what fields mean, or
whether a region is safe to write.

## Observations

Add findings here as experiments are run.

| Date | File Pair | Change Made | Changed Offsets | Notes |
| --- | --- | --- | --- | --- |
| | | | | |

## Candidate Regions

Track likely regions here. Keep confidence levels conservative.

| Offset Range | Size | Hypothesis | Evidence | Confidence |
| --- | ---: | --- | --- | --- |
| | | | | |

## Candidate Record Sizes

Track statistical candidates here. A candidate size should remain provisional
until supported by multiple controlled edit, add, delete, and reorder
experiments.

| Candidate Size | Evidence | Sessions | Confidence |
| ---: | --- | --- | --- |
| | | | |

## Writing Readiness Checklist

Binary writing should not be added until these are answered for the target
KPG111 version:

- Record layout is known for Talk Groups.
- Record layout is known for Individual IDs.
- Text encoding and padding rules are known.
- ID byte order and valid numeric ranges are known.
- Table capacity and empty-record representation are known.
- Count/index fields are known.
- Checksum or CRC behavior is known, or proven absent.
- Table starts, ends, record sizes, and empty-slot behavior are proven across
  multiple controlled experiments.
- Multiple controlled exports reproduce the same conclusions.
