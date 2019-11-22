
from django.views.generic import TemplateView
from django.shortcuts import redirect

from e_metrobus.navigation import chart
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
            "footer": widgets.FooterWidget(links=self.footer_links),
            "top_bar": widgets.TopBarWidget(
                title=self.title,
                title_icon=self.title_icon,
                title_alt=self.title_alt,
                back_url=self.back_url,
                points=points,
            ),
        }


class RouteView(TemplateView):
    template_name = "navigation/route.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context["stations"] = widgets.StationsWidget(constants.STATIONS, request)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        def get_stations():
            stations_raw = request.POST["stations"]
            start, end = stations_raw.split(",")
            return int(start[-2:]) - 1, int(end[-2:]) - 1

        request.session["stations"] = get_stations()
        return redirect("navigation:display_route")


class DashboardView(NavigationView):
    template_name = "navigation/dashboard.html"


class DisplayRouteView(NavigationView):
    template_name = "navigation/display_route.html"

    def get_context_data(self, **kwargs):
        context = super(DisplayRouteView, self).get_context_data(**kwargs)
        context["stations"] = [
            constants.STATIONS[station] for station in self.request.session["stations"]
        ]
        return context


class LandingPageView(TemplateView):
    template_name = "navigation/landing-page.html"
    # Example config
    footer_links = {"pin": {"enabled": False}, "info": {"selected": True}}
    footer_links = {"pin": {"enabled": False}, "info": {"selected": True}}


class PlotlyView(TemplateView):
    template_name = "navigation/plotly.html"

    def get_context_data(self, **kwargs):
        context = super(PlotlyView, self).get_context_data(**kwargs)
        # context["plotly"] = chart.get_mobility_figure([5, 5, 10, 30, 50])
        context["plotly"] = chart.get_mobility_figure([50, 50, 100, 300, 500])
        return context
