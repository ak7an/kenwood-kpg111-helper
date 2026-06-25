# KPG111 Candidate Table Map

This is a read-only structural scan. Printable decoded names are evidence for candidate records, not proof of table purpose.

## File

- Path: `research/dattest4/Dattest4/Program6.dat`
- Size: 168257 bytes
- SHA-256: `dcc2f23c2923b75a8870bc692372c3d4016379f7efe690c5a689c659ef33f451`
- Payload start: `0x40`
- Record size: 32
- Decode XOR: `0x54`
- Records scanned: 5256
- Occupied candidates: 216
- Empty records: 3899

## Candidate Runs
| Range | Records | Empty Slots After | Next Record |
| --- | --- | --- | --- |
| 0x00000b40-0x00000b7f | 2 | 0 | 0x00000b80 empty=False name='' |
| 0x00000ba0-0x00000c3f | 5 | 0 | 0x00000c40 empty=False name='\x02CALL' |
| 0x00001540-0x0000177f | 18 | 0 | 0x00001780 empty=False name='�   SEARCH   �' |
| 0x000017a0-0x00001c3f | 37 | 0 | 0x00001c40 empty=False name='�RECEIVE DATA�' |
| 0x00001d20-0x00001f1f | 16 | 0 | 0x00001f20 empty=False name='� REMOTE TX  �' |
| 0x00001f40-0x0000215f | 17 | 8 | 0x00002160 empty=True name='��������������' |
| 0x000024c0-0x0000257f | 6 | 0 | 0x00002580 empty=False name='��������������' |
| 0x00002680-0x000026bf | 2 | 0 | 0x000026c0 empty=False name='��������������' |
| 0x000026e0-0x0000275f | 4 | 15 | 0x00002760 empty=True name='��������������' |
| 0x00002940-0x00002a9f | 11 | 21 | 0x00002aa0 empty=True name='��������������' |
| 0x00002d80-0x00002dbf | 2 | 0 | 0x00002dc0 empty=False name='      ��������' |
| 0x00002e60-0x00002ebf | 3 | 0 | 0x00002ec0 empty=False name='CH_ENT��������' |
| 0x00002f20-0x00002f7f | 3 | 0 | 0x00002f80 empty=False name='FX_VOL��������' |
| 0x00002fa0-0x00002fff | 3 | 0 | 0x00003000 empty=False name='IND+ST��������' |
| 0x00003020-0x000030df | 6 | 0 | 0x000030e0 empty=False name='SEL+ST��������' |
| 0x00003140-0x0000317f | 2 | 0 | 0x00003180 empty=False name='PASSWD��������' |
| 0x000031e0-0x0000321f | 2 | 0 | 0x00003220 empty=False name='GRP+SD��������' |
| 0x00003280-0x000032bf | 2 | 0 | 0x000032c0 empty=False name='RX_ENT��������' |
| 0x000037a0-0x000037df | 2 | 0 | 0x000037e0 empty=False name='�p00000000000p' |
| 0x00010480-0x0001085f | 31 | 569 | 0x00010860 empty=True name='��������������' |
| 0x00014f80-0x0001535f | 31 | 320 | 0x00015360 empty=True name='��������������' |

## Run 1: `0x00000b40-0x00000b7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000b40 | ABCDEFGHIJKLMN | 07 00 | 53 54 | 21587 | no |
| 0x00000b60 | 56789 | 54 54 | 00 00 | 0 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000b80 |  | 54 54 | 0 | no | no |
| 0x00000ba0 | 1 | 17 66 | 12867 | no | yes |
| 0x00000bc0 | DEF3 | 1d 60 | 13385 | no | yes |
| 0x00000be0 | JKL5 | 1b 62 | 13903 | no | yes |
| 0x00000c00 | PQRS7 | 02 6c | 14422 | no | yes |
| 0x00000c20 | WXYZ9 | ab ab | 65535 | no | yes |
| 0x00000c40 | CALL | 17 15 | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 00 1d | 18772 | no | no |

## Run 2: `0x00000ba0-0x00000c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000ba0 | 1 | 17 66 | 43 32 | 12867 | no |
| 0x00000bc0 | DEF3 | 1d 60 | 49 34 | 13385 | no |
| 0x00000be0 | JKL5 | 1b 62 | 4f 36 | 13903 | no |
| 0x00000c00 | PQRS7 | 02 6c | 56 38 | 14422 | no |
| 0x00000c20 | WXYZ9 | ab ab | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000c40 | CALL | 17 15 | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 00 1d | 18772 | no | no |
| 0x00000c80 | Microphone | 21 30 | 25717 | no | no |
| 0x00000ca0 |  | 00 74 | 8276 | no | no |
| 0x00000cc0 | 0+CDNM4����� | ab ab | 65535 | no | no |
| 0x00000ce0 | �������������� | ab ab | 65535 | yes | no |
| 0x00000d00 | �������������� | ab ab | 65535 | yes | no |
| 0x00000d20 | �������������� | ab ab | 65535 | yes | no |

