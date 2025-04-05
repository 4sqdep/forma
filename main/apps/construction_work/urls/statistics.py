from django.urls import path
from ..views import statistics



urlpatterns = [
    path(
        'create/',
        statistics.construction_installation_statistics_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        '<int:obj>/list/',
        statistics.construction_installation_statistics_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        '<int:pk>/detail/',
        statistics.construction_installation_statistics_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        '<int:pk>/update/',
        statistics.construction_installation_statistics_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        '<int:pk>/delete/',
        statistics.construction_installation_statistics_detail_update_delete_api_view,
        name='construction_file_delete'
    ),
]