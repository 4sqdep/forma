from django.urls import path
from main.apps.project_document.views import project_document_type



urlpatterns = [
    path(
        'create/', 
        project_document_type.project_document_type_create_api_view, 
        name='project_document_type_create'
    ),
    path(
        '<int:object>/list/', 
        project_document_type.project_document_type_list_api_view,
        name='project_document_type_list'
    ),
    path(
        '<int:pk>/detail/',
        project_document_type.project_document_type_detail_api_view,
        name='project_document_type_detail'
    ),
    path(
        '<int:pk>/update/', 
        project_document_type.project_document_type_update_api_view, 
        name='project_document_type_update'
    ),
    path(
        '<int:pk>/delete/', 
        project_document_type.project_document_type_delete_api_view, 
        name='project_document_type_delete'
    ),
]


