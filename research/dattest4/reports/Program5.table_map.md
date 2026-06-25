# KPG111 Candidate Table Map

This is a read-only structural scan. Printable decoded names are evidence for candidate records, not proof of table purpose.

## File

- Path: `research/dattest4/Dattest4/Program5.dat`
- Size: 168257 bytes
- SHA-256: `dd6653642b6be56f6f7364d66c24c0d1357f7dd0e6098bd0f1c49e5fb090c15c`
- Payload start: `0x40`
- Record size: 32
- Decode XOR: `0x58`
- Records scanned: 5256
- Occupied candidates: 215
- Empty records: 3900

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
| 0x00014f80-0x0001533f | 30 | 321 | 0x00015340 empty=True name='��������������' |

## Run 1: `0x00000b40-0x00000b7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000b40 | ABCDEFGHIJKLMN | 0b 0c | 53 54 | 21587 | no |
| 0x00000b60 | 56789 | 58 58 | 00 00 | 0 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000b80 |  | 58 58 | 0 | no | no |
| 0x00000ba0 | 1 | 1b 6a | 12867 | no | yes |
| 0x00000bc0 | DEF3 | 11 6c | 13385 | no | yes |
| 0x00000be0 | JKL5 | 17 6e | 13903 | no | yes |
| 0x00000c00 | PQRS7 | 0e 60 | 14422 | no | yes |
| 0x00000c20 | WXYZ9 | a7 a7 | 65535 | no | yes |
| 0x00000c40 | CALL | 1b 19 | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 0c 11 | 18772 | no | no |

## Run 2: `0x00000ba0-0x00000c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000ba0 | 1 | 1b 6a | 43 32 | 12867 | no |
| 0x00000bc0 | DEF3 | 11 6c | 49 34 | 13385 | no |
| 0x00000be0 | JKL5 | 17 6e | 4f 36 | 13903 | no |
| 0x00000c00 | PQRS7 | 0e 60 | 56 38 | 14422 | no |
| 0x00000c20 | WXYZ9 | a7 a7 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000c40 | CALL | 1b 19 | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 0c 11 | 18772 | no | no |
| 0x00000c80 | Microphone | 2d 3c | 25717 | no | no |
| 0x00000ca0 |  | 0c 78 | 8276 | no | no |
| 0x00000cc0 | 0+CDNM4����� | a7 a7 | 65535 | no | no |
| 0x00000ce0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00000d00 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00000d20 | �������������� | a7 a7 | 65535 | yes | no |

## Run 3: `0x00001540-0x0000177f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001540 | 2-TONE | 0c 17 | 54 4f | 20308 | no |
| 0x00001560 | AUTO TELEPHONE | 78 19 | 20 41 | 16672 | no |
| 0x00001580 | AUTO DIAL | 0c 17 | 54 4f | 20308 | no |
| 0x000015a0 |     BLANK | 78 78 | 20 20 | 8224 | no |
| 0x000015c0 |     CODE? | 78 78 | 20 20 | 8224 | no |
| 0x000015e0 |  OVER WRITE? | 78 1c | 20 44 | 17440 | no |
| 0x00001600 | AUX | 00 78 | 58 20 | 8280 | no |
| 0x00001620 | AUX B | 17 19 | 4f 41 | 16719 | no |
| 0x00001640 | CHANNEL ENTRY | 78 16 | 20 4e | 20000 | no |
| 0x00001660 | PRIORITY 3 | 17 1b | 4f 43 | 17231 | no |
| 0x00001680 | CLOCK ADJUST | 19 0a | 41 52 | 21057 | no |
| 0x000016a0 | MONTH | 01 58 | 59 00 | 89 | no |
| 0x000016c0 | HOUR | 16 0d | 4e 55 | 21838 | no |
| 0x000016e0 | DIRECT CH1 SEL | 0a 1d | 52 45 | 17746 | no |
| 0x00001700 | DIRECT CH3 SEL | 0a 1d | 52 45 | 17746 | no |
| 0x00001720 | DIRECT CH5 SEL | 0b 08 | 53 50 | 20563 | no |
| 0x00001740 | FIXED VOLUME | 0a 1b | 52 43 | 17234 | no |
| 0x00001760 | SITE No. | 0c 1d | 54 45 | 17748 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001780 | �   SEARCH   � | 0b 78 | 8275 | no | no |
| 0x000017a0 | N | 58 58 | 0 | no | yes |
| 0x000017c0 | E | 58 58 | 0 | no | yes |
| 0x000017e0 | ALT | 78 78 | 8224 | no | yes |
| 0x00001800 |             ft | 17 0d | 21839 | no | yes |
| 0x00001820 | GROUP+STATUS | 15 1d | 17741 | no | yes |
| 0x00001840 | HORN ALERT | 1c 11 | 18756 | no | yes |
| 0x00001860 | INDIV+STATUS | 78 78 | 8224 | no | yes |

