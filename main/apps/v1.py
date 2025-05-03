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
        "object-passport/",
        include(
            ("main.apps.object_passport.object_passport", "main.apps.object_passport.object_passport"),
            namespace="object_passport",
        ),
    ),
    path(
        "project-document/",
        include(
            ("main.apps.project_document.project_document", "main.apps.project_document.project_document"),
            namespace="project_document",
        ),
    ),
    path(
        "construction-work/",
        include(
            ("main.apps.construction_work.construction_work", "main.apps.construction_work.construction_work"),
            namespace="construction_work",
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
    path(
        "contract/",
        include(
            ("main.apps.contract.urls", "main.apps.contract.urls"),
            namespace="contract",
        ),
    ),
    path(
        "employee-communication/",
        include(
            ("main.apps.employee_communication.urls", "main.apps.employee_communication.urls"),
            namespace="employee_communication",
        ),
    ),
    path(
        "role/",
        include(
            ("main.apps.role.urls", "main.apps.role.urls"),
            namespace="role",
        ),
    ),
]

