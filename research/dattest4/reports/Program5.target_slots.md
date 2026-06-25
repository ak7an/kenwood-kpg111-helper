# Candidate Record Probe: Program5.dat

- Dominant payload XOR to normalize modified file: `0x46`
- Record size shown: 32 bytes

- baseline `0x000105a0`
  - hex: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x1e`: `��������������`
  - bytes `+19..+20`: `e1 e1`
  - bytes `+19..+20` XOR `0x1e`: `ff ff` LE=65535 BE=65535
- normalized modified `0x000105a0`
  - hex: `e1 56 7b 72 72 71 1e 1e 1e 1e 1e 1e 1e 1e 1e e1 e1 e1 e1 78 42 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - raw printable: `.V{rrq.............xB...........`
  - bytes `+1..+14` XOR `0x1e`: `Hello`
  - bytes `+19..+20`: `78 42`
  - bytes `+19..+20` XOR `0x1e`: `66 5c` LE=23654 BE=26204

- baseline `0x000150a0`
  - hex: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x1e`: `��������������`
  - bytes `+19..+20`: `e1 e1`
  - bytes `+19..+20` XOR `0x1e`: `ff ff` LE=65535 BE=65535
- normalized modified `0x000150a0`
  - hex: `e1 59 71 71 7a 7c 67 7b 1e 1e 1e 1e 1e 1e 1e e1 e1 e1 e1 2e 5e e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - raw printable: `.Yqqz|g{............^...........`
  - bytes `+1..+14` XOR `0x1e`: `Goodbye`
  - bytes `+19..+20`: `2e 5e`
  - bytes `+19..+20` XOR `0x1e`: `30 40` LE=16432 BE=12352

- baseline `0x00010840`
  - hex: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x1e`: `��������������`
  - bytes `+19..+20`: `e1 e1`
  - bytes `+19..+20` XOR `0x1e`: `ff ff` LE=65535 BE=65535
- normalized modified `0x00010840`
  - hex: `e1 3e 4b 50 57 4a 3e 57 5a 3e 2e 2e 2d 2f 1e e1 e1 e1 e1 1f b4 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - raw printable: `.>KPWJ>WZ>..-/..................`
  - bytes `+1..+14` XOR `0x1e`: ` UNIT ID 0031`
  - bytes `+19..+20`: `1f b4`
  - bytes `+19..+20` XOR `0x1e`: `01 aa` LE=43521 BE=426

- baseline `0x00015340`
  - hex: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x1e`: `��������������`
  - bytes `+19..+20`: `e1 e1`
  - bytes `+19..+20` XOR `0x1e`: `ff ff` LE=65535 BE=65535
- normalized modified `0x00015340`
  - hex: `e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x1e`: `��������������`
  - bytes `+19..+20`: `e1 e1`
  - bytes `+19..+20` XOR `0x1e`: `ff ff` LE=65535 BE=65535

