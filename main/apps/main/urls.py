from django.urls import path
from . import views


app_name = "main"


urlpatterns = [
    path(
        'search-objects-name/', 
        views.search_object_name_api_view, 
        name='search-objects-name'
    ),
]