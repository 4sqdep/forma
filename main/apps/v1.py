from django.urls import include, path



urlpatterns = [
    path(
        "account/",
        include(
            ("main.apps.account.account", "main.apps.account.account"),
            namespace="account",
        ),
    ),
    path(
        "dashboard/",
        include(
            ("main.apps.dashboard.dashboard", "main.apps.dashboard.dashboard"),
            namespace="dashboard",
        ),
    ),
    path(
        "main/",
        include(
            ("main.apps.main.urls", "main.apps.main.urls"),
            namespace="main",
        ),
    ),
    path(
        "reestr/",
        include(
            ("main.apps.reestr.reestr", "main.apps.reestr.reestr"),
            namespace="reestr",
        ),
    ),
    path(
        "equipment/",
        include(
            ("main.apps.equipment.equipment", "main.apps.equipment.equipment"),
            namespace="equipment",
        ),
    ),
    path(
        "common/",
        include(
            ("main.apps.common.urls", "main.apps.common.urls"),
            namespace="common",
        ),
    ),
]

