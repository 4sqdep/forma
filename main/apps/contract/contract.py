from django.urls import include, path

app_name = "contract"


urlpatterns = [
    path(
        "project-fund/",
        include(
            ("main.apps.project_document.urls.project_fund", "main.apps.project_document.urls.project_fund"),
            namespace="project_fund",
        ),
    ),
]