# KPG111 Candidate Table Map

This is a read-only structural scan. Printable decoded names are evidence for candidate records, not proof of table purpose.

## File

- Path: `research/dattest3/Dattest3/Program2.dat`
- Size: 168257 bytes
- SHA-256: `885d599058a75853acc6590eb1e4e36ffb4062bcd96bcc364ecd3588198c8731`
- Payload start: `0x40`
- Record size: 32
- Decode XOR: `0x34`
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
| 0x00000b40 | ABCDEFGHIJKLMN | 67 60 | 53 54 | 21587 | no |
| 0x00000b60 | 56789 | 34 34 | 00 00 | 0 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000b80 |  | 34 34 | 0 | no | no |
| 0x00000ba0 | 1 | 77 06 | 12867 | no | yes |
| 0x00000bc0 | DEF3 | 7d 00 | 13385 | no | yes |
| 0x00000be0 | JKL5 | 7b 02 | 13903 | no | yes |
| 0x00000c00 | PQRS7 | 62 0c | 14422 | no | yes |
| 0x00000c20 | WXYZ9 | cb cb | 65535 | no | yes |
| 0x00000c40 | CALL | 77 75 | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 60 7d | 18772 | no | no |

## Run 2: `0x00000ba0-0x00000c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00000ba0 | 1 | 77 06 | 43 32 | 12867 | no |
| 0x00000bc0 | DEF3 | 7d 00 | 49 34 | 13385 | no |
| 0x00000be0 | JKL5 | 7b 02 | 4f 36 | 13903 | no |
| 0x00000c00 | PQRS7 | 62 0c | 56 38 | 14422 | no |
| 0x00000c20 | WXYZ9 | cb cb | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00000c40 | CALL | 77 75 | 16707 | no | no |
| 0x00000c60 | AUDIO/TONES | 60 7d | 18772 | no | no |
| 0x00000c80 | Microphone | 41 50 | 25717 | no | no |
| 0x00000ca0 |  | 60 14 | 8276 | no | no |
| 0x00000cc0 | 0+CDNM4����� | cb cb | 65535 | no | no |
| 0x00000ce0 | �������������� | cb cb | 65535 | yes | no |
| 0x00000d00 | �������������� | cb cb | 65535 | yes | no |
| 0x00000d20 | �������������� | cb cb | 65535 | yes | no |

## Run 3: `0x00001540-0x0000177f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001540 | 2-TONE | 60 7b | 54 4f | 20308 | no |
| 0x00001560 | AUTO TELEPHONE | 14 75 | 20 41 | 16672 | no |
| 0x00001580 | AUTO DIAL | 60 7b | 54 4f | 20308 | no |
| 0x000015a0 |     BLANK | 14 14 | 20 20 | 8224 | no |
| 0x000015c0 |     CODE? | 14 14 | 20 20 | 8224 | no |
| 0x000015e0 |  OVER WRITE? | 14 70 | 20 44 | 17440 | no |
| 0x00001600 | AUX | 6c 14 | 58 20 | 8280 | no |
| 0x00001620 | AUX B | 7b 75 | 4f 41 | 16719 | no |
| 0x00001640 | CHANNEL ENTRY | 14 7a | 20 4e | 20000 | no |
| 0x00001660 | PRIORITY 3 | 7b 77 | 4f 43 | 17231 | no |
| 0x00001680 | CLOCK ADJUST | 75 66 | 41 52 | 21057 | no |
| 0x000016a0 | MONTH | 6d 34 | 59 00 | 89 | no |
| 0x000016c0 | HOUR | 7a 61 | 4e 55 | 21838 | no |
| 0x000016e0 | DIRECT CH1 SEL | 66 71 | 52 45 | 17746 | no |
| 0x00001700 | DIRECT CH3 SEL | 66 71 | 52 45 | 17746 | no |
| 0x00001720 | DIRECT CH5 SEL | 67 64 | 53 50 | 20563 | no |
| 0x00001740 | FIXED VOLUME | 66 77 | 52 43 | 17234 | no |
| 0x00001760 | SITE No. | 60 71 | 54 45 | 17748 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001780 | �   SEARCH   � | 67 14 | 8275 | no | no |
| 0x000017a0 | N | 34 34 | 0 | no | yes |
| 0x000017c0 | E | 34 34 | 0 | no | yes |
| 0x000017e0 | ALT | 14 14 | 8224 | no | yes |
| 0x00001800 |             ft | 7b 61 | 21839 | no | yes |
| 0x00001820 | GROUP+STATUS | 79 71 | 17741 | no | yes |
| 0x00001840 | HORN ALERT | 70 7d | 18756 | no | yes |
| 0x00001860 | INDIV+STATUS | 14 14 | 8224 | no | yes |

