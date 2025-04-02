from django.urls import path
from ..views import object_gallery

app_name = 'object_gallery'


urlpatterns = [
    path(
        'object/gallery/create/',
        object_gallery.object_gallery_api_view,
        name='object_gallery_create'
    )
]