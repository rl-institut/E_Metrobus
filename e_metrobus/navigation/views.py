from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, Http404, HttpResponse, redirect
from django.template.response import SimpleTemplateResponse
from django.views.generic import TemplateView

from e_metrobus.navigation import (
    chart,
    constants,
    forms,
    models,
    questions,
    stations,
    utils,
    widgets,
)


class CheckStationsMixin:
    def get(self, request, *args, **kwargs):
        if "stations" not in request.session:
            return redirect("navigation:route")
        return super(CheckStationsMixin, self).get(request, *args, **kwargs)


class FeedbackMixin:
    def get_context_data(self, **kwargs):
        context = super(FeedbackMixin, self).get_context_data(**kwargs)
        context["feedback"] = kwargs.get("feedback", forms.FeedbackForm(),)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and "feedback" in request.POST:
            feedback = forms.FeedbackForm(request.POST)
            if feedback.is_valid():
                utils.send_feedback(feedback.cleaned_data["comment"])
                feedback.save()
            else:
                kwargs["feedback"] = feedback
            return self.get(request, kwargs)
        return super(FeedbackMixin, self).dispatch(request, **kwargs)


class PosthogMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.session.session_key:
            request.session.save()

        utils.posthog_event(request)
        return super(PosthogMixin, self).dispatch(request, *args, **kwargs)


class NavigationView(PosthogMixin, TemplateView):
    title = "E-MetroBus"
    title_icon = "images/icons/i_ebus_black_fill.svg"
    title_alt = None
    back_url = "navigation:dashboard"
    top_bar_template = None
    footer_links = {}

    def get_context_data(self, **kwargs):
        context = super(NavigationView, self).get_context_data(**kwargs)
        score = questions.get_total_score(self.request.session)
        answers = questions.get_all_answers(self.request.session)
        context["footer"] = widgets.FooterWidget(links=self.footer_links)

        context["top_bar"] = widgets.TopBarWidget(
            title=self.title,
            title_icon=self.title_icon,
            title_alt=self.title_alt,
            back_url=self.back_url,
            score=score,
            answers=answers,
            template=self.top_bar_template,
            request=self.request,
            quiz_finished="hashed_score" in self.request.session
        )
        return context


class RouteView(PosthogMixin, TemplateView):
    template_name = "navigation/route.html"

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
        if "next" in request.GET:
            return redirect(f"navigation:{request.GET['next']}")
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
        if (
            questions.all_questions_answered(request.session)
            and "hashed_score" not in request.session
        ):
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
                    questions.get_category_answers(cat_name, self.request.session),
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
        request.session.save()
        return super(DisplayRouteView, self).get(request, *args, **kwargs)


class ComparisonView(CheckStationsMixin, NavigationView):
    template_name = "navigation/comparison.html"
    footer_links = {"dashboard": {"selected": True}}
    back_url = "navigation:route"
    top_bar_template = "widgets/top_bar_route.html"

    def get_context_data(self, **kwargs):
        context = super(ComparisonView, self).get_context_data(**kwargs)
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
        context["stations"] = current_stations
        context["charts"] = [
            f"{route}_{emission}"
            for route in ("route", "fleet")
            for emission in ("co2", "nitrogen", "fine_dust")
        ]
        context["route_distance"] = stations.STATIONS.get_distance(*current_stations)
        context["fleet_distance"] = utils.set_separators(constants.get_fleet_distance())
        context["fleet_start"] = constants.FLEET_START_DATE
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
        self.title = questions.QUESTIONS[kwargs["category"]].get_label()
        self.title_icon = questions.QUESTIONS[kwargs["category"]].small_icon

        context = super(QuestionView, self).get_context_data(**kwargs)
        context["answers"] = questions.get_category_answers(
            kwargs["category"], self.request.session
        )
        return context

    def get(self, request, *args, **kwargs):
        if kwargs["category"] in request.session["questions"] and request.session[
            "questions"
        ][kwargs["category"]].get("finished", False):
            next_answer = questions.get_next_answer(kwargs["category"])
            if next_answer is None:
                return redirect("navigation:dashboard")
            else:
                request.session["last_answered_question"] = next_answer
                return redirect("navigation:answer", category=kwargs["category"])

        next_question = questions.get_next_question(kwargs["category"], request.session)
        if next_question is None:
            request.session["questions"][kwargs["category"]]["finished"] = True
            request.session.save()
            return redirect("navigation:category_finished", category=kwargs["category"])

        context = self.get_context_data(**kwargs, question=next_question)
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        question = questions.get_question_from_name(request.POST["question"])
        if isinstance(question.correct, list):
            answer = request.POST.getlist("answer")
        else:
            answer = request.POST["answer"]

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

        return redirect("navigation:answer")


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
        answer = self.request.session["questions"][question.category][question.name]
        context["given_answer"] = list(map(int, answer))
        context["correct_answer"] = list(map(int, question.correct))
        context["flashes"] = questions.get_category_answers(
            question.category, self.request.session
        )
        if "category" in kwargs and self.request.session["questions"][
            kwargs["category"]
        ].get("finished", False):
            self.request.session["last_answered_question"] = questions.get_next_answer(
                kwargs["category"], self.request.session["last_answered_question"]
            )
            context["category_finished"] = True
        return context

    def get(self, request, **kwargs):
        question_name = request.session.get("last_answered_question")
        if question_name is None:
            return redirect("navigation:dashboard")
        question = questions.get_question_from_name(question_name)
        context = self.get_context_data(question=question, **kwargs)
        return self.render_to_response(context)


