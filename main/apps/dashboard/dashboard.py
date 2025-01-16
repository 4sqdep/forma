from django.urls import include, path

app_name = "dashboard"

urlpatterns = [
    path(
        "dashboard/",
        include(
            ("main.apps.dashboard.urls.dashboard", "main.apps.dashboard.urls.dashboard"),
            namespace="dashboard",
        ),
    ),
    path(
        "document/",
        include(
            ("main.apps.dashboard.urls.document", "main.apps.dashboard.urls.document"),
            namespace="document",
        ),
    ),
]