"""Pure domain entities for OpenKPG."""

from .channel import Channel
from .contact import Contact
from .radio import Radio
from .scanlist import ScanList
from .talkgroup import TalkGroup
from .unknown_record import UnknownRecord
from .zone import Zone

__all__ = [
    "Channel",
    "Contact",
    "Radio",
    "ScanList",
    "TalkGroup",
    "UnknownRecord",
    "Zone",
]
