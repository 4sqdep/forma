from django.urls import path
from ..views import time_period



urlpatterns = [
    path(
        'year-create/', 
        time_period.year_create_api_view, 
        name='time_period_create'
    ),
    path(
        'year-list/', 
        time_period.year_list_api_view, 
        name='time_period_list'
    ),
    path(
        'year-detail/<int:pk>/', 
        time_period.year_detail_api_view, 
        name='time_period_retrieve'
    ),
    path(
        'year-update/<int:pk>/', 
        time_period.year_update_api_view, 
        name='time_period_update'
    ),
    path(
        'year-delete/<int:pk>/', 
        time_period.year_delete_api_view, 
        name='time_period_delete'
    ),
    path(
        'month-create/', 
        time_period.month_create_api_view, 
        name='time_period_create'
    ),
    path(
        'month-list/', 
        time_period.month_list_api_view, 
        name='time_period_list'
    ),
    path(
        'month-detail/<int:pk>/', 
        time_period.month_detail_api_view, 
        name='time_period_retrieve'
    ),
    path(
        'month-update/<int:pk>/', 
        time_period.month_update_api_view, 
        name='time_period_update'
    ),
    path(
        'month-delete/<int:pk>/', 
        time_period.month_delete_api_view, 
        name='time_period_delete'
    ),
    
]


