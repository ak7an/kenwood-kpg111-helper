# KPG111 Dominant XOR Rewrite Analysis

This report derives byte-level evidence only. Normalized changes are not decoded field meanings.

## Baseline

- Path: `research/dattest/Dattest/AK7AN_Travel.dat`
- Size: 168257 bytes
- SHA-256: `aa20a84b5cb76e5fd58a691eb26fdc4140e7d75fb3bd6b28fc156f3ec4144cce`

## Pair Summary
| Modified | Common Prefix | Dominant XOR | Dominant Count | Dominant Ratio | XOR Exceptions | Normalized Changed Bytes | Normalized Regions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| research/dattest/Dattest/Program_1TG.dat | 0x40 | 0x3e | 168177 | 99.9905% | 16 | 16 | 2 |
| research/dattest/Dattest/Program_1ID.dat | 0x40 | 0x0c | 168161 | 99.9810% | 32 | 32 | 4 |
| research/dattest/Dattest/Program_Rename.dat | 0x40 | 0x67 | 168181 | 99.9929% | 12 | 12 | 1 |
| research/dattest/Dattest/Program_Delete.dat | 0x40 | 0x1e | 168165 | 99.9834% | 28 | 28 | 3 |

## Program_1TG.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x3e | 168177 |
| 0xc1 | 6 |
| 0x95 | 2 |
| 0x86 | 1 |
| 0x91 | 1 |
| 0xa4 | 1 |
| 0xb2 | 1 |
| 0xb5 | 1 |
| 0xf0 | 1 |
| 0x28 | 1 |
| 0x3c | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x000151a1-0x000151ae | 14 |
| 0x000151b3-0x000151b4 | 2 |

