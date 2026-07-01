# KPG111 Comparison Session Report

This report contains statistical observations only. It does not decode or claim field meanings.

- Sessions analyzed: 10
- Total changed-offset observations: 1681930
- Total changed-region observations: 10

## Sessions
| Session | Baseline Size | Modified Size | Size Change | Changed Offsets | Changed Regions |
| --- | --- | --- | --- | --- | --- |
| research/dattest2/sessions/Program_ID_00001.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest2/sessions/Program_ID_00100.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest2/sessions/Program_ID_12345.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest2/sessions/Program_ID_65519.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest2/sessions/Program_Nochange2.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest2/sessions/Program_Nochange3.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest2/sessions/Program_TG_00001.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest2/sessions/Program_TG_00100.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest2/sessions/Program_TG_12345.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest2/sessions/Program_TG_65516.session.json | 168257 | 168257 | +0 | 168193 | 1 |

## Recurring Changed Offsets
| Offset | Sessions | Observed Byte Deltas |
| --- | --- | --- |
| 0x00000040 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000041 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000042 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000043 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000044 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000045 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000046 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000047 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000048 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000049 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x0000004a | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x0000004b | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x0000004c | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x0000004d | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x0000004e | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x0000004f | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000050 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000051 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000052 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000053 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000054 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000055 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000056 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000057 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |
| 0x00000058 | 10 | -34, -29, -24, -20, -12, -11, -10, 8, 13 |

## Recurring Changed Regions
| Region Span | Sessions | Observed Region Lengths |
| --- | --- | --- |
| 0x00000040-0x00029140 | 10 | 168193-168193 |

## Probable Record Boundary Signals

These are alignment and length observations from changed regions, not confirmed record sizes.
| Region Start Alignment | Observations |
| --- | --- |
| 2 | 10 |
| 4 | 10 |
| 8 | 10 |
| 16 | 10 |
| 32 | 10 |
| 64 | 10 |

| Changed Region Length | Observations |
| --- | --- |
| 168193 | 10 |

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
| research/dattest2/sessions/Program_ID_00001.session.json | 231 | 695 |
| research/dattest2/sessions/Program_ID_00100.session.json | 633 | 695 |
| research/dattest2/sessions/Program_ID_12345.session.json | 649 | 695 |
| research/dattest2/sessions/Program_ID_65519.session.json | 300 | 695 |
| research/dattest2/sessions/Program_Nochange2.session.json | 295 | 695 |
| research/dattest2/sessions/Program_Nochange3.session.json | 283 | 695 |
| research/dattest2/sessions/Program_TG_00001.session.json | 284 | 695 |
| research/dattest2/sessions/Program_TG_00100.session.json | 711 | 695 |
| research/dattest2/sessions/Program_TG_12345.session.json | 649 | 695 |
| research/dattest2/sessions/Program_TG_65516.session.json | 700 | 695 |
