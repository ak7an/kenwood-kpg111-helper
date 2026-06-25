# Candidate Record Probe: Program_TG_00100.dat

- Dominant payload XOR to normalize modified file: `0x0b`
- Record size shown: 32 bytes

- baseline `0x000151a0`
  - hex: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x34`: `��������������`
  - bytes `+19..+20`: `cb cb`
  - bytes `+19..+20` XOR `0x34`: `ff ff` LE=65535 BE=65535
- normalized modified `0x000151a0`
  - hex: `cb 60 73 14 60 51 47 40 14 04 04 05 04 04 34 cb cb cb cb 50 34 cb cb cb cb cb cb cb cb cb cb cb`
  - raw printable: `.`s.`QG@......4....P4...........`
  - bytes `+1..+14` XOR `0x34`: `TG Test 00100`
  - bytes `+19..+20`: `50 34`
  - bytes `+19..+20` XOR `0x34`: `64 00` LE=100 BE=25600

