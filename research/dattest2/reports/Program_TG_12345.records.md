# Candidate Record Probe: Program_TG_12345.dat

- Dominant payload XOR to normalize modified file: `0x18`
- Record size shown: 32 bytes

- baseline `0x000151a0`
  - hex: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x34`: `��������������`
  - bytes `+19..+20`: `cb cb`
  - bytes `+19..+20` XOR `0x34`: `ff ff` LE=65535 BE=65535
- normalized modified `0x000151a0`
  - hex: `cb 60 73 14 60 51 47 40 14 05 06 07 00 01 34 cb cb cb cb 0d 04 cb cb cb cb cb cb cb cb cb cb cb`
  - raw printable: `.`s.`QG@......4.................`
  - bytes `+1..+14` XOR `0x34`: `TG Test 12345`
  - bytes `+19..+20`: `0d 04`
  - bytes `+19..+20` XOR `0x34`: `39 30` LE=12345 BE=14640