## Run 4: `0x000017a0-0x00001c3f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000017a0 | N | 34 34 | 00 00 | 0 | no |
| 0x000017c0 | E | 34 34 | 00 00 | 0 | no |
| 0x000017e0 | ALT | 14 14 | 20 20 | 8224 | no |
| 0x00001800 |             ft | 7b 61 | 4f 55 | 21839 | no |
| 0x00001820 | GROUP+STATUS | 79 71 | 4d 45 | 17741 | no |
| 0x00001840 | HORN ALERT | 70 7d | 44 49 | 18756 | no |
| 0x00001860 | INDIV+STATUS | 14 14 | 20 20 | 8224 | no |
| 0x00001880 | LCD BRIGHTNESS | 63 14 | 57 20 | 8279 | no |
| 0x000018a0 | MENU | 7a 7d | 4e 49 | 18766 | no |
| 0x000018c0 | OST | 60 14 | 54 20 | 8276 | no |
| 0x000018e0 |    TONE OFF | 75 6d | 41 59 | 22849 | no |
| 0x00001900 | PRI CH SEL | 14 14 | 20 20 | 8224 | no |
| 0x00001920 |     PRIORITY 1 | 14 14 | 20 20 | 8224 | no |
| 0x00001940 |   PRIORITY 1&2 | 76 78 | 42 4c | 19522 | no |
| 0x00001960 | SCAN | 75 7a | 41 4e | 20033 | no |
| 0x00001980 |         DELETE | 14 14 | 20 20 | 8224 | no |
| 0x000019a0 |      SCAN | 75 7a | 41 4e | 20033 | no |
| 0x000019c0 | SCRAM/ENCRYP | 66 75 | 52 41 | 16722 | no |
| 0x000019e0 | CODE | 78 77 | 4c 43 | 17228 | no |
| 0x00001a00 | SELCALL+STATUS | 7a 70 | 4e 44 | 17486 | no |
| 0x00001a20 | SITE LOCK | 60 71 | 54 45 | 17748 | no |
| 0x00001a40 | SQUELCH LEVEL | 62 71 | 56 45 | 17750 | no |
| 0x00001a60 | SQUELCH OFF | 75 77 | 41 43 | 17217 | no |
| 0x00001a80 | STATUS | 78 7f | 4c 4b | 19276 | no |
| 0x00001aa0 | PASSWORD | 14 64 | 20 50 | 20512 | no |
| 0x00001ac0 | VIBRATOR | 7d 77 | 49 43 | 17225 | no |
| 0x00001ae0 | VOX | 6c 14 | 58 20 | 8280 | no |
| 0x00001b00 | ZONE DEL/ADD | 14 14 | 20 20 | 8224 | no |
| 0x00001b20 |            OFF | 14 14 | 20 20 | 8224 | no |
| 0x00001b40 |            LOW | 67 60 | 53 54 | 21587 | no |
| 0x00001b60 |      BUSY | 14 14 | 20 20 | 8224 | no |
| 0x00001b80 |      STUN | 78 78 | 4c 4c | 19532 | no |
| 0x00001ba0 | NEW MESSAGE | 71 79 | 45 4d | 19781 | no |
| 0x00001bc0 |    MAN DOWN | 7c 7b | 48 4f | 20296 | no |
| 0x00001be0 | ID | 75 60 | 41 54 | 21569 | no |
| 0x00001c00 | GID | 70 34 | 44 00 | 68 | no |
| 0x00001c20 | STATUS | 7d 7b | 49 4f | 20297 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001c40 | �RECEIVE DATA� | 67 71 | 17747 | no | no |
| 0x00001c60 | �    BUSY    � | 14 77 | 17184 | no | no |
| 0x00001c80 | �  NO REPLY  � | 14 14 | 8224 | no | no |
| 0x00001ca0 | � GPS UPLOAD � | 61 60 | 21589 | no | no |
| 0x00001cc0 | �   EMPTY    � | 14 14 | 8224 | no | no |
| 0x00001ce0 | �SYSTEM BUSY � | 14 14 | 8224 | no | no |
| 0x00001d00 | �  INVALID   � | 71 77 | 17221 | no | no |
| 0x00001d20 | REMOTE CONTROL | 78 61 | 21836 | no | yes |

