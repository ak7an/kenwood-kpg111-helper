# Experimental DAT Writer

This writer is experimental. It exists only to make tightly controlled byte edits
to an existing, already-good KPG-111D `Program.dat` file.

## Supported edits

The initial writer supports only:

- Rename one decoded Talk Group record.
- Rename one decoded Individual ID record.
- Change one decoded Talk Group numeric ID.
- Change one decoded Individual ID numeric ID.

It does not edit channels. It does not allocate records. It does not generate a
new DAT file from scratch. It copies the original bytes and changes only the
encoded name bytes and/or encoded numeric ID bytes for one occupied decoded
record.

Numeric ID editing is experimental. Talk Group IDs are limited to `1..65519`.
Individual IDs are currently treated conservatively with the same `1..65519`
range unless later evidence proves a different validated range.

## Safety rules

- Keep original backups.
- Use only an existing DAT file exported by KPG-111D.
- Write to a separate output path unless you explicitly choose otherwise.
- Inspect the byte ranges reported by `tools/dat_edit_record.py`.
- Open the edited DAT in KPG-111D before any radio use.
- Never write edited DAT files to a radio until KPG-111D opens them successfully.
- Stop if KPG-111D reports warnings, rewrites unexpected data, or displays
  unexpected records.

KPG-111D validation is required before radio use. This repository cannot prove
that a candidate DAT is safe for a radio just because the internal byte checks
pass.

## Example

KPG-111D displays record rows starting at `1` in its `No.` column. The writer
library uses internal zero-based slots. Humans should normally use `--row` with
the CLI so the number matches KPG-111D. The older `--slot` option is retained
for advanced/internal testing and remains zero-based.

```bash
python3 tools/dat_edit_record.py input.dat output.dat --table talk_groups --row 2 --name "TEST TG"
python3 tools/dat_edit_record.py input.dat output.dat --table individual_ids --row 2 --name "TEST ID"
python3 tools/dat_edit_record.py input.dat output.dat --table talk_groups --row 2 --id 12345
python3 tools/dat_edit_record.py input.dat output.dat --table individual_ids --row 2 --id 12345
python3 tools/dat_edit_record.py input.dat output.dat --table talk_groups --row 2 --name "TEST TG" --id 12345
```

The tool prints the exact byte ranges changed and verifies that the output
differs only in those ranges.

## CSV Workflow

Export the records you want to edit:

```bash
python3 tools/dat_export_records.py input.dat --table talk_groups --output talkgroups.csv
python3 tools/dat_export_records.py input.dat --table individual_ids --output ids.csv
```

Edit the CSV values in the `name` and/or `id` columns. Keep `row` when editing
from the KPG-111D visible `No.` column. `slot` is zero-based and is intended for
advanced/internal checks.

Import the edited CSV into a copy of the DAT:

```bash
python3 tools/dat_import_records.py input.dat edited.dat --table talk_groups --csv talkgroups.csv
python3 tools/dat_import_records.py input.dat edited.dat --table individual_ids --csv ids.csv
```

The import tool uses the experimental writer for every row, preserves unknown
bytes, and prints the exact changed byte ranges. Validate the edited DAT in
KPG-111D before any radio use. Never write directly to a radio until KPG-111D
opens the edited file successfully.
