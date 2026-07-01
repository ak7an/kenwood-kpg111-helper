# KPG111 Candidate Table Map

This is a read-only structural scan. Printable decoded names are evidence for candidate records, not proof of table purpose.

## File

- Path: `research/dattest3/Dattest3/Program4.dat`
- Size: 168257 bytes
- SHA-256: `c91e938bf7aead1c8c7d21f5c49a8845031c3a3ba490abfaffafd565f46e81f3`
- Payload start: `0x40`
- Record size: 32
- Decode XOR: `0x1f`
- Records scanned: 5256
- Occupied candidates: 214
- Empty records: 3901

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
| 0x00010480-0x0001083f | 30 | 570 | 0x00010840 empty=True name='��������������' |
| 0x00014f80-0x0001533f | 30 | 321 | 0x00015340 empty=True name='��������������' |

## Run 1: `0x00000b40-0x00000b7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000b40 | ABCDEFGHIJKLMN | 4c 4b | 53 54 | 21587 | no |
| 0x00000b60 | 56789 | 1f 1f | 00 00 | 0 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000b80 |  | 1f 1f | 0 | no | no |
| 0x00000ba0 | 1 | 5c 2d | 12867 | no | yes |
| 0x00000bc0 | DEF3 | 56 2b | 13385 | no | yes |
| 0x00000be0 | JKL5 | 50 29 | 13903 | no | yes |
| 0x00000c00 | PQRS7 | 49 27 | 14422 | no | yes |
| 0x00000c20 | WXYZ9 | e0 e0 | 65535 | no | yes |
| 0x00000c40 | CALL | 5c 5e | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 4b 56 | 18772 | no | no |

## Run 2: `0x00000ba0-0x00000c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000ba0 | 1 | 5c 2d | 43 32 | 12867 | no |
| 0x00000bc0 | DEF3 | 56 2b | 49 34 | 13385 | no |
| 0x00000be0 | JKL5 | 50 29 | 4f 36 | 13903 | no |
| 0x00000c00 | PQRS7 | 49 27 | 56 38 | 14422 | no |
| 0x00000c20 | WXYZ9 | e0 e0 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000c40 | CALL | 5c 5e | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 4b 56 | 18772 | no | no |
| 0x00000c80 | Microphone | 6a 7b | 25717 | no | no |
| 0x00000ca0 |  | 4b 3f | 8276 | no | no |
| 0x00000cc0 | 0+CDNM4����� | e0 e0 | 65535 | no | no |
| 0x00000ce0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00000d00 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00000d20 | �������������� | e0 e0 | 65535 | yes | no |

## Run 3: `0x00001540-0x0000177f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001540 | 2-TONE | 4b 50 | 54 4f | 20308 | no |
| 0x00001560 | AUTO TELEPHONE | 3f 5e | 20 41 | 16672 | no |
| 0x00001580 | AUTO DIAL | 4b 50 | 54 4f | 20308 | no |
| 0x000015a0 |     BLANK | 3f 3f | 20 20 | 8224 | no |
| 0x000015c0 |     CODE? | 3f 3f | 20 20 | 8224 | no |
| 0x000015e0 |  OVER WRITE? | 3f 5b | 20 44 | 17440 | no |
| 0x00001600 | AUX | 47 3f | 58 20 | 8280 | no |
| 0x00001620 | AUX B | 50 5e | 4f 41 | 16719 | no |
| 0x00001640 | CHANNEL ENTRY | 3f 51 | 20 4e | 20000 | no |
| 0x00001660 | PRIORITY 3 | 50 5c | 4f 43 | 17231 | no |
| 0x00001680 | CLOCK ADJUST | 5e 4d | 41 52 | 21057 | no |
| 0x000016a0 | MONTH | 46 1f | 59 00 | 89 | no |
| 0x000016c0 | HOUR | 51 4a | 4e 55 | 21838 | no |
| 0x000016e0 | DIRECT CH1 SEL | 4d 5a | 52 45 | 17746 | no |
| 0x00001700 | DIRECT CH3 SEL | 4d 5a | 52 45 | 17746 | no |
| 0x00001720 | DIRECT CH5 SEL | 4c 4f | 53 50 | 20563 | no |
| 0x00001740 | FIXED VOLUME | 4d 5c | 52 43 | 17234 | no |
| 0x00001760 | SITE No. | 4b 5a | 54 45 | 17748 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001780 | �   SEARCH   � | 4c 3f | 8275 | no | no |
| 0x000017a0 | N | 1f 1f | 0 | no | yes |
| 0x000017c0 | E | 1f 1f | 0 | no | yes |
| 0x000017e0 | ALT | 3f 3f | 8224 | no | yes |
| 0x00001800 |             ft | 50 4a | 21839 | no | yes |
| 0x00001820 | GROUP+STATUS | 52 5a | 17741 | no | yes |
| 0x00001840 | HORN ALERT | 5b 56 | 18756 | no | yes |
| 0x00001860 | INDIV+STATUS | 3f 3f | 8224 | no | yes |

