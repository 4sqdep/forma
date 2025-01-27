from django.urls import include, path

app_name = "reestr"

urlpatterns = [
    path(
        "construction/",
        include(
            ("main.apps.reestr.urls.construction", "main.apps.reestr.urls.construction"),
            namespace="construction",
        ),
    ),
]