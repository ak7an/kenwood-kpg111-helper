# DAT Diff Workflow

`tools/dat_diff_bytes.py` is a read-only byte diff tool for controlled KPG-111D
reverse-engineering experiments.

It does not edit DAT files, does not infer channel fields, and does not make
channel writing safe.

## Controlled Experiment Flow

1. Export a known-good baseline DAT from KPG-111D.
2. In KPG-111D, change exactly one field.
3. Save or export the changed file as a new DAT.
4. Run the diff tool:

```bash
python3 tools/dat_diff_bytes.py before.dat after.dat --context 16 --csv diff.csv
```

5. Record the observed byte ranges, before/after bytes, and the exact KPG-111D
   action that produced the change.
6. Repeat with different values for the same field before treating an offset as
   a candidate field.

## Interpretation

The tool reports exact byte changes grouped into adjacent ranges. It also shows
XOR-decoded text previews and labels nearby known regions when available, such
as known Talk Group and Individual ID table areas or candidate channel-like
regions from the current heuristic scanner.

Unknown regions remain unknown. Candidate channel-like regions are hypotheses
only. Do not write channel edits until offsets, encodings, indexes, counts, and
metadata behavior are confirmed by controlled experiments.

Use one KPG-111D change per diff. Multiple simultaneous edits make it much
harder to separate channel fields from metadata, indexes, or unrelated saved
state.
