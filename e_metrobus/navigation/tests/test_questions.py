from django.test import TestCase

from e_metrobus.navigation import questions


class QuestionTestCase(TestCase):
    def setUp(self):
        self.session = {
            "stations": (3, 4),
            "questions": {
                "e_metrobus": {"loading_time": True, "line_200": False},
                "personal": {"advantages": True},
                "politics": {"invalid": True},
            },
        }

    def test_score_category_empty(self):
        self.assertEqual(
            questions.get_score_for_category("environment", self.session), 0
        )

    def test_score_category_complete(self):
        self.assertEqual(
            questions.get_score_for_category("e_metrobus", self.session),
            questions.SCORE_CORRECT
            + questions.SCORE_WRONG
        )

    def test_score_category_not_complete(self):
        self.assertEqual(
            questions.get_score_for_category("personal", self.session),
            questions.SCORE_CORRECT + questions.SCORE_CATEGORY_COMPLETE
        )

    def test_score_category_error(self):
        with self.assertRaises(KeyError):
            questions.get_score_for_category("not_there", self.session)

    def test_score_invalid_question(self):
        self.assertEqual(questions.get_score_for_category("politics", self.session), 0)

    def test_total_score(self):
        self.assertEqual(
            questions.get_total_score(self.session),
            questions.SCORE_CORRECT * 2
            + questions.SCORE_WRONG
            + questions.SCORE_CATEGORY_COMPLETE,
        )

    def test_percentage(self):
        self.assertEqual(
            questions.get_category_done_share("e_metrobus", self.session), 2/3
        )
        self.assertEqual(
            questions.get_category_done_share("personal", self.session), 1
        )
        self.assertEqual(
            questions.get_category_done_share("politics", self.session), 0
        )

    def test_next_question(self):
        self.assertEqual(
            questions.get_next_question("e_metrobus", self.session),
            questions.QUESTIONS["e_metrobus"].questions["loading"],
        )
        self.assertIsNone(
            questions.get_next_question("personal", self.session)
        )
        self.assertEqual(
            questions.get_next_question("politics", self.session),
            questions.QUESTIONS["politics"].questions["ebus_time"],
        )
        self.assertEqual(
            questions.get_next_question("environment", self.session),
            questions.QUESTIONS["environment"].questions["co2_reduction"],
        )
