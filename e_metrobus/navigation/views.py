
from django.views.generic import TemplateView

from e_metrobus.navigation import widgets


class NavigationView(TemplateView):
    title = "E-Metrobus"
    title_icon = "/static/images/icons/Icon_E_Bus_Front.svg"
    title_alt = None
    back_url = ""

    def get_context_data(self, **kwargs):
        points = self.request.session.get("points", 0)
        return {
            'footer': widgets.FooterWidget(),
            'top_bar': widgets.TopBarWidget(
                title=self.title,
                title_icon=self.title_icon,
                title_alt=self.title_alt,
                back_url=self.back_url,
                points=points
            )
        }


class StartView(TemplateView):
    template_name = "navigation/start.html"


class RouteView(TemplateView):
    template_name = "navigation/route.html"

    def post(self, request, *args, **kwargs):
        request.session['status'] = 'Status gesetzt'
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ComparisonView(NavigationView):
    template_name = "navigation/comparison.html"


class DashboardView(TemplateView):
    template_name = "navigation/dashboard.html"