## Run 5: `0x00001d20-0x00001f1f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001d20 | REMOTE CONTROL | 78 61 | 4c 55 | 21836 | no |
| 0x00001d40 | AM | 34 34 | 00 00 | 0 | no |
| 0x00001d60 | A | 34 34 | 00 00 | 0 | no |
| 0x00001d80 |              s | 14 63 | 20 57 | 22304 | no |
| 0x00001da0 |   VGS ERROR | 71 79 | 45 4d | 19781 | no |
| 0x00001dc0 |    GREETING | 63 14 | 57 20 | 8279 | no |
| 0x00001de0 | END OF MESSAGE | 34 34 | 00 00 | 0 | no |
| 0x00001e00 | VM | 34 34 | 00 00 | 0 | no |
| 0x00001e20 | PRIORITY 4 | 14 72 | 20 46 | 17952 | no |
| 0x00001e40 |   GRP ADD-D | 73 66 | 47 52 | 21063 | no |
| 0x00001e60 |            dBm | 7d 7b | 49 4f | 20297 | no |
| 0x00001e80 |        CH NAME | 14 6e | 20 5a | 23072 | no |
| 0x00001ea0 | MAINTENANCE | 75 77 | 41 43 | 17217 | no |
| 0x00001ec0 |    MESSAGE? | 7b 61 | 4f 55 | 21839 | no |
| 0x00001ee0 | INDIV+SDM | 78 77 | 4c 43 | 17228 | no |
| 0x00001f00 | SHORT MESSAGE | 14 66 | 20 52 | 21024 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00001f20 | � REMOTE TX  � | 14 77 | 17184 | no | no |
| 0x00001f40 | LONE WORKER | 14 14 | 8224 | no | yes |
| 0x00001f60 |  SITE ROAMING | 60 71 | 17748 | no | yes |
| 0x00001f80 | ID | 75 60 | 21569 | no | yes |
| 0x00001fa0 | MY ID | 77 71 | 17731 | no | yes |
| 0x00001fc0 | FREE DIAL | 78 78 | 19532 | no | yes |
| 0x00001fe0 | TRANSFER | 71 60 | 21573 | no | yes |
| 0x00002000 | ID | 14 7b | 20256 | no | yes |

## Run 6: `0x00001f40-0x0000215f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00001f40 | LONE WORKER | 14 14 | 20 20 | 8224 | no |
| 0x00001f60 |  SITE ROAMING | 60 71 | 54 45 | 17748 | no |
| 0x00001f80 | ID | 75 60 | 41 54 | 21569 | no |
| 0x00001fa0 | MY ID | 77 71 | 43 45 | 17731 | no |
| 0x00001fc0 | FREE DIAL | 78 78 | 4c 4c | 19532 | no |
| 0x00001fe0 | TRANSFER | 71 60 | 45 54 | 21573 | no |
| 0x00002000 | ID | 14 7b | 20 4f | 20256 | no |
| 0x00002020 |     UPDATE | 14 61 | 20 55 | 21792 | no |
| 0x00002040 |   PHONE CALL | 14 14 | 20 20 | 8224 | no |
| 0x00002060 |           FLAT | 14 14 | 20 20 | 8224 | no |
| 0x00002080 |           NONE | 79 7d | 4d 49 | 18765 | no |
| 0x000020a0 |   MICROPHONE 2 | 79 7d | 4d 49 | 18765 | no |
| 0x000020c0 |   MICROPHONE 4 | 79 7d | 4d 49 | 18765 | no |
| 0x000020e0 | RX AUDIO EQ | 14 75 | 20 41 | 16672 | no |
| 0x00002100 | RX AGC | 14 75 | 20 41 | 16672 | no |
| 0x00002120 | EXT MIC TYPE | 14 78 | 20 4c | 19488 | no |
| 0x00002140 | TX NOISE SUPPR | cb cb | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002160 | �������������� | cb cb | 65535 | yes | no |
| 0x00002180 | �������������� | cb cb | 65535 | yes | no |
| 0x000021a0 | �������������� | cb cb | 65535 | yes | no |
| 0x000021c0 | �������������� | cb cb | 65535 | yes | no |
| 0x000021e0 | �������������� | cb cb | 65535 | yes | no |
| 0x00002200 | �������������� | cb cb | 65535 | yes | no |
| 0x00002220 | �������������� | cb cb | 65535 | yes | no |
| 0x00002240 | �������������� | cb cb | 65535 | yes | no |