## Run 3: `0x00001540-0x0000177f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001540 | 2-TONE | 00 1b | 54 4f | 20308 | no |
| 0x00001560 | AUTO TELEPHONE | 74 15 | 20 41 | 16672 | no |
| 0x00001580 | AUTO DIAL | 00 1b | 54 4f | 20308 | no |
| 0x000015a0 |     BLANK | 74 74 | 20 20 | 8224 | no |
| 0x000015c0 |     CODE? | 74 74 | 20 20 | 8224 | no |
| 0x000015e0 |  OVER WRITE? | 74 10 | 20 44 | 17440 | no |
| 0x00001600 | AUX | 0c 74 | 58 20 | 8280 | no |
| 0x00001620 | AUX B | 1b 15 | 4f 41 | 16719 | no |
| 0x00001640 | CHANNEL ENTRY | 74 1a | 20 4e | 20000 | no |
| 0x00001660 | PRIORITY 3 | 1b 17 | 4f 43 | 17231 | no |
| 0x00001680 | CLOCK ADJUST | 15 06 | 41 52 | 21057 | no |
| 0x000016a0 | MONTH | 0d 54 | 59 00 | 89 | no |
| 0x000016c0 | HOUR | 1a 01 | 4e 55 | 21838 | no |
| 0x000016e0 | DIRECT CH1 SEL | 06 11 | 52 45 | 17746 | no |
| 0x00001700 | DIRECT CH3 SEL | 06 11 | 52 45 | 17746 | no |
| 0x00001720 | DIRECT CH5 SEL | 07 04 | 53 50 | 20563 | no |
| 0x00001740 | FIXED VOLUME | 06 17 | 52 43 | 17234 | no |
| 0x00001760 | SITE No. | 00 11 | 54 45 | 17748 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001780 | �   SEARCH   � | 07 74 | 8275 | no | no |
| 0x000017a0 | N | 54 54 | 0 | no | yes |
| 0x000017c0 | E | 54 54 | 0 | no | yes |
| 0x000017e0 | ALT | 74 74 | 8224 | no | yes |
| 0x00001800 |             ft | 1b 01 | 21839 | no | yes |
| 0x00001820 | GROUP+STATUS | 19 11 | 17741 | no | yes |
| 0x00001840 | HORN ALERT | 10 1d | 18756 | no | yes |
| 0x00001860 | INDIV+STATUS | 74 74 | 8224 | no | yes |

