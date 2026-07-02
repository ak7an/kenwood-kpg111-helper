"""Helpers for Kenwood KPG111 Program.dat research."""

from .decoder import decode_program_tables, decode_table
from .frequency import (
    decode_frequency_bytes,
    decode_frequency_low24,
    encode_frequency_hz,
    format_frequency_mhz,
    reconstruct_frequency,
)
from .individual_ids import IndividualIDChange, IndividualIDManager
from .model import DecodedRecord, ProgramTables
from .project import Codeplug, KPG111Project
from .talkgroups import TalkGroupChange, TalkGroupManager
from .writer import ByteRange, WriteResult, WriterError, edit_record, rename_record

__all__ = [
    "ByteRange",
    "Codeplug",
    "DecodedRecord",
    "IndividualIDChange",
    "IndividualIDManager",
    "KPG111Project",
    "ProgramTables",
    "TalkGroupChange",
    "TalkGroupManager",
    "WriteResult",
    "WriterError",
    "decode_program_tables",
    "decode_table",
    "decode_frequency_bytes",
    "decode_frequency_low24",
    "edit_record",
    "encode_frequency_hz",
    "format_frequency_mhz",
    "reconstruct_frequency",
    "rename_record",
]
