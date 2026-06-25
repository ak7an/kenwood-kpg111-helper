# KPG111 Evidence Matrix

This catalog summarizes only evidence already present under `research/`. It is read-only documentation. It does not modify any `.dat` file, does not write `Program.dat`, and does not add a writer.

## Research Inventory

| Area | Existing Files |
| --- | --- |
| Dattest archive | `research/Dattest.zip` |
| Dattest data | `research/dattest/Dattest/AK7AN_Travel.dat`, `Program_1TG.dat`, `Program_1ID.dat`, `Program_Rename.dat`, `Program_Delete.dat` |
| Dattest reports | `research/dattest/README.md`, `reports/session_report.md`, `reports/offset_spacing.md`, `reports/xor_analysis.md`, `reports/*.records.md`, `reports/*.inspect.md`, `reports/*.tables.md` |
| Dattest sessions | `research/dattest/sessions/*.session.json` |
| Dattest table maps | `research/dattest/table_map.md`, `table_map.json`, `tables/*.tables.json` |
| Dattest2 archive | `research/Dattest2.zip` |
| Dattest2 data | `research/dattest2/Dattest2/Program_Nochange1.dat`, `Program_Nochange2.dat`, `Program_Nochange3.dat`, `Program_TG_00001.dat`, `Program_TG_00100.dat`, `Program_TG_12345.dat`, `Program_TG_65516.dat`, `Program_ID_00001.dat`, `Program_ID_00100.dat`, `Program_ID_12345.dat`, `Program_ID_65519.dat` |
| Dattest2 reports | `research/dattest2/README.md`, `reports/session_report.md`, `reports/offset_spacing.md`, `reports/xor_analysis.md`, `reports/numeric_evidence_table.md`, `reports/nochange1_vs_previous.records.md`, `reports/*.records.md`, `reports/*.inspect.md`, `reports/*.tables.md` |
| Dattest2 sessions | `research/dattest2/sessions/*.session.json` |
| Dattest2 table maps | `research/dattest2/table_map.md`, `table_map.json`, `tables/Program_Nochange1.tables.json` |
| Dattest3 archive | `research/Dattest3.zip` |
| Dattest3 data | `research/dattest3/Dattest3/Program.dat`, `Program1.dat`, `Program2.dat`, `Program3.dat`, `Program4.dat` |
| Dattest3 reports | `research/dattest3/README.md`, `reports/session_report.md`, `reports/offset_spacing.md`, `reports/xor_analysis.md`, `reports/program_vs_dattest1_xor.md`, `reports/change_summary_table.md`, `reports/*.records.md`, `reports/*.table_map.md` |
| Dattest3 sessions | `research/dattest3/sessions/*.session.json` |
| Dattest3 table maps | `research/dattest3/table_map.md`, `table_map.json`, `tables/*.table_map.json` |
| Dattest4 archive | `research/Dattest4.zip` |
| Dattest4 data | `research/dattest4/Dattest4/Program3.dat`, `Program5.dat`, `Program6.dat` |
| Dattest4 reports | `research/dattest4/README.md`, `reports/session_report.md`, `reports/offset_spacing.md`, `reports/xor_analysis.md`, `reports/Program5.target_slots.md`, `reports/Program6.target_slots.md`, `reports/*.table_map.md` |
| Dattest4 sessions | `research/dattest4/sessions/*.session.json` |
| Dattest4 table maps | `research/dattest4/table_map.md`, `table_map.json`, `tables/*.table_map.json` |
| Exports | `research/exports/ak7an_individual_ids.csv`, `research/exports/ak7an_talk_groups.csv` |
| Metadata reports | No standalone metadata reports were found under `research/`; metadata behavior below is limited to what current comparison reports expose. |

## Master Table

