# Candidate Record Probe: Program_ID_12345.dat

- Dominant payload XOR to normalize modified file: `0x18`
- Record size shown: 32 bytes

- baseline `0x00010640`
  - hex: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x34`: `��������������`
  - bytes `+19..+20`: `cb cb`
  - bytes `+19..+20` XOR `0x34`: `ff ff` LE=65535 BE=65535
- normalized modified `0x00010640`
  - hex: `cb 7d 70 6b 60 51 47 40 6b 05 06 07 00 01 34 cb cb cb cb 0d 04 cb cb cb cb cb cb cb cb cb cb cb`
  - raw printable: `.}pk`QG@k.....4.................`
  - bytes `+1..+14` XOR `0x34`: `ID_Test_12345`
  - bytes `+19..+20`: `0d 04`
  - bytes `+19..+20` XOR `0x34`: `39 30` LE=12345 BE=14640

