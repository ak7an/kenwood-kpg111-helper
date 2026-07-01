# Candidate Record Probe: Program_Delete.dat

- Dominant payload XOR to normalize modified file: `0x1e`
- Record size shown: 32 bytes

- baseline `0x00015120`
  - hex: `a4 1f 32 28 38 34 35 35 3e 38 2f 7b 0f 1c 5b a4 a4 a4 a4 54 7c a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - raw printable: `..2(8455>8/{..[....T|...........`
  - bytes `+1..+14` XOR `0x5b`: `Disconnect TG`
  - bytes `+19..+20`: `54 7c`
- normalized modified `0x00015120`
  - hex: `a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - raw printable: `................................`
  - bytes `+1..+14` XOR `0x5b`: `��������������`
  - bytes `+19..+20`: `a4 a4`

- baseline `0x00015180`
  - hex: `a4 1a 10 6c 1a 15 7b 0f 1c 5b 5b 5b 5b 5b 5b a4 a4 a4 a4 46 08 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - raw printable: `...l..{..[[[[[[....F............`
  - bytes `+1..+14` XOR `0x5b`: `AK7AN TG`
  - bytes `+19..+20`: `46 08`
- normalized modified `0x00015180`
  - hex: `a4 19 32 2f 19 22 19 32 2f 13 3a 36 28 5b 5b a4 a4 a4 a4 46 08 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - raw printable: `..2/.".2/.:6([[....F............`
  - bytes `+1..+14` XOR `0x5b`: `BitByBitHams`
  - bytes `+19..+20`: `46 08`

