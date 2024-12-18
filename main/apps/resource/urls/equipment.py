from django.urls import path
from ..views import equipment


urlpatterns = [
    path(
        "category-create/", 
        equipment.equipment_category_create_api_view,
        name='equipment_create'
    ),
    path(
        "category-list/", 
        equipment.equipment_category_list_api_view,
        name='equipment_list'
    ),
    path(
        "category-detail/<int:pk>/", 
        equipment.equipment_category_detail_api_view, 
        name="equipment_detail"
    ),
    path(
        "create/", 
        equipment.equipment_create_api_view,
        name='equipment_create'
    ),
    path(
        "list/", 
        equipment.equipment_list_api_view,
        name='equipment_list'
    ),
    path(
        "detail/<int:pk>/", 
        equipment.equipment_detail_api_view, 
        name="equipment_detail"
    ),
]


