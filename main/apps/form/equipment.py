from django.urls import include, path

app_name = "equipment"



urlpatterns = [
    path(
        "hydro-station/",
        include(
            ("main.apps.equipment.urls.hydro_station", "main.apps.equipment.urls.hydro_station"),
            namespace="hydro_station",
        ),
    ),
    path(
        "industrial-equipment/",
        include(
            ("main.apps.equipment.urls.industrial_equipment", "main.apps.equipment.urls.industrial_equipment"),
            namespace="industrial_equipment",
        ),
    ),
]