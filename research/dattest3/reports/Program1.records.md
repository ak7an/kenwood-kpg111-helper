# Candidate Record Probe: Program1.dat

- Dominant payload XOR to normalize modified file: `0x2f`
- Record size shown: 32 bytes

- baseline `0x00010640`
  - hex: `e0 56 5b 40 4b 7a 6c 6b 40 29 2a 2a 2e 26 1f e0 e0 e0 e0 f0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `.V[@Kzlk@)**.&..................`
  - bytes `+1..+14` XOR `0x1f`: `ID_Test_65519`
  - bytes `+19..+20`: `f0 e0`
  - bytes `+19..+20` XOR `0x1f`: `ef ff` LE=65519 BE=61439
- normalized modified `0x00010640`
  - hex: `e0 53 70 71 78 3f 58 70 71 7a 1f 1f 1f 1f 1f e0 e0 e0 e0 f0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `.Spqx?Xpqz......................`
  - bytes `+1..+14` XOR `0x1f`: `Long Gone`
  - bytes `+19..+20`: `f0 e0`
  - bytes `+19..+20` XOR `0x1f`: `ef ff` LE=65519 BE=61439

- baseline `0x00015140`
  - hex: `e0 4a 6b 7e 77 3f 5b 4d 51 3f 2f 2f 1f 1f 1f e0 e0 e0 e0 1d 64 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `.Jk~w?[MQ?//........d...........`
  - bytes `+1..+14` XOR `0x1f`: `Utah DRN 00`
  - bytes `+19..+20`: `1d 64`
  - bytes `+19..+20` XOR `0x1f`: `02 7b` LE=31490 BE=635
- normalized modified `0x00015140`
  - hex: `e0 57 70 6b 3f 71 3f 4c 7a 67 66 1f 1f 1f 1f e0 e0 e0 e0 1d 64 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `.Wpk?q?Lzgf.........d...........`
  - bytes `+1..+14` XOR `0x1f`: `Hot n Sexy`
  - bytes `+19..+20`: `1d 64`
  - bytes `+19..+20` XOR `0x1f`: `02 7b` LE=31490 BE=635