## Run 4: `0x000017a0-0x00001c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000017a0 | N | 58 58 | 00 00 | 0 | no |
| 0x000017c0 | E | 58 58 | 00 00 | 0 | no |
| 0x000017e0 | ALT | 78 78 | 20 20 | 8224 | no |
| 0x00001800 |             ft | 17 0d | 4f 55 | 21839 | no |
| 0x00001820 | GROUP+STATUS | 15 1d | 4d 45 | 17741 | no |
| 0x00001840 | HORN ALERT | 1c 11 | 44 49 | 18756 | no |
| 0x00001860 | INDIV+STATUS | 78 78 | 20 20 | 8224 | no |
| 0x00001880 | LCD BRIGHTNESS | 0f 78 | 57 20 | 8279 | no |
| 0x000018a0 | MENU | 16 11 | 4e 49 | 18766 | no |
| 0x000018c0 | OST | 0c 78 | 54 20 | 8276 | no |
| 0x000018e0 |    TONE OFF | 19 01 | 41 59 | 22849 | no |
| 0x00001900 | PRI CH SEL | 78 78 | 20 20 | 8224 | no |
| 0x00001920 |     PRIORITY 1 | 78 78 | 20 20 | 8224 | no |
| 0x00001940 |   PRIORITY 1&2 | 1a 14 | 42 4c | 19522 | no |
| 0x00001960 | SCAN | 19 16 | 41 4e | 20033 | no |
| 0x00001980 |         DELETE | 78 78 | 20 20 | 8224 | no |
| 0x000019a0 |      SCAN | 19 16 | 41 4e | 20033 | no |
| 0x000019c0 | SCRAM/ENCRYP | 0a 19 | 52 41 | 16722 | no |
| 0x000019e0 | CODE | 14 1b | 4c 43 | 17228 | no |
| 0x00001a00 | SELCALL+STATUS | 16 1c | 4e 44 | 17486 | no |
| 0x00001a20 | SITE LOCK | 0c 1d | 54 45 | 17748 | no |
| 0x00001a40 | SQUELCH LEVEL | 0e 1d | 56 45 | 17750 | no |
| 0x00001a60 | SQUELCH OFF | 19 1b | 41 43 | 17217 | no |
| 0x00001a80 | STATUS | 14 13 | 4c 4b | 19276 | no |
| 0x00001aa0 | PASSWORD | 78 08 | 20 50 | 20512 | no |
| 0x00001ac0 | VIBRATOR | 11 1b | 49 43 | 17225 | no |
| 0x00001ae0 | VOX | 00 78 | 58 20 | 8280 | no |
| 0x00001b00 | ZONE DEL/ADD | 78 78 | 20 20 | 8224 | no |
| 0x00001b20 |            OFF | 78 78 | 20 20 | 8224 | no |
| 0x00001b40 |            LOW | 0b 0c | 53 54 | 21587 | no |
| 0x00001b60 |      BUSY | 78 78 | 20 20 | 8224 | no |
| 0x00001b80 |      STUN | 14 14 | 4c 4c | 19532 | no |
| 0x00001ba0 | NEW MESSAGE | 1d 15 | 45 4d | 19781 | no |
| 0x00001bc0 |    MAN DOWN | 10 17 | 48 4f | 20296 | no |
| 0x00001be0 | ID | 19 0c | 41 54 | 21569 | no |
| 0x00001c00 | GID | 1c 58 | 44 00 | 68 | no |
| 0x00001c20 | STATUS | 11 17 | 49 4f | 20297 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001c40 | �RECEIVE DATA� | 0b 1d | 17747 | no | no |
| 0x00001c60 | �    BUSY    � | 78 1b | 17184 | no | no |
| 0x00001c80 | �  NO REPLY  � | 78 78 | 8224 | no | no |
| 0x00001ca0 | � GPS UPLOAD � | 0d 0c | 21589 | no | no |
| 0x00001cc0 | �   EMPTY    � | 78 78 | 8224 | no | no |
| 0x00001ce0 | �SYSTEM BUSY � | 78 78 | 8224 | no | no |
| 0x00001d00 | �  INVALID   � | 1d 1b | 17221 | no | no |
| 0x00001d20 | REMOTE CONTROL | 14 0d | 21836 | no | yes |

