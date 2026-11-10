"""Regression tests for offline QCET planning helpers. No network/file writes."""
import copy
from datetime import date, timedelta
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from periods import build_period, month_bounds, split_weeks
from validate_plan import check_plan


class PeriodTests(unittest.TestCase):
    def test_month_october(self):
        plan = build_period("2026-10")
        self.assertEqual((plan["period_start"], plan["period_end"]), ("2026-09-25", "2026-10-24"))
        self.assertEqual(plan["days"], 30)
        self.assertEqual(plan["weeks"][0], {"start": "2026-09-25", "end": "2026-09-27", "partial": True})
        self.assertEqual(plan["weeks"][-1], {"start": "2026-10-19", "end": "2026-10-24", "partial": True})

    def test_year_change(self):
        self.assertEqual(tuple(map(str, month_bounds("2027-01"))), ("2026-12-25", "2027-01-24"))

    def test_february_leap(self):
        self.assertEqual(tuple(map(str, month_bounds("2024-03"))), ("2024-02-25", "2024-03-24"))

    def test_weeks_contiguous(self):
        p = build_period("2026-10")
        days = []
        for w in p["weeks"]:
            a, b = date.fromisoformat(w["start"]), date.fromisoformat(w["end"])
            days += [a + timedelta(days=i) for i in range((b-a).days+1)]
        self.assertEqual(len(days), len(set(days)))
        self.assertEqual(days[0].isoformat(), p["period_start"])
        self.assertEqual(days[-1].isoformat(), p["period_end"])

    def test_invalid_month(self):
        for label in ("2026-13", "2026-0", "20-02", "2026/10", "2026-1"):
            with self.subTest(label=label), self.assertRaises(ValueError):
                month_bounds(label)


class PlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample = json.loads((HERE / "examples" / "plan-2026-10.sample.json").read_text(encoding="utf-8"))

    def test_sample_valid_with_unconfirmed_owner_warnings(self):
        errs, warns = check_plan(copy.deepcopy(self.sample))
        self.assertEqual(errs, [])
        self.assertIn("OWNER_UNCONFIRMED", [w["code"] for w in warns])
        self.assertNotIn("COVERAGE", [w["code"] for w in warns])

    def test_invalid_25_24(self):
        plan = copy.deepcopy(self.sample)
        plan["period_end"] = "2026-10-25"
        errs, _ = check_plan(plan)
        self.assertIn("MONTH_25_24", [e["code"] for e in errs])

    def test_child_outside_parent(self):
        plan = copy.deepcopy(self.sample)
        day = next(t for t in plan["tasks"] if t["id"] == "MGT-D")
        day["start"] = day["end"] = "2026-10-12"
        errs, _ = check_plan(plan)
        self.assertIn("CHILD_OUTSIDE", [e["code"] for e in errs])

    def test_no_fabricated_evidence(self):
        plan = copy.deepcopy(self.sample)
        plan["tasks"][0]["status"] = "done"
        errs, _ = check_plan(plan)
        self.assertIn("EVIDENCE", [e["code"] for e in errs])

    def test_hours_only_day(self):
        plan = copy.deepcopy(self.sample)
        plan["tasks"][0]["hours_planned"] = 1904
        errs, _ = check_plan(plan)
        self.assertIn("HOURS_LEVEL", [e["code"] for e in errs])

    def test_group_coverage(self):
        plan = copy.deepcopy(self.sample)
        plan["tasks"] = [t for t in plan["tasks"] if t["position_group"] != "EDU_SUPPORT"]
        _, warns = check_plan(plan)
        self.assertIn("COVERAGE", [w["code"] for w in warns])

    def test_unknown_source(self):
        plan = copy.deepcopy(self.sample)
        plan["tasks"][0]["source_ref"] = "FAKE"
        errs, _ = check_plan(plan)
        self.assertIn("SOURCE_REF", [e["code"] for e in errs])

    def test_week_boundary(self):
        plan = copy.deepcopy(self.sample)
        week = next(t for t in plan["tasks"] if t["id"] == "MGT-W")
        week["end"] = "2026-10-10"
        errs, _ = check_plan(plan)
        self.assertIn("WEEK_BOUNDS", [e["code"] for e in errs])


if __name__ == "__main__":
    unittest.main()
