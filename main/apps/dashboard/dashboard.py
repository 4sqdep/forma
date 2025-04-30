from django.urls import include, path


app_name = "dashboard"


urlpatterns = [
    path(
        "",
        include(
            ("main.apps.dashboard.urls.dashboard", "main.apps.dashboard.urls.dashboard"),
            namespace="dashboard",
        ),
    ),
]