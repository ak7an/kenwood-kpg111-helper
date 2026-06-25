# KPG111 Dominant XOR Rewrite Analysis

This report derives byte-level evidence only. Normalized changes are not decoded field meanings.

## Baseline

- Path: `research/dattest4/Dattest4/Program3.dat`
- Size: 168257 bytes
- SHA-256: `370e94b05d195f8eb1e3afc9c1d86159f560f217eb5aae3c6193fc8a4501528f`

## Pair Summary
| Modified | Common Prefix | Dominant XOR | Dominant Count | Dominant Ratio | XOR Exceptions | Normalized Changed Bytes | Normalized Regions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| research/dattest4/Dattest4/Program5.dat | 0x40 | 0x46 | 168145 | 99.9715% | 48 | 48 | 6 |
| research/dattest4/Dattest4/Program6.dat | 0x40 | 0x4a | 168129 | 99.9619% | 64 | 64 | 8 |

## Program5.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x46 | 168145 |
| 0xb9 | 17 |
| 0xd6 | 3 |
| 0x99 | 3 |
| 0x89 | 3 |
| 0xdc | 2 |
| 0xd5 | 2 |
| 0xf0 | 2 |
| 0xf1 | 1 |
| 0xdf | 1 |
| 0xe5 | 1 |
| 0xec | 1 |
| 0xf7 | 1 |
| 0xed | 1 |
| 0xfd | 1 |
| 0x8a | 1 |
| 0x88 | 1 |
| 0xb8 | 1 |
| 0x13 | 1 |
| 0xfe | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x000105a1-0x000105ae | 14 |
| 0x000105b3-0x000105b4 | 2 |
| 0x00010841-0x0001084e | 14 |
| 0x00010853-0x00010854 | 2 |
| 0x000150a1-0x000150ae | 14 |
| 0x000150b3-0x000150b4 | 2 |