## Run 4: `0x000017a0-0x00001c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000017a0 | N | 54 54 | 00 00 | 0 | no |
| 0x000017c0 | E | 54 54 | 00 00 | 0 | no |
| 0x000017e0 | ALT | 74 74 | 20 20 | 8224 | no |
| 0x00001800 |             ft | 1b 01 | 4f 55 | 21839 | no |
| 0x00001820 | GROUP+STATUS | 19 11 | 4d 45 | 17741 | no |
| 0x00001840 | HORN ALERT | 10 1d | 44 49 | 18756 | no |
| 0x00001860 | INDIV+STATUS | 74 74 | 20 20 | 8224 | no |
| 0x00001880 | LCD BRIGHTNESS | 03 74 | 57 20 | 8279 | no |
| 0x000018a0 | MENU | 1a 1d | 4e 49 | 18766 | no |
| 0x000018c0 | OST | 00 74 | 54 20 | 8276 | no |
| 0x000018e0 |    TONE OFF | 15 0d | 41 59 | 22849 | no |
| 0x00001900 | PRI CH SEL | 74 74 | 20 20 | 8224 | no |
| 0x00001920 |     PRIORITY 1 | 74 74 | 20 20 | 8224 | no |
| 0x00001940 |   PRIORITY 1&2 | 16 18 | 42 4c | 19522 | no |
| 0x00001960 | SCAN | 15 1a | 41 4e | 20033 | no |
| 0x00001980 |         DELETE | 74 74 | 20 20 | 8224 | no |
| 0x000019a0 |      SCAN | 15 1a | 41 4e | 20033 | no |
| 0x000019c0 | SCRAM/ENCRYP | 06 15 | 52 41 | 16722 | no |
| 0x000019e0 | CODE | 18 17 | 4c 43 | 17228 | no |
| 0x00001a00 | SELCALL+STATUS | 1a 10 | 4e 44 | 17486 | no |
| 0x00001a20 | SITE LOCK | 00 11 | 54 45 | 17748 | no |
| 0x00001a40 | SQUELCH LEVEL | 02 11 | 56 45 | 17750 | no |
| 0x00001a60 | SQUELCH OFF | 15 17 | 41 43 | 17217 | no |
| 0x00001a80 | STATUS | 18 1f | 4c 4b | 19276 | no |
| 0x00001aa0 | PASSWORD | 74 04 | 20 50 | 20512 | no |
| 0x00001ac0 | VIBRATOR | 1d 17 | 49 43 | 17225 | no |
| 0x00001ae0 | VOX | 0c 74 | 58 20 | 8280 | no |
| 0x00001b00 | ZONE DEL/ADD | 74 74 | 20 20 | 8224 | no |
| 0x00001b20 |            OFF | 74 74 | 20 20 | 8224 | no |
| 0x00001b40 |            LOW | 07 00 | 53 54 | 21587 | no |
| 0x00001b60 |      BUSY | 74 74 | 20 20 | 8224 | no |
| 0x00001b80 |      STUN | 18 18 | 4c 4c | 19532 | no |
| 0x00001ba0 | NEW MESSAGE | 11 19 | 45 4d | 19781 | no |
| 0x00001bc0 |    MAN DOWN | 1c 1b | 48 4f | 20296 | no |
| 0x00001be0 | ID | 15 00 | 41 54 | 21569 | no |
| 0x00001c00 | GID | 10 54 | 44 00 | 68 | no |
| 0x00001c20 | STATUS | 1d 1b | 49 4f | 20297 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001c40 | �RECEIVE DATA� | 07 11 | 17747 | no | no |
| 0x00001c60 | �    BUSY    � | 74 17 | 17184 | no | no |
| 0x00001c80 | �  NO REPLY  � | 74 74 | 8224 | no | no |
| 0x00001ca0 | � GPS UPLOAD � | 01 00 | 21589 | no | no |
| 0x00001cc0 | �   EMPTY    � | 74 74 | 8224 | no | no |
| 0x00001ce0 | �SYSTEM BUSY � | 74 74 | 8224 | no | no |
| 0x00001d00 | �  INVALID   � | 11 17 | 17221 | no | no |
| 0x00001d20 | REMOTE CONTROL | 18 01 | 21836 | no | yes |

## Run 5: `0x00001d20-0x00001f1f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001d20 | REMOTE CONTROL | 18 01 | 4c 55 | 21836 | no |
| 0x00001d40 | AM | 54 54 | 00 00 | 0 | no |
| 0x00001d60 | A | 54 54 | 00 00 | 0 | no |
| 0x00001d80 |              s | 74 03 | 20 57 | 22304 | no |
| 0x00001da0 |   VGS ERROR | 11 19 | 45 4d | 19781 | no |
| 0x00001dc0 |    GREETING | 03 74 | 57 20 | 8279 | no |
| 0x00001de0 | END OF MESSAGE | 54 54 | 00 00 | 0 | no |
| 0x00001e00 | VM | 54 54 | 00 00 | 0 | no |
| 0x00001e20 | PRIORITY 4 | 74 12 | 20 46 | 17952 | no |
| 0x00001e40 |   GRP ADD-D | 13 06 | 47 52 | 21063 | no |
| 0x00001e60 |            dBm | 1d 1b | 49 4f | 20297 | no |
| 0x00001e80 |        CH NAME | 74 0e | 20 5a | 23072 | no |
| 0x00001ea0 | MAINTENANCE | 15 17 | 41 43 | 17217 | no |
| 0x00001ec0 |    MESSAGE? | 1b 01 | 4f 55 | 21839 | no |
| 0x00001ee0 | INDIV+SDM | 18 17 | 4c 43 | 17228 | no |
| 0x00001f00 | SHORT MESSAGE | 74 06 | 20 52 | 21024 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001f20 | � REMOTE TX  � | 74 17 | 17184 | no | no |
| 0x00001f40 | LONE WORKER | 74 74 | 8224 | no | yes |
| 0x00001f60 |  SITE ROAMING | 00 11 | 17748 | no | yes |
| 0x00001f80 | ID | 15 00 | 21569 | no | yes |
| 0x00001fa0 | MY ID | 17 11 | 17731 | no | yes |
| 0x00001fc0 | FREE DIAL | 18 18 | 19532 | no | yes |
| 0x00001fe0 | TRANSFER | 11 00 | 21573 | no | yes |
| 0x00002000 | ID | 74 1b | 20256 | no | yes |

