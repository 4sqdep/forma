from django.urls import path
from .views import (DashboardButtonAPIView, DashboardCategoryButtonAPIView, ProjectDocumentAPIView,
                    DashboardSubCategoryButtonAPIView, NextStageDocumentsAPIView, MultipleFileUploadView,
                    GetFilesAPIView, ProjectSectionsAPIView, FilesSearchAPIView, GetFilesSectionAPIView)

app_name = "dashboard"

urlpatterns = [
    path('btn/', DashboardButtonAPIView.as_view(), name='btn'),
    path('category-btn/<int:pk>/', DashboardCategoryButtonAPIView.as_view(), name='category-btn'),
    path('sub-btn/<int:pk>/', DashboardSubCategoryButtonAPIView.as_view(), name='sub-btn'),
    path('sub-btn-post/', DashboardCategoryButtonAPIView.as_view(), name='sub-btn-post'),
    path('project-btn/<int:pk>/', ProjectDocumentAPIView.as_view(), name='project-btn'),
    path('next-project/<int:pk>/', NextStageDocumentsAPIView.as_view(), name='next-project-btn'),
    path('next-patch-project-name/<int:pk>/', NextStageDocumentsAPIView.as_view(), name='next-patch-project-name'),
    path('add-next-project/', NextStageDocumentsAPIView.as_view(), name='add-next-project-btn'),
    path('files-create/', MultipleFileUploadView.as_view(), name='files-create'),
    path('get-files/<int:pk>/', GetFilesAPIView.as_view(), name='get-files'),
    path('get-files-section/<int:pk>/', GetFilesSectionAPIView.as_view(), name='get-files'),
    path('get-sections/<int:pk>/', ProjectSectionsAPIView.as_view(), name='get-sections'),
    path('post-sections/', ProjectSectionsAPIView.as_view(), name='post-sections'),
    path('patch-sections/<int:pk>/', ProjectSectionsAPIView.as_view(), name='patch-sections'),
    path('files-search/', FilesSearchAPIView.as_view(), name='files-search'),
]


