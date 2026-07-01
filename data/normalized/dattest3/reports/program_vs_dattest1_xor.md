# KPG111 Dominant XOR Rewrite Analysis

This report derives byte-level evidence only. Normalized changes are not decoded field meanings.

## Baseline

- Path: `research/dattest/Dattest/AK7AN_Travel.dat`
- Size: 168257 bytes
- SHA-256: `aa20a84b5cb76e5fd58a691eb26fdc4140e7d75fb3bd6b28fc156f3ec4144cce`

## Pair Summary
| Modified | Common Prefix | Dominant XOR | Dominant Count | Dominant Ratio | XOR Exceptions | Normalized Changed Bytes | Normalized Regions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| research/dattest3/Dattest3/Program.dat | 0x40 | 0x44 | 167730 | 99.7247% | 463 | 463 | 58 |

## Program.dat

### Top XOR Deltas
| XOR | Count |
| --- | --- |
| 0x44 | 167730 |
| 0x9b | 67 |
| 0x8b | 54 |
| 0xf2 | 40 |
| 0xbb | 39 |
| 0xff | 27 |
| 0xee | 25 |
| 0x89 | 21 |
| 0xef | 14 |
| 0xf5 | 13 |
| 0xfc | 12 |
| 0xe9 | 12 |
| 0xf4 | 12 |
| 0xeb | 12 |
| 0x8a | 7 |
| 0x8e | 6 |
| 0x82 | 5 |
| 0xde | 4 |
| 0x83 | 4 |
| 0x8c | 4 |

### Normalized Changed Regions
| Range | Length |
| --- | --- |
| 0x00010641-0x0001064e | 14 |
| 0x00010653-0x00010653 | 1 |
| 0x00010661-0x0001066e | 14 |
| 0x00010673-0x00010674 | 2 |
| 0x00010681-0x0001068e | 14 |
| 0x00010693-0x00010694 | 2 |
| 0x000106a1-0x000106ae | 14 |
| 0x000106b3-0x000106b4 | 2 |
| 0x000106c1-0x000106ce | 14 |
| 0x000106d3-0x000106d4 | 2 |
| 0x000106e1-0x000106ee | 14 |
| 0x000106f3-0x000106f4 | 2 |
| 0x00010701-0x0001070e | 14 |
| 0x00010713-0x00010714 | 2 |
| 0x00010721-0x0001072e | 14 |
| 0x00010733-0x00010734 | 2 |
| 0x00010741-0x0001074e | 14 |
| 0x00010753-0x00010754 | 2 |
| 0x00010761-0x0001076e | 14 |
| 0x00010773-0x00010774 | 2 |

### Normalized Change Samples
- `0x00010641-0x0001064e` len=14
  - before @`0x00010639`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x00010639`: `a4 a4 a4 a4 a4 a4 a4 a4 12 1f 04 0f 3e 28 2f 04 6d 6e 6e 6a 62 5b a4 a4 a4 a4 b4 a4 a4 a4`
  - before ASCII: `..............................`
  - after ASCII: `............>(/.mnnjb[........`
- `0x00010653-0x00010653` len=1
  - before @`0x0001064b`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x0001064b`: `6e 6a 62 5b a4 a4 a4 a4 b4 a4 a4 a4 a4 a4 a4 a4 a4`
  - before ASCII: `.................`
  - after ASCII: `njb[.............`
- `0x00010661-0x0001066e` len=14
  - before @`0x00010659`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x00010659`: `a4 a4 a4 a4 a4 a4 a4 a4 16 22 7b 19 3e 28 2f 7b 1d 29 32 3e 35 3f a4 a4 a4 a4 35 e9 a4 a4`
  - before ASCII: `..............................`
  - after ASCII: `........."{.>(/{.)2>5?....5...`
- `0x00010673-0x00010674` len=2
  - before @`0x0001066b`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x0001066b`: `32 3e 35 3f a4 a4 a4 a4 35 e9 a4 a4 a4 a4 a4 a4 a4 a4`
  - before ASCII: `..................`
  - after ASCII: `2>5?....5.........`
- `0x00010681-0x0001068e` len=14
  - before @`0x00010679`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x00010679`: `a4 a4 a4 a4 a4 a4 a4 a4 1f 34 35 7c 2f 7b 37 32 30 3e 5b 5b 5b 5b a4 a4 a4 a4 3d 07 a4 a4`
  - before ASCII: `..............................`
  - after ASCII: `.........45|/{720>[[[[....=...`
- `0x00010693-0x00010694` len=2
  - before @`0x0001068b`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x0001068b`: `5b 5b 5b 5b a4 a4 a4 a4 3d 07 a4 a4 a4 a4 a4 a4 a4 a4`
  - before ASCII: `..................`
  - after ASCII: `[[[[....=.........`
- `0x000106a1-0x000106ae` len=14
  - before @`0x00010699`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x00010699`: `a4 a4 a4 a4 a4 a4 a4 a4 7b 0e 15 12 0f 7b 12 1f 7b 6b 6b 6a 63 5b a4 a4 a4 a4 ae 6c a4 a4`
  - before ASCII: `..............................`
  - after ASCII: `........{....{..{kkjc[.....l..`
- `0x000106b3-0x000106b4` len=2
  - before @`0x000106ab`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x000106ab`: `6b 6a 63 5b a4 a4 a4 a4 ae 6c a4 a4 a4 a4 a4 a4 a4 a4`
  - before ASCII: `..................`
  - after ASCII: `kjc[.....l........`
- `0x000106c1-0x000106ce` len=14
  - before @`0x000106b9`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x000106b9`: `a4 a4 a4 a4 a4 a4 a4 a4 7b 0e 15 12 0f 7b 12 1f 7b 6b 6b 6a 62 5b a4 a4 a4 a4 e6 ac a4 a4`
  - before ASCII: `..............................`
  - after ASCII: `........{....{..{kkjb[........`
- `0x000106d3-0x000106d4` len=2
  - before @`0x000106cb`: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - after  @`0x000106cb`: `6b 6a 62 5b a4 a4 a4 a4 e6 ac a4 a4 a4 a4 a4 a4 a4 a4`
  - before ASCII: `..................`
  - after ASCII: `kjb[..............`