## Run 6: `0x00001f40-0x0000215f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001f40 | LONE WORKER | 74 74 | 20 20 | 8224 | no |
| 0x00001f60 |  SITE ROAMING | 00 11 | 54 45 | 17748 | no |
| 0x00001f80 | ID | 15 00 | 41 54 | 21569 | no |
| 0x00001fa0 | MY ID | 17 11 | 43 45 | 17731 | no |
| 0x00001fc0 | FREE DIAL | 18 18 | 4c 4c | 19532 | no |
| 0x00001fe0 | TRANSFER | 11 00 | 45 54 | 21573 | no |
| 0x00002000 | ID | 74 1b | 20 4f | 20256 | no |
| 0x00002020 |     UPDATE | 74 01 | 20 55 | 21792 | no |
| 0x00002040 |   PHONE CALL | 74 74 | 20 20 | 8224 | no |
| 0x00002060 |           FLAT | 74 74 | 20 20 | 8224 | no |
| 0x00002080 |           NONE | 19 1d | 4d 49 | 18765 | no |
| 0x000020a0 |   MICROPHONE 2 | 19 1d | 4d 49 | 18765 | no |
| 0x000020c0 |   MICROPHONE 4 | 19 1d | 4d 49 | 18765 | no |
| 0x000020e0 | RX AUDIO EQ | 74 15 | 20 41 | 16672 | no |
| 0x00002100 | RX AGC | 74 15 | 20 41 | 16672 | no |
| 0x00002120 | EXT MIC TYPE | 74 18 | 20 4c | 19488 | no |
| 0x00002140 | TX NOISE SUPPR | ab ab | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002160 | �������������� | ab ab | 65535 | yes | no |
| 0x00002180 | �������������� | ab ab | 65535 | yes | no |
| 0x000021a0 | �������������� | ab ab | 65535 | yes | no |
| 0x000021c0 | �������������� | ab ab | 65535 | yes | no |
| 0x000021e0 | �������������� | ab ab | 65535 | yes | no |
| 0x00002200 | �������������� | ab ab | 65535 | yes | no |
| 0x00002220 | �������������� | ab ab | 65535 | yes | no |
| 0x00002240 | �������������� | ab ab | 65535 | yes | no |

## Run 7: `0x000024c0-0x0000257f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000024c0 |   KEY ERASED   | 74 1f | 20 4b | 19232 | no |
| 0x000024e0 |    KEYLOAD     | 74 74 | 20 20 | 8224 | no |
| 0x00002500 | SELFTEST ERROR | 19 74 | 4d 20 | 8269 | no |
| 0x00002520 | GROUP ID | 1b 01 | 4f 55 | 21839 | no |
| 0x00002540 | ACTIVITY DET | 13 74 | 47 20 | 8263 | no |
| 0x00002560 | EMG STATIONARY | 11 19 | 45 4d | 19781 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002580 | �������������� | ab ab | 65535 | no | no |
| 0x000025a0 | �������������� | ab ab | 65535 | yes | no |
| 0x000025c0 | �������������� | ab ab | 65535 | yes | no |
| 0x000025e0 | �������������� | ab ab | 65535 | yes | no |
| 0x00002600 | �������������� | ab ab | 65535 | yes | no |
| 0x00002620 | �������������� | ab ab | 65535 | yes | no |
| 0x00002640 | �������������� | ab ab | 65535 | yes | no |
| 0x00002660 | �������������� | ab ab | 65535 | yes | no |

## Run 8: `0x00002680-0x000026bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002680 |   HIGH POWER | 18 1b | 4c 4f | 20300 | no |
| 0x000026a0 |   AUTO POWER | ab ab | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000026c0 | �������������� | 74 10 | 17440 | no | no |
| 0x000026e0 | No. | 0d 07 | 21337 | no | yes |
| 0x00002700 | GPS REPORT ERR | 0d 07 | 21337 | no | yes |
| 0x00002720 | SYSTEM         | 07 00 | 21587 | no | yes |
| 0x00002740 |   ROAM | ab ab | 65535 | no | yes |
| 0x00002760 | �������������� | ab ab | 65535 | yes | no |
| 0x00002780 | �������������� | ab ab | 65535 | yes | no |
| 0x000027a0 | �������������� | ab ab | 65535 | yes | no |

