from django.urls import path

from e_metrobus.navigation import views

app_name = "navigation"
urlpatterns = [
    path("", view=views.LandingPageView.as_view(), name="landing_page"),
    path("route/", view=views.RouteView.as_view(), name="route"),
    path("display_route/", view=views.DisplayRouteView.as_view(), name="display_route"),
    path("comparison/", view=views.ComparisonView.as_view(), name="comparison"),
    path("dashboard/", view=views.DashboardView.as_view(), name="dashboard"),
    path("quiz/<str:category>/", view=views.QuestionView.as_view(), name="question"),
    path("answer/", view=views.AnswerView.as_view(), name="answer"),
    path(
        "finished/<str:category>/",
        view=views.CategoryFinishedView.as_view(),
        name="category_finished",
    ),
    path(
        "finished/",
        view=views.QuizFinishedView.as_view(),
        name="finished_quiz",
    ),
    path(
        "questions_as_text/",
        view=views.QuestionsAsTextView.as_view(),
        name="questions_as_text",
    ),
    path("legal/", view=views.LegalView.as_view(), name="legal"),
]
