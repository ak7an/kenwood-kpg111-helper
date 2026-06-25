# KPG111 Candidate Table Map

This is a read-only structural scan. Printable decoded names are evidence for candidate records, not proof of table purpose.

## File

- Path: `research/dattest/Dattest/AK7AN_Travel.dat`
- Size: 168257 bytes
- SHA-256: `aa20a84b5cb76e5fd58a691eb26fdc4140e7d75fb3bd6b28fc156f3ec4144cce`
- Payload start: `0x40`
- Record size: 32
- Decode XOR: `0x5b`
- Records scanned: 5256
- Occupied candidates: 185
- Empty records: 3930

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
| 0x00010480-0x0001063f | 14 | 586 | 0x00010640 empty=True name='��������������' |
| 0x00014f80-0x0001519f | 17 | 334 | 0x000151a0 empty=True name='��������������' |

## Run 1: `0x00000b40-0x00000b7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000b40 | ABCDEFGHIJKLMN | 08 0f | 53 54 | 21587 | no |
| 0x00000b60 | 56789 | 5b 5b | 00 00 | 0 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000b80 |  | 5b 5b | 0 | no | no |
| 0x00000ba0 | 1 | 18 69 | 12867 | no | yes |
| 0x00000bc0 | DEF3 | 12 6f | 13385 | no | yes |
| 0x00000be0 | JKL5 | 14 6d | 13903 | no | yes |
| 0x00000c00 | PQRS7 | 0d 63 | 14422 | no | yes |
| 0x00000c20 | WXYZ9 | a4 a4 | 65535 | no | yes |
| 0x00000c40 | CALL | 18 1a | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 0f 12 | 18772 | no | no |

## Run 2: `0x00000ba0-0x00000c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000ba0 | 1 | 18 69 | 43 32 | 12867 | no |
| 0x00000bc0 | DEF3 | 12 6f | 49 34 | 13385 | no |
| 0x00000be0 | JKL5 | 14 6d | 4f 36 | 13903 | no |
| 0x00000c00 | PQRS7 | 0d 63 | 56 38 | 14422 | no |
| 0x00000c20 | WXYZ9 | a4 a4 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000c40 | CALL | 18 1a | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 0f 12 | 18772 | no | no |
| 0x00000c80 | Microphone | 2e 3f | 25717 | no | no |
| 0x00000ca0 |  | 0f 7b | 8276 | no | no |
| 0x00000cc0 | 0+CDNM4����� | a4 a4 | 65535 | no | no |
| 0x00000ce0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00000d00 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00000d20 | �������������� | a4 a4 | 65535 | yes | no |

## Run 3: `0x00001540-0x0000177f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001540 | 2-TONE | 0f 14 | 54 4f | 20308 | no |
| 0x00001560 | AUTO TELEPHONE | 7b 1a | 20 41 | 16672 | no |
| 0x00001580 | AUTO DIAL | 0f 14 | 54 4f | 20308 | no |
| 0x000015a0 |     BLANK | 7b 7b | 20 20 | 8224 | no |
| 0x000015c0 |     CODE? | 7b 7b | 20 20 | 8224 | no |
| 0x000015e0 |  OVER WRITE? | 7b 1f | 20 44 | 17440 | no |
| 0x00001600 | AUX | 03 7b | 58 20 | 8280 | no |
| 0x00001620 | AUX B | 14 1a | 4f 41 | 16719 | no |
| 0x00001640 | CHANNEL ENTRY | 7b 15 | 20 4e | 20000 | no |
| 0x00001660 | PRIORITY 3 | 14 18 | 4f 43 | 17231 | no |
| 0x00001680 | CLOCK ADJUST | 1a 09 | 41 52 | 21057 | no |
| 0x000016a0 | MONTH | 02 5b | 59 00 | 89 | no |
| 0x000016c0 | HOUR | 15 0e | 4e 55 | 21838 | no |
| 0x000016e0 | DIRECT CH1 SEL | 09 1e | 52 45 | 17746 | no |
| 0x00001700 | DIRECT CH3 SEL | 09 1e | 52 45 | 17746 | no |
| 0x00001720 | DIRECT CH5 SEL | 08 0b | 53 50 | 20563 | no |
| 0x00001740 | FIXED VOLUME | 09 18 | 52 43 | 17234 | no |
| 0x00001760 | SITE No. | 0f 1e | 54 45 | 17748 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001780 | �   SEARCH   � | 08 7b | 8275 | no | no |
| 0x000017a0 | N | 5b 5b | 0 | no | yes |
| 0x000017c0 | E | 5b 5b | 0 | no | yes |
| 0x000017e0 | ALT | 7b 7b | 8224 | no | yes |
| 0x00001800 |             ft | 14 0e | 21839 | no | yes |
| 0x00001820 | GROUP+STATUS | 16 1e | 17741 | no | yes |
| 0x00001840 | HORN ALERT | 1f 12 | 18756 | no | yes |
| 0x00001860 | INDIV+STATUS | 7b 7b | 8224 | no | yes |

