from django.urls import path
from ..views import section



urlpatterns = [
    path(
        'create/',
        section.construction_installation_section_list_create_api_view,
        name='section_create'
    ),
    path(
        'list/<int:object>/',
        section.construction_installation_section_list_create_api_view,
        name='section_list'
    ),
    path(
        'detail/<int:pk>/',
        section.construction_installation_section_detail_update_delete_api_view,
        name='section_retrieve'
    ),
    path(
        'update/<int:pk>/',
        section.construction_installation_section_detail_update_delete_api_view,
        name='section_update'
    ),
    path(
        'delete/<int:pk>/',
        section.construction_installation_section_detail_update_delete_api_view,
        name='section_delete'
    )
]