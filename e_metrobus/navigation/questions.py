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


def get_points_for_category(category: str, session):
    if category not in session['questions']:
        return 0
