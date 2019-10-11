from django.views.generic import TemplateView

from e_metrobus.navigation import widgets, constants


class StartView(TemplateView):
    template_name = "navigation/start.html"


class RouteView(TemplateView):
    template_name = "navigation/route.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context['stations'] = widgets.StationsWidget(constants.STATIONS)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        request.session['status'] = 'Status gesetzt'
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ComparisonView(TemplateView):
    template_name = "navigation/comparison.html"


class DashboardView(TemplateView):
    template_name = "navigation/dashboard.html"