## Run 5: `0x00001d20-0x00001f1f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001d20 | REMOTE CONTROL | 14 0d | 4c 55 | 21836 | no |
| 0x00001d40 | AM | 58 58 | 00 00 | 0 | no |
| 0x00001d60 | A | 58 58 | 00 00 | 0 | no |
| 0x00001d80 |              s | 78 0f | 20 57 | 22304 | no |
| 0x00001da0 |   VGS ERROR | 1d 15 | 45 4d | 19781 | no |
| 0x00001dc0 |    GREETING | 0f 78 | 57 20 | 8279 | no |
| 0x00001de0 | END OF MESSAGE | 58 58 | 00 00 | 0 | no |
| 0x00001e00 | VM | 58 58 | 00 00 | 0 | no |
| 0x00001e20 | PRIORITY 4 | 78 1e | 20 46 | 17952 | no |
| 0x00001e40 |   GRP ADD-D | 1f 0a | 47 52 | 21063 | no |
| 0x00001e60 |            dBm | 11 17 | 49 4f | 20297 | no |
| 0x00001e80 |        CH NAME | 78 02 | 20 5a | 23072 | no |
| 0x00001ea0 | MAINTENANCE | 19 1b | 41 43 | 17217 | no |
| 0x00001ec0 |    MESSAGE? | 17 0d | 4f 55 | 21839 | no |
| 0x00001ee0 | INDIV+SDM | 14 1b | 4c 43 | 17228 | no |
| 0x00001f00 | SHORT MESSAGE | 78 0a | 20 52 | 21024 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001f20 | � REMOTE TX  � | 78 1b | 17184 | no | no |
| 0x00001f40 | LONE WORKER | 78 78 | 8224 | no | yes |
| 0x00001f60 |  SITE ROAMING | 0c 1d | 17748 | no | yes |
| 0x00001f80 | ID | 19 0c | 21569 | no | yes |
| 0x00001fa0 | MY ID | 1b 1d | 17731 | no | yes |
| 0x00001fc0 | FREE DIAL | 14 14 | 19532 | no | yes |
| 0x00001fe0 | TRANSFER | 1d 0c | 21573 | no | yes |
| 0x00002000 | ID | 78 17 | 20256 | no | yes |

## Run 6: `0x00001f40-0x0000215f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001f40 | LONE WORKER | 78 78 | 20 20 | 8224 | no |
| 0x00001f60 |  SITE ROAMING | 0c 1d | 54 45 | 17748 | no |
| 0x00001f80 | ID | 19 0c | 41 54 | 21569 | no |
| 0x00001fa0 | MY ID | 1b 1d | 43 45 | 17731 | no |
| 0x00001fc0 | FREE DIAL | 14 14 | 4c 4c | 19532 | no |
| 0x00001fe0 | TRANSFER | 1d 0c | 45 54 | 21573 | no |
| 0x00002000 | ID | 78 17 | 20 4f | 20256 | no |
| 0x00002020 |     UPDATE | 78 0d | 20 55 | 21792 | no |
| 0x00002040 |   PHONE CALL | 78 78 | 20 20 | 8224 | no |
| 0x00002060 |           FLAT | 78 78 | 20 20 | 8224 | no |
| 0x00002080 |           NONE | 15 11 | 4d 49 | 18765 | no |
| 0x000020a0 |   MICROPHONE 2 | 15 11 | 4d 49 | 18765 | no |
| 0x000020c0 |   MICROPHONE 4 | 15 11 | 4d 49 | 18765 | no |
| 0x000020e0 | RX AUDIO EQ | 78 19 | 20 41 | 16672 | no |
| 0x00002100 | RX AGC | 78 19 | 20 41 | 16672 | no |
| 0x00002120 | EXT MIC TYPE | 78 14 | 20 4c | 19488 | no |
| 0x00002140 | TX NOISE SUPPR | a7 a7 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002160 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002180 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000021a0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000021c0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000021e0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002200 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002220 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002240 | �������������� | a7 a7 | 65535 | yes | no |

