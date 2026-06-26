"""Main application coordinator for the read-only OpenKPG tkinter GUI."""

from __future__ import annotations

from pathlib import Path

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ModuleNotFoundError:  # pragma: no cover - depends on Python installation
    tk = None
    filedialog = None
    messagebox = None
    ttk = None

from openkpg.backend import OpenKPGProjectBackend

from .channel_tab import ChannelTab
from .compare_tab import CompareTab
from .helpers import DAT_HEADER_SIZE, LoadedDatSummary, detect_self_payload_xor_mask
from .hex_tab import HexRawTab
from .individual_tab import IndividualIdsTab
from .summary_tab import SummaryPanel
from .tg_tab import TalkGroupsTab


class OpenKPGTkApp:
    def __init__(self, root: tk.Tk) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.root = root
        self.root.title("OpenKPG")
        self.backend = OpenKPGProjectBackend()

        self.current_path: Path | None = None
        self.raw_bytes: bytes = b""
        self.xor_mask = 0x00
        self.all_talkgroups: list[object] = []
        self.all_contacts: list[object] = []

        self.status_path_var = tk.StringVar(value="File: none")
        self.status_size_var = tk.StringVar(value="Size: 0")
        self.status_tg_var = tk.StringVar(value="TG: 0")
        self.status_id_var = tk.StringVar(value="Individual IDs: 0")
        self.status_channel_var = tk.StringVar(value="Channels: 0")
        self.status_message_var = tk.StringVar(value="Ready")

        self._build_menu()
        self.summary_panel = SummaryPanel(root)
        self._build_status_bar()
        self._build_tabs()

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Open DAT", command=self.open_dat)
        file_menu.add_command(label="Open Baseline DAT for Compare", command=self.open_compare_baseline)
        file_menu.add_command(label="Open Modified DAT for Compare", command=self.open_compare_modified)
        file_menu.add_command(label="Reload", command=self.reload_dat)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menu_bar, tearoff=False)
        view_menu.add_command(label="Refresh current tab", command=self.refresh_current_tab)
        menu_bar.add_cascade(label="View", menu=view_menu)

        tools_menu = tk.Menu(menu_bar, tearoff=False)
        tools_menu.add_command(label="Run DAT Summary", command=self.run_dat_summary)
        tools_menu.add_command(label="Run Channel Layout Summary", command=self.run_channel_layout_summary)
        tools_menu.add_command(label="Run Compare", command=self.run_compare)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)

        help_menu = tk.Menu(menu_bar, tearoff=False)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def _build_status_bar(self) -> None:
        status = ttk.Frame(self.root, relief=tk.SUNKEN, padding=(6, 2))
        status.pack(side=tk.BOTTOM, fill=tk.X)
        for variable in (
            self.status_path_var,
            self.status_size_var,
            self.status_tg_var,
            self.status_id_var,
            self.status_channel_var,
            self.status_message_var,
        ):
            ttk.Label(status, textvariable=variable).pack(side=tk.LEFT, padx=(0, 12))

    def _build_tabs(self) -> None:
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        self.talk_groups_tab = TalkGroupsTab(self.notebook, self._copy_selected_record, self._set_status_message)
        self.individual_ids_tab = IndividualIdsTab(self.notebook, self._copy_selected_record, self._set_status_message)
        self.channel_tab = ChannelTab(
            self.notebook,
            self._set_text,
            self._show_error,
            self._show_info,
            self._set_channel_status,
        )
        self.hex_tab = HexRawTab(
            self.notebook,
            self.root,
            self._set_text,
            self._show_error,
            self._show_info,
            self._set_channel_status,
        )
        self.compare_tab = CompareTab(
            self.notebook,
            self._show_error,
            self._show_info,
            self._set_status_message,
        )

    def open_dat(self) -> None:
        path = self._ask_dat_path("Open DAT")
        if path is not None:
            self.load_dat_path(path)

    def reload_dat(self) -> None:
        if self.current_path is None:
            self._show_info("Reload", "No DAT file is currently loaded.")
            return
        self.load_dat_path(self.current_path)

    def open_compare_baseline(self) -> None:
        path = self._ask_dat_path("Open Baseline DAT for Compare")
        if path is None:
            return
        try:
            self.compare_tab.load_baseline(path)
        except ValueError as exc:
            self._show_error("Open Baseline DAT failed", str(exc))

    def open_compare_modified(self) -> None:
        path = self._ask_dat_path("Open Modified DAT for Compare")
        if path is None:
            return
        try:
            self.compare_tab.load_modified(path)
        except ValueError as exc:
            self._show_error("Open Modified DAT failed", str(exc))

    def _ask_dat_path(self, title: str) -> Path | None:
        if filedialog is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        filename = filedialog.askopenfilename(
            title=title,
            filetypes=(("DAT files", "*.dat"), ("All files", "*.*")),
        )
        if not filename:
            return None
        return Path(filename)

    def load_dat_path(self, path: Path) -> None:
        if not path.is_file():
            self._show_error("Open DAT failed", f"File does not exist: {path}")
            return

        self._set_status_message("Loading DAT...")
        self.root.configure(cursor="watch")
        self.root.update_idletasks()
        try:
            project = self.backend.load_dat(path)
            raw_bytes = self.backend.raw_bytes()
            xor_mask = detect_self_payload_xor_mask(raw_bytes)
            channel_rows = self.channel_tab.build_rows(raw_bytes, xor_mask)
        except Exception as exc:  # pragma: no cover - GUI error path
            self._show_error("Open DAT failed", str(exc))
            return
        finally:
            self.root.configure(cursor="")

        self.current_path = path
        self.raw_bytes = raw_bytes
        self.xor_mask = xor_mask
        self.all_talkgroups = list(project.talkgroups)
        self.all_contacts = list(project.contacts)

        self.summary_panel.load_file(path, raw_bytes, xor_mask)
        self.talk_groups_tab.load_records(self.all_talkgroups)
        self.individual_ids_tab.load_records(self.all_contacts)
        self.channel_tab.raw_bytes = raw_bytes
        self.channel_tab.xor_mask = xor_mask
        self.channel_tab.populate(channel_rows)
        self.hex_tab.load_file(raw_bytes)
        self._set_loaded_status(
            LoadedDatSummary(
                path=path,
                size=len(raw_bytes),
                talk_group_count=len(self.all_talkgroups),
                individual_id_count=len(self.all_contacts),
                channel_count=len(channel_rows),
            )
        )
        self._set_status_message("Loaded DAT")

    def refresh_current_tab(self) -> None:
        tab_text = self.notebook.tab(self.notebook.select(), "text")
        if tab_text == self.talk_groups_tab.tab_title:
            self.talk_groups_tab.refresh()
        elif tab_text == self.individual_ids_tab.tab_title:
            self.individual_ids_tab.refresh()
        elif tab_text == self.channel_tab.tab_title:
            self.channel_tab.refresh()
        elif tab_text == self.hex_tab.tab_title:
            self.hex_tab.refresh()
        elif tab_text == self.compare_tab.tab_title:
            self.compare_tab.refresh()
        self._set_status_message(f"Refreshed {tab_text}")

    def run_dat_summary(self) -> None:
        if self.current_path is None:
            self._show_info("DAT Summary", "No DAT file is currently loaded.")
            return
        self._show_info(
            "DAT Summary",
            "\n".join(
                (
                    f"File: {self.current_path}",
                    f"Size: {len(self.raw_bytes)} bytes",
                    f"Payload size: {max(0, len(self.raw_bytes) - DAT_HEADER_SIZE)} bytes",
                    f"Assumed XOR mask: 0x{self.xor_mask:02x}",
                    f"Talk Groups: {len(self.all_talkgroups)}",
                    f"Individual IDs: {len(self.all_contacts)}",
                    "Read-only GUI: no writing enabled.",
                )
            ),
        )

    def run_channel_layout_summary(self) -> None:
        if self.current_path is None:
            self._show_info("Channel Layout Summary", "No DAT file is currently loaded.")
            return
        self._show_info("Channel Layout Summary", self.channel_tab.layout_summary())

    def run_compare(self) -> None:
        self.compare_tab.run_compare()

    def show_about(self) -> None:
        self._show_info(
            "About OpenKPG",
            "OpenKPG tkinter GUI\n\nRead-only DAT browser.\nNo file writing is enabled.",
        )

    def _copy_selected_record(self, tree: ttk.Treeview) -> None:
        selection = tree.selection()
        if not selection:
            self._set_status_message("No row selected")
            return
        values = tree.item(selection[0], "values")
        self.root.clipboard_clear()
        self.root.clipboard_append("\t".join(str(value) for value in values))
        self._set_status_message("Copied selected row")

    def _set_loaded_status(self, summary: LoadedDatSummary) -> None:
        self.status_path_var.set(f"File: {summary.path}")
        self.status_size_var.set(f"Size: {summary.size} bytes")
        self.status_tg_var.set(f"TG: {summary.talk_group_count}")
        self.status_id_var.set(f"Individual IDs: {summary.individual_id_count}")
        self.status_channel_var.set(f"Channels: {summary.channel_count}")

    def _set_channel_status(self, channel_status: str | None, message: str) -> None:
        if channel_status is not None:
            self.status_channel_var.set(channel_status)
        self._set_status_message(message)

    def _set_status_message(self, message: str) -> None:
        self.status_message_var.set(message)

    def _set_text(self, widget: tk.Text, value: str) -> None:
        widget.configure(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
        widget.configure(state=tk.DISABLED)

    def _show_error(self, title: str, message: str) -> None:
        if messagebox is None:
            raise RuntimeError(message)
        messagebox.showerror(title, message)
        self._set_status_message(message)

    def _show_info(self, title: str, message: str) -> None:
        if messagebox is None:
            raise RuntimeError(message)
        messagebox.showinfo(title, message)
        self._set_status_message(title)


def main() -> int:
    if tk is None:
        raise RuntimeError("tkinter is not available in this Python installation")
    root = tk.Tk()
    root.geometry("1200x800")
    OpenKPGTkApp(root)
    root.mainloop()
    return 0
