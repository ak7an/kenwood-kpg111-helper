"""Individual IDs tab for the OpenKPG tkinter GUI."""

from __future__ import annotations

from .tg_tab import RecordTableTab


class IndividualIdsTab(RecordTableTab):
    tab_title = "Individual IDs"
    description = "Read-only decoded Individual ID records"
    count_label = "Individual ID rows"
