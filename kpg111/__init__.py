"""Helpers for Kenwood KPG111 Program.dat research."""

from .decoder import decode_program_tables, decode_table
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
    "edit_record",
    "rename_record",
]
