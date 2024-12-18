from django.urls import include, path

app_name = "resource"

urlpatterns = [
    path(
        "equipment/",
        include(
            ("main.apps.resource.urls.equipment", "main.apps.resource.urls.equipment"),
            namespace="equipment",
        ),
    ),
    path(
        "material/",
        include(
            ("main.apps.resource.urls.material", "main.apps.resource.urls.material"),
            namespace="material",
        ),
    ),
    path(
        "measurement/",
        include(
            ("main.apps.resource.urls.measurement", "main.apps.resource.urls.measurement"),
            namespace="measurement",
        ),
    ),
    path(
        "time-measurement/",
        include(
            ("main.apps.resource.urls.time_measurement", "main.apps.resource.urls.time_measurement"),
            namespace="time_measurement",
        ),
    ),
]