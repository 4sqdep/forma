from django.urls import include, path

app_name = "statement"

urlpatterns = [
    path(
        "statement/",
        include(
            ("main.apps.statement.urls.statement", "main.apps.statement.urls.statement"),
            namespace="statement",
        ),
    ),
    path(
        "statement-information/",
        include(
            ("main.apps.statement.urls.statement_information", "main.apps.statement.urls.statement_information"),
            namespace="statement_information",
        ),
    ),
]