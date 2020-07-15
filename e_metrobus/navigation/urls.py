from django.urls import path

from e_metrobus.navigation import views

app_name = "navigation"
urlpatterns = [
    path("", view=views.LandingPageView.as_view(), name="landing_page"),
    path(
        "willkommen/",
        view=views.LandingPageView.as_view(non_bus_user=True),
        name="welcome",
    ),
    path("strecke/", view=views.RouteView.as_view(), name="route"),
    path("meine-strecke/", view=views.DisplayRouteView.as_view(), name="display_route"),
    path("mein-fussabdruck/", view=views.ComparisonView.as_view(), name="comparison"),
    path("umweltbilanz/", view=views.EnvironmentView.as_view(), name="environment"),
    path("quiz/", view=views.DashboardView.as_view(), name="dashboard"),
    path("quiz/<str:category>/", view=views.QuestionView.as_view(), name="question"),
    path("antwort/", view=views.AnswerView.as_view(), name="answer"),
    path("antwort/<str:category>/", view=views.AnswerView.as_view(), name="answer"),
    path("tour/", view=views.TourView.as_view(), name="tour"),
    path(
        "abgeschlossen/<str:category>/",
        view=views.CategoryFinishedView.as_view(),
        name="category_finished",
    ),
    path("abgeschlossen/", view=views.QuizFinishedView.as_view(), name="finished_quiz",),
    path("punkte/<str:hash>/", view=views.ShareScoreView.as_view(), name="score",),
    path(
        "zusammenfassung/",
        view=views.SummaryView.as_view(),
        name="questions_as_text",
    ),
    path("informationen/", view=views.LegalView.as_view(), name="legal"),
    path("accept_privacy_policy/", views.accept_privacy_policy),
    path("send_posthog_event/", views.send_posthog_event),
    path("get_comparison_chart/", views.get_comparison_chart),
]
