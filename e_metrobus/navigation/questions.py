import os
from typing import List, Dict
from dataclasses import dataclass
from configobj import ConfigObj

from django.conf import settings


SCORE_WRONG = 5
SCORE_CORRECT = 10
SCORE_CATEGORY_COMPLETE = 11


@dataclass
class Question:
    question: str
    answers: List[str]
    correct: int
    template: str


@dataclass
class Category:
    label: str
    questions: Dict[str, Question]


question_config = ConfigObj(
    os.path.join(settings.APPS_DIR, "navigation", "questions.cfg")
)
QUESTIONS = {}

for cat in question_config:
    questions = {}
    for q in question_config[cat]["questions"]:
        questions[q] = Question(
            template=f"{cat}/{q}.html", **question_config[cat]["questions"][q]
        )
    QUESTIONS[cat] = Category(label=question_config[cat]["label"], questions=questions)


def get_score_for_category(category: str, session):
    if category not in QUESTIONS:
        raise KeyError(f'No such category "{category}"')

    if category not in session["questions"]:
        return 0

    score = 0
    for question_name in session["questions"][category]:
        if question_name not in QUESTIONS[category].questions:
            raise KeyError(f'No question "{question_name} in category "{category}"')
        if session["questions"][category][question_name]:
            score += SCORE_CORRECT
        else:
            score += SCORE_WRONG
    if all(
        [
            question in session["questions"][category]
            for question in QUESTIONS[category].questions
        ]
    ):
        score += SCORE_CATEGORY_COMPLETE
    return score
