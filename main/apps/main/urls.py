from django.urls import path
from .views import GetObjectsPasswordView, UploadFilesAPIView, GetFilesAPIView


app_name = "main"


urlpatterns = [
    path('get/objects/password/<int:pk>/', GetObjectsPasswordView.as_view(), name='get-objects-password'),
    path('post-objects-password/', GetObjectsPasswordView.as_view(), name='post-objects-password'),
    path('patch-objects-password/<int:pk>/', GetObjectsPasswordView.as_view(), name='patch-objects-password'),
    path('upload-file/', UploadFilesAPIView.as_view(), name='upload-file'),
    path('get-file/<int:pk>/', GetFilesAPIView.as_view(), name='get-file'),
]