### Normalized Change Samples
- `0x000151a1-0x000151ae` len=14
  - before @`0x00015199`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x00015199`: `a4 a4 a4 a4 a4 a4 a4 a4 1c 0b 0f 0f 3e 28 2f 6a 5b 5b 5b 5b 5b 5b a4 a4 a4 a4 b2 a6 a4 a4`
  - before ASCII: `..............................`
  - after ASCII: `............>(/j[[[[[[........`
- `0x000151b3-0x000151b4` len=2
  - before @`0x000151ab`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x000151ab`: `5b 5b 5b 5b a4 a4 a4 a4 b2 a6 a4 a4 a4 a4 a4 a4 a4 a4`
  - before ASCII: `..................`
  - after ASCII: `[[[[..............`

## Program_1ID.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x0c | 168161 |
| 0xf3 | 13 |
| 0x96 | 2 |
| 0xa7 | 2 |
| 0xb1 | 1 |
| 0x81 | 1 |
| 0x92 | 1 |
| 0x97 | 1 |
| 0x9f | 1 |
| 0x8a | 1 |
| 0xba | 1 |
| 0xee | 1 |
| 0xb4 | 1 |
| 0xa3 | 1 |
| 0x80 | 1 |
| 0x87 | 1 |
| 0xc2 | 1 |
| 0x1a | 1 |
| 0x0e | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x00010641-0x0001064e | 14 |
| 0x00010653-0x00010654 | 2 |
| 0x000151a1-0x000151ae | 14 |
| 0x000151b3-0x000151b4 | 2 |

### Normalized Change Samples
- `0x00010641-0x0001064e` len=14
  - before @`0x00010639`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x00010639`: `a4 a4 a4 a4 a4 a4 a4 a4 19 29 3a 3f 37 3e 22 5b 5b 5b 5b 5b 5b 5b a4 a4 a4 a4 12 46 a4 a4`
  - before ASCII: `..............................`
  - after ASCII: `.........):?7>"[[[[[[[.....F..`
- `0x00010653-0x00010654` len=2
  - before @`0x0001064b`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x0001064b`: `5b 5b 5b 5b a4 a4 a4 a4 12 46 a4 a4 a4 a4 a4 a4 a4 a4`
  - before ASCII: `..................`
  - after ASCII: `[[[[.....F........`
- `0x000151a1-0x000151ae` len=14
  - before @`0x00015199`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x00015199`: `a4 a4 a4 a4 a4 a4 a4 a4 1c 0b 0f 0f 3e 28 2f 6a 5b 5b 5b 5b 5b 5b a4 a4 a4 a4 b2 a6 a4 a4`
  - before ASCII: `..............................`
  - after ASCII: `............>(/j[[[[[[........`
- `0x000151b3-0x000151b4` len=2
  - before @`0x000151ab`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x000151ab`: `5b 5b 5b 5b a4 a4 a4 a4 b2 a6 a4 a4 a4 a4 a4 a4 a4 a4`
  - before ASCII: `..................`
  - after ASCII: `[[[[..............`

## Program_Rename.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x67 | 168181 |
| 0x64 | 2 |
| 0x45 | 1 |
| 0x24 | 1 |
| 0x50 | 1 |
| 0x05 | 1 |
| 0x5a | 1 |
| 0x54 | 1 |
| 0x2f | 1 |
| 0x06 | 1 |
| 0x0a | 1 |
| 0x14 | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x00015181-0x0001518c | 12 |

### Normalized Change Samples
- `0x00015181-0x0001518c` len=12
  - before @`0x00015179`: `a4 a4 a4 a4 a4 a4 a4 a4 1a 10 6c 1a 15 7b 0f 1c 5b 5b 5b 5b 5b 5b a4 a4 a4 a4 46 08`
  - after  @`0x00015179`: `a4 a4 a4 a4 a4 a4 a4 a4 19 32 2f 19 22 19 32 2f 13 3a 36 28 5b 5b a4 a4 a4 a4 46 08`
  - before ASCII: `..........l..{..[[[[[[....F.`
  - after ASCII: `.........2/.".2/.:6([[....F.`

## Program_Delete.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x1e | 168165 |
| 0x82 | 2 |
| 0x8f | 2 |
| 0x1d | 2 |
| 0xa5 | 1 |
| 0x88 | 1 |
| 0x92 | 1 |
| 0x8e | 1 |
| 0x84 | 1 |
| 0x95 | 1 |
| 0xc1 | 1 |
| 0xb5 | 1 |
| 0xa6 | 1 |
| 0xe1 | 1 |
| 0xee | 1 |
| 0xc6 | 1 |
| 0x3c | 1 |
| 0x5d | 1 |
| 0x29 | 1 |
| 0x7c | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x00015121-0x0001512e | 14 |
| 0x00015133-0x00015134 | 2 |
| 0x00015181-0x0001518c | 12 |

### Normalized Change Samples
- `0x00015121-0x0001512e` len=14
  - before @`0x00015119`: `a4 a4 a4 a4 a4 a4 a4 a4 1f 32 28 38 34 35 35 3e 38 2f 7b 0f 1c 5b a4 a4 a4 a4 54 7c a4 a4`
  - after  @`0x00015119`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - before ASCII: `.........2(8455>8/{..[....T|..`
  - after ASCII: `..............................`
- `0x00015133-0x00015134` len=2
  - before @`0x0001512b`: `7b 0f 1c 5b a4 a4 a4 a4 54 7c a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x0001512b`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - before ASCII: `{..[....T|........`
  - after ASCII: `..................`
- `0x00015181-0x0001518c` len=12
  - before @`0x00015179`: `a4 a4 a4 a4 a4 a4 a4 a4 1a 10 6c 1a 15 7b 0f 1c 5b 5b 5b 5b 5b 5b a4 a4 a4 a4 46 08`
  - after  @`0x00015179`: `a4 a4 a4 a4 a4 a4 a4 a4 19 32 2f 19 22 19 32 2f 13 3a 36 28 5b 5b a4 a4 a4 a4 46 08`
  - before ASCII: `..........l..{..[[[[[[....F.`
  - after ASCII: `.........2/.".2/.:6([[....F.`

