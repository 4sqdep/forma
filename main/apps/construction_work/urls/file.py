from django.urls import path
from ..views import file



urlpatterns = [
    path(
        'create/',
        file.construction_installation_file_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'list/<int:section>/',
        file.construction_installation_file_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'detail/<int:pk>/',
        file.construction_installation_file_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'update/<int:pk>/',
        file.construction_installation_file_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'delete/<int:pk>/',
        file.construction_installation_file_detail_update_delete_api_view,
        name='construction_file_delete'
    )
]