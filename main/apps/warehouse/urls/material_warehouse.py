from django.urls import path
from ..views import material_warehouse


urlpatterns = [
    path(
        "create/", 
        material_warehouse.material_warehouse_create_api_view,
        name='material_warehouse_create'
    ),
    path(
        "list/", 
        material_warehouse.material_warehouse_list_api_view,
        name='material_warehouse_list'
    ),
    path(
        "detail/<int:pk>/", 
        material_warehouse.material_warehouse_detail_api_view, 
        name="material_warehouse_detail"
    ),
]
