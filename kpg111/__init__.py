"""Helpers for Kenwood KPG111 Program.dat research."""

from .decoder import decode_program_tables, decode_table
from .frequency import (
    decode_frequency_bytes,
    decode_frequency_low24,
    encode_frequency_hz,
    format_frequency_mhz,
    reconstruct_frequency,
)
from .model import DecodedRecord, ProgramTables
from .project import KPG111Project
from .writer import ByteRange, WriteResult, WriterError, edit_record, rename_record

__all__ = [
    "ByteRange",
    "DecodedRecord",
    "KPG111Project",
    "ProgramTables",
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