## Run 7: `0x000024c0-0x0000257f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000024c0 |   KEY ERASED   | 14 7f | 20 4b | 19232 | no |
| 0x000024e0 |    KEYLOAD     | 14 14 | 20 20 | 8224 | no |
| 0x00002500 | SELFTEST ERROR | 79 14 | 4d 20 | 8269 | no |
| 0x00002520 | GROUP ID | 7b 61 | 4f 55 | 21839 | no |
| 0x00002540 | ACTIVITY DET | 73 14 | 47 20 | 8263 | no |
| 0x00002560 | EMG STATIONARY | 71 79 | 45 4d | 19781 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002580 | �������������� | cb cb | 65535 | no | no |
| 0x000025a0 | �������������� | cb cb | 65535 | yes | no |
| 0x000025c0 | �������������� | cb cb | 65535 | yes | no |
| 0x000025e0 | �������������� | cb cb | 65535 | yes | no |
| 0x00002600 | �������������� | cb cb | 65535 | yes | no |
| 0x00002620 | �������������� | cb cb | 65535 | yes | no |
| 0x00002640 | �������������� | cb cb | 65535 | yes | no |
| 0x00002660 | �������������� | cb cb | 65535 | yes | no |

## Run 8: `0x00002680-0x000026bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002680 |   HIGH POWER | 78 7b | 4c 4f | 20300 | no |
| 0x000026a0 |   AUTO POWER | cb cb | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000026c0 | �������������� | 14 70 | 17440 | no | no |
| 0x000026e0 | No. | 6d 67 | 21337 | no | yes |
| 0x00002700 | GPS REPORT ERR | 6d 67 | 21337 | no | yes |
| 0x00002720 | SYSTEM         | 67 60 | 21587 | no | yes |
| 0x00002740 |   ROAM | cb cb | 65535 | no | yes |
| 0x00002760 | �������������� | cb cb | 65535 | yes | no |
| 0x00002780 | �������������� | cb cb | 65535 | yes | no |
| 0x000027a0 | �������������� | cb cb | 65535 | yes | no |

## Run 9: `0x000026e0-0x0000275f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000026e0 | No. | 6d 67 | 59 53 | 21337 | no |
| 0x00002700 | GPS REPORT ERR | 6d 67 | 59 53 | 21337 | no |
| 0x00002720 | SYSTEM         | 67 60 | 53 54 | 21587 | no |
| 0x00002740 |   ROAM | cb cb | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002760 | �������������� | cb cb | 65535 | yes | no |
| 0x00002780 | �������������� | cb cb | 65535 | yes | no |
| 0x000027a0 | �������������� | cb cb | 65535 | yes | no |
| 0x000027c0 | �������������� | cb cb | 65535 | yes | no |
| 0x000027e0 | �������������� | cb cb | 65535 | yes | no |
| 0x00002800 | �������������� | cb cb | 65535 | yes | no |
| 0x00002820 | �������������� | cb cb | 65535 | yes | no |
| 0x00002840 | �������������� | cb cb | 65535 | yes | no |

