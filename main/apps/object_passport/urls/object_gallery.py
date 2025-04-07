from django.urls import path
from ..views import object_gallery

app_name = 'object-gallery'


urlpatterns = [
    path(
        'create/',
        object_gallery.object_gallery_api_view,
        name='object_gallery_create'
    ),
    path(
        '<int:pk>/update/',
        object_gallery.object_gallery_update_api_view,
        name='object_gallery_update'
    ),
    path(
        '<int:pk>/list/',
        object_gallery.object_gallery_list_api_view,
        name='object_gallery_list'
    ),
    path(
        '<int:pk>/delete/',
        object_gallery.object_gallery_delete_api_view,
        name='object_gallery_delete'
    )
]