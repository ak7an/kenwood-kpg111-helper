# KPG111 Comparison Session Report

This report contains statistical observations only. It does not decode or claim field meanings.

- Sessions analyzed: 4
- Total changed-offset observations: 672772
- Total changed-region observations: 4

## Sessions
| Session | Baseline Size | Modified Size | Size Change | Changed Offsets | Changed Regions |
| --- | --- | --- | --- | --- | --- |
| research/dattest/sessions/Program_1TG.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest/sessions/Program_1ID.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest/sessions/Program_Rename.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest/sessions/Program_Delete.session.json | 168257 | 168257 | +0 | 168193 | 1 |

## Recurring Changed Offsets
| Offset | Sessions | Observed Byte Deltas |
| --- | --- | --- |
| 0x00000040 | 4 | -10, 4, 22, 31 |
| 0x00000041 | 4 | -10, 4, 22, 31 |
| 0x00000042 | 4 | -10, 4, 22, 31 |
| 0x00000043 | 4 | -10, 4, 22, 31 |
| 0x00000044 | 4 | -10, 4, 22, 31 |
| 0x00000045 | 4 | -10, 4, 22, 31 |
| 0x00000046 | 4 | -10, 4, 22, 31 |
| 0x00000047 | 4 | -10, 4, 22, 31 |
| 0x00000048 | 4 | -10, 4, 22, 31 |
| 0x00000049 | 4 | -10, 4, 22, 31 |
| 0x0000004a | 4 | -10, 4, 22, 31 |
| 0x0000004b | 4 | -10, 4, 22, 31 |
| 0x0000004c | 4 | -10, 4, 22, 31 |
| 0x0000004d | 4 | -10, 4, 22, 31 |
| 0x0000004e | 4 | -10, 4, 22, 31 |
| 0x0000004f | 4 | -10, 4, 22, 31 |
| 0x00000050 | 4 | -10, 4, 22, 31 |
| 0x00000051 | 4 | -10, 4, 22, 31 |
| 0x00000052 | 4 | -10, 4, 22, 31 |
| 0x00000053 | 4 | -10, 4, 22, 31 |
| 0x00000054 | 4 | -10, 4, 22, 31 |
| 0x00000055 | 4 | -10, 4, 22, 31 |
| 0x00000056 | 4 | -10, 4, 22, 31 |
| 0x00000057 | 4 | -10, 4, 22, 31 |
| 0x00000058 | 4 | -10, 4, 22, 31 |

## Recurring Changed Regions
| Region Span | Sessions | Observed Region Lengths |
| --- | --- | --- |
| 0x00000040-0x00029140 | 4 | 168193-168193 |

## Probable Record Boundary Signals

These are alignment and length observations from changed regions, not confirmed record sizes.
| Region Start Alignment | Observations |
| --- | --- |
| 2 | 4 |
| 4 | 4 |
| 8 | 4 |
| 16 | 4 |
| 32 | 4 |
| 64 | 4 |

| Changed Region Length | Observations |
| --- | --- |
| 168193 | 4 |

## Possible Count Field Signals

Short recurring changed regions can be count fields, indexes, flags, or unrelated small values.
| Short Region Offset | Observations |
| --- | --- |
| none | none |

## Possible Checksum Field Signals

Recurring changes near the end of files can be checksum-like, but may also be normal data.
| Tail Region Offset | Observations |
| --- | --- |
| none | none |

## String Changes
| Session | Strings Added | Strings Removed |
| --- | --- | --- |
| research/dattest/sessions/Program_1TG.session.json | 865 | 299 |
| research/dattest/sessions/Program_1ID.session.json | 297 | 299 |
| research/dattest/sessions/Program_Rename.session.json | 665 | 299 |
| research/dattest/sessions/Program_Delete.session.json | 299 | 299 |
