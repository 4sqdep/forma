from django.urls import path
from . import views


app_name = "main"


urlpatterns = [
    path(
        'get/objects/password/<int:pk>/', 
        views.get_object_password_api_view, 
        name='get-objects-password'
    ),
    path(
        'post-objects-password/', 
        views.get_object_password_api_view, 
        name='post-objects-password'
    ),
    path(
        'patch-objects-password/<int:pk>/', 
        views.get_object_password_api_view, 
        name='patch-objects-password'
    ),
    path(
        'upload-file/', 
        views.upload_files_api_view, 
        name='upload-file'
    ),
    path(
        'get-file/<int:pk>/', 
        views.get_files_api_view, 
        name='get-file'
    ),
    path(
        'search-objects-name/', 
        views.search_object_name_api_view, 
        name='search-objects-name'
    ),
]