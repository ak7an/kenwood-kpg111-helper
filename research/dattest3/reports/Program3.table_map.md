# KPG111 Candidate Table Map

This is a read-only structural scan. Printable decoded names are evidence for candidate records, not proof of table purpose.

## File

- Path: `research/dattest3/Dattest3/Program3.dat`
- Size: 168257 bytes
- SHA-256: `370e94b05d195f8eb1e3afc9c1d86159f560f217eb5aae3c6193fc8a4501528f`
- Payload start: `0x40`
- Record size: 32
- Decode XOR: `0x1e`
- Records scanned: 5256
- Occupied candidates: 212
- Empty records: 3903

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
| 0x00010480-0x0001059f | 9 | 1 | 0x000105a0 empty=True name='��������������' |
| 0x000105c0-0x0001083f | 20 | 570 | 0x00010840 empty=True name='��������������' |
| 0x00014f80-0x0001509f | 9 | 1 | 0x000150a0 empty=True name='��������������' |
| 0x000150c0-0x0001533f | 20 | 321 | 0x00015340 empty=True name='��������������' |

## Run 1: `0x00000b40-0x00000b7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000b40 | ABCDEFGHIJKLMN | 4d 4a | 53 54 | 21587 | no |
| 0x00000b60 | 56789 | 1e 1e | 00 00 | 0 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000b80 |  | 1e 1e | 0 | no | no |
| 0x00000ba0 | 1 | 5d 2c | 12867 | no | yes |
| 0x00000bc0 | DEF3 | 57 2a | 13385 | no | yes |
| 0x00000be0 | JKL5 | 51 28 | 13903 | no | yes |
| 0x00000c00 | PQRS7 | 48 26 | 14422 | no | yes |
| 0x00000c20 | WXYZ9 | e1 e1 | 65535 | no | yes |
| 0x00000c40 | CALL | 5d 5f | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 4a 57 | 18772 | no | no |

## Run 2: `0x00000ba0-0x00000c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000ba0 | 1 | 5d 2c | 43 32 | 12867 | no |
| 0x00000bc0 | DEF3 | 57 2a | 49 34 | 13385 | no |
| 0x00000be0 | JKL5 | 51 28 | 4f 36 | 13903 | no |
| 0x00000c00 | PQRS7 | 48 26 | 56 38 | 14422 | no |
| 0x00000c20 | WXYZ9 | e1 e1 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000c40 | CALL | 5d 5f | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 4a 57 | 18772 | no | no |
| 0x00000c80 | Microphone | 6b 7a | 25717 | no | no |
| 0x00000ca0 |  | 4a 3e | 8276 | no | no |
| 0x00000cc0 | 0+CDNM4����� | e1 e1 | 65535 | no | no |
| 0x00000ce0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00000d00 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00000d20 | �������������� | e1 e1 | 65535 | yes | no |

