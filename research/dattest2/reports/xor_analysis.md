# KPG111 Dominant XOR Rewrite Analysis

This report derives byte-level evidence only. Normalized changes are not decoded field meanings.

## Baseline

- Path: `research/dattest2/Dattest2/Program_Nochange1.dat`
- Size: 168257 bytes
- SHA-256: `3b6530c9d6ceda7392947c5c99209888a58fe4352440215d73f5820ab22b68c9`

## Pair Summary
| Modified | Common Prefix | Dominant XOR | Dominant Count | Dominant Ratio | XOR Exceptions | Normalized Changed Bytes | Normalized Regions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| research/dattest2/Dattest2/Program_Nochange2.dat | 0x40 | 0x74 | 168193 | 100.0000% | 0 | 0 | 0 |
| research/dattest2/Dattest2/Program_Nochange3.dat | 0x40 | 0x7c | 168193 | 100.0000% | 0 | 0 | 0 |
| research/dattest2/Dattest2/Program_TG_00001.dat | 0x40 | 0x78 | 168177 | 99.9905% | 16 | 16 | 2 |
| research/dattest2/Dattest2/Program_TG_00100.dat | 0x40 | 0x0b | 168177 | 99.9905% | 16 | 16 | 2 |
| research/dattest2/Dattest2/Program_TG_12345.dat | 0x40 | 0x18 | 168177 | 99.9905% | 16 | 16 | 2 |
| research/dattest2/Dattest2/Program_TG_65516.dat | 0x40 | 0x13 | 168178 | 99.9911% | 15 | 15 | 2 |
| research/dattest2/Dattest2/Program_ID_00001.dat | 0x40 | 0x65 | 168177 | 99.9905% | 16 | 16 | 2 |
| research/dattest2/Dattest2/Program_ID_00100.dat | 0x40 | 0x0a | 168177 | 99.9905% | 16 | 16 | 2 |
| research/dattest2/Dattest2/Program_ID_12345.dat | 0x40 | 0x18 | 168177 | 99.9905% | 16 | 16 | 2 |
| research/dattest2/Dattest2/Program_ID_65519.dat | 0x40 | 0x62 | 168178 | 99.9911% | 15 | 15 | 2 |

## Program_Nochange2.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x74 | 168193 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| none | none |

### Normalized Change Samples

## Program_Nochange3.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x7c | 168193 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| none | none |

### Normalized Change Samples

## Program_TG_00001.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x78 | 168177 |
| 0xb7 | 4 |
| 0xd3 | 2 |
| 0xa7 | 2 |
| 0x87 | 2 |
| 0xc0 | 1 |
| 0xe2 | 1 |
| 0xf4 | 1 |
| 0xf3 | 1 |
| 0xb6 | 1 |
| 0x86 | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x000151a1-0x000151ae | 14 |
| 0x000151b3-0x000151b4 | 2 |

### Normalized Change Samples
- `0x000151a1-0x000151ae` len=14
  - before @`0x00015199`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x00015199`: `cb cb cb cb cb cb cb cb 60 73 14 60 51 47 40 14 04 04 04 04 05 34 cb cb cb cb 35 34 cb cb`
  - before ASCII: `..............................`
  - after ASCII: `........`s.`QG@......4....54..`
- `0x000151b3-0x000151b4` len=2
  - before @`0x000151ab`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x000151ab`: `04 04 05 34 cb cb cb cb 35 34 cb cb cb cb cb cb cb cb`
  - before ASCII: `..................`
  - after ASCII: `...4....54........`

## Program_TG_00100.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x0b | 168177 |
| 0xc4 | 4 |
| 0xa0 | 2 |
| 0xd4 | 2 |
| 0xf4 | 2 |
| 0xb3 | 1 |
| 0x91 | 1 |
| 0x87 | 1 |
| 0x80 | 1 |
| 0xc5 | 1 |
| 0x90 | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x000151a1-0x000151ae | 14 |
| 0x000151b3-0x000151b4 | 2 |

