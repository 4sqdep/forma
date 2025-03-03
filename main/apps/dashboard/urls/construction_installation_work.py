from django.urls import path
from ..views import construction_installation_work



urlpatterns = [
    # Section URLs
    path(
        'section/create/',
        construction_installation_work.section_list_create_api_view,
        name='section_create'
    ),
    path(
        'section/list/',
        construction_installation_work.section_list_create_api_view,
        name='section_list'
    ),
    path(
        'section/detail/<int:pk>/',
        construction_installation_work.section_detail_update_delete_api_view,
        name='section_retrieve'
    ),
    path(
        'section/update/<int:pk>/',
        construction_installation_work.section_detail_update_delete_api_view,
        name='section_update'
    ),
    path(
        'section/delete/<int:pk>/',
        construction_installation_work.section_detail_update_delete_api_view,
        name='section_delete'
    ),

    # Construction File URLs
    path(
        'construction-file/create/',
        construction_installation_work.construction_file_list_create_api_view,
        name='construction_file_create'
    ),
    path(
        'construction-file/list/<int:section>/',
        construction_installation_work.construction_file_list_create_api_view,
        name='construction_file_list'
    ),
    path(
        'construction-file/detail/<int:pk>/',
        construction_installation_work.construction_file_detail_update_delete_api_view,
        name='construction_file_retrieve'
    ),
    path(
        'construction-file/update/<int:pk>/',
        construction_installation_work.construction_file_detail_update_delete_api_view,
        name='construction_file_update'
    ),
    path(
        'construction-file/delete/<int:pk>/',
        construction_installation_work.construction_file_detail_update_delete_api_view,
        name='construction_file_delete'
    ),
]
