from django.urls import path
from ..views import construction_installation_work



urlpatterns = [
    # Construction Installation Section URLs
    path(
        'section/create/',
        construction_installation_work.construction_installation_sub_section_list_create_api_view,
        name='section_create'
    ),
    path(
        'section/list/',
        construction_installation_work.construction_installation_sub_section_list_create_api_view,
        name='section_list'
    ),
    path(
        'section/detail/<int:pk>/',
        construction_installation_work.construction_installation_sub_section_detail_update_delete_api_view,
        name='section_retrieve'
    ),
    path(
        'section/update/<int:pk>/',
        construction_installation_work.construction_installation_sub_section_detail_update_delete_api_view,
        name='section_update'
    ),
    path(
        'section/delete/<int:pk>/',
        construction_installation_work.construction_installation_sub_section_detail_update_delete_api_view,
        name='section_delete'
    ),

    # Construction Installation File URLs
    path(
        'construction-file/create/',
        construction_installation_work.construction_installation_file_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'construction-file/list/<int:section>/',
        construction_installation_work.construction_installation_file_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'construction-file/detail/<int:pk>/',
        construction_installation_work.construction_installation_file_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'construction-file/update/<int:pk>/',
        construction_installation_work.construction_installation_file_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'construction-file/delete/<int:pk>/',
        construction_installation_work.construction_installation_file_detail_update_delete_api_view,
        name='construction_file_delete'
    ),

    # Construction Installation Statistics URLs
    path(
        'construction-statistics/create/',
        construction_installation_work.construction_installation_statistics_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'construction-statistics/list/<int:obj>/',
        construction_installation_work.construction_installation_statistics_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'construction-statistics/detail/<int:pk>/',
        construction_installation_work.construction_installation_statistics_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'construction-statistics/update/<int:pk>/',
        construction_installation_work.construction_installation_statistics_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'construction-statistics/delete/<int:pk>/',
        construction_installation_work.construction_installation_statistics_detail_update_delete_api_view,
        name='construction_file_delete'
    ),

    # Construction Installation Subsection URLs
    path(
        'construction-subsection/create/',
        construction_installation_work.construction_installation_sub_section_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'construction-subsection/list/<int:section>/',
        construction_installation_work.construction_installation_sub_section_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'construction-subsection/detail/<int:pk>/',
        construction_installation_work.construction_installation_sub_section_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'construction-subsection/update/<int:pk>/',
        construction_installation_work.construction_installation_sub_section_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'construction-subsection/delete/<int:pk>/',
        construction_installation_work.construction_installation_sub_section_detail_update_delete_api_view,
        name='construction_file_delete'
    ),

    # Construction Installation Project URLs
    path(
        'construction-project/create/',
        construction_installation_work.construction_installation_project_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'construction-project/list/<int:section>/',
        construction_installation_work.construction_installation_project_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'construction-project/detail/<int:pk>/',
        construction_installation_work.construction_installation_project_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'construction-project/update/<int:pk>/',
        construction_installation_work.construction_installation_project_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'construction-project/delete/<int:pk>/',
        construction_installation_work.construction_installation_project_detail_update_delete_api_view,
        name='construction_file_delete'
    ),

    # Monthly Completed Task URLs
    path(
        'construction-completed-task/create/',
        construction_installation_work.monthly_completed_task_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'construction-completed-task/list/<int:section>/',
        construction_installation_work.monthly_completed_task_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'construction-completed-task/detail/<int:pk>/',
        construction_installation_work.monthly_completed_task_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'construction-completed-task/update/<int:pk>/',
        construction_installation_work.monthly_completed_task_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'construction-completed-task/delete/<int:pk>/',
        construction_installation_work.monthly_completed_task_detail_update_delete_api_view,
        name='construction_file_delete'
    ),
]
