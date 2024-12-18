from django.urls import path
from ..views import equipment_warehouse


urlpatterns = [
    path(
        "create/", 
        equipment_warehouse.equipment_warehouse_create_api_view,
        name='equipment_warehouse_create'
    ),
    path(
        "list/", 
        equipment_warehouse.equipment_warehouse_list_api_view,
        name='equipment_warehouse_list'
    ),
    path(
        "detail/<int:pk>/", 
        equipment_warehouse.equipment_warehouse_detail_api_view, 
        name="equipment_warehouse_detail"
    ),
]