## Run 4: `0x000017a0-0x00001c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000017a0 | N | 5b 5b | 00 00 | 0 | no |
| 0x000017c0 | E | 5b 5b | 00 00 | 0 | no |
| 0x000017e0 | ALT | 7b 7b | 20 20 | 8224 | no |
| 0x00001800 |             ft | 14 0e | 4f 55 | 21839 | no |
| 0x00001820 | GROUP+STATUS | 16 1e | 4d 45 | 17741 | no |
| 0x00001840 | HORN ALERT | 1f 12 | 44 49 | 18756 | no |
| 0x00001860 | INDIV+STATUS | 7b 7b | 20 20 | 8224 | no |
| 0x00001880 | LCD BRIGHTNESS | 0c 7b | 57 20 | 8279 | no |
| 0x000018a0 | MENU | 15 12 | 4e 49 | 18766 | no |
| 0x000018c0 | OST | 0f 7b | 54 20 | 8276 | no |
| 0x000018e0 |    TONE OFF | 1a 02 | 41 59 | 22849 | no |
| 0x00001900 | PRI CH SEL | 7b 7b | 20 20 | 8224 | no |
| 0x00001920 |     PRIORITY 1 | 7b 7b | 20 20 | 8224 | no |
| 0x00001940 |   PRIORITY 1&2 | 19 17 | 42 4c | 19522 | no |
| 0x00001960 | SCAN | 1a 15 | 41 4e | 20033 | no |
| 0x00001980 |         DELETE | 7b 7b | 20 20 | 8224 | no |
| 0x000019a0 |      SCAN | 1a 15 | 41 4e | 20033 | no |
| 0x000019c0 | SCRAM/ENCRYP | 09 1a | 52 41 | 16722 | no |
| 0x000019e0 | CODE | 17 18 | 4c 43 | 17228 | no |
| 0x00001a00 | SELCALL+STATUS | 15 1f | 4e 44 | 17486 | no |
| 0x00001a20 | SITE LOCK | 0f 1e | 54 45 | 17748 | no |
| 0x00001a40 | SQUELCH LEVEL | 0d 1e | 56 45 | 17750 | no |
| 0x00001a60 | SQUELCH OFF | 1a 18 | 41 43 | 17217 | no |
| 0x00001a80 | STATUS | 17 10 | 4c 4b | 19276 | no |
| 0x00001aa0 | PASSWORD | 7b 0b | 20 50 | 20512 | no |
| 0x00001ac0 | VIBRATOR | 12 18 | 49 43 | 17225 | no |
| 0x00001ae0 | VOX | 03 7b | 58 20 | 8280 | no |
| 0x00001b00 | ZONE DEL/ADD | 7b 7b | 20 20 | 8224 | no |
| 0x00001b20 |            OFF | 7b 7b | 20 20 | 8224 | no |
| 0x00001b40 |            LOW | 08 0f | 53 54 | 21587 | no |
| 0x00001b60 |      BUSY | 7b 7b | 20 20 | 8224 | no |
| 0x00001b80 |      STUN | 17 17 | 4c 4c | 19532 | no |
| 0x00001ba0 | NEW MESSAGE | 1e 16 | 45 4d | 19781 | no |
| 0x00001bc0 |    MAN DOWN | 13 14 | 48 4f | 20296 | no |
| 0x00001be0 | ID | 1a 0f | 41 54 | 21569 | no |
| 0x00001c00 | GID | 1f 5b | 44 00 | 68 | no |
| 0x00001c20 | STATUS | 12 14 | 49 4f | 20297 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001c40 | �RECEIVE DATA� | 08 1e | 17747 | no | no |
| 0x00001c60 | �    BUSY    � | 7b 18 | 17184 | no | no |
| 0x00001c80 | �  NO REPLY  � | 7b 7b | 8224 | no | no |
| 0x00001ca0 | � GPS UPLOAD � | 0e 0f | 21589 | no | no |
| 0x00001cc0 | �   EMPTY    � | 7b 7b | 8224 | no | no |
| 0x00001ce0 | �SYSTEM BUSY � | 7b 7b | 8224 | no | no |
| 0x00001d00 | �  INVALID   � | 1e 18 | 17221 | no | no |
| 0x00001d20 | REMOTE CONTROL | 17 0e | 21836 | no | yes |

