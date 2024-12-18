from django.urls import path
from ..views import material


urlpatterns = [
    path(
        "category-create/", 
        material.material_category_create_api_view,
        name='material_create'
    ),
    path(
        "category-list/", 
        material.material_category_list_api_view,
        name='material_list'
    ),
    path(
        "category-detail/<int:pk>/", 
        material.material_category_detail_api_view, 
        name="material_detail"
    ),

    path(
        "create/", 
        material.material_create_api_view,
        name='material_create'
    ),
    path(
        "list/", 
        material.material_list_api_view,
        name='material_list'
    ),
    path(
        "detail/<int:pk>/", 
        material.material_detail_api_view, 
        name="material_detail"
    ),
]


