from django.urls import include, path

app_name = "project_document"


urlpatterns = [
    path(
        "project-fund/",
        include(
            ("main.apps.project_document.urls.project_fund", "main.apps.project_document.urls.project_fund"),
            namespace="project_fund",
        ),
    ),
    path(
        "project-document-type/",
        include(
            ("main.apps.project_document.urls.project_document_type", "main.apps.project_document.urls.project_document_type"),
            namespace="project_document_type",
        ),
    ),
    path(
        "project-file/",
        include(
            ("main.apps.project_document.urls.project_file", "main.apps.project_document.urls.project_file"),
            namespace="project_file",
        ),
    ),
    path(
        "project-section/",
        include(
            ("main.apps.project_document.urls.project_section", "main.apps.project_document.urls.project_section"),
            namespace="project_section",
        ),
    )
]