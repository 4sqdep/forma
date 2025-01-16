from django.urls import path
from main.apps.dashboard.utils import NestedDataAPIView
from main.apps.dashboard.views.document import (
    FilesSearchAPIView, 
    GetFilesAPIView, 
    GetFilesSectionAPIView, 
    MultipleFileUploadView, 
    NextStageDocumentsAPIView, 
    ProjectDocumentAPIView, 
    ProjectSectionsAPIView
)



urlpatterns = [
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
    path('get-doc/', NestedDataAPIView.as_view(), name='get-doc'),
]


