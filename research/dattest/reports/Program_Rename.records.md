# Candidate Record Probe: Program_Rename.dat

- Dominant payload XOR to normalize modified file: `0x67`
- Record size shown: 32 bytes

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