## Run 7: `0x000024c0-0x0000257f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000024c0 |   KEY ERASED   | 78 13 | 20 4b | 19232 | no |
| 0x000024e0 |    KEYLOAD     | 78 78 | 20 20 | 8224 | no |
| 0x00002500 | SELFTEST ERROR | 15 78 | 4d 20 | 8269 | no |
| 0x00002520 | GROUP ID | 17 0d | 4f 55 | 21839 | no |
| 0x00002540 | ACTIVITY DET | 1f 78 | 47 20 | 8263 | no |
| 0x00002560 | EMG STATIONARY | 1d 15 | 45 4d | 19781 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002580 | �������������� | a7 a7 | 65535 | no | no |
| 0x000025a0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000025c0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000025e0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002600 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002620 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002640 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002660 | �������������� | a7 a7 | 65535 | yes | no |

## Run 8: `0x00002680-0x000026bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002680 |   HIGH POWER | 14 17 | 4c 4f | 20300 | no |
| 0x000026a0 |   AUTO POWER | a7 a7 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000026c0 | �������������� | 78 1c | 17440 | no | no |
| 0x000026e0 | No. | 01 0b | 21337 | no | yes |
| 0x00002700 | GPS REPORT ERR | 01 0b | 21337 | no | yes |
| 0x00002720 | SYSTEM         | 0b 0c | 21587 | no | yes |
| 0x00002740 |   ROAM | a7 a7 | 65535 | no | yes |
| 0x00002760 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002780 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000027a0 | �������������� | a7 a7 | 65535 | yes | no |

## Run 9: `0x000026e0-0x0000275f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000026e0 | No. | 01 0b | 59 53 | 21337 | no |
| 0x00002700 | GPS REPORT ERR | 01 0b | 59 53 | 21337 | no |
| 0x00002720 | SYSTEM         | 0b 0c | 53 54 | 21587 | no |
| 0x00002740 |   ROAM | a7 a7 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002760 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002780 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000027a0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000027c0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000027e0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002800 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002820 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002840 | �������������� | a7 a7 | 65535 | yes | no |

## Run 10: `0x00002940-0x00002a9f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002940 | FNC | 58 58 | 00 00 | 0 | no |
| 0x00002960 | DR1 | 6a 58 | 32 00 | 50 | no |
| 0x00002980 | DR3 | 6c 58 | 34 00 | 52 | no |
| 0x000029a0 | DR5 | 14 58 | 4c 00 | 76 | no |
| 0x000029c0 | GPS | 14 58 | 4c 00 | 76 | no |
| 0x000029e0 | OFF | 58 58 | 00 00 | 0 | no |
| 0x00002a00 | HA | a7 a7 | ff ff | 65535 | no |
| 0x00002a20 | PA | 58 58 | 00 00 | 0 | no |
| 0x00002a40 | S | 58 58 | 00 00 | 0 | no |
| 0x00002a60 | ALL | 58 58 | 00 00 | 0 | no |
| 0x00002a80 | TRS | a7 a7 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002aa0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002ac0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002ae0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002b00 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002b20 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002b40 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002b60 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00002b80 | �������������� | a7 a7 | 65535 | yes | no |

## Run 11: `0x00002d80-0x00002dbf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002d80 |  EXIT | 1d 00 | 45 58 | 22597 | no |
| 0x00002da0 |  BACK | 0c 17 | 54 4f | 20308 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002dc0 |       �������� | 0c 17 | 20308 | no | no |
| 0x00002de0 | A_RPLY�������� | 0c 1d | 17748 | no | no |
| 0x00002e00 | A_DIAL�������� | 07 08 | 20575 | no | no |
| 0x00002e20 |  AUX | 1f 10 | 18503 | no | yes |
| 0x00002e40 | B.CAST�������� | 14 14 | 19532 | no | no |
| 0x00002e60 | CALL2 | 14 14 | 19532 | no | yes |
| 0x00002e80 | CALL4 | 14 14 | 19532 | no | yes |
| 0x00002ea0 | CALL6 | 10 58 | 72 | no | yes |