## Run 9: `0x000026e0-0x0000275f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000026e0 | No. | 0d 07 | 59 53 | 21337 | no |
| 0x00002700 | GPS REPORT ERR | 0d 07 | 59 53 | 21337 | no |
| 0x00002720 | SYSTEM         | 07 00 | 53 54 | 21587 | no |
| 0x00002740 |   ROAM | ab ab | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002760 | �������������� | ab ab | 65535 | yes | no |
| 0x00002780 | �������������� | ab ab | 65535 | yes | no |
| 0x000027a0 | �������������� | ab ab | 65535 | yes | no |
| 0x000027c0 | �������������� | ab ab | 65535 | yes | no |
| 0x000027e0 | �������������� | ab ab | 65535 | yes | no |
| 0x00002800 | �������������� | ab ab | 65535 | yes | no |
| 0x00002820 | �������������� | ab ab | 65535 | yes | no |
| 0x00002840 | �������������� | ab ab | 65535 | yes | no |

## Run 10: `0x00002940-0x00002a9f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002940 | FNC | 54 54 | 00 00 | 0 | no |
| 0x00002960 | DR1 | 66 54 | 32 00 | 50 | no |
| 0x00002980 | DR3 | 60 54 | 34 00 | 52 | no |
| 0x000029a0 | DR5 | 18 54 | 4c 00 | 76 | no |
| 0x000029c0 | GPS | 18 54 | 4c 00 | 76 | no |
| 0x000029e0 | OFF | 54 54 | 00 00 | 0 | no |
| 0x00002a00 | HA | ab ab | ff ff | 65535 | no |
| 0x00002a20 | PA | 54 54 | 00 00 | 0 | no |
| 0x00002a40 | S | 54 54 | 00 00 | 0 | no |
| 0x00002a60 | ALL | 54 54 | 00 00 | 0 | no |
| 0x00002a80 | TRS | ab ab | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002aa0 | �������������� | ab ab | 65535 | yes | no |
| 0x00002ac0 | �������������� | ab ab | 65535 | yes | no |
| 0x00002ae0 | �������������� | ab ab | 65535 | yes | no |
| 0x00002b00 | �������������� | ab ab | 65535 | yes | no |
| 0x00002b20 | �������������� | ab ab | 65535 | yes | no |
| 0x00002b40 | �������������� | ab ab | 65535 | yes | no |
| 0x00002b60 | �������������� | ab ab | 65535 | yes | no |
| 0x00002b80 | �������������� | ab ab | 65535 | yes | no |

## Run 11: `0x00002d80-0x00002dbf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002d80 |  EXIT | 11 0c | 45 58 | 22597 | no |
| 0x00002da0 |  BACK | 00 1b | 54 4f | 20308 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002dc0 |       �������� | 00 1b | 20308 | no | no |
| 0x00002de0 | A_RPLY�������� | 00 11 | 17748 | no | no |
| 0x00002e00 | A_DIAL�������� | 0b 04 | 20575 | no | no |
| 0x00002e20 |  AUX | 13 1c | 18503 | no | yes |
| 0x00002e40 | B.CAST�������� | 18 18 | 19532 | no | no |
| 0x00002e60 | CALL2 | 18 18 | 19532 | no | yes |
| 0x00002e80 | CALL4 | 18 18 | 19532 | no | yes |
| 0x00002ea0 | CALL6 | 1c 54 | 72 | no | yes |

## Run 12: `0x00002e60-0x00002ebf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002e60 | CALL2 | 18 18 | 4c 4c | 19532 | no |
| 0x00002e80 | CALL4 | 18 18 | 4c 4c | 19532 | no |
| 0x00002ea0 | CALL6 | 1c 54 | 48 00 | 72 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002ec0 | CH_ENT�������� | 1c 54 | 72 | no | no |
| 0x00002ee0 | CH_RCL�������� | 1b 17 | 17231 | no | no |
| 0x00002f00 | CLK_AJ�������� | 0b 19 | 19807 | no | no |
| 0x00002f20 |  DR1 | 06 66 | 12882 | no | yes |
| 0x00002f40 |  DR3 | 06 60 | 13394 | no | yes |
| 0x00002f60 |  DR5 | 1d 07 | 21321 | no | yes |
| 0x00002f80 | FX_VOL�������� | 06 17 | 17234 | no | no |
| 0x00002fa0 |  FNC | 04 07 | 21328 | no | yes |