class CategoryFinishedView(PosthogMixin, TemplateView):
    template_name = "navigation/category_finished.html"

    def get_context_data(self, **kwargs):
        return {
            "category": questions.QUESTIONS[kwargs["category"]],
            "points": questions.SCORE_CATEGORY_COMPLETE,
        }


class QuizFinishedView(PosthogMixin, TemplateView):
    template_name = "navigation/quiz_finished.html"
    footer_links = {
        "info": {"enabled": True},
        "dashboard": {"enabled": True},
        "leaf": {"enabled": True},
        "results": {"enabled": True},
    }

    def get_context_data(self, **kwargs):
        context = super(QuizFinishedView, self).get_context_data(**kwargs)
        context["footer"] = widgets.FooterWidget(links=self.footer_links)
        answers = questions.get_all_answers(self.request.session)
        context["answers"] = answers
        percent = questions.get_total_score(self.request.session)
        context["score"] = percent
        context["slogan"] = utils.get_slogan(percent)
        context["share_url"] = utils.share_url(self.request)
        context["share_text"] = utils.share_text(self.request)
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


class ShareScoreView(PosthogMixin, TemplateView):
    template_name = "navigation/finished_base.html"

    def get_context_data(self, **kwargs):
        context = super(ShareScoreView, self).get_context_data(**kwargs)
        context["score"] = get_object_or_404(models.Score, hash=kwargs["hash"]).score
        return context


class LegalView(FeedbackMixin, NavigationView):
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
        context["bug"] = kwargs.get(
            "bug", forms.BugForm(initial={"type": models.Bug.TECHNICAL}),
        )
        return context

    def post(self, request, **kwargs):
        if "bug" in request.POST:
            bug = forms.BugForm(request.POST)
            if bug.is_valid():
                utils.send_bug_report(
                    f"E-MetroBus Bug found - {bug.cleaned_data['type']}",
                    bug.cleaned_data["description"],
                )
                bug.save()
            else:
                return self.render_to_response(self.get_context_data(bug=bug))
        if "feedback" in request.POST:
            return self.render_to_response(self.get_context_data(**kwargs))
        return redirect("navigation:legal")


class SummaryView(CheckStationsMixin, NavigationView):
    template_name = "navigation/summary.html"
    footer_links = {
        "info": {"enabled": True},
        "dashboard": {"enabled": True},
        "leaf": {"enabled": True},
        "results": {"selected": True},
    }


class LandingPageView(PosthogMixin, FeedbackMixin, TemplateView):
    template_name = "navigation/landing_page.html"
    footer_links = {"dashboard": {"selected": True}}
    non_bus_user = False

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        context["non_bus_user"] = self.non_bus_user
        if self.non_bus_user:
            # Set default route:
            self.request.session["non_bus_user"] = True
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

    def get(self, request, *args, **kwargs):
        if "non_bus_user" in request.session:
            self.template_name = "navigation/tour_non_bus_users.html"
        return self.render_to_response(self.get_context_data(**kwargs))


def accept_privacy_policy(request):
    request.session["privacy"] = True
    return HttpResponse()


def send_posthog_event(request):
    utils.posthog_event(request, event=request.GET["event"])
    return HttpResponse()


def get_comparison_chart(request):
    chart_order = ("pedestrian", "e-bus", "e-pkw", "bus", "car")
    route = request.GET["route"]
    if route == "route":
        current_stations = [
            stations.STATIONS[station] for station in request.session["stations"]
        ]
        route_data = stations.STATIONS.get_route_data(*current_stations)

    elif route == "fleet":
        route_data = stations.STATIONS.get_fleet_data()
    else:
        raise ValueError("Unknown route")

    if request.GET["emission"] == "co2":
        plotly_chart = chart.get_co2_figure(
            [route_data[vehicle].co2 for vehicle in chart_order]
        )
    elif request.GET["emission"] == "nitrogen":
        plotly_chart = chart.get_nitrogen_figure(
            [route_data[vehicle].nitrogen for vehicle in chart_order]
        )
    elif request.GET["emission"] == "fine_dust":
        plotly_chart = chart.get_fine_dust_figure(
            [route_data[vehicle].fine_dust for vehicle in chart_order]
        )
    else:
        raise ValueError("Unknown emission")
    return JsonResponse({"div": plotly_chart.div, "script": plotly_chart.script})


def get_desktop_page(request):
    return SimpleTemplateResponse("includes/desktop.html")