## Run 12: `0x00002e60-0x00002ebf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002e60 | CALL2 | 14 14 | 4c 4c | 19532 | no |
| 0x00002e80 | CALL4 | 14 14 | 4c 4c | 19532 | no |
| 0x00002ea0 | CALL6 | 10 58 | 48 00 | 72 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002ec0 | CH_ENT�������� | 10 58 | 72 | no | no |
| 0x00002ee0 | CH_RCL�������� | 17 1b | 17231 | no | no |
| 0x00002f00 | CLK_AJ�������� | 07 15 | 19807 | no | no |
| 0x00002f20 |  DR1 | 0a 6a | 12882 | no | yes |
| 0x00002f40 |  DR3 | 0a 6c | 13394 | no | yes |
| 0x00002f60 |  DR5 | 11 0b | 21321 | no | yes |
| 0x00002f80 | FX_VOL�������� | 0a 1b | 17234 | no | no |
| 0x00002fa0 |  FNC | 08 0b | 21328 | no | yes |

## Run 13: `0x00002f20-0x00002f7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002f20 |  DR1 | 0a 6a | 52 32 | 12882 | no |
| 0x00002f40 |  DR3 | 0a 6c | 52 34 | 13394 | no |
| 0x00002f60 |  DR5 | 11 0b | 49 53 | 21321 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002f80 | FX_VOL�������� | 0a 1b | 17234 | no | no |
| 0x00002fa0 |  FNC | 08 0b | 21328 | no | yes |
| 0x00002fc0 | GROUP | 08 73 | 11088 | no | yes |
| 0x00002fe0 |  HOME | 1c 1b | 17220 | no | yes |
| 0x00003000 | IND+ST�������� | 14 17 | 20300 | no | no |
| 0x00003020 |  LOW | 11 16 | 20041 | no | yes |
| 0x00003040 |  MENU | 17 16 | 20047 | no | yes |
| 0x00003060 |  MONI | 0b 0c | 21587 | no | yes |

## Run 14: `0x00002fa0-0x00002fff`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002fa0 |  FNC | 08 0b | 50 53 | 21328 | no |
| 0x00002fc0 | GROUP | 08 73 | 50 2b | 11088 | no |
| 0x00002fe0 |  HOME | 1c 1b | 44 43 | 17220 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003000 | IND+ST�������� | 14 17 | 20300 | no | no |
| 0x00003020 |  LOW | 11 16 | 20041 | no | yes |
| 0x00003040 |  MENU | 17 16 | 20047 | no | yes |
| 0x00003060 |  MONI | 0b 0c | 21587 | no | yes |
| 0x00003080 |  PLAY | 0b 08 | 20563 | no | yes |
| 0x000030a0 |  SCAN | 77 19 | 16687 | no | yes |
| 0x000030c0 |  SCR | 14 1b | 17228 | no | yes |
| 0x000030e0 | SEL+ST�������� | 0b 07 | 24403 | no | no |

## Run 15: `0x00003020-0x000030df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003020 |  LOW | 11 16 | 49 4e | 20041 | no |
| 0x00003040 |  MENU | 17 16 | 4f 4e | 20047 | no |
| 0x00003060 |  MONI | 0b 0c | 53 54 | 21587 | no |
| 0x00003080 |  PLAY | 0b 08 | 53 50 | 20563 | no |
| 0x000030a0 |  SCAN | 77 19 | 2f 41 | 16687 | no |
| 0x000030c0 |  SCR | 14 1b | 4c 43 | 17228 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000030e0 | SEL+ST�������� | 0b 07 | 24403 | no | no |
| 0x00003100 | S_LOCK�������� | 09 14 | 19537 | no | no |
| 0x00003120 | SQ_OFF�������� | 07 17 | 20319 | no | no |
| 0x00003140 | STACK | 19 0c | 21569 | no | yes |
| 0x00003160 |   TA | 14 07 | 24396 | no | yes |
| 0x00003180 | PASSWD�������� | 11 1a | 16969 | no | no |
| 0x000031a0 |  MEMO | 17 00 | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 16 1d | 17742 | no | no |

## Run 16: `0x00003140-0x0000317f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003140 | STACK | 19 0c | 41 54 | 21569 | no |
| 0x00003160 |   TA | 14 07 | 4c 5f | 24396 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003180 | PASSWD�������� | 11 1a | 16969 | no | no |
| 0x000031a0 |  MEMO | 17 00 | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 16 1d | 17742 | no | no |
| 0x000031e0 | ZONE | 0c 1d | 17748 | no | yes |
| 0x00003200 | SITE | 78 0f | 22304 | no | yes |
| 0x00003220 | GRP+SD�������� | 1c 73 | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 1c 15 | 19780 | no | no |
| 0x00003260 | �������������� | 0b 1d | 17747 | no | no |

