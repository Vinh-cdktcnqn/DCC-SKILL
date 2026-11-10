"""No network, no real QCET data, no file mutations. Run with unittest."""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from periods import month_bounds, split_weeks
from validate_report import validate, evidence_is_confirmed
from draft_report import render

FIXTURE = json.loads((ROOT / "examples" / "report-2026-11.synthetic.json").read_text(encoding="utf-8"))


class ReportingTests(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(FIXTURE)

    def test_synthetic_fixture_passes_without_errors(self):
        e, w = validate(self.data)
        self.assertEqual(e, [])
        self.assertTrue(any("no reported observation" in x for x in w))

    def test_month_25_to_24(self):
        self.assertEqual(tuple(str(x) for x in month_bounds("2026-11")), ("2026-10-25", "2026-11-24"))

    def test_january_rollover(self):
        self.assertEqual(tuple(str(x) for x in month_bounds("2027-01")), ("2026-12-25", "2027-01-24"))

    def test_leap_day_handled(self):
        start, end = month_bounds("2024-03")
        self.assertEqual((end - start).days + 1, 29)

    def test_monthly_nonstandard_without_exception_fails(self):
        self.data["period"]["start"] = "2026-11-01"
        e, _ = validate(self.data)
        self.assertTrue(any("exception_reason required" in x for x in e))

    def test_monthly_exception_requires_human_review(self):
        self.data["period"]["start"] = "2026-11-01"
        self.data["period"]["exception_reason"] = "Source order specifies calendar month"
        e, w = validate(self.data)
        self.assertEqual(e, [])
        self.assertTrue(any("nonstandard monthly" in x for x in w))

    def test_cutoff_outside_period_fails(self):
        self.data["period"]["data_cutoff"] = "2026-12-01"
        e, _ = validate(self.data)
        self.assertTrue(any("data_cutoff" in x for x in e))

    def test_duplicate_result_id_fails(self):
        self.data["results"].append(copy.deepcopy(self.data["results"][0]))
        e, _ = validate(self.data)
        self.assertTrue(any("duplicate id" in x for x in e))

    def test_duplicate_deliverable_across_staff_fails(self):
        self.data["results"][1]["deliverables"][0]["id"] = "OUT-MGT"
        e, _ = validate(self.data)
        self.assertTrue(any("duplicate id 'OUT-MGT'" in x for x in e))

    def test_unknown_source_fails(self):
        self.data["evidence"][0]["source_id"] = "DOES-NOT-EXIST"
        e, _ = validate(self.data)
        self.assertTrue(any("unknown source" in x for x in e))

    def test_missing_evidence_reference_fails(self):
        self.data["results"][0]["evidence_ids"] = ["MISSING-EVIDENCE"]
        e, _ = validate(self.data)
        self.assertTrue(any("unknown evidence" in x for x in e))

    def test_unverified_completed_not_confirmed(self):
        self.data["evidence"][0]["verification"] = "pending"
        e, w = validate(self.data)
        self.assertEqual(e, [])
        self.assertTrue(any("completed result is NOT confirmed" in x for x in w))
        report = render(self.data)
        self.assertIn("Claimed complete, unverified", report)

    def test_draft_source_never_authoritative(self):
        self.data["evidence"][0]["source_id"] = "SRC-DRAFT"
        self.assertFalse(evidence_is_confirmed(["EV-MGT"], {x["id"]: x for x in self.data["evidence"]}, {x["id"]: x for x in self.data["sources"]}))

    def test_wrong_workstream_fails(self):
        self.data["metrics"][0]["workstream"] = "OTHER"
        e, _ = validate(self.data)
        self.assertTrue(any("unknown workstream" in x for x in e))

    def test_missing_owner_warns(self):
        self.data["plan"][0]["owner"] = None
        e, w = validate(self.data)
        self.assertEqual(e, [])
        self.assertTrue(any("missing assigned person" in x for x in w))

    def test_extra_plan_result_flagged(self):
        self.data["results"][0]["task_id"] = None
        e, w = validate(self.data)
        self.assertEqual(e, [])
        self.assertTrue(any("extra-plan" in x for x in w))

    def test_unmatched_plan_not_assumed_failed(self):
        self.data["results"] = [x for x in self.data["results"] if x["task_id"] != "P-MGT"]
        e, w = validate(self.data)
        self.assertEqual(e, [])
        self.assertTrue(any("NOT evidence of non-performance" in x for x in w))

    def test_ratio_math(self):
        self.data["metrics"][0].update({"aggregation": "ratio", "value": 75, "unit": "%", "numerator": 3, "denominator": 4})
        e, _ = validate(self.data)
        self.assertEqual(e, [])
        self.data["metrics"][0]["value"] = 70
        e, _ = validate(self.data)
        self.assertTrue(any("numerator/denominator" in x for x in e))

    def test_ratio_zero_denominator_fails(self):
        self.data["metrics"][0].update({"aggregation": "ratio", "value": 0, "numerator": 0, "denominator": 0})
        e, _ = validate(self.data)
        self.assertTrue(any("denominator >0" in x for x in e))

    def test_missing_not_zero(self):
        self.assertIsNone(self.data["metrics"][2]["value"])
        self.assertIn("NO DATA", render(self.data))

    def test_false_boolean_not_valid_number(self):
        self.data["metrics"][0]["value"] = True
        e, _ = validate(self.data)
        self.assertTrue(any("nonnegative finite number" in x for x in e))

    def test_no_monthly_assumption_for_quarterly(self):
        self.data["report_type"] = "quarterly"
        self.data["period"]["month"] = None
        self.data["period"]["label"] = "Official Q4 reporting period"
        e, _ = validate(self.data)
        self.assertEqual(e, [])

    def test_report_draft_separates_unverified_metric(self):
        output = render(self.data)
        self.assertIn("Unverified or missing metric: Sample learning-material", output)
        self.assertIn("SYNTHETIC FIXTURE", output)
        self.assertIn("NOT APPROVED", output)

    def test_source_files_unchanged_by_cli(self):
        sample = ROOT / "examples" / "report-2026-11.synthetic.json"
        before = sample.read_bytes()
        for script in ["validate_report.py", "draft_report.py"]:
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / script), str(sample)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, sample.read_bytes())

    def test_invalid_json_cli_exit_2(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "invalid.json"
            target.write_text("{oops", encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_report.py"), str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)

    def test_unusable_date_detected(self):
        self.data["results"][0]["activity_date"] = "2026-02-30"
        e, _ = validate(self.data)
        self.assertTrue(any("invalid calendar date" in x for x in e))


if __name__ == "__main__":
    unittest.main()
