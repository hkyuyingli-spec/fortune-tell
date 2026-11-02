import json
import unittest
from pathlib import Path

from bazi_engine import analyze_bazi, get_bazi_reference


class BaziReferenceTests(unittest.TestCase):
    def test_reference_data_has_explicit_source_limits(self):
        path = Path(__file__).parent / "data" / "reference_bazi.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len(data["day_masters"]), 10)
        self.assertEqual(len(data["ten_gods"]), 10)
        self.assertEqual(len(data["elemental_counts"]), 10)
        self.assertEqual(len(data["source_notes"]), 1)

        source = data["source_notes"][0]
        self.assertEqual(source["verification_status"], "source_unknown_or_unverified")
        self.assertIn("does not independently validate", source["scope_note"])
        self.assertTrue(source["url"].startswith("https://"))

    def test_reference_output_distinguishes_locator_from_validated_meanings(self):
        pillars = {
            "year": "己卯",
            "month": "丙子",
            "day": "戊午",
            "hour": "戊午",
        }
        reference = get_bazi_reference(analyze_bazi(pillars))

        self.assertIn("BaZi reference (modern symbolic summaries)", reference)
        self.assertIn("Historical source locator — Yuanhai Ziping", reference)
        self.assertIn("source_unknown_or_unverified", reference)
        self.assertIn("does not independently validate", reference)


if __name__ == "__main__":
    unittest.main()
