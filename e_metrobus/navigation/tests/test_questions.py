from django.test import TestCase, tag

from e_metrobus.navigation import questions


@tag("questions")
class QuestionTestCase(TestCase):
    def setUp(self):
        self.session = {
            "stations": (3, 4),
            "questions": {
                "e_metrobus": {"loading_time": True, "line_200": False},
                "ich": {"advantages": True},
                "politik": {"invalid": True},
            },
        }

    def test_score_category_empty(self):
        self.assertEqual(questions.get_score_for_category("umwelt", self.session), 0)

    def test_score_category_complete(self):
        self.assertEqual(
            questions.get_score_for_category("e_metrobus", self.session), 1 / 4
        )

    def test_score_category_not_complete(self):
        self.assertEqual(
            questions.get_score_for_category("ich", self.session),
            questions.SCORE_CORRECT + questions.SCORE_CATEGORY_COMPLETE,
        )

    def test_score_category_error(self):
        with self.assertRaises(KeyError):
            questions.get_score_for_category("not_there", self.session)

    def test_score_invalid_question(self):
        self.assertEqual(questions.get_score_for_category("politik", self.session), 0)

    def test_total_score(self):
        self.assertEqual(
            questions.get_total_score(self.session),
            questions.SCORE_CORRECT * 2
            + questions.SCORE_WRONG
            + questions.SCORE_CATEGORY_COMPLETE,
        )

    def test_percentage(self):
        self.assertEqual(
            questions.get_category_shares("e_metrobus", self.session).done, 1 / 4
        )
        self.assertEqual(questions.get_category_shares("ich", self.session), 1)
        self.assertEqual(questions.get_category_shares("politik", self.session), 0)

    def test_next_question(self):
        self.assertEqual(
            questions.get_next_question("e_metrobus", self.session),
            questions.QUESTIONS["e_metrobus"].questions["loading"],
        )
        self.assertIsNone(questions.get_next_question("ich", self.session))
        self.assertEqual(
            questions.get_next_question("politik", self.session),
            questions.QUESTIONS["politik"].questions["ebus_time"],
        )
        self.assertEqual(
            questions.get_next_question("umwelt", self.session),
            questions.QUESTIONS["umwelt"].questions["co2_reduction"],
        )

    def test_next_answer(self):
        self.assertEqual(questions.get_next_answer("e_metrobus"), "loading_time")
        self.assertEqual(
            questions.get_next_answer("e_metrobus", "loading_time"), "loading"
        )
        self.assertEqual(
            questions.get_next_answer("e_metrobus", "costs"), None
        )
