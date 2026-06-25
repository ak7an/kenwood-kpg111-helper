from pathlib import Path
import unittest

from kpg111.allocation import analyze_allocation


ROOTS = [
    Path("research/dattest"),
    Path("research/dattest2"),
    Path("research/dattest3"),
    Path("research/dattest4"),
]


class AllocationAnalysisTests(unittest.TestCase):
    def test_observed_reuse_and_append_events(self) -> None:
        analysis = analyze_allocation(ROOTS)
        keys = {
            (event.modified_path.name, event.table_id, event.slot, event.offset)
            for event in analysis.events
        }

        self.assertIn(("Program5.dat", "individual_ids", 9, 0x105A0), keys)
        self.assertIn(("Program5.dat", "individual_ids", 30, 0x10840), keys)
        self.assertIn(("Program5.dat", "talk_groups", 9, 0x150A0), keys)
        self.assertIn(("Program6.dat", "talk_groups", 30, 0x15340), keys)

    def test_observed_behavior_and_mechanism_confidence(self) -> None:
        analysis = analyze_allocation(ROOTS)
        policies = {policy.policy: policy for policy in analysis.policies}

        self.assertGreaterEqual(len(analysis.events), 1)
        observed = policies["observed first available empty record in slot order"]
        self.assertEqual(observed.confidence, "HIGH")
        self.assertEqual(observed.counterexamples, 0)
        self.assertEqual(policies["lowest-available-slot implementation"].confidence, "MODERATE")
        self.assertEqual(policies["sequential scan implementation"].confidence, "MODERATE")
        self.assertEqual(policies["append after last occupied"].confidence, "MODERATE")


if __name__ == "__main__":
    unittest.main()
