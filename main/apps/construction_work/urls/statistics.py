from django.urls import path
from ..views import statistics



urlpatterns = [
    path(
        'create/',
        statistics.construction_installation_statistics_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'list/<int:obj>/',
        statistics.construction_installation_statistics_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'detail/<int:pk>/',
        statistics.construction_installation_statistics_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'update/<int:pk>/',
        statistics.construction_installation_statistics_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'delete/<int:pk>/',
        statistics.construction_installation_statistics_detail_update_delete_api_view,
        name='construction_file_delete'
    ),
]