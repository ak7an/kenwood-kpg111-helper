# Candidate Record Probe: Program3.dat

- Dominant payload XOR to normalize modified file: `0x01`
- Record size shown: 32 bytes

- baseline `0x000105a0`
  - hex: `e0 55 7e 72 76 7a 33 3f 54 4e 2e 4a 4c 5e 1f e0 e0 e0 e0 95 09 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `.U~rvz3?TN.JL^..................`
  - bytes `+1..+14` XOR `0x1f`: `Jamie, KQ1USA`
  - bytes `+19..+20`: `95 09`
  - bytes `+19..+20` XOR `0x1f`: `8a 16` LE=5770 BE=35350
- normalized modified `0x000105a0`
  - hex: `e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x1f`: `��������������`
  - bytes `+19..+20`: `e0 e0`
  - bytes `+19..+20` XOR `0x1f`: `ff ff` LE=65535 BE=65535

- baseline `0x00010640`
  - hex: `e0 56 5b 40 4b 7a 6c 6b 40 29 2a 2a 2e 26 1f e0 e0 e0 e0 f0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `.V[@Kzlk@)**.&..................`
  - bytes `+1..+14` XOR `0x1f`: `ID_Test_65519`
  - bytes `+19..+20`: `f0 e0`
  - bytes `+19..+20` XOR `0x1f`: `ef ff` LE=65519 BE=61439
- normalized modified `0x00010640`
  - hex: `e0 53 70 71 78 3f 58 70 71 7a 1f 1f 1f 1f 1f e0 e0 e0 e0 f1 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `.Spqx?Xpqz......................`
  - bytes `+1..+14` XOR `0x1f`: `Long Gone`
  - bytes `+19..+20`: `f1 e0`
  - bytes `+19..+20` XOR `0x1f`: `ee ff` LE=65518 BE=61183

- baseline `0x000150a0`
  - hex: `e0 4c 7c 70 6b 73 7e 71 7b 3f 4b 58 1f 1f 1f e0 e0 e0 e0 e0 44 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `.L|pks~q{?KX........D...........`
  - bytes `+1..+14` XOR `0x1f`: `Scotland TG`
  - bytes `+19..+20`: `e0 44`
  - bytes `+19..+20` XOR `0x1f`: `ff 5b` LE=23551 BE=65371
- normalized modified `0x000150a0`
  - hex: `e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x1f`: `��������������`
  - bytes `+19..+20`: `e0 e0`
  - bytes `+19..+20` XOR `0x1f`: `ff ff` LE=65535 BE=65535

- baseline `0x00015140`
  - hex: `e0 4a 6b 7e 77 3f 5b 4d 51 3f 2f 2f 1f 1f 1f e0 e0 e0 e0 1d 64 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `.Jk~w?[MQ?//........d...........`
  - bytes `+1..+14` XOR `0x1f`: `Utah DRN 00`
  - bytes `+19..+20`: `1d 64`
  - bytes `+19..+20` XOR `0x1f`: `02 7b` LE=31490 BE=635
- normalized modified `0x00015140`
  - hex: `e0 57 70 6b 3f 71 3f 4c 7a 67 66 1f 1f 1f 1f e0 e0 e0 e0 1c 64 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0 e0`
  - raw printable: `.Wpk?q?Lzgf.........d...........`
  - bytes `+1..+14` XOR `0x1f`: `Hot n Sexy`
  - bytes `+19..+20`: `1c 64`
  - bytes `+19..+20` XOR `0x1f`: `03 7b` LE=31491 BE=891