## Run 3: `0x00001540-0x0000177f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001540 | 2-TONE | 4a 51 | 54 4f | 20308 | no |
| 0x00001560 | AUTO TELEPHONE | 3e 5f | 20 41 | 16672 | no |
| 0x00001580 | AUTO DIAL | 4a 51 | 54 4f | 20308 | no |
| 0x000015a0 |     BLANK | 3e 3e | 20 20 | 8224 | no |
| 0x000015c0 |     CODE? | 3e 3e | 20 20 | 8224 | no |
| 0x000015e0 |  OVER WRITE? | 3e 5a | 20 44 | 17440 | no |
| 0x00001600 | AUX | 46 3e | 58 20 | 8280 | no |
| 0x00001620 | AUX B | 51 5f | 4f 41 | 16719 | no |
| 0x00001640 | CHANNEL ENTRY | 3e 50 | 20 4e | 20000 | no |
| 0x00001660 | PRIORITY 3 | 51 5d | 4f 43 | 17231 | no |
| 0x00001680 | CLOCK ADJUST | 5f 4c | 41 52 | 21057 | no |
| 0x000016a0 | MONTH | 47 1e | 59 00 | 89 | no |
| 0x000016c0 | HOUR | 50 4b | 4e 55 | 21838 | no |
| 0x000016e0 | DIRECT CH1 SEL | 4c 5b | 52 45 | 17746 | no |
| 0x00001700 | DIRECT CH3 SEL | 4c 5b | 52 45 | 17746 | no |
| 0x00001720 | DIRECT CH5 SEL | 4d 4e | 53 50 | 20563 | no |
| 0x00001740 | FIXED VOLUME | 4c 5d | 52 43 | 17234 | no |
| 0x00001760 | SITE No. | 4a 5b | 54 45 | 17748 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001780 | �   SEARCH   � | 4d 3e | 8275 | no | no |
| 0x000017a0 | N | 1e 1e | 0 | no | yes |
| 0x000017c0 | E | 1e 1e | 0 | no | yes |
| 0x000017e0 | ALT | 3e 3e | 8224 | no | yes |
| 0x00001800 |             ft | 51 4b | 21839 | no | yes |
| 0x00001820 | GROUP+STATUS | 53 5b | 17741 | no | yes |
| 0x00001840 | HORN ALERT | 5a 57 | 18756 | no | yes |
| 0x00001860 | INDIV+STATUS | 3e 3e | 8224 | no | yes |

## Run 4: `0x000017a0-0x00001c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000017a0 | N | 1e 1e | 00 00 | 0 | no |
| 0x000017c0 | E | 1e 1e | 00 00 | 0 | no |
| 0x000017e0 | ALT | 3e 3e | 20 20 | 8224 | no |
| 0x00001800 |             ft | 51 4b | 4f 55 | 21839 | no |
| 0x00001820 | GROUP+STATUS | 53 5b | 4d 45 | 17741 | no |
| 0x00001840 | HORN ALERT | 5a 57 | 44 49 | 18756 | no |
| 0x00001860 | INDIV+STATUS | 3e 3e | 20 20 | 8224 | no |
| 0x00001880 | LCD BRIGHTNESS | 49 3e | 57 20 | 8279 | no |
| 0x000018a0 | MENU | 50 57 | 4e 49 | 18766 | no |
| 0x000018c0 | OST | 4a 3e | 54 20 | 8276 | no |
| 0x000018e0 |    TONE OFF | 5f 47 | 41 59 | 22849 | no |
| 0x00001900 | PRI CH SEL | 3e 3e | 20 20 | 8224 | no |
| 0x00001920 |     PRIORITY 1 | 3e 3e | 20 20 | 8224 | no |
| 0x00001940 |   PRIORITY 1&2 | 5c 52 | 42 4c | 19522 | no |
| 0x00001960 | SCAN | 5f 50 | 41 4e | 20033 | no |
| 0x00001980 |         DELETE | 3e 3e | 20 20 | 8224 | no |
| 0x000019a0 |      SCAN | 5f 50 | 41 4e | 20033 | no |
| 0x000019c0 | SCRAM/ENCRYP | 4c 5f | 52 41 | 16722 | no |
| 0x000019e0 | CODE | 52 5d | 4c 43 | 17228 | no |
| 0x00001a00 | SELCALL+STATUS | 50 5a | 4e 44 | 17486 | no |
| 0x00001a20 | SITE LOCK | 4a 5b | 54 45 | 17748 | no |
| 0x00001a40 | SQUELCH LEVEL | 48 5b | 56 45 | 17750 | no |
| 0x00001a60 | SQUELCH OFF | 5f 5d | 41 43 | 17217 | no |
| 0x00001a80 | STATUS | 52 55 | 4c 4b | 19276 | no |
| 0x00001aa0 | PASSWORD | 3e 4e | 20 50 | 20512 | no |
| 0x00001ac0 | VIBRATOR | 57 5d | 49 43 | 17225 | no |
| 0x00001ae0 | VOX | 46 3e | 58 20 | 8280 | no |
| 0x00001b00 | ZONE DEL/ADD | 3e 3e | 20 20 | 8224 | no |
| 0x00001b20 |            OFF | 3e 3e | 20 20 | 8224 | no |
| 0x00001b40 |            LOW | 4d 4a | 53 54 | 21587 | no |
| 0x00001b60 |      BUSY | 3e 3e | 20 20 | 8224 | no |
| 0x00001b80 |      STUN | 52 52 | 4c 4c | 19532 | no |
| 0x00001ba0 | NEW MESSAGE | 5b 53 | 45 4d | 19781 | no |
| 0x00001bc0 |    MAN DOWN | 56 51 | 48 4f | 20296 | no |
| 0x00001be0 | ID | 5f 4a | 41 54 | 21569 | no |
| 0x00001c00 | GID | 5a 1e | 44 00 | 68 | no |
| 0x00001c20 | STATUS | 57 51 | 49 4f | 20297 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001c40 | �RECEIVE DATA� | 4d 5b | 17747 | no | no |
| 0x00001c60 | �    BUSY    � | 3e 5d | 17184 | no | no |
| 0x00001c80 | �  NO REPLY  � | 3e 3e | 8224 | no | no |
| 0x00001ca0 | � GPS UPLOAD � | 4b 4a | 21589 | no | no |
| 0x00001cc0 | �   EMPTY    � | 3e 3e | 8224 | no | no |
| 0x00001ce0 | �SYSTEM BUSY � | 3e 3e | 8224 | no | no |
| 0x00001d00 | �  INVALID   � | 5b 5d | 17221 | no | no |
| 0x00001d20 | REMOTE CONTROL | 52 4b | 21836 | no | yes |

