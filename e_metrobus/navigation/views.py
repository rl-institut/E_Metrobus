
from django.views.generic import TemplateView
from django.shortcuts import redirect

from e_metrobus.navigation import widgets, constants


class StartView(TemplateView):
    template_name = "navigation/start.html"


class RouteView(TemplateView):
    template_name = "navigation/route.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context['stations'] = widgets.StationsWidget(constants.STATIONS, request)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        def get_stations():
            stations_raw = request.POST["stations"]
            start, end = stations_raw.split(',')
            return int(start[-2:]) - 1, int(end[-2:]) - 1

        request.session['stations'] = get_stations()
        return redirect('navigation:comparison')


class ComparisonView(TemplateView):
    template_name = "navigation/comparison.html"

    def get(self, request, *args, **kwargs):
        stations = request.session['stations']
        context = self.get_context_data(stations, **kwargs)
        return self.render_to_response(context)

    def get_context_data(self, stations, **kwargs):
        context = super(ComparisonView, self).get_context_data(**kwargs)
        context['stations'] = [constants.STATIONS[i] for i in stations]
        return context


class DashboardView(TemplateView):
    template_name = "navigation/dashboard.html"