## Run 17: `0x000031e0-0x0000321f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000031e0 | ZONE | 0c 1d | 54 45 | 17748 | no |
| 0x00003200 | SITE | 78 0f | 20 57 | 22304 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003220 | GRP+SD�������� | 1c 73 | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 1c 15 | 19780 | no | no |
| 0x00003260 | �������������� | 0b 1d | 17747 | no | no |
| 0x00003280 |  1x | 20 58 | 120 | no | yes |
| 0x000032a0 |  10x | 68 20 | 30768 | no | yes |
| 0x000032c0 | RX_ENT�������� | a7 a7 | 65535 | no | no |
| 0x000032e0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00003300 | �������������� | a7 a7 | 65535 | yes | no |

## Run 18: `0x00003280-0x000032bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003280 |  1x | 20 58 | 78 00 | 120 | no |
| 0x000032a0 |  10x | 68 20 | 30 78 | 30768 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000032c0 | RX_ENT�������� | a7 a7 | 65535 | no | no |
| 0x000032e0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00003300 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00003320 |  HIGH | a7 a7 | 65535 | no | yes |
| 0x00003340 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00003360 | ACT_DT�������� | 0c 07 | 24404 | no | no |
| 0x00003380 | �������������� | a7 a7 | 65535 | no | no |
| 0x000033a0 | CH_ENT�������� | a7 a7 | 65535 | no | no |

## Run 19: `0x000037a0-0x000037df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000037a0 | 00 | a8 28 | f0 70 | 28912 | no |
| 0x000037c0 | 0000000 | 68 68 | 30 30 | 12336 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000037e0 | �p00000000000p | 58 a8 | 61440 | no | no |
| 0x00003800 | 00��� | a7 a7 | 65535 | no | no |
| 0x00003820 |  | 67 27 | 32575 | no | no |
| 0x00003840 |  | 58 58 | 0 | no | no |
| 0x00003860 |  | a1 a1 | 63993 | no | no |
| 0x00003880 |  | 58 59 | 256 | no | no |
| 0x000038a0 |  | 58 58 | 0 | no | no |
| 0x000038c0 |  | 5f 5f | 1799 | no | no |

## Run 20: `0x00010480-0x0001085f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00010480 | Curtis, AE4BT | f2 66 | aa 3e | 16042 | no |
| 0x000104a0 | Frank, KF4CLO | 7b 5e | 23 06 | 1571 | no |
| 0x000104c0 | Ed, AK7AN | 1a 68 | 42 30 | 12354 | no |
| 0x000104e0 | Kelli, KD0CVD | 19 68 | 41 30 | 12353 | no |
| 0x00010500 | Chris, K4DKK | 97 77 | cf 2f | 12239 | no |
| 0x00010520 | DVNET | 57 7f | 0f 27 | 9999 | no |
| 0x00010540 | No NXDN ID | 23 21 | 7b 79 | 31099 | no |
| 0x00010560 | Bjorn, SA7AUX | ea 66 | b2 3e | 16050 | no |
| 0x00010580 | Doug, W4DBG | 4c 5c | 14 04 | 1044 | no |
| 0x000105a0 | Hello | 3e 04 | 66 5c | 23654 | no |
| 0x000105c0 | Randy, W8EJC | cc c3 | 94 9b | 39828 | no |
| 0x000105e0 | BitByBit Hams | 61 68 | 39 30 | 12345 | no |
| 0x00010600 | Tom, K4TH | c6 7d | 9e 25 | 9630 | no |
| 0x00010620 | NX4DX BitbyBit | e9 70 | b1 28 | 10417 | no |
| 0x00010640 | Long Gone | b6 a7 | ee ff | 65518 | no |
| 0x00010660 | My Best Friend | 36 ea | 6e b2 | 45678 | no |
| 0x00010680 | Don't like | 3e 04 | 66 5c | 23654 | no |
| 0x000106a0 |  UNIT ID 0018 | ad 6f | f5 37 | 14325 | no |
| 0x000106c0 |  UNIT ID 0019 | e5 af | bd f7 | 63421 | no |
| 0x000106e0 |  UNIT ID 0020 | c3 03 | 9b 5b | 23451 | no |
| 0x00010700 |  UNIT ID 0021 | c2 25 | 9a 7d | 32154 | no |
| 0x00010720 |  UNIT ID 0022 | 49 f9 | 11 a1 | 41233 | no |
| 0x00010740 |  UNIT ID 0023 | ff 9f | a7 c7 | 51111 | no |
| 0x00010760 |  UNIT ID 0024 | 43 b7 | 1b ef | 61211 | no |
| 0x00010780 |  UNIT ID 0025 | c4 f5 | 9c ad | 44444 | no |
| 0x000107a0 |  UNIT ID 0026 | 5b 81 | 03 d9 | 55555 | no |
| 0x000107c0 |  UNIT ID 0027 | 6d da | 35 82 | 33333 | no |
| 0x000107e0 |  UNIT ID 0028 | 96 0e | ce 56 | 22222 | no |
| 0x00010800 |  UNIT ID 0029 | 3f 73 | 67 2b | 11111 | no |
| 0x00010820 |  UNIT ID 0030 | 11 8c | 49 d4 | 54345 | no |
| 0x00010840 |  UNIT ID 0031 | 59 f2 | 01 aa | 43521 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00010860 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00010880 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000108a0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000108c0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000108e0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00010900 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00010920 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00010940 | �������������� | a7 a7 | 65535 | yes | no |