## Run 10: `0x00002940-0x00002a9f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002940 | FNC | 34 34 | 00 00 | 0 | no |
| 0x00002960 | DR1 | 06 34 | 32 00 | 50 | no |
| 0x00002980 | DR3 | 00 34 | 34 00 | 52 | no |
| 0x000029a0 | DR5 | 78 34 | 4c 00 | 76 | no |
| 0x000029c0 | GPS | 78 34 | 4c 00 | 76 | no |
| 0x000029e0 | OFF | 34 34 | 00 00 | 0 | no |
| 0x00002a00 | HA | cb cb | ff ff | 65535 | no |
| 0x00002a20 | PA | 34 34 | 00 00 | 0 | no |
| 0x00002a40 | S | 34 34 | 00 00 | 0 | no |
| 0x00002a60 | ALL | 34 34 | 00 00 | 0 | no |
| 0x00002a80 | TRS | cb cb | ff ff | 65535 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002aa0 | �������������� | cb cb | 65535 | yes | no |
| 0x00002ac0 | �������������� | cb cb | 65535 | yes | no |
| 0x00002ae0 | �������������� | cb cb | 65535 | yes | no |
| 0x00002b00 | �������������� | cb cb | 65535 | yes | no |
| 0x00002b20 | �������������� | cb cb | 65535 | yes | no |
| 0x00002b40 | �������������� | cb cb | 65535 | yes | no |
| 0x00002b60 | �������������� | cb cb | 65535 | yes | no |
| 0x00002b80 | �������������� | cb cb | 65535 | yes | no |

## Run 11: `0x00002d80-0x00002dbf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002d80 |  EXIT | 71 6c | 45 58 | 22597 | no |
| 0x00002da0 |  BACK | 60 7b | 54 4f | 20308 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002dc0 |       �������� | 60 7b | 20308 | no | no |
| 0x00002de0 | A_RPLY�������� | 60 71 | 17748 | no | no |
| 0x00002e00 | A_DIAL�������� | 6b 64 | 20575 | no | no |
| 0x00002e20 |  AUX | 73 7c | 18503 | no | yes |
| 0x00002e40 | B.CAST�������� | 78 78 | 19532 | no | no |
| 0x00002e60 | CALL2 | 78 78 | 19532 | no | yes |
| 0x00002e80 | CALL4 | 78 78 | 19532 | no | yes |
| 0x00002ea0 | CALL6 | 7c 34 | 72 | no | yes |

## Run 12: `0x00002e60-0x00002ebf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002e60 | CALL2 | 78 78 | 4c 4c | 19532 | no |
| 0x00002e80 | CALL4 | 78 78 | 4c 4c | 19532 | no |
| 0x00002ea0 | CALL6 | 7c 34 | 48 00 | 72 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002ec0 | CH_ENT�������� | 7c 34 | 72 | no | no |
| 0x00002ee0 | CH_RCL�������� | 7b 77 | 17231 | no | no |
| 0x00002f00 | CLK_AJ�������� | 6b 79 | 19807 | no | no |
| 0x00002f20 |  DR1 | 66 06 | 12882 | no | yes |
| 0x00002f40 |  DR3 | 66 00 | 13394 | no | yes |
| 0x00002f60 |  DR5 | 7d 67 | 21321 | no | yes |
| 0x00002f80 | FX_VOL�������� | 66 77 | 17234 | no | no |
| 0x00002fa0 |  FNC | 64 67 | 21328 | no | yes |

## Run 13: `0x00002f20-0x00002f7f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002f20 |  DR1 | 66 06 | 52 32 | 12882 | no |
| 0x00002f40 |  DR3 | 66 00 | 52 34 | 13394 | no |
| 0x00002f60 |  DR5 | 7d 67 | 49 53 | 21321 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00002f80 | FX_VOL�������� | 66 77 | 17234 | no | no |
| 0x00002fa0 |  FNC | 64 67 | 21328 | no | yes |
| 0x00002fc0 | GROUP | 64 1f | 11088 | no | yes |
| 0x00002fe0 |  HOME | 70 77 | 17220 | no | yes |
| 0x00003000 | IND+ST�������� | 78 7b | 20300 | no | no |
| 0x00003020 |  LOW | 7d 7a | 20041 | no | yes |
| 0x00003040 |  MENU | 7b 7a | 20047 | no | yes |
| 0x00003060 |  MONI | 67 60 | 21587 | no | yes |

