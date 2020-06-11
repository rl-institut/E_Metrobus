from django import forms

from e_metrobus.navigation.models import Feedback, Bug
from e_metrobus.navigation.widgets import FeedbackStarsWidget, FeedbackCommentWidget


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"
        labels = {
            "question1": "Frage 1:",
            "question2": "Frage 2:",
            "question3": "Frage 3:",
            "comment": "Schreib uns Deine Meinung/Kritik:",
        }
        widgets = {
            "question1": FeedbackStarsWidget,
            "question2": FeedbackStarsWidget,
            "question3": FeedbackStarsWidget,
            "comment": FeedbackCommentWidget
        }

    class Media:
        js = ("js/feedback.js",)


class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ("type", "description")
