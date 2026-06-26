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
from .explorer import CodeplugExplorer, ExplorerNode, channel_number_to_offset, explorer_model_for_dat
from .helpers import DAT_HEADER_SIZE, LoadedDatSummary, detect_self_payload_xor_mask
from .hex_tab import HexRawTab
from .individual_tab import IndividualIdsTab
from .preferences import Preferences
from .summary_tab import SummaryPanel
from .tg_tab import TalkGroupsTab
from .ui_helpers import coerce_pane_position, row_to_clipboard_text, valid_window_geometry


class OpenKPGTkApp:
    def __init__(self, root: tk.Tk) -> None:
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is not available in this Python installation")
        self.root = root
        self.root.title("OpenKPG")
        self.backend = OpenKPGProjectBackend()
        self.preferences = Preferences.load()

        self.current_path: Path | None = None
        self.raw_bytes: bytes = b""
        self.xor_mask = 0x00
        self.all_talkgroups: list[object] = []
        self.all_contacts: list[object] = []

        self.status_path_var = tk.StringVar(value="File: none")
        self.status_channel_current_var = tk.StringVar(value="Channel: none")
        self.status_tg_var = tk.StringVar(value="TG: 0")
        self.status_id_var = tk.StringVar(value="Individual IDs: 0")
        self.status_compare_var = tk.StringVar(value="Compare: not run")
        self.status_message_var = tk.StringVar(value="Ready")

        self._restore_window_geometry()
        self._build_menu()
        self._build_toolbar()
        self._build_status_bar()
        self._build_main_layout()
        self._bind_shortcuts()
        self._restore_selected_tab()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        self.file_menu = file_menu
        file_menu.add_command(label="Open DAT", command=self.open_dat)
        file_menu.add_command(label="Open Baseline DAT for Compare", command=self.open_compare_baseline)
        file_menu.add_command(label="Open Modified DAT for Compare", command=self.open_compare_modified)
        file_menu.add_command(label="Reload", command=self.reload_dat)
        self.recent_menu = tk.Menu(file_menu, tearoff=False)
        file_menu.add_cascade(label="Recent Files", menu=self.recent_menu)
        file_menu.add_command(label="Clear Recent Files", command=self.clear_recent_files)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self._rebuild_recent_menu()

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

    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self.root, padding=(6, 4))
        toolbar.pack(fill=tk.X)
        ttk.Button(toolbar, text="Open DAT", command=self.open_dat).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(toolbar, text="Reload", command=self.reload_dat).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(toolbar, text="Compare", command=self.run_compare).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(toolbar, text="Refresh", command=self.refresh_current_tab).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(toolbar, text="About", command=self.show_about).pack(side=tk.LEFT, padx=(0, 4))

    def _build_status_bar(self) -> None:
        status = ttk.Frame(self.root, relief=tk.SUNKEN, padding=(6, 2))
        status.pack(side=tk.BOTTOM, fill=tk.X)
        for variable in (
            self.status_path_var,
            self.status_channel_current_var,
            self.status_tg_var,
            self.status_id_var,
            self.status_compare_var,
            self.status_message_var,
        ):
            ttk.Label(status, textvariable=variable).pack(side=tk.LEFT, padx=(0, 12))

    def _build_main_layout(self) -> None:
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 8))

        self.explorer = CodeplugExplorer(self.main_pane, self._on_explorer_selected)

        right_frame = ttk.Frame(self.main_pane)
        self.main_pane.add(self.explorer.frame, weight=0)
        self.main_pane.add(right_frame, weight=1)
        pane_position = coerce_pane_position(self.preferences.pane_position)
        if pane_position is not None:
            self.root.after(100, lambda: self.main_pane.sashpos(0, pane_position))

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.summary_panel = SummaryPanel(self.notebook)
        self.talk_groups_tab = TalkGroupsTab(self.notebook, self.root, self._copy_selected_record, self._set_status_message)
        self.individual_ids_tab = IndividualIdsTab(
            self.notebook, self.root, self._copy_selected_record, self._set_status_message
        )
        self.channel_tab = ChannelTab(
            self.notebook,
            self.root,
            self._set_text,
            self._show_error,
            self._show_info,
            self._set_channel_status,
            initial_start=self.preferences.channel_start,
            initial_stride=self.preferences.channel_stride,
            initial_count=self.preferences.channel_count,
            preferences_callback=self._save_channel_preferences,
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
            self.root,
            self._show_error,
            self._show_info,
            self._set_status_message,
            result_callback=self._on_compare_result,
        )
        self.notebook.bind("<<NotebookTabChanged>>", lambda _event=None: self._remember_selected_tab())

    def open_dat(self) -> None:
        path = self._ask_dat_path("Open DAT")
        if path is not None:
            self.load_dat_path(path)

    def reload_dat(self) -> None:
        if self.current_path is None:
            self._show_info("Reload", "No DAT file is currently loaded. Open a DAT before reloading.")
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
        dialog_options: dict[str, object] = {
            "title": title,
            "filetypes": (("DAT files", "*.dat"), ("All files", "*.*")),
        }
        if self.preferences.last_open_dir:
            dialog_options["initialdir"] = self.preferences.last_open_dir
        filename = filedialog.askopenfilename(**dialog_options)
        if not filename:
            return None
        return Path(filename)

    def load_dat_path(self, path: Path) -> None:
        if not path.is_file():
            self._show_error("Missing file", f"The DAT file could not be found:\n{path}")
            return

        self._set_status_message(f"Loading {path.name}...")
        self.root.configure(cursor="watch")
        self.root.update_idletasks()
        try:
            project = self.backend.load_dat(path)
            raw_bytes = self.backend.raw_bytes()
            xor_mask = detect_self_payload_xor_mask(raw_bytes)
            channel_rows = self.channel_tab.build_rows(raw_bytes, xor_mask)
        except Exception as exc:  # pragma: no cover - GUI error path
            self._show_error("Invalid DAT", f"OpenKPG could not open this DAT file:\n{path}\n\n{exc}")
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
        self.explorer.load_model(
            explorer_model_for_dat(
                path=path,
                channel_count=len(channel_rows),
                talk_group_count=len(self.all_talkgroups),
                individual_id_count=len(self.all_contacts),
            )
        )
        self.preferences.add_recent_file(path)
        self._save_preferences()
        self._rebuild_recent_menu()
        self._set_status_message("Loaded DAT")

    def open_recent_file(self, path_text: str) -> None:
        path = Path(path_text)
        if not path.is_file():
            self._show_error("Missing recent file", f"The recent DAT file could not be found:\n{path}")
            return
        self.load_dat_path(path)

    def clear_recent_files(self) -> None:
        self.preferences.clear_recent_files()
        self._save_preferences()
        self._rebuild_recent_menu()
        self._set_status_message("Recent files cleared")

    def _rebuild_recent_menu(self) -> None:
        self.recent_menu.delete(0, tk.END)
        if not self.preferences.recent_files:
            self.recent_menu.add_command(label="No recent files", state=tk.DISABLED)
            return
        for recent in self.preferences.recent_files:
            self.recent_menu.add_command(label=recent, command=lambda path=recent: self.open_recent_file(path))

    def _save_channel_preferences(self, start: str, stride: str, count: int) -> None:
        self.preferences.set_channel_defaults(start, stride, count)
        self._save_preferences()

    def _save_preferences(self) -> None:
        try:
            self.preferences.save()
        except OSError as exc:
            self._set_status_message(f"Preferences not saved: {exc}")

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

    def _bind_shortcuts(self) -> None:
        self.root.bind("<Control-o>", lambda _event=None: self.open_dat())
        self.root.bind("<F5>", lambda _event=None: self.refresh_current_tab())
        self.root.bind("<Control-r>", lambda _event=None: self.reload_dat())
        self.root.bind("<Control-f>", lambda _event=None: self.focus_current_search())
        self.root.bind("<Control-Tab>", lambda _event=None: self.select_next_tab())

    def focus_current_search(self) -> None:
        tab = self._current_tab_object()
        if tab is not None and hasattr(tab, "focus_search"):
            tab.focus_search()

    def select_next_tab(self) -> None:
        tabs = self.notebook.tabs()
        if not tabs:
            return
        current = self.notebook.select()
        index = tabs.index(current) if current in tabs else 0
        self.notebook.select(tabs[(index + 1) % len(tabs)])

    def _current_tab_object(self) -> object | None:
        tab_text = self.notebook.tab(self.notebook.select(), "text")
        for tab in (
            self.summary_panel,
            self.talk_groups_tab,
            self.individual_ids_tab,
            self.channel_tab,
            self.hex_tab,
            self.compare_tab,
        ):
            if getattr(tab, "tab_title", None) == tab_text:
                return tab
        return None

    def _on_explorer_selected(self, node: ExplorerNode) -> None:
        if node.target in ("none", "root"):
            return
        if node.target == "summary":
            self._select_tab(self.summary_panel.tab_title)
        elif node.target == "talk_groups":
            self._select_tab(self.talk_groups_tab.tab_title)
        elif node.target == "individual_ids":
            self._select_tab(self.individual_ids_tab.tab_title)
        elif node.target == "channels":
            self._select_tab(self.channel_tab.tab_title)
        elif node.target == "channel" and node.channel_number is not None:
            self._select_tab(self.channel_tab.tab_title)
            self.channel_tab.select_channel(node.channel_number)
            self.status_channel_current_var.set(f"Channel: {node.channel_number}")
            try:
                self.hex_tab.jump_to_offset(channel_number_to_offset(node.channel_number))
            except ValueError:
                pass
        elif node.target == "hex":
            self._select_tab(self.hex_tab.tab_title)
        elif node.target == "compare":
            self._select_tab(self.compare_tab.tab_title)

    def _select_tab(self, tab_title: str) -> None:
        for tab_id in self.notebook.tabs():
            if self.notebook.tab(tab_id, "text") == tab_title:
                self.notebook.select(tab_id)
                return

    def _remember_selected_tab(self) -> None:
        if not hasattr(self, "notebook"):
            return
        selected = self.notebook.select()
        if selected:
            self.preferences.selected_tab = self.notebook.tab(selected, "text")

    def _restore_selected_tab(self) -> None:
        if self.preferences.selected_tab:
            self.root.after(100, lambda: self._select_tab(self.preferences.selected_tab))

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

    def _on_compare_result(self, result: object) -> None:
        self.channel_tab.set_compare_result(result)
        count = result.normalized_differing_byte_count
        self.status_compare_var.set(f"Compare: {count} diffs")

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
        self.root.clipboard_append(row_to_clipboard_text(values))
        self._set_status_message("Copied selected row")

    def _set_loaded_status(self, summary: LoadedDatSummary) -> None:
        self.status_path_var.set(f"File: {summary.path.name}")
        self.status_channel_current_var.set("Channel: none")
        self.status_tg_var.set(f"TG: {summary.talk_group_count}")
        self.status_id_var.set(f"Individual IDs: {summary.individual_id_count}")

    def _set_channel_status(self, channel_status: str | None, message: str) -> None:
        if channel_status is not None:
            self.status_channel_current_var.set(channel_status)
        self._set_status_message(message)

    def _set_status_message(self, message: str) -> None:
        self.status_message_var.set(message)

    def _set_text(self, widget: tk.Text, value: str) -> None:
        widget.configure(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
        widget.configure(state=tk.DISABLED)

    def _restore_window_geometry(self) -> None:
        geometry = valid_window_geometry(self.preferences.window_geometry)
        if geometry:
            self.root.geometry(geometry)

    def close(self) -> None:
        pane_position = None
        if hasattr(self, "main_pane"):
            try:
                pane_position = self.main_pane.sashpos(0)
            except tk.TclError:
                pane_position = None
        selected_tab = ""
        if hasattr(self, "notebook") and self.notebook.select():
            selected_tab = self.notebook.tab(self.notebook.select(), "text")
        self.preferences.set_window_state(self.root.geometry(), pane_position, selected_tab)
        self._save_preferences()
        self.root.destroy()

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