| Experiment | Operation | TG Changes | ID Changes | Raw Metadata | Normalized Metadata | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Dattest | Add TG, add ID, rename TG, delete TG against `AK7AN_Travel.dat` | Add at `0x151a0`; rename at `0x15180`; delete clears `0x15120`; fields observed at name `+1..+14` and numeric `+19..+20` | Add at `0x10640`; fields observed at name `+1..+14` and numeric `+19..+20` | Whole payload after `0x40` changes in raw byte comparisons; independent metadata not observable directly in raw diff | After dominant XOR normalization, no separate count, index, checksum-like, header, or tail metadata change was observed in current reports | HIGH for listed record changes; PARTIAL for absence of observed metadata changes |
| Dattest2 | No-change saves plus controlled TG/ID numeric add values | TG add slot remains `0x151a0`; numeric values 1, 100, 12345, and 65519 decode at `+19/+20` as little-endian after active XOR | ID add slot remains `0x10640`; same numeric encoding pattern as TG | No-change saves rewrite the entire payload with a different dominant XOR key | No-change saves normalize to zero logical changes; controlled saves normalize to 15 or 16 logical changed bytes in target record fields only | HIGH for numeric field encoding in observed add slots; PARTIAL for metadata behavior |
| Dattest3 | Rename, numeric edit, clear records, and in-place record changes | `0x15140` renamed/numeric edited; `0x150a0` cleared or changed depending on file | `0x10640` renamed/numeric edited; `0x105a0` cleared or changed depending on file | `Program1.dat` through `Program3.dat` mostly rewrite through dominant XOR; `Program4.dat` keeps dominant XOR `0x00` and has localized raw changes | All normalized residual changes are inside candidate TG/ID records; no separate count, index, checksum-like location observed | HIGH for changed record fields and table-map effects; PARTIAL for broader table metadata |
| Dattest4 | Reuse deleted slots and append records from `Program3.dat` baseline | Reuses cleared `0x150a0`; `Program6.dat` also appends `0x15340` | Reuses cleared `0x105a0`; `Program5.dat` and `Program6.dat` also append `0x10840` | Raw comparisons show whole-payload rewrite with dominant XOR values `0x46` and `0x4a` | Normalized residual changes are confined to target records; no outside-table, count, index, checksum-like, header, or tail change observed | HIGH for slot reuse/append observations; PARTIAL for empty-slot allocation rules |
| Exports | CSV exports from decoded AK7AN baseline tables | `ak7an_talk_groups.csv` lists 17 non-empty TG records from `0x14f80` through `0x15180` | `ak7an_individual_ids.csv` lists 14 non-empty ID records from `0x10480` through `0x10620` | Not applicable; CSV export is decoded output, not raw binary metadata | Not applicable; export supports decoder/table mapping for known baseline records | HIGH for exported rows matching current decoder output |

## Experiment Details

### Dattest

- Experiment name: Dattest controlled add, rename, and delete set.
- Files used: `research/dattest/Dattest/AK7AN_Travel.dat`, `Program_1TG.dat`, `Program_1ID.dat`, `Program_Rename.dat`, `Program_Delete.dat`; reports and sessions under `research/dattest/`.
- Apparent purpose: Locate logical changes for one added TG, one added Individual ID, one renamed TG, and one deleted TG.
- Observed TG changes: Added `GPTTest1` at candidate record `0x151a0`; renamed `AK7AN TG` to `BitByBitHams` at `0x15180`; deleted `Disconnect TG` at `0x15120`.
- Observed Individual ID changes: Added `Bradley` at candidate record `0x10640`.
- Raw metadata behavior if known: Direct diffs show the entire payload region `0x40-0x29140` changes, so raw comparison alone does not isolate metadata.
- Normalized metadata behavior if known: Current reports observe only localized record-field changes after XOR normalization. Separate count, index, free-list, checksum-like, header, or tail metadata changes were not observed in current experiments.
- Dominant XOR behavior if known: Modified files have dominant payload XOR deltas `0x3e`, `0x0c`, `0x67`, and `0x1e` versus baseline, each explaining more than 99.98% of payload bytes.
- Confidence: High for candidate 32-byte records and observed field offsets in these files; partial for table boundaries and metadata behavior.
- Notes: Name bytes are observed at `+1..+14`; numeric bytes are observed at `+19..+20`. The report supports candidate Individual ID and Talk Group table starts but does not prove full table boundaries.

### Dattest2

