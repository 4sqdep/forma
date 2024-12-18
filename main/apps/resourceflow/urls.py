from django.urls import path
from . import views


urlpatterns = [
    path(
        "request-create/", 
        views.resource_request_create_api_view,
        name='resuource_request_create'
    ),
    path(
        "request-list/", 
        views.resource_request_list_api_view,
        name='resource_request_list'
    ),
    path(
        "request-detail/<int:pk>/", 
        views.resource_request_detail_api_view, 
        name="resource_request_detail"
    ),
    path(
        "return-create/", 
        views.resource_return_create_api_view,
        name='resuource_return_create'
    ),
    path(
        "return-list/", 
        views.resource_return_list_api_view,
        name='resource_return_list'
    ),
    path(
        "return-detail/<int:pk>/", 
        views.resource_return_detail_api_view, 
        name="resource_return_detail"
    ),
]