## Run 4: `0x000017a0-0x00001c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000017a0 | N | 1f 1f | 00 00 | 0 | no |
| 0x000017c0 | E | 1f 1f | 00 00 | 0 | no |
| 0x000017e0 | ALT | 3f 3f | 20 20 | 8224 | no |
| 0x00001800 |             ft | 50 4a | 4f 55 | 21839 | no |
| 0x00001820 | GROUP+STATUS | 52 5a | 4d 45 | 17741 | no |
| 0x00001840 | HORN ALERT | 5b 56 | 44 49 | 18756 | no |
| 0x00001860 | INDIV+STATUS | 3f 3f | 20 20 | 8224 | no |
| 0x00001880 | LCD BRIGHTNESS | 48 3f | 57 20 | 8279 | no |
| 0x000018a0 | MENU | 51 56 | 4e 49 | 18766 | no |
| 0x000018c0 | OST | 4b 3f | 54 20 | 8276 | no |
| 0x000018e0 |    TONE OFF | 5e 46 | 41 59 | 22849 | no |
| 0x00001900 | PRI CH SEL | 3f 3f | 20 20 | 8224 | no |
| 0x00001920 |     PRIORITY 1 | 3f 3f | 20 20 | 8224 | no |
| 0x00001940 |   PRIORITY 1&2 | 5d 53 | 42 4c | 19522 | no |
| 0x00001960 | SCAN | 5e 51 | 41 4e | 20033 | no |
| 0x00001980 |         DELETE | 3f 3f | 20 20 | 8224 | no |
| 0x000019a0 |      SCAN | 5e 51 | 41 4e | 20033 | no |
| 0x000019c0 | SCRAM/ENCRYP | 4d 5e | 52 41 | 16722 | no |
| 0x000019e0 | CODE | 53 5c | 4c 43 | 17228 | no |
| 0x00001a00 | SELCALL+STATUS | 51 5b | 4e 44 | 17486 | no |
| 0x00001a20 | SITE LOCK | 4b 5a | 54 45 | 17748 | no |
| 0x00001a40 | SQUELCH LEVEL | 49 5a | 56 45 | 17750 | no |
| 0x00001a60 | SQUELCH OFF | 5e 5c | 41 43 | 17217 | no |
| 0x00001a80 | STATUS | 53 54 | 4c 4b | 19276 | no |
| 0x00001aa0 | PASSWORD | 3f 4f | 20 50 | 20512 | no |
| 0x00001ac0 | VIBRATOR | 56 5c | 49 43 | 17225 | no |
| 0x00001ae0 | VOX | 47 3f | 58 20 | 8280 | no |
| 0x00001b00 | ZONE DEL/ADD | 3f 3f | 20 20 | 8224 | no |
| 0x00001b20 |            OFF | 3f 3f | 20 20 | 8224 | no |
| 0x00001b40 |            LOW | 4c 4b | 53 54 | 21587 | no |
| 0x00001b60 |      BUSY | 3f 3f | 20 20 | 8224 | no |
| 0x00001b80 |      STUN | 53 53 | 4c 4c | 19532 | no |
| 0x00001ba0 | NEW MESSAGE | 5a 52 | 45 4d | 19781 | no |
| 0x00001bc0 |    MAN DOWN | 57 50 | 48 4f | 20296 | no |
| 0x00001be0 | ID | 5e 4b | 41 54 | 21569 | no |
| 0x00001c00 | GID | 5b 1f | 44 00 | 68 | no |
| 0x00001c20 | STATUS | 56 50 | 49 4f | 20297 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001c40 | �RECEIVE DATA� | 4c 5a | 17747 | no | no |
| 0x00001c60 | �    BUSY    � | 3f 5c | 17184 | no | no |
| 0x00001c80 | �  NO REPLY  � | 3f 3f | 8224 | no | no |
| 0x00001ca0 | � GPS UPLOAD � | 4a 4b | 21589 | no | no |
| 0x00001cc0 | �   EMPTY    � | 3f 3f | 8224 | no | no |
| 0x00001ce0 | �SYSTEM BUSY � | 3f 3f | 8224 | no | no |
| 0x00001d00 | �  INVALID   � | 5a 5c | 17221 | no | no |
| 0x00001d20 | REMOTE CONTROL | 53 4a | 21836 | no | yes |

