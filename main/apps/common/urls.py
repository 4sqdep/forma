from django.urls import path
from . import views



urlpatterns = [
    path(
        'currency-create/', 
        views.currency_create_api_view, 
        name='currency_create'
    ),
    path(
        'currency-list/', 
        views.currency_list_api_view, 
        name='currency_list'
    ),
    path(
        'currency-detail/<int:pk>/', 
        views.currency_detail_api_view, 
        name='currency_retrieve'
    ),
    path(
        'currency-update/<int:pk>/', 
        views.currency_update_api_view, 
        name='currency_update'
    ),
    path(
        'currency-delete/<int:pk>/', 
        views.currency_delete_api_view, 
        name='currency_delete'
    ),
    path(
        'measurement-create/', 
        views.measurement_create_api_view, 
        name='measurement_create'
    ),
    path(
        'measurement-list/', 
        views.measurement_list_api_view, 
        name='measurement_list'
    ),
    path(
        'measurement-detail/<int:pk>/', 
        views.measurement_detail_api_view, 
        name='measurement_retrieve'
    ),
    path(
        'measurement-update/<int:pk>/', 
        views.measurement_update_api_view, 
        name='measurement_update'
    ),
    path(
        'measurement-delete/<int:pk>/', 
        views.measurement_delete_api_view, 
        name='measurement_delete'
    ),
    
]


