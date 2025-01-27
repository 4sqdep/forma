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
]