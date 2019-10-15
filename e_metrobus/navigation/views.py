from django.views.generic import TemplateView


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


class DashboardView(TemplateView):
    template_name = "navigation/dashboard.html"

class LandingPageView(TemplateView):
    template_name = "navigation/landing_page.html"
