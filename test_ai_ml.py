import unittest

from ai_chat import classify_question


class TestQuestionClassification(unittest.TestCase):
    def test_wealth_classification(self):
        label, confidence = classify_question("我想知道財運和投資機會會怎麼樣？")
        self.assertEqual(label, "wealth")
        self.assertGreater(confidence, 0.4)

    def test_career_classification(self):
        label, confidence = classify_question("我的工作發展和職涯方向怎麼看？")
        self.assertEqual(label, "career")
        self.assertGreater(confidence, 0.4)

    def test_love_classification(self):
        label, confidence = classify_question("我和另一半的緣分和感情模式是什麼？")
        self.assertEqual(label, "love")
        self.assertGreater(confidence, 0.4)


if __name__ == "__main__":
    unittest.main()
