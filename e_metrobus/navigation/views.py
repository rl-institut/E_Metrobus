
import plotly
import plotly.graph_objects as go

from django.views.generic import TemplateView
from django.shortcuts import redirect

from e_metrobus.navigation import constants

from e_metrobus.navigation import widgets


class NavigationView(TemplateView):
    title = "E-Metrobus"
    title_icon = "/static/images/icons/Icon_E_Bus_Front.svg"
    title_alt = None
    back_url = ""
    footer_links = {}

    def get_context_data(self, **kwargs):
        points = self.request.session.get("points", 0)
        return {
            'footer': widgets.FooterWidget(links=self.footer_links),
            'top_bar': widgets.TopBarWidget(
                title=self.title,
                title_icon=self.title_icon,
                title_alt=self.title_alt,
                back_url=self.back_url,
                points=points
            )
        }


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


class ComparisonView(NavigationView):
    template_name = "navigation/comparison.html"

    def get(self, request, *args, **kwargs):
        stations = request.session['stations']
        context = self.get_context_data(stations, **kwargs)
        return self.render_to_response(context)

    def get_context_data(self, stations, **kwargs):
        context = super(ComparisonView, self).get_context_data(**kwargs)
        context['stations'] = [constants.STATIONS[i] for i in stations]
        return context


class DashboardView(NavigationView):
    template_name = "navigation/dashboard.html"


class LandingPageView(TemplateView):
    template_name = "navigation/landing-page.html"
    # Example config
    footer_links = {'pin': {'enabled': False}, 'info': {'selected': True}}


class PlotlyView(TemplateView):
    template_name = "navigation/plotly.html"

    def get_context_data(self, **kwargs):
        context = super(PlotlyView, self).get_context_data(**kwargs)

        # Plotly Figure:
        animals = ['giraffes', 'orangutans', 'monkeys']
        fig = go.Figure([go.Bar(x=animals, y=[20, 14, 23])])
        fig.layout.width = None
        fig.layout.height = None
        plotly_div = plotly.offline.plot(fig, include_plotlyjs=False, output_type="div")
        context["plotly"] = plotly_div
        script = plotly_div[plotly_div.find("<script") + len(
            '<script type="text/javascript">'):plotly_div.find("</script>")]
        div_id_start = plotly_div.find('<div id="') + 9
        div_id_end = plotly_div.find('"', div_id_start)
        context["plotly_id"] = plotly_div[div_id_start:div_id_end]
        return context
