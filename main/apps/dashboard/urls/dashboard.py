from django.urls import path
from main.apps.dashboard.views import dashboard



urlpatterns = [
    path(
        'object-category-list/', 
        dashboard.object_category_api_view, 
        name='object_category_list'
    ),
    path(
        'object-subcategory-create/',
        dashboard.object_subcategory_api_view,
        name='object_subcategory_create'
    ),
    path(
        'object-subcategory-detail/<int:pk>/',
        dashboard.object_subcategory_api_view,
        name='object_subcategory_detail'
    ),
    path(
        'object-subcategory-update/<int:pk>/',
        dashboard.object_subcategory_api_view,
        name='object_subcategory_update'
    ),
    path(
        'object-subcategory-delete/<int:pk>/',
        dashboard.object_subcategory_api_view,
        name='object_subcategory_delete'
    ),

    path(
        'object-subcategory-list/<int:pk>/', 
        dashboard.object_subcategory_list_api_view, 
        name='object_subcategory_list'
    ),
    path(
        'object-list/<int:sub_category>/', 
        dashboard.object_list_api_view, 
        name='object'
    ),
    path(
        'object-create/', 
        dashboard.object_api_view, 
        name='object_create'
    ),
    path(
        'object-detail/<int:pk>/', 
        dashboard.object_retrieve_api_view, 
        name='object_detail'
    ),
    path(
        'object-update/<int:pk>/', 
        dashboard.object_api_view, 
        name='object_update'
    ),
    path(
        'object-delete/<int:pk>/', 
        dashboard.object_api_view, 
        name='object_delete'
    )
]