- Experiment name: Dattest2 no-change and numeric-value set.
- Files used: `research/dattest2/Dattest2/*.dat`; reports, sessions, and table maps under `research/dattest2/`.
- Apparent purpose: Test no-change save behavior and controlled TG/ID numeric encodings for 1, 100, 12345, and a high value observed as 65519.
- Observed TG changes: Controlled TG rows write the add slot `0x151a0`; numeric values decode from bytes `+19/+20` with the active XOR key and little-endian order.
- Observed Individual ID changes: Controlled ID rows write the add slot `0x10640`; numeric encoding matches the TG pattern in this dataset.
- Raw metadata behavior if known: No-change saves are not byte-identical; each raw payload changes by a constant dominant XOR key.
- Normalized metadata behavior if known: No-change saves normalize to zero logical changes. Controlled saves normalize to target record-field changes only; separate metadata changes were not observed in current experiments.
- Dominant XOR behavior if known: No-change saves show 100% dominant XOR over the payload. Controlled saves show a dominant XOR over more than 99.99% of payload bytes, with residual bytes in target record fields.
- Confidence: High for little-endian 16-bit numeric ID encoding in observed add slots; high for whole-payload constant XOR behavior in this dataset; partial for broader metadata behavior.
- Notes: The archive contains `Program_TG_65516.dat`, but the report notes the bytes decode to 65519.

### Dattest3

- Experiment name: Dattest3 edit, clear, and in-place change set.
- Files used: `research/dattest3/Dattest3/Program.dat`, `Program1.dat`, `Program2.dat`, `Program3.dat`, `Program4.dat`; reports, sessions, and table maps under `research/dattest3/`.
- Apparent purpose: Test renames, numeric edits, record clearing, and in-place updates against a larger baseline table.
- Observed TG changes: `0x15140` changes from `Utah DRN 00` to `Hot n Sexy`, with numeric unchanged or incremented depending on file; `0x150a0` changes from `Scotland TG` to empty in `Program3.dat` or to `Goodbye` in `Program4.dat`.
- Observed Individual ID changes: `0x10640` changes from `ID_Test_65519` to `Long Gone`, with numeric unchanged or decremented depending on file; `0x105a0` changes from `Jamie, KQ1USA` to empty in `Program3.dat` or to `Hello` in `Program4.dat`.
- Raw metadata behavior if known: `Program1.dat` through `Program3.dat` mostly differ by whole-payload dominant XOR. `Program4.dat` has dominant XOR `0x00` and localized raw changes.
- Normalized metadata behavior if known: Reports state all residual changed ranges map to candidate TG/ID table records. Separate count, index, checksum-like, header, or tail metadata changes were not observed in current experiments.
- Dominant XOR behavior if known: Dominant XOR values are `0x2f`, `0x2b`, `0x01`, and `0x00` for `Program1.dat` through `Program4.dat`.
- Confidence: High for the listed record modifications and clear-slot observations; partial for inferred table limits.
- Notes: Baseline table maps show 30 occupied candidate Individual ID records ending at `0x1083f` and 30 occupied candidate Talk Group records ending at `0x1533f`, with first empty slots at `0x10840` and `0x15340`.

### Dattest4

- Experiment name: Dattest4 slot reuse and append set.
- Files used: `research/dattest4/Dattest4/Program3.dat`, `Program5.dat`, `Program6.dat`; reports, sessions, and table maps under `research/dattest4/`.
- Apparent purpose: Check whether new records reuse deleted slots or append after the occupied run.
- Observed TG changes: Both modified files reuse cleared slot `0x150a0` with `Goodbye`, TG 16432. `Program6.dat` also appends `GROUP ID 0031`, TG 15432, at `0x15340`.
- Observed Individual ID changes: Both modified files reuse cleared slot `0x105a0` with `Hello`, ID 23654, and append ` UNIT ID 0031`, ID 43521, at `0x10840`.
- Raw metadata behavior if known: Raw diffs show whole-payload rewrites with dominant XOR values `0x46` and `0x4a`.
- Normalized metadata behavior if known: Residual changes are confined to the target table records. Separate count, index, checksum-like, header, tail, or outside-table changes were not observed in current experiments.
- Dominant XOR behavior if known: Dominant payload XOR values are `0x46` for `Program5.dat` and `0x4a` for `Program6.dat`.
- Confidence: High that deleted slots can be reused and first append slots can be used in these files; partial for general empty-slot allocation policy.
- Notes: This experiment shows both gap filling and append behavior, but it does not fully define ordering rules when multiple empty slots or table limits are involved.

### Exports