## Run 5: `0x00001d20-0x00001f1f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001d20 | REMOTE CONTROL | 53 4a | 4c 55 | 21836 | no |
| 0x00001d40 | AM | 1f 1f | 00 00 | 0 | no |
| 0x00001d60 | A | 1f 1f | 00 00 | 0 | no |
| 0x00001d80 |              s | 3f 48 | 20 57 | 22304 | no |
| 0x00001da0 |   VGS ERROR | 5a 52 | 45 4d | 19781 | no |
| 0x00001dc0 |    GREETING | 48 3f | 57 20 | 8279 | no |
| 0x00001de0 | END OF MESSAGE | 1f 1f | 00 00 | 0 | no |
| 0x00001e00 | VM | 1f 1f | 00 00 | 0 | no |
| 0x00001e20 | PRIORITY 4 | 3f 59 | 20 46 | 17952 | no |
| 0x00001e40 |   GRP ADD-D | 58 4d | 47 52 | 21063 | no |
| 0x00001e60 |            dBm | 56 50 | 49 4f | 20297 | no |
| 0x00001e80 |        CH NAME | 3f 45 | 20 5a | 23072 | no |
| 0x00001ea0 | MAINTENANCE | 5e 5c | 41 43 | 17217 | no |
| 0x00001ec0 |    MESSAGE? | 50 4a | 4f 55 | 21839 | no |
| 0x00001ee0 | INDIV+SDM | 53 5c | 4c 43 | 17228 | no |
| 0x00001f00 | SHORT MESSAGE | 3f 4d | 20 52 | 21024 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001f20 | � REMOTE TX  � | 3f 5c | 17184 | no | no |
| 0x00001f40 | LONE WORKER | 3f 3f | 8224 | no | yes |
| 0x00001f60 |  SITE ROAMING | 4b 5a | 17748 | no | yes |
| 0x00001f80 | ID | 5e 4b | 21569 | no | yes |
| 0x00001fa0 | MY ID | 5c 5a | 17731 | no | yes |
| 0x00001fc0 | FREE DIAL | 53 53 | 19532 | no | yes |
| 0x00001fe0 | TRANSFER | 5a 4b | 21573 | no | yes |
| 0x00002000 | ID | 3f 50 | 20256 | no | yes |

