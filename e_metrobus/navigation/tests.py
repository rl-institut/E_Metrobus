from django.test import TestCase

from e_metrobus.navigation import questions


class QuestionTestCase(TestCase):
    def setUp(self):
        self.session = {
            "stations": (3, 4),
            "questions": {
                "e_metrobus": {"electrification": True, "busses": False},
                "personal": {"ego": True},
                "politics": {"not_there": True},
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
            + questions.SCORE_CATEGORY_COMPLETE,
        )

    def test_score_category_not_complete(self):
        self.assertEqual(
            questions.get_score_for_category("personal", self.session),
            questions.SCORE_CORRECT,
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

    def test_percentage_complete(self):
        self.assertEqual(
            questions.get_category_done_percentage("e_metrobus", self.session), 1
        )

    def test_percentage_half(self):
        self.assertEqual(
            questions.get_category_done_percentage("personal", self.session), .5
        )

    def test_percentage_zero(self):
        self.assertEqual(
            questions.get_category_done_percentage("politics", self.session), 0
        )
