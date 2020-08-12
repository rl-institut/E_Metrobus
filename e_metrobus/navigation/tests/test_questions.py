from django.test import TestCase, tag

from e_metrobus.navigation import questions


@tag("questions")
class QuestionTestCase(TestCase):
    def setUp(self):
        self.session = {
            "stations": (3, 4),
            "questions": {
                "e_metrobus": {"loading_time": "2", "invalid": "1"},
                "ich": {
                    "advantages": ["0", "1", "4"],
                    "footprint": "1",
                    "e_bus": ["0", "1", "2"],
                    "lines": "2",
                },
                "politik": {"invalid": True},
            },
        }

    def test_score_category_empty(self):
        self.assertEqual(questions.get_score_for_category("umwelt", self.session), 0)

    def test_score_category_not_complete(self):
        self.assertEqual(
            questions.get_score_for_category("e_metrobus", self.session), 25
        )

    def test_score_category_complete(self):
        self.assertEqual(
            questions.get_score_for_category("ich", self.session),
            100,
        )

    def test_score_category_error(self):
        with self.assertRaises(KeyError):
            questions.get_score_for_category("not_there", self.session)

    def test_score_invalid_question(self):
        self.assertEqual(questions.get_score_for_category("politik", self.session), 0)

    def test_total_score(self):
        self.assertEqual(
            questions.get_total_score(self.session),
            31
        )

    def test_percentage(self):
        self.assertEqual(
            questions.get_category_shares("e_metrobus", self.session).done, 1 / 4
        )
        self.assertEqual(questions.get_category_shares("ich", self.session).done, 1)
        self.assertEqual(questions.get_category_shares("politik", self.session).done, 0)

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
            questions.QUESTIONS["umwelt"].questions["energy"],
        )

    def test_next_answer(self):
        self.assertEqual(questions.get_next_answer("e_metrobus"), "loading_time")
        self.assertEqual(
            questions.get_next_answer("e_metrobus", "loading_time"), "loading"
        )
        self.assertEqual(questions.get_next_answer("e_metrobus", "costs"), None)
