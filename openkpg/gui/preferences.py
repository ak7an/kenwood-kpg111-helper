"""Lightweight JSON preferences for the OpenKPG tkinter GUI."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path


DEFAULT_CHANNEL_START = "0x5E80"
DEFAULT_CHANNEL_STRIDE = "0x40"
DEFAULT_CHANNEL_COUNT = 128
MAX_RECENT_FILES = 10


def default_preferences_path() -> Path:
    return Path.home() / ".config" / "openkpg" / "preferences.json"


@dataclass
class Preferences:
    recent_files: list[str] = field(default_factory=list)
    last_open_dir: str = ""
    channel_start: str = DEFAULT_CHANNEL_START
    channel_stride: str = DEFAULT_CHANNEL_STRIDE
    channel_count: int = DEFAULT_CHANNEL_COUNT
    window_geometry: str = ""
    pane_position: int | None = None
    selected_tab: str = ""

    @classmethod
    def load(cls, path: Path | None = None) -> "Preferences":
        pref_path = default_preferences_path() if path is None else path
        try:
            data = json.loads(pref_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return cls()
        if not isinstance(data, dict):
            return cls()
        return cls(
            recent_files=_string_list(data.get("recent_files"))[:MAX_RECENT_FILES],
            last_open_dir=data.get("last_open_dir") if isinstance(data.get("last_open_dir"), str) else "",
            channel_start=data.get("channel_start") if isinstance(data.get("channel_start"), str) else DEFAULT_CHANNEL_START,
            channel_stride=data.get("channel_stride")
            if isinstance(data.get("channel_stride"), str)
            else DEFAULT_CHANNEL_STRIDE,
            channel_count=data.get("channel_count") if isinstance(data.get("channel_count"), int) else DEFAULT_CHANNEL_COUNT,
            window_geometry=data.get("window_geometry") if isinstance(data.get("window_geometry"), str) else "",
            pane_position=data.get("pane_position") if isinstance(data.get("pane_position"), int) else None,
            selected_tab=data.get("selected_tab") if isinstance(data.get("selected_tab"), str) else "",
        )

    def save(self, path: Path | None = None) -> None:
        pref_path = default_preferences_path() if path is None else path
        pref_path.parent.mkdir(parents=True, exist_ok=True)
        pref_path.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def to_dict(self) -> dict[str, object]:
        return {
            "recent_files": self.recent_files[:MAX_RECENT_FILES],
            "last_open_dir": self.last_open_dir,
            "channel_start": self.channel_start,
            "channel_stride": self.channel_stride,
            "channel_count": self.channel_count,
            "window_geometry": self.window_geometry,
            "pane_position": self.pane_position,
            "selected_tab": self.selected_tab,
        }

    def add_recent_file(self, path: Path | str) -> None:
        file_path = str(Path(path))
        self.recent_files = [recent for recent in self.recent_files if recent != file_path]
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:MAX_RECENT_FILES]
        parent = str(Path(file_path).parent)
        if parent != ".":
            self.last_open_dir = parent

    def clear_recent_files(self) -> None:
        self.recent_files.clear()

    def set_channel_defaults(self, start: str, stride: str, count: int) -> None:
        self.channel_start = start
        self.channel_stride = stride
        self.channel_count = count

    def set_window_state(self, geometry: str, pane_position: int | None, selected_tab: str) -> None:
        self.window_geometry = geometry
        self.pane_position = pane_position
        self.selected_tab = selected_tab


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]
