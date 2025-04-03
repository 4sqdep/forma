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
        'all-statistics-data/',
        dashboard.all_statistics_data_api_view,
        name='all_statistics_data'
    ),
]