## Run 5: `0x00001d20-0x00001f1f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001d20 | REMOTE CONTROL | 52 4b | 4c 55 | 21836 | no |
| 0x00001d40 | AM | 1e 1e | 00 00 | 0 | no |
| 0x00001d60 | A | 1e 1e | 00 00 | 0 | no |
| 0x00001d80 |              s | 3e 49 | 20 57 | 22304 | no |
| 0x00001da0 |   VGS ERROR | 5b 53 | 45 4d | 19781 | no |
| 0x00001dc0 |    GREETING | 49 3e | 57 20 | 8279 | no |
| 0x00001de0 | END OF MESSAGE | 1e 1e | 00 00 | 0 | no |
| 0x00001e00 | VM | 1e 1e | 00 00 | 0 | no |
| 0x00001e20 | PRIORITY 4 | 3e 58 | 20 46 | 17952 | no |
| 0x00001e40 |   GRP ADD-D | 59 4c | 47 52 | 21063 | no |
| 0x00001e60 |            dBm | 57 51 | 49 4f | 20297 | no |
| 0x00001e80 |        CH NAME | 3e 44 | 20 5a | 23072 | no |
| 0x00001ea0 | MAINTENANCE | 5f 5d | 41 43 | 17217 | no |
| 0x00001ec0 |    MESSAGE? | 51 4b | 4f 55 | 21839 | no |
| 0x00001ee0 | INDIV+SDM | 52 5d | 4c 43 | 17228 | no |
| 0x00001f00 | SHORT MESSAGE | 3e 4c | 20 52 | 21024 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001f20 | � REMOTE TX  � | 3e 5d | 17184 | no | no |
| 0x00001f40 | LONE WORKER | 3e 3e | 8224 | no | yes |
| 0x00001f60 |  SITE ROAMING | 4a 5b | 17748 | no | yes |
| 0x00001f80 | ID | 5f 4a | 21569 | no | yes |
| 0x00001fa0 | MY ID | 5d 5b | 17731 | no | yes |
| 0x00001fc0 | FREE DIAL | 52 52 | 19532 | no | yes |
| 0x00001fe0 | TRANSFER | 5b 4a | 21573 | no | yes |
| 0x00002000 | ID | 3e 51 | 20256 | no | yes |

