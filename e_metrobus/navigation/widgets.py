
from abc import abstractmethod

from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.forms.renderers import get_default_renderer
from django.templatetags.static import static


class CustomWidget:
    template_name = None
    js = tuple()

    @abstractmethod
    def get_context(self, **kwargs):
        pass

    def render(self, **kwargs):
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

    def __init__(self, stations):
        self.stations = stations

    def get_context(self, **kwargs):
        return {'stations': self.stations}
