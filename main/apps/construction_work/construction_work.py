from django.urls import include, path

app_name = "construction_work"


urlpatterns = [
    path(
        "file/",
        include(
            ("main.apps.construction_work.urls.file", "main.apps.construction_work.urls.file"),
            namespace="file",
        ),
    ),
    path(
        "fund/",
        include(
            ("main.apps.construction_work.urls.fund", "main.apps.construction_work.urls.fund"),
            namespace="fund",
        ),
    ),
    path(
        "section/",
        include(
            ("main.apps.construction_work.urls.section", "main.apps.construction_work.urls.section"),
            namespace="section",
        ),
    ),
    path(
        "statistics/",
        include(
            ("main.apps.construction_work.urls.statistics", "main.apps.construction_work.urls.statistics"),
            namespace="statistics",
        ),
    ),
]