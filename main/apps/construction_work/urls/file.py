from django.urls import path
from ..views import file



urlpatterns = [
    path(
        'create/',
        file.construction_installation_file_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        '<int:section>/list/',
        file.construction_installation_file_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        '<int:pk>/detail/',
        file.construction_installation_file_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        '<int:pk>/update/',
        file.construction_installation_file_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        '<int:pk>/delete/',
        file.construction_installation_file_detail_update_delete_api_view,
        name='construction_file_delete'
    )
]