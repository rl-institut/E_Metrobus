import plotly
import plotly.graph_objects as go

from django.views.generic import TemplateView
from django.shortcuts import redirect

from e_metrobus.navigation import constants

from e_metrobus.navigation import widgets, utils


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
        return redirect("navigation:comparison")


class ComparisonView(NavigationView):
    template_name = "navigation/comparison.html"

    def get(self, request, *args, **kwargs):
        stations = request.session["stations"]
        context = self.get_context_data(stations, **kwargs)
        return self.render_to_response(context)

    def get_context_data(self, stations, **kwargs):
        context = super(ComparisonView, self).get_context_data(**kwargs)
        context["stations"] = [constants.STATIONS[i] for i in stations]
        return context


class DashboardView(NavigationView):
    template_name = "navigation/dashboard.html"


class LandingPageView(TemplateView):
    template_name = "navigation/landing-page.html"
    # Example config
    footer_links = {"pin": {"enabled": False}, "info": {"selected": True}}


class PlotlyView(TemplateView):
    template_name = "navigation/plotly.html"

    def get_context_data(self, **kwargs):
        context = super(PlotlyView, self).get_context_data(**kwargs)

        colors = ["Gainsboro",] * 5
        colors[2] = "black"

        # Plotly Figure:
        mobiles = ["Zu Fuß", "Fahrrad", "E-Bus", "Dieselbus", "PKW"]
        fig = go.Figure([go.Bar(x=mobiles, y=[5, 5, 20, 30, 40], marker_color=colors)])
        fig.layout.margin.t = 0
        fig.layout.margin.b = 0
        fig.layout.margin.l = 0
        fig.layout.margin.r = 0
        fig.layout.autosize = True
        fig.layout.plot_bgcolor = "#fff"
        fig.layout.yaxis.visible = False

        fig.add_layout_image(
            go.layout.Image(source="/static/images/icons/i_walk.svg", x=0, y=0.1)
        )
        fig.add_layout_image(
            go.layout.Image(source="/static/images/icons/i_bus.svg", x=1, y=0.1)
        )
        fig.update_layout_images(
            dict(
                xref="x", yref="paper", sizex=0.2, sizey=0.2, xanchor="right", yanchor="bottom"
            )
        )

        dj_fig = utils.DjangoFigure(fig, displayModeBar=False)
        context["plotly"] = dj_fig
        return context
