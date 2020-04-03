import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from e_metrobus.navigation import questions


class Score(models.Model):
    score = models.IntegerField()
    hash = models.CharField(max_length=32)

    @classmethod
    def save_score(cls, session):
        score = cls(score=questions.get_total_score(session), hash=uuid.uuid4().hex)
        score.save()
        return score


class Feedback(models.Model):
    question1 = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    question2 = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    question3 = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)
