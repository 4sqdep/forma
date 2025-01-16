from django.urls import include, path

app_name = "account"

urlpatterns = [
    path(
        "user/",
        include(
            ("main.apps.account.urls.user", "main.apps.account.urls.user"),
            namespace="account",
        ),
    ),
    # path(
    #     "department/",
    #     include(
    #         ("main.apps.dashboard.urls.department", "main.apps.dashboard.urls.department"),
    #         namespace="department",
    #     ),
    # ),
    # path(
    #     "position/",
    #     include(
    #         ("main.apps.dashboard.urls.position", "main.apps.dashboard.urls.position"),
    #         namespace="position",
    #     ),
    # ),
]