## Run 6: `0x00001f40-0x0000215f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001f40 | LONE WORKER | 3f 3f | 20 20 | 8224 | no |
| 0x00001f60 |  SITE ROAMING | 4b 5a | 54 45 | 17748 | no |
| 0x00001f80 | ID | 5e 4b | 41 54 | 21569 | no |
| 0x00001fa0 | MY ID | 5c 5a | 43 45 | 17731 | no |
| 0x00001fc0 | FREE DIAL | 53 53 | 4c 4c | 19532 | no |
| 0x00001fe0 | TRANSFER | 5a 4b | 45 54 | 21573 | no |
| 0x00002000 | ID | 3f 50 | 20 4f | 20256 | no |
| 0x00002020 |     UPDATE | 3f 4a | 20 55 | 21792 | no |
| 0x00002040 |   PHONE CALL | 3f 3f | 20 20 | 8224 | no |
| 0x00002060 |           FLAT | 3f 3f | 20 20 | 8224 | no |
| 0x00002080 |           NONE | 52 56 | 4d 49 | 18765 | no |
| 0x000020a0 |   MICROPHONE 2 | 52 56 | 4d 49 | 18765 | no |
| 0x000020c0 |   MICROPHONE 4 | 52 56 | 4d 49 | 18765 | no |
| 0x000020e0 | RX AUDIO EQ | 3f 5e | 20 41 | 16672 | no |
| 0x00002100 | RX AGC | 3f 5e | 20 41 | 16672 | no |
| 0x00002120 | EXT MIC TYPE | 3f 53 | 20 4c | 19488 | no |
| 0x00002140 | TX NOISE SUPPR | e0 e0 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002160 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002180 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000021a0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000021c0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000021e0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002200 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002220 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002240 | �������������� | e0 e0 | 65535 | yes | no |

## Run 7: `0x000024c0-0x0000257f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000024c0 |   KEY ERASED   | 3f 54 | 20 4b | 19232 | no |
| 0x000024e0 |    KEYLOAD     | 3f 3f | 20 20 | 8224 | no |
| 0x00002500 | SELFTEST ERROR | 52 3f | 4d 20 | 8269 | no |
| 0x00002520 | GROUP ID | 50 4a | 4f 55 | 21839 | no |
| 0x00002540 | ACTIVITY DET | 58 3f | 47 20 | 8263 | no |
| 0x00002560 | EMG STATIONARY | 5a 52 | 45 4d | 19781 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002580 | �������������� | e0 e0 | 65535 | no | no |
| 0x000025a0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000025c0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000025e0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002600 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002620 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002640 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002660 | �������������� | e0 e0 | 65535 | yes | no |

## Run 8: `0x00002680-0x000026bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002680 |   HIGH POWER | 53 50 | 4c 4f | 20300 | no |
| 0x000026a0 |   AUTO POWER | e0 e0 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000026c0 | �������������� | 3f 5b | 17440 | no | no |
| 0x000026e0 | No. | 46 4c | 21337 | no | yes |
| 0x00002700 | GPS REPORT ERR | 46 4c | 21337 | no | yes |
| 0x00002720 | SYSTEM         | 4c 4b | 21587 | no | yes |
| 0x00002740 |   ROAM | e0 e0 | 65535 | no | yes |
| 0x00002760 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002780 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000027a0 | �������������� | e0 e0 | 65535 | yes | no |

## Run 9: `0x000026e0-0x0000275f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000026e0 | No. | 46 4c | 59 53 | 21337 | no |
| 0x00002700 | GPS REPORT ERR | 46 4c | 59 53 | 21337 | no |
| 0x00002720 | SYSTEM         | 4c 4b | 53 54 | 21587 | no |
| 0x00002740 |   ROAM | e0 e0 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002760 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002780 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000027a0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000027c0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000027e0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002800 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002820 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002840 | �������������� | e0 e0 | 65535 | yes | no |

