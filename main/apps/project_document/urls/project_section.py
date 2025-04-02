from django.urls import path
from main.apps.project_document.views import project_section



urlpatterns = [
    path(
        'create/', 
        project_section.project_section_create_api_view, 
        name='project_section_create'
    ),
    path(
        '<int:project_document_file>/list/', 
        project_section.project_section_list_api_view,
        name='project_section_list'
    ),
    path(
        '<int:pk>/detail/',
        project_section.project_section_detail_api_view,
        name='project_section_detail'
    ),
    path(
        '<int:pk>/update/', 
        project_section.project_section_update_api_view, 
        name='project_section_update'
    ),
    path(
        '<int:pk>/delete/', 
        project_section.project_section_delete_api_view, 
        name='project_section_delete'
    ),
]