## Run 6: `0x00001f40-0x0000215f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001f40 | LONE WORKER | 3e 3e | 20 20 | 8224 | no |
| 0x00001f60 |  SITE ROAMING | 4a 5b | 54 45 | 17748 | no |
| 0x00001f80 | ID | 5f 4a | 41 54 | 21569 | no |
| 0x00001fa0 | MY ID | 5d 5b | 43 45 | 17731 | no |
| 0x00001fc0 | FREE DIAL | 52 52 | 4c 4c | 19532 | no |
| 0x00001fe0 | TRANSFER | 5b 4a | 45 54 | 21573 | no |
| 0x00002000 | ID | 3e 51 | 20 4f | 20256 | no |
| 0x00002020 |     UPDATE | 3e 4b | 20 55 | 21792 | no |
| 0x00002040 |   PHONE CALL | 3e 3e | 20 20 | 8224 | no |
| 0x00002060 |           FLAT | 3e 3e | 20 20 | 8224 | no |
| 0x00002080 |           NONE | 53 57 | 4d 49 | 18765 | no |
| 0x000020a0 |   MICROPHONE 2 | 53 57 | 4d 49 | 18765 | no |
| 0x000020c0 |   MICROPHONE 4 | 53 57 | 4d 49 | 18765 | no |
| 0x000020e0 | RX AUDIO EQ | 3e 5f | 20 41 | 16672 | no |
| 0x00002100 | RX AGC | 3e 5f | 20 41 | 16672 | no |
| 0x00002120 | EXT MIC TYPE | 3e 52 | 20 4c | 19488 | no |
| 0x00002140 | TX NOISE SUPPR | e1 e1 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002160 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002180 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000021a0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000021c0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000021e0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002200 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002220 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002240 | �������������� | e1 e1 | 65535 | yes | no |

## Run 7: `0x000024c0-0x0000257f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000024c0 |   KEY ERASED   | 3e 55 | 20 4b | 19232 | no |
| 0x000024e0 |    KEYLOAD     | 3e 3e | 20 20 | 8224 | no |
| 0x00002500 | SELFTEST ERROR | 53 3e | 4d 20 | 8269 | no |
| 0x00002520 | GROUP ID | 51 4b | 4f 55 | 21839 | no |
| 0x00002540 | ACTIVITY DET | 59 3e | 47 20 | 8263 | no |
| 0x00002560 | EMG STATIONARY | 5b 53 | 45 4d | 19781 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002580 | �������������� | e1 e1 | 65535 | no | no |
| 0x000025a0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000025c0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000025e0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002600 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002620 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002640 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002660 | �������������� | e1 e1 | 65535 | yes | no |

## Run 8: `0x00002680-0x000026bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002680 |   HIGH POWER | 52 51 | 4c 4f | 20300 | no |
| 0x000026a0 |   AUTO POWER | e1 e1 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000026c0 | �������������� | 3e 5a | 17440 | no | no |
| 0x000026e0 | No. | 47 4d | 21337 | no | yes |
| 0x00002700 | GPS REPORT ERR | 47 4d | 21337 | no | yes |
| 0x00002720 | SYSTEM         | 4d 4a | 21587 | no | yes |
| 0x00002740 |   ROAM | e1 e1 | 65535 | no | yes |
| 0x00002760 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002780 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000027a0 | �������������� | e1 e1 | 65535 | yes | no |

## Run 9: `0x000026e0-0x0000275f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000026e0 | No. | 47 4d | 59 53 | 21337 | no |
| 0x00002700 | GPS REPORT ERR | 47 4d | 59 53 | 21337 | no |
| 0x00002720 | SYSTEM         | 4d 4a | 53 54 | 21587 | no |
| 0x00002740 |   ROAM | e1 e1 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002760 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002780 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000027a0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000027c0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000027e0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002800 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002820 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002840 | �������������� | e1 e1 | 65535 | yes | no |