## Run 21: `0x00014f80-0x0001533f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00014f80 | World Wide TG | b0 a5 | e8 fd | 65000 | no |
| 0x00014fa0 | Parrot | 52 58 | 0a 00 | 10 | no |
| 0x00014fc0 | Colo Fun Mach | 31 21 | 69 79 | 31081 | no |
| 0x00014fe0 | MO Digi Call | 93 24 | cb 7c | 31947 | no |
| 0x00015000 | AlabamaLink TG | 7a 21 | 22 79 | 31010 | no |
| 0x00015020 | SW Missouri TG | 63 22 | 3b 7a | 31291 | no |
| 0x00015040 | PiStar TG | e0 23 | b8 7b | 31672 | no |
| 0x00015060 | VK Radio TG | 3f 9d | 67 c5 | 50535 | no |
| 0x00015080 | NXDN N America | 80 7f | d8 27 | 10200 | no |
| 0x000150a0 | Goodbye | 68 18 | 30 40 | 16432 | no |
| 0x000150c0 | Utah DRN 01 | 5b 23 | 03 7b | 31491 | no |
| 0x000150e0 | Utah DRN 05 | 5f 23 | 07 7b | 31495 | no |
| 0x00015100 | PA7LIM TG | 90 17 | c8 4f | 20424 | no |
| 0x00015120 | Disconnect TG | 57 7f | 0f 27 | 9999 | no |
| 0x00015140 | Hot n Sexy | 5b 23 | 03 7b | 31491 | no |
| 0x00015160 | Lookout Mtn TG | 25 f1 | 7d a9 | 43389 | no |
| 0x00015180 | AK7AN TG | 45 0b | 1d 53 | 21277 | no |
| 0x000151a0 | GROUP ID 0018 | 3f 73 | 67 2b | 11111 | no |
| 0x000151c0 | GROUP ID 0019 | 96 0e | ce 56 | 22222 | no |
| 0x000151e0 | GROUP ID 0020 | 6d da | 35 82 | 33333 | no |
| 0x00015200 | GROUP ID 0021 | c4 f5 | 9c ad | 44444 | no |
| 0x00015220 | GROUP ID 0022 | 5b 81 | 03 d9 | 55555 | no |
| 0x00015240 | GROUP ID 0023 | 5c 81 | 04 d9 | 55556 | no |
| 0x00015260 | BY BY | c5 f5 | 9d ad | 44445 | no |
| 0x00015280 | GROUP ID 0025 | 6f da | 37 82 | 33335 | no |
| 0x000152a0 | GROUP ID 0026 | 97 0e | cf 56 | 22223 | no |
| 0x000152c0 | GROUP ID 0027 | b9 80 | e1 d8 | 55521 | no |
| 0x000152e0 | GROUP ID 0028 | ba 73 | e2 2b | 11234 | no |
| 0x00015300 | GROUP ID 0029 | 00 74 | 58 2c | 11352 | no |
| 0x00015320 | GROUP ID 0030 | fd a3 | a5 fb | 64421 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00015340 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00015360 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00015380 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000153a0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000153c0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x000153e0 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00015400 | �������������� | a7 a7 | 65535 | yes | no |
| 0x00015420 | �������������� | a7 a7 | 65535 | yes | no |