- Experiment name: AK7AN decoded CSV exports.
- Files used: `research/exports/ak7an_individual_ids.csv`, `research/exports/ak7an_talk_groups.csv`.
- Apparent purpose: Preserve decoded baseline Individual ID and Talk Group rows as CSV.
- Observed TG changes: No change experiment; export lists 17 baseline TG records from `0x14f80` through `0x15180`.
- Observed Individual ID changes: No change experiment; export lists 14 baseline ID records from `0x10480` through `0x10620`.
- Raw metadata behavior if known: Not applicable to CSV output.
- Normalized metadata behavior if known: Not applicable to CSV output.
- Dominant XOR behavior if known: Not applicable to CSV output.
- Confidence: High for current decoder/export output on the baseline rows represented in CSV.
- Notes: These exports support read-only decode/export workflow evidence, not writer safety.

# Confirmed Findings

- All `.dat` files cataloged in these experiments are reported as `168257` bytes.
- The visible unchanged header prefix in the controlled comparisons is `0x40` bytes; raw payload comparisons after `0x40` are often dominated by a single-byte XOR rewrite.
- No-change saves in Dattest2 normalize to zero logical byte changes after applying the dominant payload XOR.
- Candidate TG and Individual ID records are 32 bytes in the observed table regions.
- In observed records, the name field is at record bytes `+1..+14`.
- In observed records, the numeric field is at record bytes `+19/+20`.
- In Dattest2 and later record probes, the numeric field decodes as a 16-bit little-endian value after applying the active XOR key.
- Candidate Individual ID regions observed in the reports include starts at `0x10480`; candidate Talk Group regions include starts at `0x14f80`.
- Dattest4 shows deleted candidate records can be reused in the observed files.
- Dattest4 shows append slots `0x10840` for Individual IDs and `0x15340` for Talk Groups can be populated in the observed files.
- Separate count, index, checksum-like, header, tail, or outside-table metadata changes were not observed after XOR normalization in the current controlled reports.

# Remaining Unknowns

- Record count fields: not observed in current experiments.
- Allocation bitmap: not observed in current experiments.
- Checksum behavior: no positive checksum evidence in current experiments; whole-payload XOR can hide raw behavior, and absence of normalized side changes is not proof of absence.
- Pointer/index tables: not observed in current experiments.
- Maximum table capacity: not established by current experiments.
- Empty slot allocation rules: partially observed for one reused gap and first append slots, but not fully defined.
- Writer safety: not established.
- Full table boundaries: candidate starts and occupied runs are supported, but absolute capacity and boundary rules remain unresolved.
- Reorder behavior: not established by current experiments.
- KPG111 version/layout variability: not established beyond the files currently present.

# Writer Readiness Checklist

| Item | Status | Evidence Basis |
| --- | --- | --- |
| Decoder | COMPLETE | Existing decoded exports and tests support current read-only decoding of observed tables. |
| Table mapping | PARTIAL | Candidate record starts, record size, and observed occupied runs are mapped, but full boundaries/capacity remain unresolved. |
| CSV Import | COMPLETE | Project contains CSV import tooling and tests; this is not writer support. |
| CSV Export | COMPLETE | `research/exports/*.csv` and export tooling exist for read-only decoded rows. |
| Validator | PARTIAL | Validation tooling exists, but binary writer safety checks are not complete while metadata/checksum behavior remains unknown. |
| Comparator | COMPLETE | Existing session, diff, XOR, and table comparison reports support read-only comparison. |
| Merge Planner | PARTIAL | Planning can be performed at decoded-record level, but cannot be safely applied to binary output. |
| Project API | PARTIAL | Existing project facade is read-only/export/planning oriented; binary save support is not present. |
| Metadata Discovery | PARTIAL | Current experiments report metadata changes not observed after normalization, but metadata is not proven absent. |
| Count Fields | UNKNOWN | Not observed in current experiments. |
| Checksums | UNKNOWN | No positive evidence in current experiments; not proven absent. |
| Writer | NOT STARTED | No binary writer is implemented. |
| KPG111 Validation | UNKNOWN | No generated `.dat` has been validated by KPG111 because no writer exists. |
| Radio Validation | UNKNOWN | No generated `.dat` has been validated on radio hardware because no writer exists. |