## Run 10: `0x00002940-0x00002a9f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002940 | FNC | 1e 1e | 00 00 | 0 | no |
| 0x00002960 | DR1 | 2c 1e | 32 00 | 50 | no |
| 0x00002980 | DR3 | 2a 1e | 34 00 | 52 | no |
| 0x000029a0 | DR5 | 52 1e | 4c 00 | 76 | no |
| 0x000029c0 | GPS | 52 1e | 4c 00 | 76 | no |
| 0x000029e0 | OFF | 1e 1e | 00 00 | 0 | no |
| 0x00002a00 | HA | e1 e1 | ff ff | 65535 | no |
| 0x00002a20 | PA | 1e 1e | 00 00 | 0 | no |
| 0x00002a40 | S | 1e 1e | 00 00 | 0 | no |
| 0x00002a60 | ALL | 1e 1e | 00 00 | 0 | no |
| 0x00002a80 | TRS | e1 e1 | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002aa0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002ac0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002ae0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002b00 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002b20 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002b40 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002b60 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00002b80 | �������������� | e1 e1 | 65535 | yes | no |

## Run 11: `0x00002d80-0x00002dbf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002d80 |  EXIT | 5b 46 | 45 58 | 22597 | no |
| 0x00002da0 |  BACK | 4a 51 | 54 4f | 20308 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002dc0 |       �������� | 4a 51 | 20308 | no | no |
| 0x00002de0 | A_RPLY�������� | 4a 5b | 17748 | no | no |
| 0x00002e00 | A_DIAL�������� | 41 4e | 20575 | no | no |
| 0x00002e20 |  AUX | 59 56 | 18503 | no | yes |
| 0x00002e40 | B.CAST�������� | 52 52 | 19532 | no | no |
| 0x00002e60 | CALL2 | 52 52 | 19532 | no | yes |
| 0x00002e80 | CALL4 | 52 52 | 19532 | no | yes |
| 0x00002ea0 | CALL6 | 56 1e | 72 | no | yes |

## Run 12: `0x00002e60-0x00002ebf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002e60 | CALL2 | 52 52 | 4c 4c | 19532 | no |
| 0x00002e80 | CALL4 | 52 52 | 4c 4c | 19532 | no |
| 0x00002ea0 | CALL6 | 56 1e | 48 00 | 72 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002ec0 | CH_ENT�������� | 56 1e | 72 | no | no |
| 0x00002ee0 | CH_RCL�������� | 51 5d | 17231 | no | no |
| 0x00002f00 | CLK_AJ�������� | 41 53 | 19807 | no | no |
| 0x00002f20 |  DR1 | 4c 2c | 12882 | no | yes |
| 0x00002f40 |  DR3 | 4c 2a | 13394 | no | yes |
| 0x00002f60 |  DR5 | 57 4d | 21321 | no | yes |
| 0x00002f80 | FX_VOL�������� | 4c 5d | 17234 | no | no |
| 0x00002fa0 |  FNC | 4e 4d | 21328 | no | yes |

## Run 13: `0x00002f20-0x00002f7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002f20 |  DR1 | 4c 2c | 52 32 | 12882 | no |
| 0x00002f40 |  DR3 | 4c 2a | 52 34 | 13394 | no |
| 0x00002f60 |  DR5 | 57 4d | 49 53 | 21321 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002f80 | FX_VOL�������� | 4c 5d | 17234 | no | no |
| 0x00002fa0 |  FNC | 4e 4d | 21328 | no | yes |
| 0x00002fc0 | GROUP | 4e 35 | 11088 | no | yes |
| 0x00002fe0 |  HOME | 5a 5d | 17220 | no | yes |
| 0x00003000 | IND+ST�������� | 52 51 | 20300 | no | no |
| 0x00003020 |  LOW | 57 50 | 20041 | no | yes |
| 0x00003040 |  MENU | 51 50 | 20047 | no | yes |
| 0x00003060 |  MONI | 4d 4a | 21587 | no | yes |

## Run 14: `0x00002fa0-0x00002fff`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002fa0 |  FNC | 4e 4d | 50 53 | 21328 | no |
| 0x00002fc0 | GROUP | 4e 35 | 50 2b | 11088 | no |
| 0x00002fe0 |  HOME | 5a 5d | 44 43 | 17220 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003000 | IND+ST�������� | 52 51 | 20300 | no | no |
| 0x00003020 |  LOW | 57 50 | 20041 | no | yes |
| 0x00003040 |  MENU | 51 50 | 20047 | no | yes |
| 0x00003060 |  MONI | 4d 4a | 21587 | no | yes |
| 0x00003080 |  PLAY | 4d 4e | 20563 | no | yes |
| 0x000030a0 |  SCAN | 31 5f | 16687 | no | yes |
| 0x000030c0 |  SCR | 52 5d | 17228 | no | yes |
| 0x000030e0 | SEL+ST�������� | 4d 41 | 24403 | no | no |

