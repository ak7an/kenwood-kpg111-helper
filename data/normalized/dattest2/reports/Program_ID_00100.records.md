# Candidate Record Probe: Program_ID_00100.dat

- Dominant payload XOR to normalize modified file: `0x0a`
- Record size shown: 32 bytes

- baseline `0x00010640`
  - hex: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x34`: `��������������`
  - bytes `+19..+20`: `cb cb`
  - bytes `+19..+20` XOR `0x34`: `ff ff` LE=65535 BE=65535
- normalized modified `0x00010640`
  - hex: `cb 7d 70 6b 60 51 47 40 6b 04 04 05 04 04 34 cb cb cb cb 50 34 cb cb cb cb cb cb cb cb cb cb cb`
  - raw printable: `.}pk`QG@k.....4....P4...........`
  - bytes `+1..+14` XOR `0x34`: `ID_Test_00100`
  - bytes `+19..+20`: `50 34`
  - bytes `+19..+20` XOR `0x34`: `64 00` LE=100 BE=25600

