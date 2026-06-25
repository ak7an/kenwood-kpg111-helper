# Candidate Record Probe: Program_TG_65516.dat

- Dominant payload XOR to normalize modified file: `0x13`
- Record size shown: 32 bytes

- baseline `0x000151a0`
  - hex: `cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x34`: `��������������`
  - bytes `+19..+20`: `cb cb`
  - bytes `+19..+20` XOR `0x34`: `ff ff` LE=65535 BE=65535
- normalized modified `0x000151a0`
  - hex: `cb 60 73 14 60 51 47 40 14 02 01 01 05 0d 34 cb cb cb cb db cb cb cb cb cb cb cb cb cb cb cb cb`
  - raw printable: `.`s.`QG@......4.................`
  - bytes `+1..+14` XOR `0x34`: `TG Test 65519`
  - bytes `+19..+20`: `db cb`
  - bytes `+19..+20` XOR `0x34`: `ef ff` LE=65519 BE=61439