## Run 15: `0x00003020-0x000030df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003020 |  LOW | 57 50 | 49 4e | 20041 | no |
| 0x00003040 |  MENU | 51 50 | 4f 4e | 20047 | no |
| 0x00003060 |  MONI | 4d 4a | 53 54 | 21587 | no |
| 0x00003080 |  PLAY | 4d 4e | 53 50 | 20563 | no |
| 0x000030a0 |  SCAN | 31 5f | 2f 41 | 16687 | no |
| 0x000030c0 |  SCR | 52 5d | 4c 43 | 17228 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000030e0 | SEL+ST�������� | 4d 41 | 24403 | no | no |
| 0x00003100 | S_LOCK�������� | 4f 52 | 19537 | no | no |
| 0x00003120 | SQ_OFF�������� | 41 51 | 20319 | no | no |
| 0x00003140 | STACK | 5f 4a | 21569 | no | yes |
| 0x00003160 |   TA | 52 41 | 24396 | no | yes |
| 0x00003180 | PASSWD�������� | 57 5c | 16969 | no | no |
| 0x000031a0 |  MEMO | 51 46 | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 50 5b | 17742 | no | no |

## Run 16: `0x00003140-0x0000317f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003140 | STACK | 5f 4a | 41 54 | 21569 | no |
| 0x00003160 |   TA | 52 41 | 4c 5f | 24396 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003180 | PASSWD�������� | 57 5c | 16969 | no | no |
| 0x000031a0 |  MEMO | 51 46 | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 50 5b | 17742 | no | no |
| 0x000031e0 | ZONE | 4a 5b | 17748 | no | yes |
| 0x00003200 | SITE | 3e 49 | 22304 | no | yes |
| 0x00003220 | GRP+SD�������� | 5a 35 | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 5a 53 | 19780 | no | no |
| 0x00003260 | �������������� | 4d 5b | 17747 | no | no |

## Run 17: `0x000031e0-0x0000321f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000031e0 | ZONE | 4a 5b | 54 45 | 17748 | no |
| 0x00003200 | SITE | 3e 49 | 20 57 | 22304 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003220 | GRP+SD�������� | 5a 35 | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 5a 53 | 19780 | no | no |
| 0x00003260 | �������������� | 4d 5b | 17747 | no | no |
| 0x00003280 |  1x | 66 1e | 120 | no | yes |
| 0x000032a0 |  10x | 2e 66 | 30768 | no | yes |
| 0x000032c0 | RX_ENT�������� | e1 e1 | 65535 | no | no |
| 0x000032e0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00003300 | �������������� | e1 e1 | 65535 | yes | no |

## Run 18: `0x00003280-0x000032bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003280 |  1x | 66 1e | 78 00 | 120 | no |
| 0x000032a0 |  10x | 2e 66 | 30 78 | 30768 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000032c0 | RX_ENT�������� | e1 e1 | 65535 | no | no |
| 0x000032e0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00003300 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00003320 |  HIGH | e1 e1 | 65535 | no | yes |
| 0x00003340 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00003360 | ACT_DT�������� | 4a 41 | 24404 | no | no |
| 0x00003380 | �������������� | e1 e1 | 65535 | no | no |
| 0x000033a0 | CH_ENT�������� | e1 e1 | 65535 | no | no |

