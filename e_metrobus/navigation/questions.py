import os
from collections import namedtuple
from dataclasses import dataclass
from typing import Dict, List, Union
from enum import Enum

from configobj import ConfigObj
from django.conf import settings
from django.utils.html import format_html
from django.utils.translation import gettext as _

QUESTION_TEMPLATE_FOLDER = "questions"

SCORE_WRONG = 5
SCORE_CORRECT = 10
SCORE_CATEGORY_COMPLETE = 11

Shares = namedtuple("Shares", ["done", "correct"])


class Answer(Enum):
    Wrong = "wrong"
    Correct = "correct"
    Unanswered = "empty"

    @classmethod
    def get(cls, value):
        return {False: cls.Wrong, True: cls.Correct, None: cls.Unanswered}.get(
            value, cls.Unanswered
        )


@dataclass
class Question:
    name: str
    label: str
    question: str
    is_multiple_choice: bool
    answers: List[str]
    short_answer: str
    correct: Union[int, List[int]]
    template: str
    category: str

    def get_label(self):
        return _(self.label)


@dataclass
class Category:
    label: str
    icon: str
    small_icon: str
    questions: Dict[str, Question]

    def get_label(self):
        return _(self.label)


question_config = ConfigObj(
    os.path.join(settings.APPS_DIR, "navigation", "questions.cfg")
)
QUESTIONS = {}

for cat in question_config:
    questions = {}
    for q in question_config[cat]["questions"]:
        questions[q] = Question(
            template=f"{QUESTION_TEMPLATE_FOLDER}/{cat}/{q}.html",
            name=q,
            category=cat,
            is_multiple_choice=isinstance(
                question_config[cat]["questions"][q]["correct"], list
            ),
            label=format_html(question_config[cat]["questions"][q]["label"]),
            question=format_html(question_config[cat]["questions"][q]["question"]),
            answers=[
                format_html(answer)
                for answer in question_config[cat]["questions"][q]["answers"]
            ],
            short_answer=format_html(
                question_config[cat]["questions"][q]["short_answer"]
            ),
            correct=question_config[cat]["questions"][q]["correct"],
        )
    QUESTIONS[cat] = Category(
        label=question_config[cat]["label"],
        icon=question_config[cat]["icon"],
        small_icon=question_config[cat]["small_icon"],
        questions=questions,
    )


def get_score_for_category(category: str, session):
    if category not in QUESTIONS:
        raise KeyError(f'No such category "{category}"')

    if "questions" not in session or category not in session["questions"]:
        return 0

    score = 0
    for question_name in session["questions"][category]:
        if question_name not in QUESTIONS[category].questions:
            continue
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


def get_total_score(session):
    score = 0
    for category in QUESTIONS:
        score += get_score_for_category(category, session)
    return score


def get_category_shares(category, session):
    total = 0
    done = 0
    correct = 0
    if "questions" not in session or category not in session["questions"]:
        return Shares(0, 0)
    for question in QUESTIONS[category].questions:
        total += 1
        if question in session["questions"][category]:
            done += 1
            correct += session["questions"][category][question]
    return Shares(done / total, correct / total)


def get_category_answers(category, session):
    """Returns list of correct/wrong/unanswered questions for category"""
    if "questions" not in session or category not in session["questions"]:
        return [Answer.Unanswered for question in QUESTIONS[category].questions]
    return [
        Answer.get(session["questions"][category].get(question))
        for question in QUESTIONS[category].questions
    ]


def get_all_answers(session):
    answers = []
    for category in QUESTIONS:
        answers.extend(get_category_answers(category, session))
    return answers


def get_next_question(category, session):
    if category not in QUESTIONS:
        raise KeyError("Invalid category")
    if "questions" not in session or category not in session["questions"]:
        return list(QUESTIONS[category].questions.values())[0]
    for question_name, question in QUESTIONS[category].questions.items():
        if question_name not in session["questions"][category]:
            return question
    return None


def get_question_from_name(question_name):
    for category in QUESTIONS.values():
        if question_name in category.questions:
            return category.questions[question_name]
    raise KeyError(f'Question "{question_name}" not found.')


def all_questions_answered(session):
    for category in QUESTIONS:
        if get_category_shares(category, session).done != 1.0:
            return False
    return True
