import re
import unittest
from urllib.parse import quote

from knowledge_lookup import (
    _load,
    _load_patterns,
    format_patterns,
    format_star_definitions,
    lookup_star_definitions,
)


class FakeChart:
    def __init__(self, rows):
        self.rows = rows

    def palace_table(self):
        return self.rows


class KnowledgeLookupTests(unittest.TestCase):
    def setUp(self):
        self.chart = FakeChart([
            {"palace": "命宮", "stars": ["紫微"]},
            {"palace": "夫妻", "stars": ["天機"]},
            {"palace": "官祿", "stars": ["武曲"]},
        ])

    def test_question_related_palace_precedes_life_palace(self):
        definitions = lookup_star_definitions(
            self.chart, max_stars=1, question="How should I approach my career?"
        )
        self.assertEqual([item["star_id"] for item in definitions], ["wuqu-star"])

    def test_chinese_question_prioritizes_its_palace(self):
        definitions = lookup_star_definitions(
            self.chart, max_stars=1, question="我想問工作方面的運勢"
        )
        self.assertEqual([item["star_id"] for item in definitions], ["wuqu-star"])

    def test_indonesian_question_prioritizes_its_palace(self):
        definitions = lookup_star_definitions(
            self.chart, max_stars=1, question="Bagaimana karier saya?"
        )
        self.assertEqual([item["star_id"] for item in definitions], ["wuqu-star"])

    def test_default_lookup_keeps_life_palace_priority(self):
        definitions = lookup_star_definitions(self.chart, max_stars=1)
        self.assertEqual([item["star_id"] for item in definitions], ["ziwei-star"])

    def test_english_format_omits_chinese_and_pinyin(self):
        definition = lookup_star_definitions(self.chart, max_stars=1)[0]
        formatted = format_star_definitions([definition], lang="en")
        self.assertIn("Star definitions:", formatted)
        self.assertIn("Provenance is unverified", formatted)
        self.assertIsNone(re.search(r"[\u4e00-\u9fff]", formatted))
        self.assertNotIn(definition["pinyin"], formatted)

    def test_chinese_format_marks_unverified_expansion(self):
        definition = lookup_star_definitions(self.chart, max_stars=1)[0]
        formatted = format_star_definitions([definition], lang="zh")
        self.assertIn("Classical:", formatted)
        self.assertIn("來源尚未核實", formatted)
        self.assertIn("並非確定預測或醫療建議", formatted)

    def test_reference_data_has_consistent_source_and_expansion_status(self):
        definitions = _load()
        self.assertEqual(len(definitions), 20)
        expanded_count = 0
        for definition in definitions:
            self.assertIn("classical_expansion", definition)
            expansion = definition.get("classical_expansion")
            if expansion is None:
                self.assertEqual(
                    definition["source"]["name"], "User-provided reference content"
                )
                self.assertIsNone(definition["source"]["url"])
                continue

            expanded_count += 1
            self.assertTrue(definition["source"]["url"])
            self.assertEqual(
                expansion["provenance"]["verification_status"],
                "transcription_located_edition_unverified",
            )
            self.assertIsNone(expansion["provenance"]["edition"])
            self.assertTrue(expansion["provenance"]["url"])
            self.assertTrue(expansion["modern_summary_en"])
            self.assertTrue(expansion["practical_advice"])
            self.assertTrue(expansion["interpretation_note"])
        self.assertEqual(expanded_count, 14)

    def test_english_and_indonesian_formats_include_caution(self):
        definition = lookup_star_definitions(self.chart, max_stars=1)[0]
        english = format_star_definitions([definition], lang="en")
        indonesian = format_star_definitions([definition], lang="id")
        self.assertIn("not a factual prediction or medical advice", english)
        self.assertIn("bukan prediksi pasti", indonesian)
        self.assertIn("Sumber belum diverifikasi", indonesian)

    def test_pattern_context_includes_source_and_unverified_status(self):
        pattern = _load_patterns()[0]
        formatted = format_patterns([pattern], lang="en")
        self.assertIn("Source: Zi Wei Dou Shu Quan Shu, Volume III", formatted)
        self.assertIn("print edition not independently verified", formatted)
        expected_url = quote(
            pattern["provenance"]["url"], safe=":/?#[]@!$&'()*+,;=%"
        )
        self.assertIn(expected_url, formatted)
        citation_lines = [
            line for line in formatted.splitlines()
            if line.strip().startswith(("Source:", "Source status:", "Source URL:"))
        ]
        self.assertTrue(citation_lines)
        self.assertIsNone(
            re.search(r"[\u4e00-\u9fff]", "\n".join(citation_lines))
        )

    def test_pattern_records_preserve_unverified_provenance(self):
        patterns = _load_patterns()
        self.assertEqual(len(patterns), 33)
        for pattern in patterns:
            self.assertTrue(pattern["classical_source"])
            self.assertTrue(pattern["provenance"]["url"])
            self.assertEqual(
                pattern["provenance"]["verification_status"],
                "transcription_located_edition_unverified",
            )
        formatted = format_patterns(patterns, lang="en")
        citation_lines = [
            line for line in formatted.splitlines()
            if line.strip().startswith(("Source:", "Source status:", "Source URL:"))
        ]
        self.assertEqual(
            sum(line.strip().startswith("Source URL:") for line in citation_lines),
            33,
        )
        self.assertIsNone(
            re.search(r"[\u4e00-\u9fff]", "\n".join(citation_lines))
        )


if __name__ == "__main__":
    unittest.main()