## Run 13: `0x00002f20-0x00002f7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002f20 |  DR1 | 06 66 | 52 32 | 12882 | no |
| 0x00002f40 |  DR3 | 06 60 | 52 34 | 13394 | no |
| 0x00002f60 |  DR5 | 1d 07 | 49 53 | 21321 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002f80 | FX_VOL�������� | 06 17 | 17234 | no | no |
| 0x00002fa0 |  FNC | 04 07 | 21328 | no | yes |
| 0x00002fc0 | GROUP | 04 7f | 11088 | no | yes |
| 0x00002fe0 |  HOME | 10 17 | 17220 | no | yes |
| 0x00003000 | IND+ST�������� | 18 1b | 20300 | no | no |
| 0x00003020 |  LOW | 1d 1a | 20041 | no | yes |
| 0x00003040 |  MENU | 1b 1a | 20047 | no | yes |
| 0x00003060 |  MONI | 07 00 | 21587 | no | yes |

## Run 14: `0x00002fa0-0x00002fff`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002fa0 |  FNC | 04 07 | 50 53 | 21328 | no |
| 0x00002fc0 | GROUP | 04 7f | 50 2b | 11088 | no |
| 0x00002fe0 |  HOME | 10 17 | 44 43 | 17220 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003000 | IND+ST�������� | 18 1b | 20300 | no | no |
| 0x00003020 |  LOW | 1d 1a | 20041 | no | yes |
| 0x00003040 |  MENU | 1b 1a | 20047 | no | yes |
| 0x00003060 |  MONI | 07 00 | 21587 | no | yes |
| 0x00003080 |  PLAY | 07 04 | 20563 | no | yes |
| 0x000030a0 |  SCAN | 7b 15 | 16687 | no | yes |
| 0x000030c0 |  SCR | 18 17 | 17228 | no | yes |
| 0x000030e0 | SEL+ST�������� | 07 0b | 24403 | no | no |

## Run 15: `0x00003020-0x000030df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003020 |  LOW | 1d 1a | 49 4e | 20041 | no |
| 0x00003040 |  MENU | 1b 1a | 4f 4e | 20047 | no |
| 0x00003060 |  MONI | 07 00 | 53 54 | 21587 | no |
| 0x00003080 |  PLAY | 07 04 | 53 50 | 20563 | no |
| 0x000030a0 |  SCAN | 7b 15 | 2f 41 | 16687 | no |
| 0x000030c0 |  SCR | 18 17 | 4c 43 | 17228 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000030e0 | SEL+ST�������� | 07 0b | 24403 | no | no |
| 0x00003100 | S_LOCK�������� | 05 18 | 19537 | no | no |
| 0x00003120 | SQ_OFF�������� | 0b 1b | 20319 | no | no |
| 0x00003140 | STACK | 15 00 | 21569 | no | yes |
| 0x00003160 |   TA | 18 0b | 24396 | no | yes |
| 0x00003180 | PASSWD�������� | 1d 16 | 16969 | no | no |
| 0x000031a0 |  MEMO | 1b 0c | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 1a 11 | 17742 | no | no |

## Run 16: `0x00003140-0x0000317f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003140 | STACK | 15 00 | 41 54 | 21569 | no |
| 0x00003160 |   TA | 18 0b | 4c 5f | 24396 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003180 | PASSWD�������� | 1d 16 | 16969 | no | no |
| 0x000031a0 |  MEMO | 1b 0c | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 1a 11 | 17742 | no | no |
| 0x000031e0 | ZONE | 00 11 | 17748 | no | yes |
| 0x00003200 | SITE | 74 03 | 22304 | no | yes |
| 0x00003220 | GRP+SD�������� | 10 7f | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 10 19 | 19780 | no | no |
| 0x00003260 | �������������� | 07 11 | 17747 | no | no |

## Run 17: `0x000031e0-0x0000321f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000031e0 | ZONE | 00 11 | 54 45 | 17748 | no |
| 0x00003200 | SITE | 74 03 | 20 57 | 22304 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003220 | GRP+SD�������� | 10 7f | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 10 19 | 19780 | no | no |
| 0x00003260 | �������������� | 07 11 | 17747 | no | no |
| 0x00003280 |  1x | 2c 54 | 120 | no | yes |
| 0x000032a0 |  10x | 64 2c | 30768 | no | yes |
| 0x000032c0 | RX_ENT�������� | ab ab | 65535 | no | no |
| 0x000032e0 | �������������� | ab ab | 65535 | yes | no |
| 0x00003300 | �������������� | ab ab | 65535 | yes | no |

