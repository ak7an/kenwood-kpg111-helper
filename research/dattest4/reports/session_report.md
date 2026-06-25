# KPG111 Comparison Session Report

This report contains statistical observations only. It does not decode or claim field meanings.

- Sessions analyzed: 2
- Total changed-offset observations: 336386
- Total changed-region observations: 2

## Sessions
| Session | Baseline Size | Modified Size | Size Change | Changed Offsets | Changed Regions |
| --- | --- | --- | --- | --- | --- |
| research/dattest4/sessions/Program5.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest4/sessions/Program6.session.json | 168257 | 168257 | +0 | 168193 | 1 |

## Recurring Changed Offsets
| Offset | Sessions | Observed Byte Deltas |
| --- | --- | --- |
| 0x00000040 | 2 | -58, -54 |
| 0x00000041 | 2 | -58, -54 |
| 0x00000042 | 2 | -58, -54 |
| 0x00000043 | 2 | -58, -54 |
| 0x00000044 | 2 | -58, -54 |
| 0x00000045 | 2 | -58, -54 |
| 0x00000046 | 2 | -58, -54 |
| 0x00000047 | 2 | -58, -54 |
| 0x00000048 | 2 | -58, -54 |
| 0x00000049 | 2 | -58, -54 |
| 0x0000004a | 2 | -58, -54 |
| 0x0000004b | 2 | -58, -54 |
| 0x0000004c | 2 | -58, -54 |
| 0x0000004d | 2 | -58, -54 |
| 0x0000004e | 2 | -58, -54 |
| 0x0000004f | 2 | -58, -54 |
| 0x00000050 | 2 | -58, -54 |
| 0x00000051 | 2 | -58, -54 |
| 0x00000052 | 2 | -58, -54 |
| 0x00000053 | 2 | -58, -54 |
| 0x00000054 | 2 | -58, -54 |
| 0x00000055 | 2 | -58, -54 |
| 0x00000056 | 2 | -58, -54 |
| 0x00000057 | 2 | -58, -54 |
| 0x00000058 | 2 | -58, -54 |

## Recurring Changed Regions
| Region Span | Sessions | Observed Region Lengths |
| --- | --- | --- |
| 0x00000040-0x00029140 | 2 | 168193-168193 |

## Probable Record Boundary Signals

These are alignment and length observations from changed regions, not confirmed record sizes.
| Region Start Alignment | Observations |
| --- | --- |
| 2 | 2 |
| 4 | 2 |
| 8 | 2 |
| 16 | 2 |
| 32 | 2 |
| 64 | 2 |

| Changed Region Length | Observations |
| --- | --- |
| 168193 | 2 |

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
| research/dattest4/sessions/Program5.session.json | 318 | 816 |
| research/dattest4/sessions/Program6.session.json | 318 | 816 |