## Run 10: `0x00002940-0x00002a9f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002940 | FNC | 1f 1f | 00 00 | 0 | no |
| 0x00002960 | DR1 | 2d 1f | 32 00 | 50 | no |
| 0x00002980 | DR3 | 2b 1f | 34 00 | 52 | no |
| 0x000029a0 | DR5 | 53 1f | 4c 00 | 76 | no |
| 0x000029c0 | GPS | 53 1f | 4c 00 | 76 | no |
| 0x000029e0 | OFF | 1f 1f | 00 00 | 0 | no |
| 0x00002a00 | HA | e0 e0 | ff ff | 65535 | no |
| 0x00002a20 | PA | 1f 1f | 00 00 | 0 | no |
| 0x00002a40 | S | 1f 1f | 00 00 | 0 | no |
| 0x00002a60 | ALL | 1f 1f | 00 00 | 0 | no |
| 0x00002a80 | TRS | e0 e0 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002aa0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002ac0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002ae0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002b00 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002b20 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002b40 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002b60 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00002b80 | �������������� | e0 e0 | 65535 | yes | no |

## Run 11: `0x00002d80-0x00002dbf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002d80 |  EXIT | 5a 47 | 45 58 | 22597 | no |
| 0x00002da0 |  BACK | 4b 50 | 54 4f | 20308 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002dc0 |       �������� | 4b 50 | 20308 | no | no |
| 0x00002de0 | A_RPLY�������� | 4b 5a | 17748 | no | no |
| 0x00002e00 | A_DIAL�������� | 40 4f | 20575 | no | no |
| 0x00002e20 |  AUX | 58 57 | 18503 | no | yes |
| 0x00002e40 | B.CAST�������� | 53 53 | 19532 | no | no |
| 0x00002e60 | CALL2 | 53 53 | 19532 | no | yes |
| 0x00002e80 | CALL4 | 53 53 | 19532 | no | yes |
| 0x00002ea0 | CALL6 | 57 1f | 72 | no | yes |

## Run 12: `0x00002e60-0x00002ebf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002e60 | CALL2 | 53 53 | 4c 4c | 19532 | no |
| 0x00002e80 | CALL4 | 53 53 | 4c 4c | 19532 | no |
| 0x00002ea0 | CALL6 | 57 1f | 48 00 | 72 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002ec0 | CH_ENT�������� | 57 1f | 72 | no | no |
| 0x00002ee0 | CH_RCL�������� | 50 5c | 17231 | no | no |
| 0x00002f00 | CLK_AJ�������� | 40 52 | 19807 | no | no |
| 0x00002f20 |  DR1 | 4d 2d | 12882 | no | yes |
| 0x00002f40 |  DR3 | 4d 2b | 13394 | no | yes |
| 0x00002f60 |  DR5 | 56 4c | 21321 | no | yes |
| 0x00002f80 | FX_VOL�������� | 4d 5c | 17234 | no | no |
| 0x00002fa0 |  FNC | 4f 4c | 21328 | no | yes |

## Run 13: `0x00002f20-0x00002f7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002f20 |  DR1 | 4d 2d | 52 32 | 12882 | no |
| 0x00002f40 |  DR3 | 4d 2b | 52 34 | 13394 | no |
| 0x00002f60 |  DR5 | 56 4c | 49 53 | 21321 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002f80 | FX_VOL�������� | 4d 5c | 17234 | no | no |
| 0x00002fa0 |  FNC | 4f 4c | 21328 | no | yes |
| 0x00002fc0 | GROUP | 4f 34 | 11088 | no | yes |
| 0x00002fe0 |  HOME | 5b 5c | 17220 | no | yes |
| 0x00003000 | IND+ST�������� | 53 50 | 20300 | no | no |
| 0x00003020 |  LOW | 56 51 | 20041 | no | yes |
| 0x00003040 |  MENU | 50 51 | 20047 | no | yes |
| 0x00003060 |  MONI | 4c 4b | 21587 | no | yes |

