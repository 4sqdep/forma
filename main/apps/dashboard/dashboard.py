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
    path(
        "document/",
        include(
            ("main.apps.dashboard.urls.document", "main.apps.dashboard.urls.document"),
            namespace="document",
        ),
    ),
    path(
        "installation-work/",
        include(
            ("main.apps.dashboard.urls.construction_installation_work", "main.apps.dashboard.urls.construction_installation_work"),
            namespace="construction_installation_work",
        ),
    ),
]