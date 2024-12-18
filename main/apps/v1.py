from django.urls import include, path



urlpatterns = [
    path(
        "user/",
        include(
            ("main.apps.account.urls", "main.apps.account.urls"),
            namespace="account",
        ),
    ),
    path(
        "location/",
        include(
            ("main.apps.location.urls", "main.apps.location.urls"),
            namespace="location",
        ),
    ),
    path(
        "statement/",
        include(
            ("main.apps.statement.statement", "main.apps.statement.statement"),
            namespace="statement",
        ),
    ),
    path(
        "resource/",
        include(
            ("main.apps.resource.resource", "main.apps.resource.resource"),
            namespace="resource",
        ),
    ),
    path(
        "service/",
        include(
            ("main.apps.service.urls", "main.apps.service.urls"),
            namespace="service",
        ),
    ),
    path(
        "order/",
        include(
            ("main.apps.order.urls", "main.apps.order.urls"),
            namespace="order",
        ),
    ),
    path(
        "resourceflow/",
        include(
            ("main.apps.resourceflow.urls", "main.apps.resourceflow.urls"),
            namespace="resourceflow",
        ),
    ),
    path(
        "warehouse/",
        include(
            ("main.apps.warehouse.warehouse", "main.apps.warehouse.warehouse"),
            namespace="warehouse",
        ),
    ),
    path(
        "notification/",
        include(
            ("main.apps.notification.urls", "main.apps.notification.urls"),
            namespace="notification",
        ),
    ),
    path(
        "checklist/",
        include(
            ("main.apps.checklist.urls", "main.apps.checklist.urls"),
            namespace="checklist",
        ),
    ),
    path(
        "contract/",
        include(
            ("main.apps.contract.urls", "main.apps.contract.urls"),
            namespace="contract",
        ),
    ),
]

