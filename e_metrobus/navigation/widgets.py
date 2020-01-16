from collections import ChainMap

from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.forms.renderers import get_default_renderer
from django.templatetags.static import static
from django.template.context_processors import csrf


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
                '<script type="text/javascript" src="{}"></script>',
                static(path)
            ) for path in self.js
        ]
        return mark_safe('\n'.join(js))


class StationsWidget(CustomWidget):
    template_name = 'widgets/stations.html'
    js = ('js/stations.js',)

    def __init__(self, stations, request):
        self.stations = stations
        self.request = request

    def get_context(self, **kwargs):
        context = {'stations': self.stations}
        context.update(csrf(self.request))
        return context


class TopBarWidget(CustomWidget):
    template_name = "widgets/top_bar.html"

    def __init__(self, title, title_icon, back_url, points, title_alt=None):
        self.title = title
        self.title_icon = title_icon
        self.title_alt = title if title_alt is None else title_alt
        self.back_url = back_url
        self.points = points


class FooterWidget(CustomWidget):
    template_name = "widgets/footer.html"
    default_links = {
        "info": {
            "name": "info",
            "url": "navigation:dashboard",
            "enabled": False,
            "selected": False,
        },
        "leaf": {
            "name": "leaf",
            "url": "navigation:environment",
            "enabled": True,
            "selected": False,
        },
        "results": {
            "name": "results",
            "url": "navigation:questions_as_text",
            "enabled": True,
            "selected": False,
        },
        "dashboard": {
            "name": "quiz",
            "url": "navigation:dashboard",
            "enabled": True,
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
