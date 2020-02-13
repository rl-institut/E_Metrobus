
import uuid
from django.db import models

from e_metrobus.navigation import questions


class Score(models.Model):
    score = models.IntegerField()
    hash = models.CharField(max_length=32)

    @classmethod
    def save_score(cls, session):
        score = cls(score=questions.get_total_score(session), hash=uuid.uuid4().hex)
        score.save()
        return score
