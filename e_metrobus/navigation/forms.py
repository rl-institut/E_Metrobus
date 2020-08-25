import json

from django import forms
from django.utils.safestring import mark_safe

from e_metrobus.navigation.models import Bug, Feedback
from e_metrobus.navigation.widgets import FeedbackCommentWidget
from django.utils.translation import gettext_lazy as _


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("comment",)
        labels = {
            "comment": _("Schreib uns deine Meinung/Kritik:"),
        }
        widgets = {
            "comment": FeedbackCommentWidget
        }


class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ("type", "description")

    @property
    def descriptions(self):
        return mark_safe(self.Meta.model.initial_descriptions)