### Normalized Change Samples
- `0x000151a1-0x000151ae` len=14
  - before @`0x00015199`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x00015199`: `cb cb cb cb cb cb cb cb 60 73 14 60 51 47 40 14 04 04 05 04 04 34 cb cb cb cb 50 34 cb cb`
  - before ASCII: `..............................`
  - after ASCII: `........`s.`QG@......4....P4..`
- `0x000151b3-0x000151b4` len=2
  - before @`0x000151ab`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x000151ab`: `05 04 04 34 cb cb cb cb 50 34 cb cb cb cb cb cb cb cb`
  - before ASCII: `..................`
  - after ASCII: `...4....P4........`

## Program_TG_12345.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x18 | 168177 |
| 0xb3 | 2 |
| 0xc7 | 2 |
| 0xa0 | 1 |
| 0x82 | 1 |
| 0x94 | 1 |
| 0x93 | 1 |
| 0xd6 | 1 |
| 0xd5 | 1 |
| 0xd4 | 1 |
| 0xd3 | 1 |
| 0xd2 | 1 |
| 0xe7 | 1 |
| 0xde | 1 |
| 0xd7 | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x000151a1-0x000151ae | 14 |
| 0x000151b3-0x000151b4 | 2 |

### Normalized Change Samples
- `0x000151a1-0x000151ae` len=14
  - before @`0x00015199`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x00015199`: `cb cb cb cb cb cb cb cb 60 73 14 60 51 47 40 14 05 06 07 00 01 34 cb cb cb cb 0d 04 cb cb`
  - before ASCII: `..............................`
  - after ASCII: `........`s.`QG@......4........`
- `0x000151b3-0x000151b4` len=2
  - before @`0x000151ab`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x000151ab`: `07 00 01 34 cb cb cb cb 0d 04 cb cb cb cb cb cb cb cb`
  - before ASCII: `..................`
  - after ASCII: `...4..............`

## Program_TG_65516.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x13 | 168178 |
| 0xb8 | 2 |
| 0xcc | 2 |
| 0xd9 | 2 |
| 0xab | 1 |
| 0x89 | 1 |
| 0x9f | 1 |
| 0x98 | 1 |
| 0xda | 1 |
| 0xdd | 1 |
| 0xd5 | 1 |
| 0xec | 1 |
| 0x03 | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x000151a1-0x000151ae | 14 |
| 0x000151b3-0x000151b3 | 1 |

### Normalized Change Samples
- `0x000151a1-0x000151ae` len=14
  - before @`0x00015199`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x00015199`: `cb cb cb cb cb cb cb cb 60 73 14 60 51 47 40 14 02 01 01 05 0d 34 cb cb cb cb db cb cb cb`
  - before ASCII: `..............................`
  - after ASCII: `........`s.`QG@......4........`
- `0x000151b3-0x000151b3` len=1
  - before @`0x000151ab`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x000151ab`: `01 05 0d 34 cb cb cb cb db cb cb cb cb cb cb cb cb`
  - before ASCII: `.................`
  - after ASCII: `...4.............`

## Program_ID_00001.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x65 | 168177 |
| 0xaa | 4 |
| 0xc5 | 2 |
| 0x9a | 2 |
| 0xd3 | 1 |
| 0xde | 1 |
| 0xce | 1 |
| 0xff | 1 |
| 0xe9 | 1 |
| 0xee | 1 |
| 0xab | 1 |
| 0x9b | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x00010641-0x0001064e | 14 |
| 0x00010653-0x00010654 | 2 |

### Normalized Change Samples
- `0x00010641-0x0001064e` len=14
  - before @`0x00010639`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x00010639`: `cb cb cb cb cb cb cb cb 7d 70 6b 60 51 47 40 6b 04 04 04 04 05 34 cb cb cb cb 35 34 cb cb`
  - before ASCII: `..............................`
  - after ASCII: `........}pk`QG@k.....4....54..`
