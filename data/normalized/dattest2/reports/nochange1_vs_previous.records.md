# Candidate Record Probe: Program_Nochange1.dat

- Dominant payload XOR to normalize modified file: `0x6f`
- Record size shown: 32 bytes

- baseline `0x00015180`
  - hex: `a4 1a 10 6c 1a 15 7b 0f 1c 5b 5b 5b 5b 5b 5b a4 a4 a4 a4 46 08 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - raw printable: `...l..{..[[[[[[....F............`
  - bytes `+1..+14` XOR `0x5b`: `AK7AN TG`
  - bytes `+19..+20`: `46 08`
  - bytes `+19..+20` XOR `0x5b`: `1d 53` LE=21277 BE=7507
- normalized modified `0x00015180`
  - hex: `a4 1a 10 6c 1a 15 7b 0f 1c 5b 5b 5b 5b 5b 5b a4 a4 a4 a4 46 08 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - raw printable: `...l..{..[[[[[[....F............`
  - bytes `+1..+14` XOR `0x5b`: `AK7AN TG`
  - bytes `+19..+20`: `46 08`
  - bytes `+19..+20` XOR `0x5b`: `1d 53` LE=21277 BE=7507

- baseline `0x00010620`
  - hex: `a4 15 03 6f 1f 03 7b 19 32 2f 39 22 19 32 2f a4 a4 a4 a4 ea 73 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - raw printable: `...o..{.2/9".2/.....s...........`
  - bytes `+1..+14` XOR `0x5b`: `NX4DX BitbyBit`
  - bytes `+19..+20`: `ea 73`
  - bytes `+19..+20` XOR `0x5b`: `b1 28` LE=10417 BE=45352
- normalized modified `0x00010620`
  - hex: `a4 15 03 6f 1f 03 7b 19 32 2f 39 22 19 32 2f a4 a4 a4 a4 ea 73 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4 a4`
  - raw printable: `...o..{.2/9".2/.....s...........`
  - bytes `+1..+14` XOR `0x5b`: `NX4DX BitbyBit`
  - bytes `+19..+20`: `ea 73`
  - bytes `+19..+20` XOR `0x5b`: `b1 28` LE=10417 BE=45352

