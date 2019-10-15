
from django.views.generic import TemplateView

from e_metrobus.navigation import widgets


class StartView(TemplateView):
    template_name = "navigation/start.html"


class RouteView(TemplateView):
    template_name = "navigation/route.html"

    def post(self, request, *args, **kwargs):
        request.session['status'] = 'Status gesetzt'
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ComparisonView(TemplateView):
    template_name = "navigation/comparison.html"

    def get_context_data(self, **kwargs):
        return {
            'top_bar': widgets.TopBarWidget(
                title="E-Metrobus",
                title_icon="/static/images/icons/Icon_E_Bus_Front.svg"
            )
        }


class DashboardView(TemplateView):
    template_name = "navigation/dashboard.html"

class TopBarView(TemplateView):
    template_name = "navigation/top-bar.html"
