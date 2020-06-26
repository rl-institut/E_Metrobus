from django.shortcuts import redirect, Http404, get_object_or_404, HttpResponse
from django.views.generic import TemplateView

from e_metrobus.navigation import chart
from e_metrobus.navigation import constants
from e_metrobus.navigation import widgets
from e_metrobus.navigation import questions
from e_metrobus.navigation import models
from e_metrobus.navigation import stations
from e_metrobus.navigation import forms


class CheckStationsMixin:
    def get(self, request, *args, **kwargs):
        if "stations" not in request.session:
            return redirect("navigation:route")
        return super(CheckStationsMixin, self).get(request, *args, **kwargs)


class NavigationView(TemplateView):
    title = "E-MetroBus"
    title_icon = "images/icons/i_ebus_black_fill.svg"
    title_alt = None
    back_url = "navigation:dashboard"
    top_bar_template = None
    footer_links = {}

    def get_context_data(self, **kwargs):
        context = super(NavigationView, self).get_context_data(**kwargs)
        score = questions.get_total_score(self.request.session)
        context["footer"] = widgets.FooterWidget(links=self.footer_links)
        context["top_bar"] = widgets.TopBarWidget(
            title=self.title,
            title_icon=self.title_icon,
            title_alt=self.title_alt,
            back_url=self.back_url,
            score=score,
            template=self.top_bar_template,
            request=self.request,
        )
        return context


class RouteView(TemplateView):
    template_name = "navigation/route_dropdown.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["stations"] = stations.STATIONS.get_stations()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        def get_stations():
            start = request.POST["stationStart"]
            end = request.POST["stationEnd"]
            station_list = stations.STATIONS.get_stations()
            return station_list.index(start), station_list.index(end)

        request.session["stations"] = get_stations()
        return redirect("navigation:display_route")


