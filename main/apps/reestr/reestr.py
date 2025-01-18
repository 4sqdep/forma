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
    path(
        "currency/",
        include(
            ("main.apps.reestr.urls.currency", "main.apps.reestr.urls.currency"),
            namespace="currency",
        ),
    ),
]