## Run 18: `0x00003280-0x000032bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003280 |  1x | 2c 54 | 78 00 | 120 | no |
| 0x000032a0 |  10x | 64 2c | 30 78 | 30768 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000032c0 | RX_ENT�������� | ab ab | 65535 | no | no |
| 0x000032e0 | �������������� | ab ab | 65535 | yes | no |
| 0x00003300 | �������������� | ab ab | 65535 | yes | no |
| 0x00003320 |  HIGH | ab ab | 65535 | no | yes |
| 0x00003340 | �������������� | ab ab | 65535 | yes | no |
| 0x00003360 | ACT_DT�������� | 00 0b | 24404 | no | no |
| 0x00003380 | �������������� | ab ab | 65535 | no | no |
| 0x000033a0 | CH_ENT�������� | ab ab | 65535 | no | no |

## Run 19: `0x000037a0-0x000037df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000037a0 | 00 | a4 24 | f0 70 | 28912 | no |
| 0x000037c0 | 0000000 | 64 64 | 30 30 | 12336 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000037e0 | �p00000000000p | 54 a4 | 61440 | no | no |
| 0x00003800 | 00��� | ab ab | 65535 | no | no |
| 0x00003820 |  | 6b 2b | 32575 | no | no |
| 0x00003840 |  | 54 54 | 0 | no | no |
| 0x00003860 |  | ad ad | 63993 | no | no |
| 0x00003880 |  | 54 55 | 256 | no | no |
| 0x000038a0 |  | 54 54 | 0 | no | no |
| 0x000038c0 |  | 53 53 | 1799 | no | no |

## Run 20: `0x00010480-0x0001085f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00010480 | Curtis, AE4BT | fe 6a | aa 3e | 16042 | no |
| 0x000104a0 | Frank, KF4CLO | 77 52 | 23 06 | 1571 | no |
| 0x000104c0 | Ed, AK7AN | 16 64 | 42 30 | 12354 | no |
| 0x000104e0 | Kelli, KD0CVD | 15 64 | 41 30 | 12353 | no |
| 0x00010500 | Chris, K4DKK | 9b 7b | cf 2f | 12239 | no |
| 0x00010520 | DVNET | 5b 73 | 0f 27 | 9999 | no |
| 0x00010540 | No NXDN ID | 2f 2d | 7b 79 | 31099 | no |
| 0x00010560 | Bjorn, SA7AUX | e6 6a | b2 3e | 16050 | no |
| 0x00010580 | Doug, W4DBG | 40 50 | 14 04 | 1044 | no |
| 0x000105a0 | Hello | 32 08 | 66 5c | 23654 | no |
| 0x000105c0 | Randy, W8EJC | c0 cf | 94 9b | 39828 | no |
| 0x000105e0 | BitByBit Hams | 6d 64 | 39 30 | 12345 | no |
| 0x00010600 | Tom, K4TH | ca 71 | 9e 25 | 9630 | no |
| 0x00010620 | NX4DX BitbyBit | e5 7c | b1 28 | 10417 | no |
| 0x00010640 | Long Gone | ba ab | ee ff | 65518 | no |
| 0x00010660 | My Best Friend | 3a e6 | 6e b2 | 45678 | no |
| 0x00010680 | Don't like | 32 08 | 66 5c | 23654 | no |
| 0x000106a0 |  UNIT ID 0018 | a1 63 | f5 37 | 14325 | no |
| 0x000106c0 |  UNIT ID 0019 | e9 a3 | bd f7 | 63421 | no |
| 0x000106e0 |  UNIT ID 0020 | cf 0f | 9b 5b | 23451 | no |
| 0x00010700 |  UNIT ID 0021 | ce 29 | 9a 7d | 32154 | no |
| 0x00010720 |  UNIT ID 0022 | 45 f5 | 11 a1 | 41233 | no |
| 0x00010740 |  UNIT ID 0023 | f3 93 | a7 c7 | 51111 | no |
| 0x00010760 |  UNIT ID 0024 | 4f bb | 1b ef | 61211 | no |
| 0x00010780 |  UNIT ID 0025 | c8 f9 | 9c ad | 44444 | no |
| 0x000107a0 |  UNIT ID 0026 | 57 8d | 03 d9 | 55555 | no |
| 0x000107c0 |  UNIT ID 0027 | 61 d6 | 35 82 | 33333 | no |
| 0x000107e0 |  UNIT ID 0028 | 9a 02 | ce 56 | 22222 | no |
| 0x00010800 |  UNIT ID 0029 | 33 7f | 67 2b | 11111 | no |
| 0x00010820 |  UNIT ID 0030 | 1d 80 | 49 d4 | 54345 | no |
| 0x00010840 |  UNIT ID 0031 | 55 fe | 01 aa | 43521 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00010860 | �������������� | ab ab | 65535 | yes | no |
| 0x00010880 | �������������� | ab ab | 65535 | yes | no |
| 0x000108a0 | �������������� | ab ab | 65535 | yes | no |
| 0x000108c0 | �������������� | ab ab | 65535 | yes | no |
| 0x000108e0 | �������������� | ab ab | 65535 | yes | no |
| 0x00010900 | �������������� | ab ab | 65535 | yes | no |
| 0x00010920 | �������������� | ab ab | 65535 | yes | no |
| 0x00010940 | �������������� | ab ab | 65535 | yes | no |

