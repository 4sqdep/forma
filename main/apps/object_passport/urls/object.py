from django.urls import path
from ..views import object

app_name = 'object'


urlpatterns = [
    path(
        'create/', 
        object.object_create_api_view, 
        name='object_create'
    ),
    path(
        '<int:sub_category>/list/', 
        object.object_list_api_view, 
        name='object_list'
    ),
    path(
        '<int:pk>/detail/', 
        object.object_detail_api_view, 
        name='object_retrieve'
    ),
    path(
        '<int:pk>/update/', 
        object.object_update_api_view, 
        name='object_update'
    ),
    path(
        '<int:pk>/delete/', 
        object.object_delete_api_view, 
        name='object_delete'
    ),
    path(
        'all/list/', 
        object.all_object_list_api_view, 
        name='all_object_list'
    ),
]


