from django.urls import path
from ..views import document



urlpatterns = [
    path(
        'project-document/<int:pk>/', 
        document.project_document_api_view, 
        name='project-btn'
    ),
    path(
        'next-project-list/<int:pk>/', 
        document.next_stage_document_api_view,
        name='next-project-btn'
    ),
    path(
        'next-priject-update/<int:pk>/', 
        document.next_stage_document_api_view, 
        name='next-patch-project-name'
    ),
    path(
        'next-project-create/', 
        document.next_stage_document_api_view, 
        name='add-next-project-btn'
    ),
    path(
        'file-create/', 
        document.multiple_file_upload_api_view, 
        name='files-create'
    ),
    path(
        'file-list/<int:pk>/', 
        document.get_files_api_view, 
        name='get-files'
    ),
    path(
        'file-section-list/<int:pk>/', 
        document.get_files_section_api_view, 
        name='get-files'
    ),
    path(
        'project-section-list/<int:pk>/', 
        document.project_section_api_view, 
        name='get-sections'
    ),
    path(
        'project-section-create/', 
        document.project_section_api_view, 
        name='post-sections'
    ),
    path(
        'project-section-update/<int:pk>/', 
        document.project_section_api_view, 
        name='patch-sections'
    ),
    path(
        'file-search/', 
        document.file_search_api_view, 
        name='files-search'
    ),
    path(
        'get-doc/', 
        document.nested_data_api_view, 
        name='get-doc'
    ),
    path(
        'statistics-data/<int:pk>/', 
        document.object_password_detail_api_view, 
        name='post-doc'
    ),
    path(
        'all-statistics-data/', 
        document.statistical_data_api_view, 
        name='all-statistic'
    ),
]