## Run 5: `0x00001d20-0x00001f1f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001d20 | REMOTE CONTROL | 17 0e | 4c 55 | 21836 | no |
| 0x00001d40 | AM | 5b 5b | 00 00 | 0 | no |
| 0x00001d60 | A | 5b 5b | 00 00 | 0 | no |
| 0x00001d80 |              s | 7b 0c | 20 57 | 22304 | no |
| 0x00001da0 |   VGS ERROR | 1e 16 | 45 4d | 19781 | no |
| 0x00001dc0 |    GREETING | 0c 7b | 57 20 | 8279 | no |
| 0x00001de0 | END OF MESSAGE | 5b 5b | 00 00 | 0 | no |
| 0x00001e00 | VM | 5b 5b | 00 00 | 0 | no |
| 0x00001e20 | PRIORITY 4 | 7b 1d | 20 46 | 17952 | no |
| 0x00001e40 |   GRP ADD-D | 1c 09 | 47 52 | 21063 | no |
| 0x00001e60 |            dBm | 12 14 | 49 4f | 20297 | no |
| 0x00001e80 |        CH NAME | 7b 01 | 20 5a | 23072 | no |
| 0x00001ea0 | MAINTENANCE | 1a 18 | 41 43 | 17217 | no |
| 0x00001ec0 |    MESSAGE? | 14 0e | 4f 55 | 21839 | no |
| 0x00001ee0 | INDIV+SDM | 17 18 | 4c 43 | 17228 | no |
| 0x00001f00 | SHORT MESSAGE | 7b 09 | 20 52 | 21024 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001f20 | � REMOTE TX  � | 7b 18 | 17184 | no | no |
| 0x00001f40 | LONE WORKER | 7b 7b | 8224 | no | yes |
| 0x00001f60 |  SITE ROAMING | 0f 1e | 17748 | no | yes |
| 0x00001f80 | ID | 1a 0f | 21569 | no | yes |
| 0x00001fa0 | MY ID | 18 1e | 17731 | no | yes |
| 0x00001fc0 | FREE DIAL | 17 17 | 19532 | no | yes |
| 0x00001fe0 | TRANSFER | 1e 0f | 21573 | no | yes |
| 0x00002000 | ID | 7b 14 | 20256 | no | yes |

