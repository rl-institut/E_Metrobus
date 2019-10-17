
from typing import List
from dataclasses import dataclass


SCORE_WRONG = 5
SCORE_CORRECT = 10
SCORE_CATEGORY_COMPLETE = 10


@dataclass
class Question:
    name: str
    url: str


@dataclass
class Category:
    name: str
    questions: List[Question]


QUESTIONS = [
    Category(
        name='Ich',
        questions=[Question(f'Q{i}', f'qurl_{i}') for i in range(3)]
    ),
    Category(
        name='Umwelt',
        questions=[Question(f'Q{i}', f'qurl_{i}') for i in range(3)]
    )
]


def get_points_for_category(category: str, session):
    if category not in session['questions']:
        return 0
