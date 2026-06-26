# Channel Export

`tools/dat_export_channels.py` is a read-only research tool for Phase 2 channel
record visibility.

It does not edit channels, does not write DAT files, and does not generate DAT
files from scratch. It scans an existing DAT with the current heuristic channel
analysis and exports candidate channel-like records to CSV.

## Usage

```bash
python3 tools/dat_export_channels.py input.dat --output channels.csv
python3 tools/dat_export_channels.py input.dat --output channels.csv --decode-key 0x5b --limit 50
python3 tools/dat_export_channels.py input.dat --output channels.csv --include-unknown
```

The CSV has a stable research-oriented header:

```text
row,slot,record_offset,name,rx_frequency,tx_frequency,mode,bandwidth,power,group_list,unit_list,scan_list,raw_hex,confidence,notes
```

## Interpretation

No channel record table is confirmed yet. Rows exported by this tool are
candidate channel-like records from heuristic scans, not decoded channel records.

Blank fields mean unknown, not absent. For example, a blank `rx_frequency`
means the RX frequency field is not confidently decoded for that candidate. It
does not mean the channel has no RX frequency.

Use `--include-unknown` to include the raw candidate bytes in `raw_hex`. Without
that option, `raw_hex` is blank and the notes explain that raw bytes were
omitted.

Channel editing is not implemented. KPG-111D controlled experiments are still
required before channel offsets, record sizes, field encodings, indexes, counts,
or metadata can be treated as known.