## Run 6: `0x00001f40-0x0000215f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001f40 | LONE WORKER | 7b 7b | 20 20 | 8224 | no |
| 0x00001f60 |  SITE ROAMING | 0f 1e | 54 45 | 17748 | no |
| 0x00001f80 | ID | 1a 0f | 41 54 | 21569 | no |
| 0x00001fa0 | MY ID | 18 1e | 43 45 | 17731 | no |
| 0x00001fc0 | FREE DIAL | 17 17 | 4c 4c | 19532 | no |
| 0x00001fe0 | TRANSFER | 1e 0f | 45 54 | 21573 | no |
| 0x00002000 | ID | 7b 14 | 20 4f | 20256 | no |
| 0x00002020 |     UPDATE | 7b 0e | 20 55 | 21792 | no |
| 0x00002040 |   PHONE CALL | 7b 7b | 20 20 | 8224 | no |
| 0x00002060 |           FLAT | 7b 7b | 20 20 | 8224 | no |
| 0x00002080 |           NONE | 16 12 | 4d 49 | 18765 | no |
| 0x000020a0 |   MICROPHONE 2 | 16 12 | 4d 49 | 18765 | no |
| 0x000020c0 |   MICROPHONE 4 | 16 12 | 4d 49 | 18765 | no |
| 0x000020e0 | RX AUDIO EQ | 7b 1a | 20 41 | 16672 | no |
| 0x00002100 | RX AGC | 7b 1a | 20 41 | 16672 | no |
| 0x00002120 | EXT MIC TYPE | 7b 17 | 20 4c | 19488 | no |
| 0x00002140 | TX NOISE SUPPR | a4 a4 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002160 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002180 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000021a0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000021c0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000021e0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002200 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002220 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002240 | �������������� | a4 a4 | 65535 | yes | no |

## Run 7: `0x000024c0-0x0000257f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000024c0 |   KEY ERASED   | 7b 10 | 20 4b | 19232 | no |
| 0x000024e0 |    KEYLOAD     | 7b 7b | 20 20 | 8224 | no |
| 0x00002500 | SELFTEST ERROR | 16 7b | 4d 20 | 8269 | no |
| 0x00002520 | GROUP ID | 14 0e | 4f 55 | 21839 | no |
| 0x00002540 | ACTIVITY DET | 1c 7b | 47 20 | 8263 | no |
| 0x00002560 | EMG STATIONARY | 1e 16 | 45 4d | 19781 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002580 | �������������� | a4 a4 | 65535 | no | no |
| 0x000025a0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000025c0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000025e0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002600 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002620 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002640 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002660 | �������������� | a4 a4 | 65535 | yes | no |

## Run 8: `0x00002680-0x000026bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002680 |   HIGH POWER | 17 14 | 4c 4f | 20300 | no |
| 0x000026a0 |   AUTO POWER | a4 a4 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000026c0 | �������������� | 7b 1f | 17440 | no | no |
| 0x000026e0 | No. | 02 08 | 21337 | no | yes |
| 0x00002700 | GPS REPORT ERR | 02 08 | 21337 | no | yes |
| 0x00002720 | SYSTEM         | 08 0f | 21587 | no | yes |
| 0x00002740 |   ROAM | a4 a4 | 65535 | no | yes |
| 0x00002760 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002780 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000027a0 | �������������� | a4 a4 | 65535 | yes | no |

## Run 9: `0x000026e0-0x0000275f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000026e0 | No. | 02 08 | 59 53 | 21337 | no |
| 0x00002700 | GPS REPORT ERR | 02 08 | 59 53 | 21337 | no |
| 0x00002720 | SYSTEM         | 08 0f | 53 54 | 21587 | no |
| 0x00002740 |   ROAM | a4 a4 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002760 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002780 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000027a0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000027c0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000027e0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002800 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002820 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002840 | �������������� | a4 a4 | 65535 | yes | no |

## Run 10: `0x00002940-0x00002a9f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002940 | FNC | 5b 5b | 00 00 | 0 | no |
| 0x00002960 | DR1 | 69 5b | 32 00 | 50 | no |
| 0x00002980 | DR3 | 6f 5b | 34 00 | 52 | no |
| 0x000029a0 | DR5 | 17 5b | 4c 00 | 76 | no |
| 0x000029c0 | GPS | 17 5b | 4c 00 | 76 | no |
| 0x000029e0 | OFF | 5b 5b | 00 00 | 0 | no |
| 0x00002a00 | HA | a4 a4 | ff ff | 65535 | no |
| 0x00002a20 | PA | 5b 5b | 00 00 | 0 | no |
| 0x00002a40 | S | 5b 5b | 00 00 | 0 | no |
| 0x00002a60 | ALL | 5b 5b | 00 00 | 0 | no |
| 0x00002a80 | TRS | a4 a4 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002aa0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002ac0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002ae0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002b00 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002b20 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002b40 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002b60 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00002b80 | �������������� | a4 a4 | 65535 | yes | no |