## Run 14: `0x00002fa0-0x00002fff`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002fa0 |  FNC | 4f 4c | 50 53 | 21328 | no |
| 0x00002fc0 | GROUP | 4f 34 | 50 2b | 11088 | no |
| 0x00002fe0 |  HOME | 5b 5c | 44 43 | 17220 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003000 | IND+ST�������� | 53 50 | 20300 | no | no |
| 0x00003020 |  LOW | 56 51 | 20041 | no | yes |
| 0x00003040 |  MENU | 50 51 | 20047 | no | yes |
| 0x00003060 |  MONI | 4c 4b | 21587 | no | yes |
| 0x00003080 |  PLAY | 4c 4f | 20563 | no | yes |
| 0x000030a0 |  SCAN | 30 5e | 16687 | no | yes |
| 0x000030c0 |  SCR | 53 5c | 17228 | no | yes |
| 0x000030e0 | SEL+ST�������� | 4c 40 | 24403 | no | no |

## Run 15: `0x00003020-0x000030df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003020 |  LOW | 56 51 | 49 4e | 20041 | no |
| 0x00003040 |  MENU | 50 51 | 4f 4e | 20047 | no |
| 0x00003060 |  MONI | 4c 4b | 53 54 | 21587 | no |
| 0x00003080 |  PLAY | 4c 4f | 53 50 | 20563 | no |
| 0x000030a0 |  SCAN | 30 5e | 2f 41 | 16687 | no |
| 0x000030c0 |  SCR | 53 5c | 4c 43 | 17228 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000030e0 | SEL+ST�������� | 4c 40 | 24403 | no | no |
| 0x00003100 | S_LOCK�������� | 4e 53 | 19537 | no | no |
| 0x00003120 | SQ_OFF�������� | 40 50 | 20319 | no | no |
| 0x00003140 | STACK | 5e 4b | 21569 | no | yes |
| 0x00003160 |   TA | 53 40 | 24396 | no | yes |
| 0x00003180 | PASSWD�������� | 56 5d | 16969 | no | no |
| 0x000031a0 |  MEMO | 50 47 | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 51 5a | 17742 | no | no |

## Run 16: `0x00003140-0x0000317f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003140 | STACK | 5e 4b | 41 54 | 21569 | no |
| 0x00003160 |   TA | 53 40 | 4c 5f | 24396 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003180 | PASSWD�������� | 56 5d | 16969 | no | no |
| 0x000031a0 |  MEMO | 50 47 | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 51 5a | 17742 | no | no |
| 0x000031e0 | ZONE | 4b 5a | 17748 | no | yes |
| 0x00003200 | SITE | 3f 48 | 22304 | no | yes |
| 0x00003220 | GRP+SD�������� | 5b 34 | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 5b 52 | 19780 | no | no |
| 0x00003260 | �������������� | 4c 5a | 17747 | no | no |

## Run 17: `0x000031e0-0x0000321f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000031e0 | ZONE | 4b 5a | 54 45 | 17748 | no |
| 0x00003200 | SITE | 3f 48 | 20 57 | 22304 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003220 | GRP+SD�������� | 5b 34 | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 5b 52 | 19780 | no | no |
| 0x00003260 | �������������� | 4c 5a | 17747 | no | no |
| 0x00003280 |  1x | 67 1f | 120 | no | yes |
| 0x000032a0 |  10x | 2f 67 | 30768 | no | yes |
| 0x000032c0 | RX_ENT�������� | e0 e0 | 65535 | no | no |
| 0x000032e0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00003300 | �������������� | e0 e0 | 65535 | yes | no |

