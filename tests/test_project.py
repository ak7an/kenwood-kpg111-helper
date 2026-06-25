from pathlib import Path
import unittest

from kpg111.project import KPG111Project


FIXTURE = Path("research/dattest/Dattest/AK7AN_Travel.dat")


def import_csv() -> Path:
    path = Path("/tmp/kpg111_project_test.csv")
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


class ProjectTests(unittest.TestCase):
    def test_project_workflow_summaries(self) -> None:
        project = KPG111Project()
        project.load_program(FIXTURE, 0x5B)
        table_summary = project.table_summary()
        self.assertEqual(table_summary["individual_ids"]["occupied"], 14)
        self.assertEqual(table_summary["talk_groups"]["occupied"], 17)

        project.import_csv(import_csv())
        import_summary = project.import_summary()
        self.assertEqual(import_summary["total"], 4)
        self.assertEqual(import_summary["individual_ids"], 2)
        self.assertEqual(import_summary["talk_groups"], 2)

        project.plan_merge()
        plan_summary = project.plan_summary()
        self.assertEqual(plan_summary["duplicate_exact"], 1)
        self.assertEqual(plan_summary["possible_update"], 1)
        self.assertEqual(plan_summary["new_record"], 2)
        self.assertEqual(plan_summary["invalid"], 0)


if __name__ == "__main__":
    unittest.main()