## Run 11: `0x00002d80-0x00002dbf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002d80 |  EXIT | 1e 03 | 45 58 | 22597 | no |
| 0x00002da0 |  BACK | 0f 14 | 54 4f | 20308 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002dc0 |       �������� | 0f 14 | 20308 | no | no |
| 0x00002de0 | A_RPLY�������� | 0f 1e | 17748 | no | no |
| 0x00002e00 | A_DIAL�������� | 04 0b | 20575 | no | no |
| 0x00002e20 |  AUX | 1c 13 | 18503 | no | yes |
| 0x00002e40 | B.CAST�������� | 17 17 | 19532 | no | no |
| 0x00002e60 | CALL2 | 17 17 | 19532 | no | yes |
| 0x00002e80 | CALL4 | 17 17 | 19532 | no | yes |
| 0x00002ea0 | CALL6 | 13 5b | 72 | no | yes |

## Run 12: `0x00002e60-0x00002ebf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002e60 | CALL2 | 17 17 | 4c 4c | 19532 | no |
| 0x00002e80 | CALL4 | 17 17 | 4c 4c | 19532 | no |
| 0x00002ea0 | CALL6 | 13 5b | 48 00 | 72 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002ec0 | CH_ENT�������� | 13 5b | 72 | no | no |
| 0x00002ee0 | CH_RCL�������� | 14 18 | 17231 | no | no |
| 0x00002f00 | CLK_AJ�������� | 04 16 | 19807 | no | no |
| 0x00002f20 |  DR1 | 09 69 | 12882 | no | yes |
| 0x00002f40 |  DR3 | 09 6f | 13394 | no | yes |
| 0x00002f60 |  DR5 | 12 08 | 21321 | no | yes |
| 0x00002f80 | FX_VOL�������� | 09 18 | 17234 | no | no |
| 0x00002fa0 |  FNC | 0b 08 | 21328 | no | yes |

## Run 13: `0x00002f20-0x00002f7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002f20 |  DR1 | 09 69 | 52 32 | 12882 | no |
| 0x00002f40 |  DR3 | 09 6f | 52 34 | 13394 | no |
| 0x00002f60 |  DR5 | 12 08 | 49 53 | 21321 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002f80 | FX_VOL�������� | 09 18 | 17234 | no | no |
| 0x00002fa0 |  FNC | 0b 08 | 21328 | no | yes |
| 0x00002fc0 | GROUP | 0b 70 | 11088 | no | yes |
| 0x00002fe0 |  HOME | 1f 18 | 17220 | no | yes |
| 0x00003000 | IND+ST�������� | 17 14 | 20300 | no | no |
| 0x00003020 |  LOW | 12 15 | 20041 | no | yes |
| 0x00003040 |  MENU | 14 15 | 20047 | no | yes |
| 0x00003060 |  MONI | 08 0f | 21587 | no | yes |

## Run 14: `0x00002fa0-0x00002fff`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002fa0 |  FNC | 0b 08 | 50 53 | 21328 | no |
| 0x00002fc0 | GROUP | 0b 70 | 50 2b | 11088 | no |
| 0x00002fe0 |  HOME | 1f 18 | 44 43 | 17220 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003000 | IND+ST�������� | 17 14 | 20300 | no | no |
| 0x00003020 |  LOW | 12 15 | 20041 | no | yes |
| 0x00003040 |  MENU | 14 15 | 20047 | no | yes |
| 0x00003060 |  MONI | 08 0f | 21587 | no | yes |
| 0x00003080 |  PLAY | 08 0b | 20563 | no | yes |
| 0x000030a0 |  SCAN | 74 1a | 16687 | no | yes |
| 0x000030c0 |  SCR | 17 18 | 17228 | no | yes |
| 0x000030e0 | SEL+ST�������� | 08 04 | 24403 | no | no |