## Run 14: `0x00002fa0-0x00002fff`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00002fa0 |  FNC | 64 67 | 50 53 | 21328 | no |
| 0x00002fc0 | GROUP | 64 1f | 50 2b | 11088 | no |
| 0x00002fe0 |  HOME | 70 77 | 44 43 | 17220 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003000 | IND+ST�������� | 78 7b | 20300 | no | no |
| 0x00003020 |  LOW | 7d 7a | 20041 | no | yes |
| 0x00003040 |  MENU | 7b 7a | 20047 | no | yes |
| 0x00003060 |  MONI | 67 60 | 21587 | no | yes |
| 0x00003080 |  PLAY | 67 64 | 20563 | no | yes |
| 0x000030a0 |  SCAN | 1b 75 | 16687 | no | yes |
| 0x000030c0 |  SCR | 78 77 | 17228 | no | yes |
| 0x000030e0 | SEL+ST�������� | 67 6b | 24403 | no | no |

## Run 15: `0x00003020-0x000030df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003020 |  LOW | 7d 7a | 49 4e | 20041 | no |
| 0x00003040 |  MENU | 7b 7a | 4f 4e | 20047 | no |
| 0x00003060 |  MONI | 67 60 | 53 54 | 21587 | no |
| 0x00003080 |  PLAY | 67 64 | 53 50 | 20563 | no |
| 0x000030a0 |  SCAN | 1b 75 | 2f 41 | 16687 | no |
| 0x000030c0 |  SCR | 78 77 | 4c 43 | 17228 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000030e0 | SEL+ST�������� | 67 6b | 24403 | no | no |
| 0x00003100 | S_LOCK�������� | 65 78 | 19537 | no | no |
| 0x00003120 | SQ_OFF�������� | 6b 7b | 20319 | no | no |
| 0x00003140 | STACK | 75 60 | 21569 | no | yes |
| 0x00003160 |   TA | 78 6b | 24396 | no | yes |
| 0x00003180 | PASSWD�������� | 7d 76 | 16969 | no | no |
| 0x000031a0 |  MEMO | 7b 6c | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 7a 71 | 17742 | no | no |

## Run 16: `0x00003140-0x0000317f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003140 | STACK | 75 60 | 41 54 | 21569 | no |
| 0x00003160 |   TA | 78 6b | 4c 5f | 24396 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003180 | PASSWD�������� | 7d 76 | 16969 | no | no |
| 0x000031a0 |  MEMO | 7b 6c | 22607 | no | yes |
| 0x000031c0 | ZN_D/A�������� | 7a 71 | 17742 | no | no |
| 0x000031e0 | ZONE | 60 71 | 17748 | no | yes |
| 0x00003200 | SITE | 14 63 | 22304 | no | yes |
| 0x00003220 | GRP+SD�������� | 70 1f | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 70 79 | 19780 | no | no |
| 0x00003260 | �������������� | 67 71 | 17747 | no | no |

## Run 17: `0x000031e0-0x0000321f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000031e0 | ZONE | 60 71 | 54 45 | 17748 | no |
| 0x00003200 | SITE | 14 63 | 20 57 | 22304 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00003220 | GRP+SD�������� | 70 1f | 11076 | no | no |
| 0x00003240 | SEL+SD�������� | 70 79 | 19780 | no | no |
| 0x00003260 | �������������� | 67 71 | 17747 | no | no |
| 0x00003280 |  1x | 4c 34 | 120 | no | yes |
| 0x000032a0 |  10x | 04 4c | 30768 | no | yes |
| 0x000032c0 | RX_ENT�������� | cb cb | 65535 | no | no |
| 0x000032e0 | �������������� | cb cb | 65535 | yes | no |
| 0x00003300 | �������������� | cb cb | 65535 | yes | no |

## Run 18: `0x00003280-0x000032bf`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00003280 |  1x | 4c 34 | 78 00 | 120 | no |
| 0x000032a0 |  10x | 04 4c | 30 78 | 30768 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000032c0 | RX_ENT�������� | cb cb | 65535 | no | no |
| 0x000032e0 | �������������� | cb cb | 65535 | yes | no |
| 0x00003300 | �������������� | cb cb | 65535 | yes | no |
| 0x00003320 |  HIGH | cb cb | 65535 | no | yes |
| 0x00003340 | �������������� | cb cb | 65535 | yes | no |
| 0x00003360 | ACT_DT�������� | 60 6b | 24404 | no | no |
| 0x00003380 | �������������� | cb cb | 65535 | no | no |
| 0x000033a0 | CH_ENT�������� | cb cb | 65535 | no | no |

