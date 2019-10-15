from django.urls import path

from e_metrobus.navigation import views

app_name = "navigation"
urlpatterns = [
    path("", view=views.StartView.as_view(), name="start"),
    path("route/", view=views.RouteView.as_view(), name="route"),
    path("comparison/", view=views.ComparisonView.as_view(), name="comparison"),
    path("dashboard/", view=views.DashboardView.as_view(), name="dashboard"),
    path("top-bar/", view=views.TopBarView.as_view(), name="top-bar"),
    path("landing_page/", view=views.LandingPageView.as_view(), name="landingpage")
]