### Normalized Change Samples
- `0x000105a1-0x000105ae` len=14
  - before @`0x00010599`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x00010599`: `e1 e1 e1 e1 e1 e1 e1 e1 56 7b 72 72 71 1e 1e 1e 1e 1e 1e 1e 1e 1e e1 e1 e1 e1 78 42 e1 e1`
  - before ASCII: `..............................`
  - after ASCII: `........V{rrq.............xB..`
- `0x000105b3-0x000105b4` len=2
  - before @`0x000105ab`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x000105ab`: `1e 1e 1e 1e e1 e1 e1 e1 78 42 e1 e1 e1 e1 e1 e1 e1 e1`
  - before ASCII: `..................`
  - after ASCII: `........xB........`
- `0x00010841-0x0001084e` len=14
  - before @`0x00010839`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x00010839`: `e1 e1 e1 e1 e1 e1 e1 e1 3e 4b 50 57 4a 3e 57 5a 3e 2e 2e 2d 2f 1e e1 e1 e1 e1 1f b4 e1 e1`
  - before ASCII: `..............................`
  - after ASCII: `........>KPWJ>WZ>..-/.........`
- `0x00010853-0x00010854` len=2
  - before @`0x0001084b`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x0001084b`: `2e 2d 2f 1e e1 e1 e1 e1 1f b4 e1 e1 e1 e1 e1 e1 e1 e1`
  - before ASCII: `..................`
  - after ASCII: `.-/...............`
- `0x000150a1-0x000150ae` len=14
  - before @`0x00015099`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x00015099`: `e1 e1 e1 e1 e1 e1 e1 e1 59 71 71 7a 7c 67 7b 1e 1e 1e 1e 1e 1e 1e e1 e1 e1 e1 2e 5e e1 e1`
  - before ASCII: `..............................`
  - after ASCII: `........Yqqz|g{............^..`
- `0x000150b3-0x000150b4` len=2
  - before @`0x000150ab`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x000150ab`: `1e 1e 1e 1e e1 e1 e1 e1 2e 5e e1 e1 e1 e1 e1 e1 e1 e1`
  - before ASCII: `..................`
  - after ASCII: `.........^........`

## Program6.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x4a | 168129 |
| 0xb5 | 18 |
| 0x95 | 5 |
| 0x85 | 5 |
| 0xda | 3 |
| 0xfc | 3 |
| 0xfd | 2 |
| 0xd0 | 2 |
| 0xd9 | 2 |
| 0xe0 | 2 |
| 0xf1 | 2 |
| 0x86 | 2 |
| 0x84 | 2 |
| 0xf2 | 2 |
| 0xd3 | 1 |
| 0xe9 | 1 |
| 0xfb | 1 |
| 0xe1 | 1 |
| 0xb4 | 1 |
| 0x1f | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x000105a1-0x000105ae | 14 |
| 0x000105b3-0x000105b4 | 2 |
| 0x00010841-0x0001084e | 14 |
| 0x00010853-0x00010854 | 2 |
| 0x000150a1-0x000150ae | 14 |
| 0x000150b3-0x000150b4 | 2 |
| 0x00015341-0x0001534e | 14 |
| 0x00015353-0x00015354 | 2 |

### Normalized Change Samples
- `0x000105a1-0x000105ae` len=14
  - before @`0x00010599`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x00010599`: `e1 e1 e1 e1 e1 e1 e1 e1 56 7b 72 72 71 1e 1e 1e 1e 1e 1e 1e 1e 1e e1 e1 e1 e1 78 42 e1 e1`
  - before ASCII: `..............................`
  - after ASCII: `........V{rrq.............xB..`
- `0x000105b3-0x000105b4` len=2
  - before @`0x000105ab`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x000105ab`: `1e 1e 1e 1e e1 e1 e1 e1 78 42 e1 e1 e1 e1 e1 e1 e1 e1`
  - before ASCII: `..................`
  - after ASCII: `........xB........`
- `0x00010841-0x0001084e` len=14
  - before @`0x00010839`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x00010839`: `e1 e1 e1 e1 e1 e1 e1 e1 3e 4b 50 57 4a 3e 57 5a 3e 2e 2e 2d 2f 1e e1 e1 e1 e1 1f b4 e1 e1`
  - before ASCII: `..............................`
  - after ASCII: `........>KPWJ>WZ>..-/.........`
- `0x00010853-0x00010854` len=2
  - before @`0x0001084b`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x0001084b`: `2e 2d 2f 1e e1 e1 e1 e1 1f b4 e1 e1 e1 e1 e1 e1 e1 e1`
  - before ASCII: `..................`
  - after ASCII: `.-/...............`
- `0x000150a1-0x000150ae` len=14
  - before @`0x00015099`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x00015099`: `e1 e1 e1 e1 e1 e1 e1 e1 59 71 71 7a 7c 67 7b 1e 1e 1e 1e 1e 1e 1e e1 e1 e1 e1 2e 5e e1 e1`
  - before ASCII: `..............................`
  - after ASCII: `........Yqqz|g{............^..`
- `0x000150b3-0x000150b4` len=2
  - before @`0x000150ab`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x000150ab`: `1e 1e 1e 1e e1 e1 e1 e1 2e 5e e1 e1 e1 e1 e1 e1 e1 e1`
  - before ASCII: `..................`
  - after ASCII: `.........^........`
- `0x00015341-0x0001534e` len=14
  - before @`0x00015339`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x00015339`: `e1 e1 e1 e1 e1 e1 e1 e1 59 4c 51 4b 4e 3e 57 5a 3e 2e 2e 2d 2f 1e e1 e1 e1 e1 56 22 e1 e1`
  - before ASCII: `..............................`
  - after ASCII: `........YLQKN>WZ>..-/.....V"..`
- `0x00015353-0x00015354` len=2
  - before @`0x0001534b`: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - after  @`0x0001534b`: `2e 2d 2f 1e e1 e1 e1 e1 56 22 e1 e1 e1 e1 e1 e1 e1 e1`
  - before ASCII: `..................`
  - after ASCII: `.-/.....V"........`

