import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

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
    comment = models.TextField(null=True, blank=True)


class Bug(models.Model):
    TECHNICAL = "technical"
    USAGE = "usage"
    CONTENT = "content"
    OTHER = "other"
    BUG_TYPES = (
        (TECHNICAL, _("Technisches Problem")),
        (USAGE, _("Schwierigkeit bei der Nutzung der App")),
        (CONTENT, _("Inkorrekter oder unverständlicher Inhalt")),
        (OTHER, _("Anderes")),
    )
    initial_descriptions = {
        TECHNICAL: _(
            "Etwas funktioniert nicht? Ein Link ist kaputt?"
        ),
        USAGE: _(
            "Ist etwas schwierig oder frustrierend zu nutzen?"
        ),
        CONTENT: _("Um welchen Inhalt geht es?"),
        OTHER: _("Kannst du uns dein Problem beschreiben?"),
    }
    type = models.CharField(
        max_length=20, default=None, choices=BUG_TYPES, verbose_name=_("Problem")
    )
    description = models.TextField(verbose_name=_("Beschreibung"))
