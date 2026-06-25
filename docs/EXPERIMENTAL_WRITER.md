# Experimental DAT Writer

This writer is experimental. It exists only to make tightly controlled byte edits
to an existing, already-good KPG-111D `Program.dat` file.

## Supported edits

The initial writer supports only:

- Rename one decoded Talk Group record.
- Rename one decoded Individual ID record.

It does not edit channels. It does not allocate records. It does not generate a
new DAT file from scratch. It copies the original bytes and changes only the
encoded name bytes for one occupied decoded record.

Numeric ID writing is intentionally not exposed by this first writer, even
though the decoder can read numeric IDs. Keeping the first writer name-only
reduces the validation surface.

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

```bash
python3 tools/dat_edit_record.py input.dat output.dat --table talk_groups --slot 1 --name "TEST TG"
python3 tools/dat_edit_record.py input.dat output.dat --table individual_ids --slot 1 --name "TEST ID"
```

The tool prints the exact byte ranges changed and verifies that the output
differs only in those ranges.