## Run 19: `0x000037a0-0x000037df`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x000037a0 | 00 | c4 44 | f0 70 | 28912 | no |
| 0x000037c0 | 0000000 | 04 04 | 30 30 | 12336 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x000037e0 | �p00000000000p | 34 c4 | 61440 | no | no |
| 0x00003800 | 00��� | cb cb | 65535 | no | no |
| 0x00003820 |  | 0b 4b | 32575 | no | no |
| 0x00003840 |  | 34 34 | 0 | no | no |
| 0x00003860 |  | cd cd | 63993 | no | no |
| 0x00003880 |  | 34 35 | 256 | no | no |
| 0x000038a0 |  | 34 34 | 0 | no | no |
| 0x000038c0 |  | 33 33 | 1799 | no | no |

## Run 20: `0x00010480-0x0001083f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00010480 | Curtis, AE4BT | 9e 0a | aa 3e | 16042 | no |
| 0x000104a0 | Frank, KF4CLO | 17 32 | 23 06 | 1571 | no |
| 0x000104c0 | Ed, AK7AN | 76 04 | 42 30 | 12354 | no |
| 0x000104e0 | Kelli, KD0CVD | 75 04 | 41 30 | 12353 | no |
| 0x00010500 | Chris, K4DKK | fb 1b | cf 2f | 12239 | no |
| 0x00010520 | DVNET | 3b 13 | 0f 27 | 9999 | no |
| 0x00010540 | No NXDN ID | 4f 4d | 7b 79 | 31099 | no |
| 0x00010560 | Bjorn, SA7AUX | 86 0a | b2 3e | 16050 | no |
| 0x00010580 | Doug, W4DBG | 20 30 | 14 04 | 1044 | no |
| 0x000105a0 | Jamie, KQ1USA | be 22 | 8a 16 | 5770 | no |
| 0x000105c0 | Randy, W8EJC | a0 af | 94 9b | 39828 | no |
| 0x000105e0 | BitByBit Hams | 0d 04 | 39 30 | 12345 | no |
| 0x00010600 | Tom, K4TH | aa 11 | 9e 25 | 9630 | no |
| 0x00010620 | NX4DX BitbyBit | 85 1c | b1 28 | 10417 | no |
| 0x00010640 | Long Gone | da cb | ee ff | 65518 | no |
| 0x00010660 | My Best Friend | 5a 86 | 6e b2 | 45678 | no |
| 0x00010680 | Don't like | 52 68 | 66 5c | 23654 | no |
| 0x000106a0 |  UNIT ID 0018 | c1 03 | f5 37 | 14325 | no |
| 0x000106c0 |  UNIT ID 0019 | 89 c3 | bd f7 | 63421 | no |
| 0x000106e0 |  UNIT ID 0020 | af 6f | 9b 5b | 23451 | no |
| 0x00010700 |  UNIT ID 0021 | ae 49 | 9a 7d | 32154 | no |
| 0x00010720 |  UNIT ID 0022 | 25 95 | 11 a1 | 41233 | no |
| 0x00010740 |  UNIT ID 0023 | 93 f3 | a7 c7 | 51111 | no |
| 0x00010760 |  UNIT ID 0024 | 2f db | 1b ef | 61211 | no |
| 0x00010780 |  UNIT ID 0025 | a8 99 | 9c ad | 44444 | no |
| 0x000107a0 |  UNIT ID 0026 | 37 ed | 03 d9 | 55555 | no |
| 0x000107c0 |  UNIT ID 0027 | 01 b6 | 35 82 | 33333 | no |
| 0x000107e0 |  UNIT ID 0028 | fa 62 | ce 56 | 22222 | no |
| 0x00010800 |  UNIT ID 0029 | 53 1f | 67 2b | 11111 | no |
| 0x00010820 |  UNIT ID 0030 | 7d e0 | 49 d4 | 54345 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00010840 | �������������� | cb cb | 65535 | yes | no |
| 0x00010860 | �������������� | cb cb | 65535 | yes | no |
| 0x00010880 | �������������� | cb cb | 65535 | yes | no |
| 0x000108a0 | �������������� | cb cb | 65535 | yes | no |
| 0x000108c0 | �������������� | cb cb | 65535 | yes | no |
| 0x000108e0 | �������������� | cb cb | 65535 | yes | no |
| 0x00010900 | �������������� | cb cb | 65535 | yes | no |
| 0x00010920 | �������������� | cb cb | 65535 | yes | no |