## Run 18: `0x00003280-0x000032bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003280 |  1x | 67 1f | 78 00 | 120 | no |
| 0x000032a0 |  10x | 2f 67 | 30 78 | 30768 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000032c0 | RX_ENT�������� | e0 e0 | 65535 | no | no |
| 0x000032e0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00003300 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00003320 |  HIGH | e0 e0 | 65535 | no | yes |
| 0x00003340 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00003360 | ACT_DT�������� | 4b 40 | 24404 | no | no |
| 0x00003380 | �������������� | e0 e0 | 65535 | no | no |
| 0x000033a0 | CH_ENT�������� | e0 e0 | 65535 | no | no |

## Run 19: `0x000037a0-0x000037df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000037a0 | 00 | ef 6f | f0 70 | 28912 | no |
| 0x000037c0 | 0000000 | 2f 2f | 30 30 | 12336 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000037e0 | �p00000000000p | 1f ef | 61440 | no | no |
| 0x00003800 | 00��� | e0 e0 | 65535 | no | no |
| 0x00003820 |  | 20 60 | 32575 | no | no |
| 0x00003840 |  | 1f 1f | 0 | no | no |
| 0x00003860 |  | e6 e6 | 63993 | no | no |
| 0x00003880 |  | 1f 1e | 256 | no | no |
| 0x000038a0 |  | 1f 1f | 0 | no | no |
| 0x000038c0 |  | 18 18 | 1799 | no | no |

## Run 20: `0x00010480-0x0001083f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00010480 | Curtis, AE4BT | b5 21 | aa 3e | 16042 | no |
| 0x000104a0 | Frank, KF4CLO | 3c 19 | 23 06 | 1571 | no |
| 0x000104c0 | Ed, AK7AN | 5d 2f | 42 30 | 12354 | no |
| 0x000104e0 | Kelli, KD0CVD | 5e 2f | 41 30 | 12353 | no |
| 0x00010500 | Chris, K4DKK | d0 30 | cf 2f | 12239 | no |
| 0x00010520 | DVNET | 10 38 | 0f 27 | 9999 | no |
| 0x00010540 | No NXDN ID | 64 66 | 7b 79 | 31099 | no |
| 0x00010560 | Bjorn, SA7AUX | ad 21 | b2 3e | 16050 | no |
| 0x00010580 | Doug, W4DBG | 0b 1b | 14 04 | 1044 | no |
| 0x000105a0 | Hello | 79 43 | 66 5c | 23654 | no |
| 0x000105c0 | Randy, W8EJC | 8b 84 | 94 9b | 39828 | no |
| 0x000105e0 | BitByBit Hams | 26 2f | 39 30 | 12345 | no |
| 0x00010600 | Tom, K4TH | 81 3a | 9e 25 | 9630 | no |
| 0x00010620 | NX4DX BitbyBit | ae 37 | b1 28 | 10417 | no |
| 0x00010640 | Long Gone | f1 e0 | ee ff | 65518 | no |
| 0x00010660 | My Best Friend | 71 ad | 6e b2 | 45678 | no |
| 0x00010680 | Don't like | 79 43 | 66 5c | 23654 | no |
| 0x000106a0 |  UNIT ID 0018 | ea 28 | f5 37 | 14325 | no |
| 0x000106c0 |  UNIT ID 0019 | a2 e8 | bd f7 | 63421 | no |
| 0x000106e0 |  UNIT ID 0020 | 84 44 | 9b 5b | 23451 | no |
| 0x00010700 |  UNIT ID 0021 | 85 62 | 9a 7d | 32154 | no |
| 0x00010720 |  UNIT ID 0022 | 0e be | 11 a1 | 41233 | no |
| 0x00010740 |  UNIT ID 0023 | b8 d8 | a7 c7 | 51111 | no |
| 0x00010760 |  UNIT ID 0024 | 04 f0 | 1b ef | 61211 | no |
| 0x00010780 |  UNIT ID 0025 | 83 b2 | 9c ad | 44444 | no |
| 0x000107a0 |  UNIT ID 0026 | 1c c6 | 03 d9 | 55555 | no |
| 0x000107c0 |  UNIT ID 0027 | 2a 9d | 35 82 | 33333 | no |
| 0x000107e0 |  UNIT ID 0028 | d1 49 | ce 56 | 22222 | no |
| 0x00010800 |  UNIT ID 0029 | 78 34 | 67 2b | 11111 | no |
| 0x00010820 |  UNIT ID 0030 | 56 cb | 49 d4 | 54345 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00010840 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00010860 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00010880 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000108a0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000108c0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000108e0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00010900 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00010920 | �������������� | e0 e0 | 65535 | yes | no |