## Run 19: `0x000037a0-0x000037df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000037a0 | 00 | ee 6e | f0 70 | 28912 | no |
| 0x000037c0 | 0000000 | 2e 2e | 30 30 | 12336 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000037e0 | �p00000000000p | 1e ee | 61440 | no | no |
| 0x00003800 | 00��� | e1 e1 | 65535 | no | no |
| 0x00003820 |  | 21 61 | 32575 | no | no |
| 0x00003840 |  | 1e 1e | 0 | no | no |
| 0x00003860 |  | e7 e7 | 63993 | no | no |
| 0x00003880 |  | 1e 1f | 256 | no | no |
| 0x000038a0 |  | 1e 1e | 0 | no | no |
| 0x000038c0 |  | 19 19 | 1799 | no | no |

## Run 20: `0x00010480-0x0001059f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00010480 | Curtis, AE4BT | b4 20 | aa 3e | 16042 | no |
| 0x000104a0 | Frank, KF4CLO | 3d 18 | 23 06 | 1571 | no |
| 0x000104c0 | Ed, AK7AN | 5c 2e | 42 30 | 12354 | no |
| 0x000104e0 | Kelli, KD0CVD | 5f 2e | 41 30 | 12353 | no |
| 0x00010500 | Chris, K4DKK | d1 31 | cf 2f | 12239 | no |
| 0x00010520 | DVNET | 11 39 | 0f 27 | 9999 | no |
| 0x00010540 | No NXDN ID | 65 67 | 7b 79 | 31099 | no |
| 0x00010560 | Bjorn, SA7AUX | ac 20 | b2 3e | 16050 | no |
| 0x00010580 | Doug, W4DBG | 0a 1a | 14 04 | 1044 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000105a0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000105c0 | Randy, W8EJC | 8a 85 | 39828 | no | yes |
| 0x000105e0 | BitByBit Hams | 27 2e | 12345 | no | yes |
| 0x00010600 | Tom, K4TH | 80 3b | 9630 | no | yes |
| 0x00010620 | NX4DX BitbyBit | af 36 | 10417 | no | yes |
| 0x00010640 | Long Gone | f0 e1 | 65518 | no | yes |
| 0x00010660 | My Best Friend | 70 ac | 45678 | no | yes |
| 0x00010680 | Don't like | 78 42 | 23654 | no | yes |

## Run 21: `0x000105c0-0x0001083f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000105c0 | Randy, W8EJC | 8a 85 | 94 9b | 39828 | no |
| 0x000105e0 | BitByBit Hams | 27 2e | 39 30 | 12345 | no |
| 0x00010600 | Tom, K4TH | 80 3b | 9e 25 | 9630 | no |
| 0x00010620 | NX4DX BitbyBit | af 36 | b1 28 | 10417 | no |
| 0x00010640 | Long Gone | f0 e1 | ee ff | 65518 | no |
| 0x00010660 | My Best Friend | 70 ac | 6e b2 | 45678 | no |
| 0x00010680 | Don't like | 78 42 | 66 5c | 23654 | no |
| 0x000106a0 |  UNIT ID 0018 | eb 29 | f5 37 | 14325 | no |
| 0x000106c0 |  UNIT ID 0019 | a3 e9 | bd f7 | 63421 | no |
| 0x000106e0 |  UNIT ID 0020 | 85 45 | 9b 5b | 23451 | no |
| 0x00010700 |  UNIT ID 0021 | 84 63 | 9a 7d | 32154 | no |
| 0x00010720 |  UNIT ID 0022 | 0f bf | 11 a1 | 41233 | no |
| 0x00010740 |  UNIT ID 0023 | b9 d9 | a7 c7 | 51111 | no |
| 0x00010760 |  UNIT ID 0024 | 05 f1 | 1b ef | 61211 | no |
| 0x00010780 |  UNIT ID 0025 | 82 b3 | 9c ad | 44444 | no |
| 0x000107a0 |  UNIT ID 0026 | 1d c7 | 03 d9 | 55555 | no |
| 0x000107c0 |  UNIT ID 0027 | 2b 9c | 35 82 | 33333 | no |
| 0x000107e0 |  UNIT ID 0028 | d0 48 | ce 56 | 22222 | no |
| 0x00010800 |  UNIT ID 0029 | 79 35 | 67 2b | 11111 | no |
| 0x00010820 |  UNIT ID 0030 | 57 ca | 49 d4 | 54345 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00010840 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00010860 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00010880 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000108a0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000108c0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000108e0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00010900 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00010920 | �������������� | e1 e1 | 65535 | yes | no |

