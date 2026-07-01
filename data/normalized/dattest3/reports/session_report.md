# KPG111 Comparison Session Report

This report contains statistical observations only. It does not decode or claim field meanings.

- Sessions analyzed: 4
- Total changed-offset observations: 504627
- Total changed-region observations: 17

## Sessions
| Session | Baseline Size | Modified Size | Size Change | Changed Offsets | Changed Regions |
| --- | --- | --- | --- | --- | --- |
| research/dattest3/sessions/Program1.session.json | 168257 | 168257 | +0 | 168193 | 1 |
| research/dattest3/sessions/Program2.session.json | 168257 | 168257 | +0 | 168191 | 3 |
| research/dattest3/sessions/Program3.session.json | 168257 | 168257 | +0 | 168190 | 4 |
| research/dattest3/sessions/Program4.session.json | 168257 | 168257 | +0 | 53 | 9 |

## Recurring Changed Offsets
| Offset | Sessions | Observed Byte Deltas |
| --- | --- | --- |
| 0x000105a1 | 4 | 2, 37, 41, 140 |
| 0x000105a2 | 4 | -45, -41, -4, 99 |
| 0x000105a3 | 4 | -25, -21, 1, 111 |
| 0x000105a4 | 4 | -29, -25, -3, 107 |
| 0x000105a5 | 4 | -41, -37, -10, 103 |
| 0x000105a6 | 4 | -27, -23, -20, 174 |
| 0x000105a7 | 4 | -47, -43, -32, 162 |
| 0x000105a8 | 4 | -53, 39, 43, 141 |
| 0x000105a9 | 4 | -47, 19, 23, 147 |
| 0x000105aa | 4 | -45, -41, -15, 179 |
| 0x000105ab | 4 | -43, 23, 27, 151 |
| 0x000105ac | 4 | -45, 23, 27, 149 |
| 0x000105ad | 4 | -63, 19, 23, 131 |
| 0x000105b3 | 4 | -28, 37, 41, 76 |
| 0x000105b4 | 4 | 25, 29, 58, 216 |
| 0x00010641 | 4 | -4, -3, 34, 38 |
| 0x00010643 | 4 | 26, 30, 48, 49 |
| 0x00010644 | 4 | 8, 12, 45, 46 |
| 0x00010645 | 4 | -106, -102, -60, -59 |
| 0x00010646 | 4 | -20, -19, 7, 11 |
| 0x00010647 | 4 | -16, -12, 5, 6 |
| 0x00010648 | 4 | 26, 30, 48, 49 |
| 0x00010649 | 4 | 40, 44, 81, 82 |
| 0x0001064a | 4 | -12, -11, 6, 10 |
| 0x0001064b | 4 | -12, -11, 6, 10 |

## Recurring Changed Regions
| Region Span | Sessions | Observed Region Lengths |
| --- | --- | --- |
| 0x00000040-0x00029140 | 4 | 1-168193 |

## Probable Record Boundary Signals

These are alignment and length observations from changed regions, not confirmed record sizes.
| Region Start Alignment | Observations |
| --- | --- |
| 2 | 7 |
| 4 | 7 |
| 8 | 4 |
| 16 | 3 |
| 32 | 3 |
| 64 | 3 |

| Changed Region Length | Observations |
| --- | --- |
| 2 | 3 |
| 11 | 2 |
| 13 | 2 |
| 1 | 2 |
| 168193 | 1 |
| 67074 | 1 |
| 19205 | 1 |
| 81912 | 1 |
| 67091 | 1 |
| 19187 | 1 |
| 81901 | 1 |
| 8 | 1 |

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
| research/dattest3/sessions/Program1.session.json | 660 | 818 |
| research/dattest3/sessions/Program2.session.json | 703 | 818 |
| research/dattest3/sessions/Program3.session.json | 816 | 818 |
| research/dattest3/sessions/Program4.session.json | 4 | 4 |