## Run 21: `0x00014f80-0x0001533f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00014f80 | World Wide TG | f7 e2 | e8 fd | 65000 | no |
| 0x00014fa0 | Parrot | 15 1f | 0a 00 | 10 | no |
| 0x00014fc0 | Colo Fun Mach | 76 66 | 69 79 | 31081 | no |
| 0x00014fe0 | MO Digi Call | d4 63 | cb 7c | 31947 | no |
| 0x00015000 | AlabamaLink TG | 3d 66 | 22 79 | 31010 | no |
| 0x00015020 | SW Missouri TG | 24 65 | 3b 7a | 31291 | no |
| 0x00015040 | PiStar TG | a7 64 | b8 7b | 31672 | no |
| 0x00015060 | VK Radio TG | 78 da | 67 c5 | 50535 | no |
| 0x00015080 | NXDN N America | c7 38 | d8 27 | 10200 | no |
| 0x000150a0 | Goodbye | 2f 5f | 30 40 | 16432 | no |
| 0x000150c0 | Utah DRN 01 | 1c 64 | 03 7b | 31491 | no |
| 0x000150e0 | Utah DRN 05 | 18 64 | 07 7b | 31495 | no |
| 0x00015100 | PA7LIM TG | d7 50 | c8 4f | 20424 | no |
| 0x00015120 | Disconnect TG | 10 38 | 0f 27 | 9999 | no |
| 0x00015140 | Hot n Sexy | 1c 64 | 03 7b | 31491 | no |
| 0x00015160 | Lookout Mtn TG | 62 b6 | 7d a9 | 43389 | no |
| 0x00015180 | AK7AN TG | 02 4c | 1d 53 | 21277 | no |
| 0x000151a0 | GROUP ID 0018 | 78 34 | 67 2b | 11111 | no |
| 0x000151c0 | GROUP ID 0019 | d1 49 | ce 56 | 22222 | no |
| 0x000151e0 | GROUP ID 0020 | 2a 9d | 35 82 | 33333 | no |
| 0x00015200 | GROUP ID 0021 | 83 b2 | 9c ad | 44444 | no |
| 0x00015220 | GROUP ID 0022 | 1c c6 | 03 d9 | 55555 | no |
| 0x00015240 | GROUP ID 0023 | 1b c6 | 04 d9 | 55556 | no |
| 0x00015260 | BY BY | 82 b2 | 9d ad | 44445 | no |
| 0x00015280 | GROUP ID 0025 | 28 9d | 37 82 | 33335 | no |
| 0x000152a0 | GROUP ID 0026 | d0 49 | cf 56 | 22223 | no |
| 0x000152c0 | GROUP ID 0027 | fe c7 | e1 d8 | 55521 | no |
| 0x000152e0 | GROUP ID 0028 | fd 34 | e2 2b | 11234 | no |
| 0x00015300 | GROUP ID 0029 | 47 33 | 58 2c | 11352 | no |
| 0x00015320 | GROUP ID 0030 | ba e4 | a5 fb | 64421 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00015340 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00015360 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00015380 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000153a0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000153c0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x000153e0 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00015400 | �������������� | e0 e0 | 65535 | yes | no |
| 0x00015420 | �������������� | e0 e0 | 65535 | yes | no |

