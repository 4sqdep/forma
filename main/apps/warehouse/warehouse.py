from django.urls import include, path

app_name = "warehouse"

urlpatterns = [
    path(
        "equipment-warehouse/",
        include(
            ("main.apps.warehouse.urls.equipment_warehouse", "main.apps.warehouse.urls.equipment_warehouse"),
            namespace="equipment_warehouse",
        ),
    ),
    path(
        "material-warehouse/",
        include(
            ("main.apps.warehouse.urls.material_warehouse", "main.apps.warehouse.urls.material_warehouse"),
            namespace="material_warehouse",
        ),
    ),
]