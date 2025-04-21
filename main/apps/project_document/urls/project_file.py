from django.urls import path
from main.apps.project_document.views import project_file



urlpatterns = [
    path(
        'project-document-file/create/', 
        project_file.project_document_file_create_api_view, 
        name='project_document_file_create'
    ),
    path(
        'project-document-file/<int:document>/list/', 
        project_file.project_document_file_list_api_view,
        name='project_document_file_list'
    ),
    path(
        'project-document-file/<int:pk>/detail/',
        project_file.project_document_file_detail_api_view,
        name='project_document_file_detail'
    ),
    path(
        'project-document-file/<int:pk>/update/', 
        project_file.project_document_file_update_api_view, 
        name='project_document_file_update'
    ),
    path(
        'project-document-file/<int:pk>/delete/', 
        project_file.project_document_file_delete_api_view, 
        name='project_document_file_delete'
    ),
]


