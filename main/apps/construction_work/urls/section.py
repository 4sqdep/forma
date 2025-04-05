from django.urls import path
from ..views import section



urlpatterns = [
    path(
        'create/',
        section.construction_installation_section_list_create_api_view,
        name='section_create'
    ),
    path(
        '<int:object>/list/',
        section.construction_installation_section_list_create_api_view,
        name='section_list'
    ),
    path(
        '<int:pk>/detail/',
        section.construction_installation_section_detail_update_delete_api_view,
        name='section_retrieve'
    ),
    path(
        '<int:pk>/update/',
        section.construction_installation_section_detail_update_delete_api_view,
        name='section_update'
    ),
    path(
        '<int:pk>/delete/',
        section.construction_installation_section_detail_update_delete_api_view,
        name='section_delete'
    )
]