class DashboardView(CheckStationsMixin, NavigationView):
    template_name = "navigation/dashboard.html"
    footer_links = {
        "info": {"enabled": True},
        "dashboard": {"selected": True},
        "leaf": {"enabled": True},
        "results": {"enabled": True},
    }
    back_url = None

    def get(self, request, *args, **kwargs):
        if questions.all_questions_answered(request.session):
            return redirect("navigation:finished_quiz")
        return super(DashboardView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        current_score = questions.get_total_score(self.request.session)
        if self.request.session.get("score_at_last_visit", 0) < current_score:
            self.request.session["score_at_last_visit"] = current_score
            context["top_bar"].score_changed = True

        categories = []
        for cat_name, category in questions.QUESTIONS.items():
            categories.append(
                (
                    cat_name,
                    category,
                    questions.get_category_answers(cat_name, self.request.session)
                )
            )
        context["categories"] = categories

        return context


class DisplayRouteView(CheckStationsMixin, NavigationView):
    template_name = "navigation/display_route.html"
    footer_links = {"dashboard": {"selected": True}}
    back_url = "navigation:route"
    top_bar_template = "widgets/top_bar_route.html"

    def get_context_data(self, **kwargs):
        context = super(DisplayRouteView, self).get_context_data(**kwargs)
        current_stations = [
            stations.STATIONS[station] for station in self.request.session["stations"]
        ]
        context["stations"] = current_stations
        context["distance"] = stations.STATIONS.get_distance(*current_stations)
        context["distance_in_meter"] = context["distance"] * 1000
        route_data = stations.STATIONS.get_route_data(*current_stations)
        context["co2"] = {
            "bus": {
                "percent": (route_data["bus"].co2 - route_data["e-bus"].co2)
                / route_data["bus"].co2
                * 100,
                "gram": route_data["bus"].co2 - route_data["e-bus"].co2,
            },
            "e_pkw": {
                "percent": (route_data["e-pkw"].co2 - route_data["e-bus"].co2)
                / route_data["e-pkw"].co2
                * 100,
                "gram": route_data["e-pkw"].co2 - route_data["e-bus"].co2,
            },
            "car": {
                "percent": (route_data["car"].co2 - route_data["e-bus"].co2)
                / route_data["car"].co2
                * 100,
                "gram": route_data["car"].co2 - route_data["e-bus"].co2,
            },
        }
        return context

    def get(self, request, *args, **kwargs):
        # Set first question as "answered":
        if "questions" not in request.session:
            request.session["questions"] = {}
        if "e_metrobus" not in request.session["questions"]:
            request.session["questions"]["e_metrobus"] = {}
        request.session["questions"]["e_metrobus"]["route"] = True
        request.session["last_answered_question"] = "route"
        request.session.save()
        return super(DisplayRouteView, self).get(request, *args, **kwargs)


class ComparisonView(CheckStationsMixin, NavigationView):
    template_name = "navigation/comparison.html"
    footer_links = {"dashboard": {"selected": True}}
    back_url = "navigation:route"
    top_bar_template = "widgets/top_bar_route.html"

    def get_context_data(self, **kwargs):
        context = super(ComparisonView, self).get_context_data(**kwargs)
        current_stations = [
            stations.STATIONS[station] for station in self.request.session["stations"]
        ]
        route_data = stations.STATIONS.get_route_data(*current_stations)
        chart_order = ("pedestrian", "e-bus", "e-pkw", "bus", "car")
        context["plotly"] = chart.get_mobility_figure(
            [int(route_data[vehicle].co2) for vehicle in chart_order]
        )
        context["info_table"] = widgets.InfoTable()
        if "first_time" not in self.request.session:
            self.request.session["first_time"] = False
            context["first_time"] = True
        return context


class EnvironmentView(CheckStationsMixin, NavigationView):
    template_name = "navigation/environment.html"
    footer_links = {
        "info": {"enabled": True},
        "dashboard": {"enabled": True},
        "leaf": {"selected": True},
        "results": {"enabled": True},
    }

    def get_context_data(self, **kwargs):
        context = super(EnvironmentView, self).get_context_data(**kwargs)

        current_stations = [
            stations.STATIONS[station] for station in self.request.session["stations"]
        ]
        e_bus_data = stations.STATIONS.get_route_data_for_vehicle(
            *current_stations, vehicle="e-bus"
        )
        user_consumption = constants.Consumption(
            distance=stations.STATIONS.get_distance(*current_stations),
            **e_bus_data.__dict__
        )
        bus_data = stations.STATIONS.get_route_data_for_vehicle(
            *current_stations, vehicle="bus"
        )
        bus_consumption = constants.Consumption(distance=1, **bus_data.__dict__)
        fleet_consumption = constants.FLEET_CONSUMPTION
        context["user"] = user_consumption
        context["fleet"] = fleet_consumption
        context["comparison"] = constants.Consumption(
            *(
                (x - y) / x * 100 if x != 0 else 0
                for x, y in zip(bus_consumption, user_consumption)
            )
        )
        return context


class QuestionView(NavigationView):
    template_name = "navigation/question.html"
    back_url = "navigation:dashboard"
    footer_links = {
        "info": {"enabled": True},
        "dashboard": {"selected": True},
        "leaf": {"enabled": True},
        "results": {"enabled": True},
    }

    def get_context_data(self, **kwargs):
        self.title = questions.QUESTIONS[kwargs["category"]].label
        self.title_icon = questions.QUESTIONS[kwargs["category"]].small_icon

        context = super(QuestionView, self).get_context_data(**kwargs)
        shares = questions.get_category_shares(
            category=kwargs["category"], session=self.request.session
        )
        context["category_percentage_done"] = round(shares.done * 100)
        context["category_percentage_correct"] = round(shares.correct * 100)
        return context

    def get(self, request, *args, **kwargs):
        next_question = questions.get_next_question(kwargs["category"], request.session)
        if next_question is None:
            return redirect("navigation:category_finished", category=kwargs["category"])

        context = self.get_context_data(**kwargs, question=next_question)
        return self.render_to_response(context)


class AnswerView(NavigationView):
    template_name = "navigation/answer.html"
    back_url = "navigation:dashboard"
    footer_links = {
        "info": {"enabled": True},
        "dashboard": {"selected": True},
        "leaf": {"enabled": True},
        "results": {"enabled": True},
    }

    def get_context_data(self, question, **kwargs):
        self.title = questions.QUESTIONS[question.category].label
        self.title_icon = questions.QUESTIONS[question.category].small_icon
        context = super(AnswerView, self).get_context_data(**kwargs)
        context["question"] = question
        return context

    def get(self, request, **kwargs):
        question_name = request.session.get("last_answered_question")
        if question_name is None:
            raise ValueError("No question answered yet!")
        question = questions.get_question_from_name(question_name)
        context = self.get_context_data(question=question, **kwargs)
        return self.render_to_response(context)


class AnswerScoreView(TemplateView):
    template_name = "navigation/answer_score.html"

    def get_context_data(self, question, answer, **kwargs):
        context = super(AnswerScoreView, self).get_context_data(**kwargs)
        context["answer"] = answer
        context["question"] = question
        context["points"] = questions.SCORE_CORRECT if answer else questions.SCORE_WRONG
        return context

    def post(self, request, **kwargs):
        question = questions.get_question_from_name(request.POST["question"])
        if isinstance(question.correct, list):
            answer = request.POST.getlist("answer") == [
                question.answers[i] for i in map(int, question.correct)
            ]
        else:
            answer = request.POST["answer"] == question.answers[int(question.correct)]

        if "questions" not in request.session:
            request.session["questions"] = {}
        if question.category not in request.session["questions"]:
            request.session["questions"][question.category] = {}
        if question.name in request.session["questions"][question.category]:
            raise ValueError("Answer already given")
        else:
            request.session["questions"][question.category][question.name] = answer
            request.session["last_answered_question"] = question.name
        request.session.save()

        context = self.get_context_data(question=question, answer=answer, **kwargs)
        return self.render_to_response(context)


class CategoryFinishedView(TemplateView):
    template_name = "navigation/category_finished.html"

    def get_context_data(self, **kwargs):
        return {
            "category": questions.QUESTIONS[kwargs["category"]],
            "points": questions.SCORE_CATEGORY_COMPLETE,
        }


class QuizFinishedView(TemplateView):
    template_name = "navigation/quiz_finished.html"

    def get_context_data(self, **kwargs):
        context = super(QuizFinishedView, self).get_context_data(**kwargs)
        context["points"] = questions.get_total_score(self.request.session)
        return context

    def get(self, request, *args, **kwargs):
        if not questions.all_questions_answered(request.session):
            raise Http404("Not all questions answered. Please go back to quiz.")
        if "hashed_score" not in request.session:
            score = models.Score.save_score(request.session)
            request.session["hashed_score"] = score.hash
            context = self.get_context_data(hash=score.hash, share=True)
        else:
            context = self.get_context_data(
                hash=request.session["hashed_score"], share=True
            )
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        if "reset" in request.POST:
            request.session.clear()
            return redirect("navigation:landing_page")


class ShareScoreView(TemplateView):
    template_name = "navigation/finished_base.html"

    def get_context_data(self, **kwargs):
        context = super(ShareScoreView, self).get_context_data(**kwargs)
        context["points"] = get_object_or_404(models.Score, hash=kwargs["hash"]).score
        return context


class LegalView(NavigationView):
    template_name = "navigation/legal.html"
    footer_links = {
        "info": {"selected": True},
        "dashboard": {"enabled": True},
        "leaf": {"enabled": True},
        "results": {"enabled": True},
    }

    def get_context_data(self, **kwargs):
        context = super(LegalView, self).get_context_data(**kwargs)
        context["info_table"] = widgets.InfoTable()
        context["feedback"] = kwargs.get(
            "feedback",
            forms.FeedbackForm(),
        )
        context["bug"] = kwargs.get(
            "bug", forms.BugForm(initial={"type": models.Bug.TECHNICAL}),
        )
        return context

    def post(self, request, **kwargs):
        if "bug" in request.POST:
            bug = forms.BugForm(request.POST)
            if bug.is_valid():
                bug.save()
            else:
                return self.render_to_response(self.get_context_data(bug=bug))
        elif "feedback" in request.POST:
            feedback = forms.FeedbackForm(request.POST)
            if feedback.is_valid():
                feedback.save()
            else:
                return self.render_to_response(self.get_context_data(feedback=feedback))
        return redirect("navigation:legal")


class QuestionsAsTextView(NavigationView):
    template_name = "navigation/questions_as_text.html"
    footer_links = {
        "info": {"enabled": True},
        "dashboard": {"enabled": True},
        "leaf": {"enabled": True},
        "results": {"selected": True},
    }

    def get_context_data(self, **kwargs):
        context = super(QuestionsAsTextView, self).get_context_data(**kwargs)
        context["categories"] = questions.QUESTIONS
        return context


class LandingPageView(TemplateView):
    template_name = "navigation/landing_page.html"
    footer_links = {"dashboard": {"selected": True}}
    non_bus_user = False

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        context["non_bus_user"] = self.non_bus_user
        if self.non_bus_user:
            # Set default route:
            self.request.session["stations"] = stations.DEFAULT_STATIONS
        if "visited" in self.request.GET:
            context["visited"] = True
        if "privacy" in self.request.session:
            context["privacy_accepted"] = True
        return context


class TourView(NavigationView):
    template_name = "navigation/tour.html"

    def get_context_data(self, **kwargs):
        context = super(TourView, self).get_context_data(**kwargs)
        return context


def accept_privacy_policy(request):
    request.session["privacy"] = True
    return HttpResponse()
