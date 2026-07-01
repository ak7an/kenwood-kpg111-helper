# KPG111 Dominant XOR Rewrite Analysis

This report derives byte-level evidence only. Normalized changes are not decoded field meanings.

## Baseline

- Path: `research/dattest3/Dattest3/Program.dat`
- Size: 168257 bytes
- SHA-256: `c73e0cb6bcbff5765e90ceb4fcf856cb7e8088587a8deb4412b5b57868ee0cf5`

## Pair Summary
| Modified | Common Prefix | Dominant XOR | Dominant Count | Dominant Ratio | XOR Exceptions | Normalized Changed Bytes | Normalized Regions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| research/dattest3/Dattest3/Program1.dat | 0x40 | 0x2f | 168169 | 99.9857% | 24 | 24 | 2 |
| research/dattest3/Dattest3/Program2.dat | 0x40 | 0x2b | 168167 | 99.9845% | 26 | 26 | 4 |
| research/dattest3/Dattest3/Program3.dat | 0x40 | 0x01 | 168136 | 99.9661% | 57 | 57 | 8 |
| research/dattest3/Dattest3/Program4.dat | 0x105a1 | 0x00 | 168140 | 99.9685% | 53 | 53 | 9 |

## Program1.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x2f | 168169 |
| 0x1e | 3 |
| 0x04 | 2 |
| 0x34 | 2 |
| 0x1a | 2 |
| 0x2a | 1 |
| 0x1c | 1 |
| 0x6a | 1 |
| 0x1b | 1 |
| 0x7c | 1 |
| 0x16 | 1 |
| 0x32 | 1 |
| 0x3a | 1 |
| 0x67 | 1 |
| 0x61 | 1 |
| 0x4b | 1 |
| 0x2e | 1 |
| 0x77 | 1 |
| 0x66 | 1 |
| 0x1f | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x00010641-0x0001064d | 13 |
| 0x00015141-0x0001514b | 11 |

### Normalized Change Samples
- `0x00010641-0x0001064d` len=13
  - before @`0x00010639`: `e0 e0 e0 e0 e0 e0 e0 e0 56 5b 40 4b 7a 6c 6b 40 29 2a 2a 2e 26 1f e0 e0 e0 e0 f0 e0 e0`
  - after  @`0x00010639`: `e0 e0 e0 e0 e0 e0 e0 e0 53 70 71 78 3f 58 70 71 7a 1f 1f 1f 1f 1f e0 e0 e0 e0 f0 e0 e0`
  - before ASCII: `........V[@Kzlk@)**.&........`
  - after ASCII: `........Spqx?Xpqz............`
- `0x00015141-0x0001514b` len=11
  - before @`0x00015139`: `e0 e0 e0 e0 e0 e0 e0 e0 4a 6b 7e 77 3f 5b 4d 51 3f 2f 2f 1f 1f 1f e0 e0 e0 e0 1d`
  - after  @`0x00015139`: `e0 e0 e0 e0 e0 e0 e0 e0 57 70 6b 3f 71 3f 4c 7a 67 66 1f 1f 1f 1f e0 e0 e0 e0 1d`
  - before ASCII: `........Jk~w?[MQ?//........`
  - after ASCII: `........Wpk?q?Lzgf.........`

## Program2.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x2b | 168167 |
| 0x1a | 3 |
| 0x2a | 3 |
| 0x00 | 2 |
| 0x30 | 2 |
| 0x1e | 2 |
| 0x2e | 1 |
| 0x18 | 1 |
| 0x6e | 1 |
| 0x1f | 1 |
| 0x78 | 1 |
| 0x12 | 1 |
| 0x36 | 1 |
| 0x3e | 1 |
| 0x63 | 1 |
| 0x65 | 1 |
| 0x4f | 1 |
| 0x73 | 1 |
| 0x62 | 1 |
| 0x1b | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x00010641-0x0001064d | 13 |
| 0x00010653-0x00010653 | 1 |
| 0x00015141-0x0001514b | 11 |
| 0x00015153-0x00015153 | 1 |

