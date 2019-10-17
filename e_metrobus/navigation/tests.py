
from django.test import TestCase

from e_metrobus.navigation import questions


class ScoreTestCase(TestCase):
    def setUp(self):
        self.session = {
            "stations": (3, 4),
            "questions": {'Ich': [True, False, True]}
        }

    def test_score_category0(self):
        self.assertEqual(questions.get_points_for_category("Umwelt", self.session), 0)

    def test_score_category25(self):
        self.assertEqual(
            questions.get_points_for_category("Ich", self.session),
            questions.SCORE_CORRECT * 2 + questions.SCORE_WRONG
        )
