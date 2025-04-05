from django.urls import path
from ..views import fund



urlpatterns = [
    path(
        'construction-project/create/',
        fund.construction_installation_project_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'construction-project/<int:section>/list/',
        fund.construction_installation_project_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'construction-project/<int:pk>/detail/',
        fund.construction_installation_project_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'construction-project/<int:pk>/update/',
        fund.construction_installation_project_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'construction-project/<int:pk>/delete/',
        fund.construction_installation_project_detail_update_delete_api_view,
        name='construction_file_delete'
    ),

    # Monthly Completed Task URLs
    path(
        'construction-completed-task/create/',
        fund.monthly_completed_task_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'construction-completed-task/<int:section>/list/',
        fund.monthly_completed_task_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'construction-completed-task/<int:pk>/detail/',
        fund.monthly_completed_task_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'construction-completed-task/<int:pk>/update/',
        fund.monthly_completed_task_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'construction-completed-task/<int:pk>/delete/',
        fund.monthly_completed_task_detail_update_delete_api_view,
        name='construction_file_delete'
    ),
]