- `0x00010653-0x00010654` len=2
  - before @`0x0001064b`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x0001064b`: `04 04 05 34 cb cb cb cb 35 34 cb cb cb cb cb cb cb cb`
  - before ASCII: `..................`
  - after ASCII: `...4....54........`

## Program_ID_00100.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x0a | 168177 |
| 0xc5 | 4 |
| 0xaa | 2 |
| 0xf5 | 2 |
| 0xbc | 1 |
| 0xb1 | 1 |
| 0xa1 | 1 |
| 0x90 | 1 |
| 0x86 | 1 |
| 0x81 | 1 |
| 0xc4 | 1 |
| 0x91 | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x00010641-0x0001064e | 14 |
| 0x00010653-0x00010654 | 2 |

### Normalized Change Samples
- `0x00010641-0x0001064e` len=14
  - before @`0x00010639`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x00010639`: `cb cb cb cb cb cb cb cb 7d 70 6b 60 51 47 40 6b 04 04 05 04 04 34 cb cb cb cb 50 34 cb cb`
  - before ASCII: `..............................`
  - after ASCII: `........}pk`QG@k.....4....P4..`
- `0x00010653-0x00010654` len=2
  - before @`0x0001064b`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x0001064b`: `05 04 04 34 cb cb cb cb 50 34 cb cb cb cb cb cb cb cb`
  - before ASCII: `..................`
  - after ASCII: `...4....P4........`

## Program_ID_12345.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x18 | 168177 |
| 0xb8 | 2 |
| 0xae | 1 |
| 0xa3 | 1 |
| 0xb3 | 1 |
| 0x82 | 1 |
| 0x94 | 1 |
| 0x93 | 1 |
| 0xd6 | 1 |
| 0xd5 | 1 |
| 0xd4 | 1 |
| 0xd3 | 1 |
| 0xd2 | 1 |
| 0xe7 | 1 |
| 0xde | 1 |
| 0xd7 | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x00010641-0x0001064e | 14 |
| 0x00010653-0x00010654 | 2 |

### Normalized Change Samples
- `0x00010641-0x0001064e` len=14
  - before @`0x00010639`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x00010639`: `cb cb cb cb cb cb cb cb 7d 70 6b 60 51 47 40 6b 05 06 07 00 01 34 cb cb cb cb 0d 04 cb cb`
  - before ASCII: `..............................`
  - after ASCII: `........}pk`QG@k.....4........`
- `0x00010653-0x00010654` len=2
  - before @`0x0001064b`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x0001064b`: `07 00 01 34 cb cb cb cb 0d 04 cb cb cb cb cb cb cb cb`
  - before ASCII: `..................`
  - after ASCII: `...4..............`

## Program_ID_65519.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x62 | 168178 |
| 0xc2 | 2 |
| 0xa8 | 2 |
| 0xd4 | 1 |
| 0xd9 | 1 |
| 0xc9 | 1 |
| 0xf8 | 1 |
| 0xee | 1 |
| 0xe9 | 1 |
| 0xab | 1 |
| 0xac | 1 |
| 0xa4 | 1 |
| 0x9d | 1 |
| 0x72 | 1 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x00010641-0x0001064e | 14 |
| 0x00010653-0x00010653 | 1 |

### Normalized Change Samples
- `0x00010641-0x0001064e` len=14
  - before @`0x00010639`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x00010639`: `cb cb cb cb cb cb cb cb 7d 70 6b 60 51 47 40 6b 02 01 01 05 0d 34 cb cb cb cb db cb cb cb`
  - before ASCII: `..............................`
  - after ASCII: `........}pk`QG@k.....4........`
- `0x00010653-0x00010653` len=1
  - before @`0x0001064b`: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - after  @`0x0001064b`: `01 05 0d 34 cb cb cb cb db cb cb cb cb cb cb cb cb`
  - before ASCII: `.................`
  - after ASCII: `...4.............`

