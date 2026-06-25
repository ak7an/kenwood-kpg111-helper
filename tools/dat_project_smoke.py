#!/usr/bin/env python3
"""Smoke test the read-only KPG111Project facade."""

from __future__ import annotations

import pprint
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kpg111.project import KPG111Project


IMPORT_PATH = Path("/tmp/kpg111_import_test.csv")
PROGRAM_PATH = Path("research/dattest/Dattest/AK7AN_Travel.dat")


def ensure_import_csv() -> None:
    if IMPORT_PATH.exists():
        return
    IMPORT_PATH.write_text(
        "\n".join(
            [
                "type,name,id",
                "TG,Parrot,10",
                "TG,NEW TEST TG,4242",
                "INDIVIDUAL,Curtis AE4BT,16042",
                "INDIVIDUAL,NEW TEST ID,42424",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    ensure_import_csv()
    project = KPG111Project()
    project.load_program(PROGRAM_PATH, 0x5B)
    project.import_csv(IMPORT_PATH)
    project.plan_merge()

    print("table summary:")
    pprint.pp(project.table_summary())
    print()
    print("import summary:")
    pprint.pp(project.import_summary())
    print()
    print("plan summary:")
    pprint.pp(project.plan_summary())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
