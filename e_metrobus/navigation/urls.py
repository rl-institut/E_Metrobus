from django.urls import path

from e_metrobus.navigation import views

app_name = "navigation"
urlpatterns = [
    path("", view=views.LandingPageView.as_view(), name="landing-page"),
    path("route/", view=views.RouteView.as_view(), name="route"),
    path("dashboard/", view=views.DashboardView.as_view(), name="dashboard"),
    path("comparison/", view=views.ComparisonView.as_view(), name="comparison"),
    path("display_route/", view=views.DisplayRouteView.as_view(), name="display_route"),
    path("legal/", view=views.LegalView.as_view(), name="legal"),
]
