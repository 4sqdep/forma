from django.urls import path
from . import views


urlpatterns = [
    path(
        'list/',
        views.role_list_api_view,
        name='role_list'
    ),
    path(
        '<int:pk>/detail/',
        views.role_detail_api_view,
        name='role_detail'
    ),
    path(
        '<int:pk>/update/',
        views.role_update_api_view,
        name='role_update'
    ),
    path(
        '<int:pk>/delete/',
        views.role_delete_api_view,
        name='delete'
    ),
]