## Run 15: `0x00003020-0x000030df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003020 |  LOW | 12 15 | 49 4e | 20041 | no |
| 0x00003040 |  MENU | 14 15 | 4f 4e | 20047 | no |
| 0x00003060 |  MONI | 08 0f | 53 54 | 21587 | no |
| 0x00003080 |  PLAY | 08 0b | 53 50 | 20563 | no |
| 0x000030a0 |  SCAN | 74 1a | 2f 41 | 16687 | no |
| 0x000030c0 |  SCR | 17 18 | 4c 43 | 17228 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000030e0 | SEL+ST�������� | 08 04 | 24403 | no | no |
| 0x00003100 | S_LOCK�������� | 0a 17 | 19537 | no | no |
| 0x00003120 | SQ_OFF�������� | 04 14 | 20319 | no | no |
| 0x00003140 | STACK | 1a 0f | 21569 | no | yes |
| 0x00003160 |   TA | 17 04 | 24396 | no | yes |
| 0x00003180 | PASSWD�������� | 12 19 | 16969 | no | no |
| 0x000031a0 |  MEMO | 14 03 | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 15 1e | 17742 | no | no |

## Run 16: `0x00003140-0x0000317f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003140 | STACK | 1a 0f | 41 54 | 21569 | no |
| 0x00003160 |   TA | 17 04 | 4c 5f | 24396 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003180 | PASSWD�������� | 12 19 | 16969 | no | no |
| 0x000031a0 |  MEMO | 14 03 | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 15 1e | 17742 | no | no |
| 0x000031e0 | ZONE | 0f 1e | 17748 | no | yes |
| 0x00003200 | SITE | 7b 0c | 22304 | no | yes |
| 0x00003220 | GRP+SD�������� | 1f 70 | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 1f 16 | 19780 | no | no |
| 0x00003260 | �������������� | 08 1e | 17747 | no | no |

## Run 17: `0x000031e0-0x0000321f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000031e0 | ZONE | 0f 1e | 54 45 | 17748 | no |
| 0x00003200 | SITE | 7b 0c | 20 57 | 22304 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003220 | GRP+SD�������� | 1f 70 | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 1f 16 | 19780 | no | no |
| 0x00003260 | �������������� | 08 1e | 17747 | no | no |
| 0x00003280 |  1x | 23 5b | 120 | no | yes |
| 0x000032a0 |  10x | 6b 23 | 30768 | no | yes |
| 0x000032c0 | RX_ENT�������� | a4 a4 | 65535 | no | no |
| 0x000032e0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00003300 | �������������� | a4 a4 | 65535 | yes | no |

## Run 18: `0x00003280-0x000032bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003280 |  1x | 23 5b | 78 00 | 120 | no |
| 0x000032a0 |  10x | 6b 23 | 30 78 | 30768 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000032c0 | RX_ENT�������� | a4 a4 | 65535 | no | no |
| 0x000032e0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00003300 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00003320 |  HIGH | a4 a4 | 65535 | no | yes |
| 0x00003340 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00003360 | ACT_DT�������� | 0f 04 | 24404 | no | no |
| 0x00003380 | �������������� | a4 a4 | 65535 | no | no |
| 0x000033a0 | CH_ENT�������� | a4 a4 | 65535 | no | no |

## Run 19: `0x000037a0-0x000037df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000037a0 | 00 | ab 2b | f0 70 | 28912 | no |
| 0x000037c0 | 0000000 | 6b 6b | 30 30 | 12336 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000037e0 | �p00000000000p | 5b ab | 61440 | no | no |
| 0x00003800 | 00��� | a4 a4 | 65535 | no | no |
| 0x00003820 |  | 64 24 | 32575 | no | no |
| 0x00003840 |  | 5b 5b | 0 | no | no |
| 0x00003860 |  | a2 a2 | 63993 | no | no |
| 0x00003880 |  | 5b 5a | 256 | no | no |
| 0x000038a0 |  | 5b 5b | 0 | no | no |
| 0x000038c0 |  | 5c 5c | 1799 | no | no |