## Run 22: `0x00014f80-0x0001509f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00014f80 | World Wide TG | f6 e3 | e8 fd | 65000 | no |
| 0x00014fa0 | Parrot | 14 1e | 0a 00 | 10 | no |
| 0x00014fc0 | Colo Fun Mach | 77 67 | 69 79 | 31081 | no |
| 0x00014fe0 | MO Digi Call | d5 62 | cb 7c | 31947 | no |
| 0x00015000 | AlabamaLink TG | 3c 67 | 22 79 | 31010 | no |
| 0x00015020 | SW Missouri TG | 25 64 | 3b 7a | 31291 | no |
| 0x00015040 | PiStar TG | a6 65 | b8 7b | 31672 | no |
| 0x00015060 | VK Radio TG | 79 db | 67 c5 | 50535 | no |
| 0x00015080 | NXDN N America | c6 39 | d8 27 | 10200 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000150a0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000150c0 | Utah DRN 01 | 1d 65 | 31491 | no | yes |
| 0x000150e0 | Utah DRN 05 | 19 65 | 31495 | no | yes |
| 0x00015100 | PA7LIM TG | d6 51 | 20424 | no | yes |
| 0x00015120 | Disconnect TG | 11 39 | 9999 | no | yes |
| 0x00015140 | Hot n Sexy | 1d 65 | 31491 | no | yes |
| 0x00015160 | Lookout Mtn TG | 63 b7 | 43389 | no | yes |
| 0x00015180 | AK7AN TG | 03 4d | 21277 | no | yes |

## Run 23: `0x000150c0-0x0001533f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000150c0 | Utah DRN 01 | 1d 65 | 03 7b | 31491 | no |
| 0x000150e0 | Utah DRN 05 | 19 65 | 07 7b | 31495 | no |
| 0x00015100 | PA7LIM TG | d6 51 | c8 4f | 20424 | no |
| 0x00015120 | Disconnect TG | 11 39 | 0f 27 | 9999 | no |
| 0x00015140 | Hot n Sexy | 1d 65 | 03 7b | 31491 | no |
| 0x00015160 | Lookout Mtn TG | 63 b7 | 7d a9 | 43389 | no |
| 0x00015180 | AK7AN TG | 03 4d | 1d 53 | 21277 | no |
| 0x000151a0 | GROUP ID 0018 | 79 35 | 67 2b | 11111 | no |
| 0x000151c0 | GROUP ID 0019 | d0 48 | ce 56 | 22222 | no |
| 0x000151e0 | GROUP ID 0020 | 2b 9c | 35 82 | 33333 | no |
| 0x00015200 | GROUP ID 0021 | 82 b3 | 9c ad | 44444 | no |
| 0x00015220 | GROUP ID 0022 | 1d c7 | 03 d9 | 55555 | no |
| 0x00015240 | GROUP ID 0023 | 1a c7 | 04 d9 | 55556 | no |
| 0x00015260 | BY BY | 83 b3 | 9d ad | 44445 | no |
| 0x00015280 | GROUP ID 0025 | 29 9c | 37 82 | 33335 | no |
| 0x000152a0 | GROUP ID 0026 | d1 48 | cf 56 | 22223 | no |
| 0x000152c0 | GROUP ID 0027 | ff c6 | e1 d8 | 55521 | no |
| 0x000152e0 | GROUP ID 0028 | fc 35 | e2 2b | 11234 | no |
| 0x00015300 | GROUP ID 0029 | 46 32 | 58 2c | 11352 | no |
| 0x00015320 | GROUP ID 0030 | bb e5 | a5 fb | 64421 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00015340 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00015360 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00015380 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000153a0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000153c0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x000153e0 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00015400 | �������������� | e1 e1 | 65535 | yes | no |
| 0x00015420 | �������������� | e1 e1 | 65535 | yes | no |

