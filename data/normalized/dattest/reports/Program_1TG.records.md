# Candidate Record Probe: Program_1TG.dat

- Dominant payload XOR to normalize modified file: `0x3e`
- Record size shown: 32 bytes

- baseline `0x000151a0`
  - hex: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x5b`: `��������������`
  - bytes `+19..+20`: `a4 a4`
- normalized modified `0x000151a0`
  - hex: `a4 1c 0b 0f 0f 3e 28 2f 6a 5b 5b 5b 5b 5b 5b a4 a4 a4 a4 b2 a6 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - raw printable: `.....>(/j[[[[[[.................`
  - bytes `+1..+14` XOR `0x5b`: `GPTTest1`
  - bytes `+19..+20`: `b2 a6`

