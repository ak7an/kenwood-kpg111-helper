# KPG111 Record Size Audit

This audit reviews the basis for the 32-byte record size used by the current decoder and generated record specification. It is read-only and does not modify `Program.dat`, research files, or writer behavior.

## Question

Determine whether the documented 32-byte record size is:

- the complete physical record for known Talk Group and Individual ID table entries,
- only a decoded payload inside a larger record, or
- an incorrect earlier assumption.

## Evidence Reviewed

| Source | Evidence |
| --- | --- |
| `kpg111/decoder.py` | Defines `RECORD_SIZE = 32`; decodes table slots by `start + slot * RECORD_SIZE`; slices exactly 32 bytes per decoded record. |
| `tools/dat_table_map.py` | Describes and defaults to scanning candidate 32-byte records. |
| `tools/dat_decode_tables.py` | Accepts `--record-size` but rejects anything other than current decoder `RECORD_SIZE`; current supported decode is 32 bytes only. |
| `tools/dat_tables.py` | Statistical discovery tested candidate sizes `(8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128)`. It did not include 44 bytes as a candidate. |
| `tools/offset_spacing.py` | Spacing candidates mirror the table-discovery set and do not include 44 bytes. |
| `research/dattest/README.md` | States normalized logical changes align to 32-byte record bases; fields recur at offsets `+1..+14` and `+19..+20`; observed record bytes are described through `+31`. |
| `research/dattest2/README.md` | Supports 32-byte records for observed TG and ID add slots; shows empty slots as exactly 32 bytes. |
| `research/dattest3/README.md` | Candidate table boundaries contain 30 occupied records from `0x10480-0x1083f` and `0x14f80-0x1533f`, with first empty slots at the next 32-byte offsets. |
| `research/dattest4/README.md` | Slot reuse and append evidence uses target slots spaced by 32 bytes and reports 32-byte target record probes. |
| `docs/EVIDENCE_MATRIX.md` | Summarizes candidate TG and Individual ID records as 32 bytes in observed table regions. |
| `docs/WRITER_DESIGN.md` | Treats 32-byte candidate records as supported but keeps table boundaries/capacity and writer safety unresolved. |

## Search Results

- No human-readable report or Python source file was found claiming a 44-byte Talk Group or Individual ID record.
- No `RECORD_SIZE = 44` definition was found.
- No `44-byte record` or `44 byte record` wording was found.
- Earlier tools tested many candidate sizes, including 40 and 48, but not 44.
- Earlier reports repeatedly describe 32-byte candidate records and explicitly warn that statistical spacing evidence alone is not proof.

## Calculations

| Calculation | Result | Interpretation |
| --- | ---: | --- |
| Dattest ID previous occupied `0x10620` to add slot `0x10640` | `0x20 = 32` | Next observed ID slot is one 32-byte step. |
| Dattest TG previous occupied `0x15180` to add slot `0x151a0` | `0x20 = 32` | Next observed TG slot is one 32-byte step. |
| Dattest3 ID occupied run `0x10480` through `0x1083f` | `0x3c0 = 960`; `960 / 32 = 30` | Exactly matches the reported 30 occupied ID records. |
| Dattest3 TG occupied run `0x14f80` through `0x1533f` | `0x3c0 = 960`; `960 / 32 = 30` | Exactly matches the reported 30 occupied TG records. |
| ID table start `0x10480` to TG table start `0x14f80` | `0x4b00 = 19200`; `19200 / 32 = 600` | Table-start spacing is an exact multiple of 32. |
| Same ID table start to TG table start using 44 | `19200 / 44 = 436.36` | Not an integral 44-byte stride. |
| Dattest3 occupied run using 44 | `960 / 44 = 21.82` | Does not match reported 30 records. |

Changed-field offsets also support a 32-byte base:

| Example | Base | Changed Field Offset | Base Mod 32 | Base Mod 44 |
| --- | ---: | ---: | ---: | ---: |
| Dattest add TG name | `0x151a0` | `+1` | `0` | `16` |
| Dattest add TG numeric | `0x151a0` | `+19` | `0` | `16` |
| Dattest add ID name | `0x10640` | `+1` | `0` | `36` |
| Dattest add ID numeric | `0x10640` | `+19` | `0` | `36` |
| Dattest3 TG edit name | `0x15140` | `+1` | `0` | `8` |
| Dattest3 ID clear name | `0x105a0` | `+1` | `0` | `8` |

The observed bases are aligned to 32-byte boundaries and do not share a stable 44-byte alignment.

## Determination

Current evidence supports 32 bytes as the complete supported table-record slice for known Talk Group and Individual ID entries in the observed files.

This does not prove every possible KPG111 table uses 32 bytes, nor does it prove global table capacity or all metadata behavior. It does mean the current 32-byte decoder is not merely decoding a 32-byte payload inside a proven 44-byte record. No evidence was found for a larger 44-byte TG/ID record whose trailing bytes are outside the decoder slice.

## Confidence

| Claim | Confidence | Reason |
| --- | --- | --- |
| Known TG/ID table entries in current experiments use a 32-byte stride | HIGH | Add, edit, delete, reuse, and append observations all align to 32-byte slots. |
| The current decoder's 32-byte slice covers the complete observed TG/ID table record | HIGH for observed files | Reports describe fields through `+31`; no adjacent changed bytes or 44-byte tail evidence is reported. |
| 44-byte TG/ID records exist in current evidence | LOW | No source or report evidence found; calculations do not fit observed runs. |
| All KPG111 records/tables everywhere are 32 bytes | UNKNOWN | Other candidate runs exist in table maps, and this audit only covers known TG/ID records. |

## Recommendation

- Keep `RECORD_SIZE = 32` for the current read-only TG/ID decoder.
- Treat `32 bytes` as the complete supported TG/ID table record slice for observed files, not as a decoded payload nested inside a known larger record.
- Continue calling full table boundaries, capacity, count fields, checksums, and metadata behavior unresolved.
- Do not introduce 44-byte writer or encoder assumptions without new controlled evidence.
- Keep unknown bytes `+0`, `+15..+18`, and `+21..+31` marked UNKNOWN / candidate reserved or padding.

## Record Specification Impact

`docs/RECORD_SPECIFICATION.md` did not require a record-size correction. Its wording was tightened from "decoded record size" to "supported TG/ID table record size" to avoid implying that 32 bytes is only a decoded payload.
