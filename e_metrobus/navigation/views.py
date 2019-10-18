from django.shortcuts import redirect
from django.views.generic import TemplateView

from e_metrobus.navigation import widgets, questions


class NavigationView(TemplateView):
    title = "E-Metrobus"
    title_icon = "images/icons/Icon_E_Bus_Front.svg"
    title_alt = None
    back_url = "navigation:dashboard"
    footer_links = {}

    def get_context_data(self, **kwargs):
        context = super(NavigationView, self).get_context_data(**kwargs)
        points = questions.get_total_score(self.request.session)
        context["footer"] = widgets.FooterWidget(links=self.footer_links)
        context["top_bar"] = widgets.TopBarWidget(
            title=self.title,
            title_icon=self.title_icon,
            title_alt=self.title_alt,
            back_url=self.back_url,
            points=points,
        )
        return context


class StartView(TemplateView):
    template_name = "navigation/start.html"


class RouteView(TemplateView):
    template_name = "navigation/route.html"

    def post(self, request, *args, **kwargs):
        request.session["status"] = "Status gesetzt"
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ComparisonView(NavigationView):
    template_name = "navigation/comparison.html"


class DashboardView(NavigationView):
    template_name = "navigation/dashboard.html"
    # Example config
    footer_links = {"pin": {"enabled": False}, "info": {"selected": True}}


class QuestionView(NavigationView):
    template_name = "navigation/question.html"
    back_url = "navigation:dashboard"

    def get(self, request, *args, **kwargs):
        category = kwargs["category"]
        next_question = questions.get_next_question(category, request.session)
        if next_question is None:
            return redirect("navigation:dashboard")

        context = self.get_context_data(**kwargs, question=next_question)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # Set top bar:
        self.title = questions.QUESTIONS[kwargs["category"]].label
        self.title_icon = questions.QUESTIONS[kwargs["category"]].icon

        return super(QuestionView, self).get_context_data(**kwargs)