## Run 20: `0x00010480-0x0001063f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00010480 | Curtis, AE4BT | f1 65 | aa 3e | 16042 | no |
| 0x000104a0 | Frank, KF4CLO | 78 5d | 23 06 | 1571 | no |
| 0x000104c0 | Ed, AK7AN | 19 6b | 42 30 | 12354 | no |
| 0x000104e0 | Kelli, KD0CVD | 1a 6b | 41 30 | 12353 | no |
| 0x00010500 | Chris, K4DKK | 94 74 | cf 2f | 12239 | no |
| 0x00010520 | DVNET | 54 7c | 0f 27 | 9999 | no |
| 0x00010540 | No NXDN ID | 20 22 | 7b 79 | 31099 | no |
| 0x00010560 | Bjorn, SA7AUX | e9 65 | b2 3e | 16050 | no |
| 0x00010580 | Doug, W4DBG | 4f 5f | 14 04 | 1044 | no |
| 0x000105a0 | Jamie, KQ1USA | d1 4d | 8a 16 | 5770 | no |
| 0x000105c0 | Randy, W8EJC | cf c0 | 94 9b | 39828 | no |
| 0x000105e0 | BitByBit Hams | 62 6b | 39 30 | 12345 | no |
| 0x00010600 | Tom, K4TH | c5 7e | 9e 25 | 9630 | no |
| 0x00010620 | NX4DX BitbyBit | ea 73 | b1 28 | 10417 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00010640 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00010660 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00010680 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000106a0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000106c0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000106e0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00010700 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00010720 | �������������� | a4 a4 | 65535 | yes | no |

## Run 21: `0x00014f80-0x0001519f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00014f80 | World Wide TG | b3 a6 | e8 fd | 65000 | no |
| 0x00014fa0 | Parrot | 51 5b | 0a 00 | 10 | no |
| 0x00014fc0 | Colo Fun Mach | 32 22 | 69 79 | 31081 | no |
| 0x00014fe0 | MO Digi Call | 90 27 | cb 7c | 31947 | no |
| 0x00015000 | AlabamaLink TG | 79 22 | 22 79 | 31010 | no |
| 0x00015020 | SW Missouri TG | 60 21 | 3b 7a | 31291 | no |
| 0x00015040 | PiStar TG | e3 20 | b8 7b | 31672 | no |
| 0x00015060 | VK Radio TG | 3c 9e | 67 c5 | 50535 | no |
| 0x00015080 | NXDN N America | 83 7c | d8 27 | 10200 | no |
| 0x000150a0 | Scotland TG | a4 00 | ff 5b | 23551 | no |
| 0x000150c0 | Utah DRN 01 | 58 20 | 03 7b | 31491 | no |
| 0x000150e0 | Utah DRN 05 | 5c 20 | 07 7b | 31495 | no |
| 0x00015100 | PA7LIM TG | 93 14 | c8 4f | 20424 | no |
| 0x00015120 | Disconnect TG | 54 7c | 0f 27 | 9999 | no |
| 0x00015140 | Utah DRN 00 | 59 20 | 02 7b | 31490 | no |
| 0x00015160 | Lookout Mtn TG | 26 f2 | 7d a9 | 43389 | no |
| 0x00015180 | AK7AN TG | 46 08 | 1d 53 | 21277 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000151a0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000151c0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x000151e0 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00015200 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00015220 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00015240 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00015260 | �������������� | a4 a4 | 65535 | yes | no |
| 0x00015280 | �������������� | a4 a4 | 65535 | yes | no |

## Cross-Map Comparison Summary

This map was compared with `research/dattest2/table_map.md`. The two files use different active decode keys (`0x5b` here, `0x34` in Dattest2), but the decoded names, decoded `+19/+20` values, record offsets, and run boundaries match for the candidate Individual ID and Talk Group runs.

| Candidate Table | Start | Occupied End | Occupied Records | First Empty Slot | Empty Slots After Run |
| --- | ---: | ---: | ---: | ---: | ---: |
| Individual ID | `0x00010480` | `0x0001063f` | 14 | `0x00010640` | 586 |
| Talk Group | `0x00014f80` | `0x0001519f` | 17 | `0x000151a0` | 334 |

Boundary interpretation:

- `0x10480-0x1063f` is the occupied candidate Individual ID run observed in both maps.
- `0x10640` is empty in both maps and is the add slot used by the Dattest2 Individual ID experiments.
- `0x14f80-0x1519f` is the occupied candidate Talk Group run observed in both maps.
- `0x151a0` is empty in both maps and is the add slot used by the Dattest2 Talk Group experiments.
- These offsets remain stable across the saves analyzed here after accounting for the file-level XOR key.
