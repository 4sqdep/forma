from django.urls import path
from ..views import construction



urlpatterns = [
    path(
        'create/', 
        construction.construction_task_create_api_view, 
        name='construction_create'
    ),
    path(
        'list/', 
        construction.construction_task_list_api_view, 
        name='construction_list'
    ),
    path(
        'detail/<int:pk>/', 
        construction.construction_task_detail_api_view, 
        name='construction_retrieve'
    ),
    path(
        'update/<int:pk>/', 
        construction.construction_task_update_api_view, 
        name='construction_update'
    ),
    path(
        'delete/<int:pk>/', 
        construction.construction_task_delete_api_view, 
        name='construction_delete'
    ),
    
]


