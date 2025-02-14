from django.urls import path
from ..views import dashboard



urlpatterns = [
    path(
        'object-category-list/', 
        dashboard.object_category_api_view, 
        name='object_category_list'
    ),
    path(
        'object-subcategory/<int:pk>/', 
        dashboard.object_subcategory_button_api_view, 
        name='object_subcategory_list'
    ),
    path(
        'object/<int:pk>/', 
        dashboard.object_api_view, 
        name='object'
    ),
    path(
        'object-subcategory-create/', 
        dashboard.object_subcategory_button_api_view, 
        name='object_subcategory_create'
    ),
]


