# DAT Diff Experiments

`tools/dat_diff.py` compares two KPG111 `.dat` files byte-for-byte and reports
contiguous changed byte ranges. It is intended for controlled evidence
experiments, especially early channel record decoding.

This tool is read-only. It does not edit DAT files and does not infer field
meaning by itself.

## Controlled Workflow

1. Export a known-good baseline DAT from KPG-111D.
2. Make exactly one change in KPG-111D.
3. Export the modified DAT.
4. Run `tools/dat_diff.py` against the two files.
5. Record the changed offsets, changed ranges, and byte values.
6. Repeat with one controlled change per experiment.

Example:

```bash
python3 tools/dat_diff.py baseline.dat modified.dat --context 16 --markdown
```

Use `--context N` to include unchanged bytes before and after each changed
range. Use `--max-ranges N` when a noisy experiment produces too many ranges
for a readable first pass.

## Evidence Rules

- Do not infer field meaning from uncontrolled changes.
- Do not combine multiple KPG-111D edits in one evidence experiment.
- Treat changed offsets as observations, not decoded fields, until repeated
  experiments isolate the same bytes.
- Preserve both baseline and modified DAT files.
- Record the exact KPG-111D action used to create the modified file.
- Compare multiple experiments before documenting a field as likely decoded.

## Report Contents

The diff report includes:

- baseline file path
- modified file path
- baseline and modified file sizes
- total changed bytes
- number of changed ranges
- each changed range start, end, and length
- baseline hex bytes
- modified hex bytes
- ASCII previews where useful

Ranges caused only by file size differences are reported at the first offset
after the shorter file ends.

## Recommended Channel Experiments

Run each experiment as a separate baseline/modified pair:

1. Blank codeplug vs one analog channel.
2. RX frequency only.
3. TX frequency only.
4. Channel name only.
5. Bandwidth only.
6. Power only.
7. QT/DQT only.
8. NXDN RAN only.
9. One channel vs two channels.
10. Zone move only.

For channel field discovery, repeat the same edit with different values where
possible. For example, use several RX frequencies before marking a byte range as
a candidate RX frequency field.

## Current Interpretation Limits

The diff tool confirms only byte-level differences. It does not prove:

- channel record start offsets
- channel record size
- field encoding
- checksum behavior
- pointer or index table behavior
- allocation rules
- radio safety of edited DAT files

Any field map built from these reports should clearly separate confirmed byte
changes from hypotheses about their meaning.