## Run 21: `0x00014f80-0x0001533f`
| Offset | Decoded Name | Raw +19/+20 | Decoded +19/+20 | LE Value | Empty |
| --- | --- | --- | --- | --- | --- |
| 0x00014f80 | World Wide TG | dc c9 | e8 fd | 65000 | no |
| 0x00014fa0 | Parrot | 3e 34 | 0a 00 | 10 | no |
| 0x00014fc0 | Colo Fun Mach | 5d 4d | 69 79 | 31081 | no |
| 0x00014fe0 | MO Digi Call | ff 48 | cb 7c | 31947 | no |
| 0x00015000 | AlabamaLink TG | 16 4d | 22 79 | 31010 | no |
| 0x00015020 | SW Missouri TG | 0f 4e | 3b 7a | 31291 | no |
| 0x00015040 | PiStar TG | 8c 4f | b8 7b | 31672 | no |
| 0x00015060 | VK Radio TG | 53 f1 | 67 c5 | 50535 | no |
| 0x00015080 | NXDN N America | ec 13 | d8 27 | 10200 | no |
| 0x000150a0 | Scotland TG | cb 6f | ff 5b | 23551 | no |
| 0x000150c0 | Utah DRN 01 | 37 4f | 03 7b | 31491 | no |
| 0x000150e0 | Utah DRN 05 | 33 4f | 07 7b | 31495 | no |
| 0x00015100 | PA7LIM TG | fc 7b | c8 4f | 20424 | no |
| 0x00015120 | Disconnect TG | 3b 13 | 0f 27 | 9999 | no |
| 0x00015140 | Hot n Sexy | 37 4f | 03 7b | 31491 | no |
| 0x00015160 | Lookout Mtn TG | 49 9d | 7d a9 | 43389 | no |
| 0x00015180 | AK7AN TG | 29 67 | 1d 53 | 21277 | no |
| 0x000151a0 | GROUP ID 0018 | 53 1f | 67 2b | 11111 | no |
| 0x000151c0 | GROUP ID 0019 | fa 62 | ce 56 | 22222 | no |
| 0x000151e0 | GROUP ID 0020 | 01 b6 | 35 82 | 33333 | no |
| 0x00015200 | GROUP ID 0021 | a8 99 | 9c ad | 44444 | no |
| 0x00015220 | GROUP ID 0022 | 37 ed | 03 d9 | 55555 | no |
| 0x00015240 | GROUP ID 0023 | 30 ed | 04 d9 | 55556 | no |
| 0x00015260 | BY BY | a9 99 | 9d ad | 44445 | no |
| 0x00015280 | GROUP ID 0025 | 03 b6 | 37 82 | 33335 | no |
| 0x000152a0 | GROUP ID 0026 | fb 62 | cf 56 | 22223 | no |
| 0x000152c0 | GROUP ID 0027 | d5 ec | e1 d8 | 55521 | no |
| 0x000152e0 | GROUP ID 0028 | d6 1f | e2 2b | 11234 | no |
| 0x00015300 | GROUP ID 0029 | 6c 18 | 58 2c | 11352 | no |
| 0x00015320 | GROUP ID 0030 | 91 cf | a5 fb | 64421 | no |

### Following Records
| Offset | Decoded Name | Raw +19/+20 | LE Value | Empty | Printable Name |
| --- | --- | --- | --- | --- | --- |
| 0x00015340 | �������������� | cb cb | 65535 | yes | no |
| 0x00015360 | �������������� | cb cb | 65535 | yes | no |
| 0x00015380 | �������������� | cb cb | 65535 | yes | no |
| 0x000153a0 | �������������� | cb cb | 65535 | yes | no |
| 0x000153c0 | �������������� | cb cb | 65535 | yes | no |
| 0x000153e0 | �������������� | cb cb | 65535 | yes | no |
| 0x00015400 | �������������� | cb cb | 65535 | yes | no |
| 0x00015420 | �������������� | cb cb | 65535 | yes | no |