### Normalized Change Samples
- `0x00010641-0x0001064d` len=13
  - before @`0x00010639`: `e0 e0 e0 e0 e0 e0 e0 e0 56 5b 40 4b 7a 6c 6b 40 29 2a 2a 2e 26 1f e0 e0 e0 e0 f0 e0 e0`
  - after  @`0x00010639`: `e0 e0 e0 e0 e0 e0 e0 e0 53 70 71 78 3f 58 70 71 7a 1f 1f 1f 1f 1f e0 e0 e0 e0 f1 e0 e0`
  - before ASCII: `........V[@Kzlk@)**.&........`
  - after ASCII: `........Spqx?Xpqz............`
- `0x00010653-0x00010653` len=1
  - before @`0x0001064b`: `2a 2e 26 1f e0 e0 e0 e0 f0 e0 e0 e0 e0 e0 e0 e0 e0`
  - after  @`0x0001064b`: `1f 1f 1f 1f e0 e0 e0 e0 f1 e0 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `*.&..............`
  - after ASCII: `.................`
- `0x00015141-0x0001514b` len=11
  - before @`0x00015139`: `e0 e0 e0 e0 e0 e0 e0 e0 4a 6b 7e 77 3f 5b 4d 51 3f 2f 2f 1f 1f 1f e0 e0 e0 e0 1d`
  - after  @`0x00015139`: `e0 e0 e0 e0 e0 e0 e0 e0 57 70 6b 3f 71 3f 4c 7a 67 66 1f 1f 1f 1f e0 e0 e0 e0 1c`
  - before ASCII: `........Jk~w?[MQ?//........`
  - after ASCII: `........Wpk?q?Lzgf.........`
- `0x00015153-0x00015153` len=1
  - before @`0x0001514b`: `2f 1f 1f 1f e0 e0 e0 e0 1d 64 e0 e0 e0 e0 e0 e0 e0`
  - after  @`0x0001514b`: `1f 1f 1f 1f e0 e0 e0 e0 1c 64 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `/........d.......`
  - after ASCII: `.........d.......`

## Program3.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x01 | 168136 |
| 0xfe | 4 |
| 0x30 | 3 |
| 0x00 | 3 |
| 0x9f | 2 |
| 0xde | 2 |
| 0xad | 2 |
| 0x2a | 2 |
| 0x1a | 2 |
| 0x34 | 2 |
| 0xb4 | 1 |
| 0x93 | 1 |
| 0x97 | 1 |
| 0x9b | 1 |
| 0xd2 | 1 |
| 0xb5 | 1 |
| 0xaf | 1 |
| 0xcf | 1 |
| 0xab | 1 |
| 0xbf | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x000105a1-0x000105ae | 14 |
| 0x000105b3-0x000105b4 | 2 |
| 0x00010641-0x0001064d | 13 |
| 0x00010653-0x00010653 | 1 |
| 0x000150a1-0x000150ae | 14 |
| 0x000150b4-0x000150b4 | 1 |
| 0x00015141-0x0001514b | 11 |
| 0x00015153-0x00015153 | 1 |

### Normalized Change Samples
- `0x000105a1-0x000105ae` len=14
  - before @`0x00010599`: `e0 e0 e0 e0 e0 e0 e0 e0 55 7e 72 76 7a 33 3f 54 4e 2e 4a 4c 5e 1f e0 e0 e0 e0 95 09 e0 e0`
  - after  @`0x00010599`: `e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `........U~rvz3?TN.JL^.........`
  - after ASCII: `..............................`
- `0x000105b3-0x000105b4` len=2
  - before @`0x000105ab`: `4a 4c 5e 1f e0 e0 e0 e0 95 09 e0 e0 e0 e0 e0 e0 e0 e0`
  - after  @`0x000105ab`: `e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `JL^...............`
  - after ASCII: `..................`
- `0x00010641-0x0001064d` len=13
  - before @`0x00010639`: `e0 e0 e0 e0 e0 e0 e0 e0 56 5b 40 4b 7a 6c 6b 40 29 2a 2a 2e 26 1f e0 e0 e0 e0 f0 e0 e0`
  - after  @`0x00010639`: `e0 e0 e0 e0 e0 e0 e0 e0 53 70 71 78 3f 58 70 71 7a 1f 1f 1f 1f 1f e0 e0 e0 e0 f1 e0 e0`
  - before ASCII: `........V[@Kzlk@)**.&........`
  - after ASCII: `........Spqx?Xpqz............`
- `0x00010653-0x00010653` len=1
  - before @`0x0001064b`: `2a 2e 26 1f e0 e0 e0 e0 f0 e0 e0 e0 e0 e0 e0 e0 e0`
  - after  @`0x0001064b`: `1f 1f 1f 1f e0 e0 e0 e0 f1 e0 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `*.&..............`
  - after ASCII: `.................`
- `0x000150a1-0x000150ae` len=14
  - before @`0x00015099`: `e0 e0 e0 e0 e0 e0 e0 e0 4c 7c 70 6b 73 7e 71 7b 3f 4b 58 1f 1f 1f e0 e0 e0 e0 e0 44 e0 e0`
  - after  @`0x00015099`: `e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `........L|pks~q{?KX........D..`
  - after ASCII: `..............................`
- `0x000150b4-0x000150b4` len=1
  - before @`0x000150ac`: `1f 1f 1f e0 e0 e0 e0 e0 44 e0 e0 e0 e0 e0 e0 e0 e0`
  - after  @`0x000150ac`: `e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `........D........`
  - after ASCII: `.................`
- `0x00015141-0x0001514b` len=11
  - before @`0x00015139`: `e0 e0 e0 e0 e0 e0 e0 e0 4a 6b 7e 77 3f 5b 4d 51 3f 2f 2f 1f 1f 1f e0 e0 e0 e0 1d`
  - after  @`0x00015139`: `e0 e0 e0 e0 e0 e0 e0 e0 57 70 6b 3f 71 3f 4c 7a 67 66 1f 1f 1f 1f e0 e0 e0 e0 1c`
  - before ASCII: `........Jk~w?[MQ?//........`
  - after ASCII: `........Wpk?q?Lzgf.........`
- `0x00015153-0x00015153` len=1
  - before @`0x0001514b`: `2f 1f 1f 1f e0 e0 e0 e0 1d 64 e0 e0 e0 e0 e0 e0 e0`
  - after  @`0x0001514b`: `1f 1f 1f 1f e0 e0 e0 e0 1c 64 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `/........d.......`
  - after ASCII: `.........d.......`

## Program4.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x00 | 168140 |
| 0x01 | 4 |
| 0x31 | 4 |
| 0x1b | 3 |
| 0x05 | 2 |
| 0x20 | 2 |
| 0x53 | 2 |
| 0x2b | 2 |
| 0x35 | 2 |
| 0x64 | 2 |
| 0x02 | 1 |
| 0x04 | 1 |
| 0x0a | 1 |
| 0x2c | 1 |
| 0x4b | 1 |
| 0x51 | 1 |
| 0x55 | 1 |
| 0x41 | 1 |
| 0xec | 1 |
| 0x4a | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x000105a1-0x000105ad | 13 |
| 0x000105b3-0x000105b4 | 2 |
| 0x00010641-0x0001064d | 13 |
| 0x00010653-0x00010653 | 1 |
| 0x000150a1-0x000150a2 | 2 |
| 0x000150a4-0x000150ab | 8 |
| 0x000150b3-0x000150b4 | 2 |
| 0x00015141-0x0001514b | 11 |
| 0x00015153-0x00015153 | 1 |

### Normalized Change Samples
- `0x000105a1-0x000105ad` len=13
  - before @`0x00010599`: `e0 e0 e0 e0 e0 e0 e0 e0 55 7e 72 76 7a 33 3f 54 4e 2e 4a 4c 5e 1f e0 e0 e0 e0 95 09 e0`
  - after  @`0x00010599`: `e0 e0 e0 e0 e0 e0 e0 e0 57 7a 73 73 70 1f 1f 1f 1f 1f 1f 1f 1f 1f e0 e0 e0 e0 79 43 e0`
  - before ASCII: `........U~rvz3?TN.JL^........`
  - after ASCII: `........Wzssp.............yC.`
- `0x000105b3-0x000105b4` len=2
  - before @`0x000105ab`: `4a 4c 5e 1f e0 e0 e0 e0 95 09 e0 e0 e0 e0 e0 e0 e0 e0`
  - after  @`0x000105ab`: `1f 1f 1f 1f e0 e0 e0 e0 79 43 e0 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `JL^...............`
  - after ASCII: `........yC........`
- `0x00010641-0x0001064d` len=13
  - before @`0x00010639`: `e0 e0 e0 e0 e0 e0 e0 e0 56 5b 40 4b 7a 6c 6b 40 29 2a 2a 2e 26 1f e0 e0 e0 e0 f0 e0 e0`
  - after  @`0x00010639`: `e0 e0 e0 e0 e0 e0 e0 e0 53 70 71 78 3f 58 70 71 7a 1f 1f 1f 1f 1f e0 e0 e0 e0 f1 e0 e0`
  - before ASCII: `........V[@Kzlk@)**.&........`
  - after ASCII: `........Spqx?Xpqz............`
- `0x00010653-0x00010653` len=1
  - before @`0x0001064b`: `2a 2e 26 1f e0 e0 e0 e0 f0 e0 e0 e0 e0 e0 e0 e0 e0`
  - after  @`0x0001064b`: `1f 1f 1f 1f e0 e0 e0 e0 f1 e0 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `*.&..............`
  - after ASCII: `.................`
- `0x000150a1-0x000150a2` len=2
  - before @`0x00015099`: `e0 e0 e0 e0 e0 e0 e0 e0 4c 7c 70 6b 73 7e 71 7b 3f 4b`
  - after  @`0x00015099`: `e0 e0 e0 e0 e0 e0 e0 e0 58 70 70 7b 7d 66 7a 1f 1f 1f`
  - before ASCII: `........L|pks~q{?K`
  - after ASCII: `........Xpp{}fz...`
- `0x000150a4-0x000150ab` len=8
  - before @`0x0001509c`: `e0 e0 e0 e0 e0 4c 7c 70 6b 73 7e 71 7b 3f 4b 58 1f 1f 1f e0 e0 e0 e0 e0`
  - after  @`0x0001509c`: `e0 e0 e0 e0 e0 58 70 70 7b 7d 66 7a 1f 1f 1f 1f 1f 1f 1f e0 e0 e0 e0 2f`
  - before ASCII: `.....L|pks~q{?KX........`
  - after ASCII: `.....Xpp{}fz.........../`
- `0x000150b3-0x000150b4` len=2
  - before @`0x000150ab`: `58 1f 1f 1f e0 e0 e0 e0 e0 44 e0 e0 e0 e0 e0 e0 e0 e0`
  - after  @`0x000150ab`: `1f 1f 1f 1f e0 e0 e0 e0 2f 5f e0 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `X........D........`
  - after ASCII: `......../_........`
- `0x00015141-0x0001514b` len=11
  - before @`0x00015139`: `e0 e0 e0 e0 e0 e0 e0 e0 4a 6b 7e 77 3f 5b 4d 51 3f 2f 2f 1f 1f 1f e0 e0 e0 e0 1d`
  - after  @`0x00015139`: `e0 e0 e0 e0 e0 e0 e0 e0 57 70 6b 3f 71 3f 4c 7a 67 66 1f 1f 1f 1f e0 e0 e0 e0 1c`
  - before ASCII: `........Jk~w?[MQ?//........`
  - after ASCII: `........Wpk?q?Lzgf.........`
- `0x00015153-0x00015153` len=1
  - before @`0x0001514b`: `2f 1f 1f 1f e0 e0 e0 e0 1d 64 e0 e0 e0 e0 e0 e0 e0`
  - after  @`0x0001514b`: `1f 1f 1f 1f e0 e0 e0 e0 1c 64 e0 e0 e0 e0 e0 e0 e0`
  - before ASCII: `/........d.......`
  - after ASCII: `.........d.......`

