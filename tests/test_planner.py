from pathlib import Path
import unittest

from kpg111.imports import load_import_csv
from kpg111.planner import plan_merge


FIXTURE = Path("data/normalized/dattest/Dattest/AK7AN_Travel.dat")


def import_csv() -> Path:
    path = Path("/tmp/kpg111_planner_test.csv")
    path.write_text(
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
    return path


class PlannerTests(unittest.TestCase):
    def test_expected_actions(self) -> None:
        records = load_import_csv(import_csv())
        plan = plan_merge(FIXTURE, 0x5B, records)
        by_name = {action.name: action for action in plan.actions}

        self.assertEqual(by_name["Parrot"].action, "duplicate_exact")

        tg = by_name["NEW TEST TG"]
        self.assertEqual(tg.action, "new_record")
        self.assertEqual(tg.chosen_offset, 0x151A0)

        curtis = by_name["Curtis AE4BT"]
        self.assertEqual(curtis.action, "possible_update")
        self.assertEqual(curtis.recommended_action, "review_update")

        individual = by_name["NEW TEST ID"]
        self.assertEqual(individual.action, "new_record")
        self.assertEqual(individual.chosen_offset, 0x10640)


if __name__ == "__main__":
    unittest.main()