## Run 21: `0x00014f80-0x0001535f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00014f80 | World Wide TG | bc a9 | e8 fd | 65000 | no |
| 0x00014fa0 | Parrot | 5e 54 | 0a 00 | 10 | no |
| 0x00014fc0 | Colo Fun Mach | 3d 2d | 69 79 | 31081 | no |
| 0x00014fe0 | MO Digi Call | 9f 28 | cb 7c | 31947 | no |
| 0x00015000 | AlabamaLink TG | 76 2d | 22 79 | 31010 | no |
| 0x00015020 | SW Missouri TG | 6f 2e | 3b 7a | 31291 | no |
| 0x00015040 | PiStar TG | ec 2f | b8 7b | 31672 | no |
| 0x00015060 | VK Radio TG | 33 91 | 67 c5 | 50535 | no |
| 0x00015080 | NXDN N America | 8c 73 | d8 27 | 10200 | no |
| 0x000150a0 | Goodbye | 64 14 | 30 40 | 16432 | no |
| 0x000150c0 | Utah DRN 01 | 57 2f | 03 7b | 31491 | no |
| 0x000150e0 | Utah DRN 05 | 53 2f | 07 7b | 31495 | no |
| 0x00015100 | PA7LIM TG | 9c 1b | c8 4f | 20424 | no |
| 0x00015120 | Disconnect TG | 5b 73 | 0f 27 | 9999 | no |
| 0x00015140 | Hot n Sexy | 57 2f | 03 7b | 31491 | no |
| 0x00015160 | Lookout Mtn TG | 29 fd | 7d a9 | 43389 | no |
| 0x00015180 | AK7AN TG | 49 07 | 1d 53 | 21277 | no |
| 0x000151a0 | GROUP ID 0018 | 33 7f | 67 2b | 11111 | no |
| 0x000151c0 | GROUP ID 0019 | 9a 02 | ce 56 | 22222 | no |
| 0x000151e0 | GROUP ID 0020 | 61 d6 | 35 82 | 33333 | no |
| 0x00015200 | GROUP ID 0021 | c8 f9 | 9c ad | 44444 | no |
| 0x00015220 | GROUP ID 0022 | 57 8d | 03 d9 | 55555 | no |
| 0x00015240 | GROUP ID 0023 | 50 8d | 04 d9 | 55556 | no |
| 0x00015260 | BY BY | c9 f9 | 9d ad | 44445 | no |
| 0x00015280 | GROUP ID 0025 | 63 d6 | 37 82 | 33335 | no |
| 0x000152a0 | GROUP ID 0026 | 9b 02 | cf 56 | 22223 | no |
| 0x000152c0 | GROUP ID 0027 | b5 8c | e1 d8 | 55521 | no |
| 0x000152e0 | GROUP ID 0028 | b6 7f | e2 2b | 11234 | no |
| 0x00015300 | GROUP ID 0029 | 0c 78 | 58 2c | 11352 | no |
| 0x00015320 | GROUP ID 0030 | f1 af | a5 fb | 64421 | no |
| 0x00015340 | GROUP ID 0031 | 1c 68 | 48 3c | 15432 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00015360 | �������������� | ab ab | 65535 | yes | no |
| 0x00015380 | �������������� | ab ab | 65535 | yes | no |
| 0x000153a0 | �������������� | ab ab | 65535 | yes | no |
| 0x000153c0 | �������������� | ab ab | 65535 | yes | no |
| 0x000153e0 | �������������� | ab ab | 65535 | yes | no |
| 0x00015400 | �������������� | ab ab | 65535 | yes | no |
| 0x00015420 | �������������� | ab ab | 65535 | yes | no |
| 0x00015440 | �������������� | ab ab | 65535 | yes | no |

