from django.urls import path
from . import views


urlpatterns = [
    path(
        "category-create/", 
        views.service_category_create_api_view,
        name='service_category_create'
    ),
    path(
        "category-list/", 
        views.service_category_list_api_view,
        name='service_category_list'
    ),
    path(
        "category-detail/<int:pk>/", 
        views.service_category_detail_api_view, 
        name="service_category_detail"
    ),
    path(
        "create/", 
        views.service_create_api_view,
        name='service_create'
    ),
    path(
        "list/", 
        views.service_list_api_view,
        name='service_list'
    ),
    path(
        "detail/<int:pk>/", 
        views.service_detail_api_view, 
        name="service_detail"
    ),
]


