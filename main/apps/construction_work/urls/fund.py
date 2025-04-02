from django.urls import path
from ..views import fund



urlpatterns = [
    path(
        'construction-project/create/',
        fund.construction_installation_project_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'construction-project/list/<int:section>/',
        fund.construction_installation_project_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'construction-project/detail/<int:pk>/',
        fund.construction_installation_project_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'construction-project/update/<int:pk>/',
        fund.construction_installation_project_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'construction-project/delete/<int:pk>/',
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
        'construction-completed-task/list/<int:section>/',
        fund.monthly_completed_task_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'construction-completed-task/detail/<int:pk>/',
        fund.monthly_completed_task_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'construction-completed-task/update/<int:pk>/',
        fund.monthly_completed_task_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'construction-completed-task/delete/<int:pk>/',
        fund.monthly_completed_task_detail_update_delete_api_view,
        name='construction_file_delete'
    ),
]