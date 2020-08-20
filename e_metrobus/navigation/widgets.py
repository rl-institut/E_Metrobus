from collections import ChainMap

from django.forms import widgets
from django.forms.renderers import get_default_renderer
from django.template.context_processors import csrf
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from e_metrobus.navigation import constants, utils, questions


class CustomWidget:
    template_name = None
    js = tuple()

    def get_context(self, **kwargs):
        context = {**kwargs}
        context.update(**self.__dict__)
        return context

    def render(self, **kwargs):
        if self.template_name is None:
            raise ValueError("No template name given")
        return self._render(self.template_name, self.get_context(**kwargs))

    @staticmethod
    def _render(template_name, context, renderer=None):
        if renderer is None:
            renderer = get_default_renderer()
        return mark_safe(renderer.render(template_name, context))

    def __str__(self):
        return self.render()

    @property
    def media(self):
        """Include widget media (currently only js)"""
        js = [
            format_html(
                '<script type="text/javascript" src="{}"></script>', static(path)
            )
            for path in self.js
        ]
        return mark_safe("\n".join(js))


class StationsWidget(CustomWidget):
    template_name = "widgets/stations.html"
    js = ("js/stations.js",)

    def __init__(self, stations, request):
        self.stations = stations
        self.request = request

    def get_context(self, **kwargs):
        context = {"stations": self.stations}
        context.update(csrf(self.request))
        return context


class TopBarWidget(CustomWidget):
    template_name = "widgets/top_bar.html"

    def __init__(
        self,
        title,
        title_icon,
        back_url,
        score,
        answers,
        title_alt=None,
        template=None,
        request=None,
        quiz_finished=False
    ):
        if template:
            self.template_name = template
        self.title = title
        self.title_icon = title_icon
        self.title_alt = title if title_alt is None else title_alt
        self.back_url = back_url
        self.score = score
        self.answers = answers
        self.score_changed = False
        self.request = request
        self.share_link_js = True
        self.quiz_finished = quiz_finished

    def get_context(self, **kwargs):
        context = super(TopBarWidget, self).get_context(**kwargs)
        context["share_url"] = utils.share_url(self.request)
        context["share_text"] = utils.share_text(self.request)
        percent = questions.get_total_score(self.request.session)
        context["score"] = percent
        context["slogan"] = utils.get_slogan(percent)
        return context


class FooterWidget(CustomWidget):
    template_name = "widgets/footer.html"
    default_links = {
        "dashboard": {
            "name": "quiz",
            "label": _("Quiz"),
            "url": "navigation:dashboard",
            "enabled": False,
            "selected": False,
        },
        "leaf": {
            "name": "pin",
            "label": _("Meine Strecke"),
            "url": "navigation:environment",
            "enabled": False,
            "selected": False,
        },
        "results": {
            "name": "flash",
            "label": _("E-MetroBus"),
            "url": "navigation:questions_as_text",
            "enabled": False,
            "selected": False,
        },
        "info": {
            "name": "info",
            "label": _("Infos"),
            "url": "navigation:legal",
            "enabled": False,
            "selected": False,
        },
    }

    def __init__(self, links=None):
        if links is None:
            self.links = self.default_links
        else:
            self.links = {}
            for key, values in self.default_links.items():
                self.links[key] = ChainMap(links.get(key, {}), values)

    def get_context(self, **kwargs):
        return {"links": self.links}


class FeedbackStarsWidget(widgets.NumberInput):
    template_name = "widgets/feedback_stars.html"


class FeedbackCommentWidget(widgets.TextInput):
    template_name = "widgets/feedback_comment.html"


class InfoTable(CustomWidget):
    template_name = "widgets/info_table.html"

    def get_context(self, **kwargs):
        return {"vehicles": constants.VEHICLES, "sources": constants.DATA_SOURCES}
