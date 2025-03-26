from django.urls import path
from . import views



urlpatterns = [
    path(
        'currency/create/', 
        views.currency_create_api_view, 
        name='currency_create'
    ),
    path(
        'currency/list/', 
        views.currency_list_api_view, 
        name='currency_list'
    ),
    path(
        'currency/<int:pk>/detail/', 
        views.currency_detail_api_view, 
        name='currency_retrieve'
    ),
    path(
        'currency/<int:pk>/update/', 
        views.currency_update_api_view, 
        name='currency_update'
    ),
    path(
        'currency/<int:pk>/delete/', 
        views.currency_delete_api_view, 
        name='currency_delete'
    ),
    path(
        'measurement/create/', 
        views.measurement_create_api_view, 
        name='measurement_create'
    ),
    path(
        'measurement/list/', 
        views.measurement_list_api_view, 
        name='measurement_list'
    ),
    path(
        'measurement/<int:pk>/detail/', 
        views.measurement_detail_api_view, 
        name='measurement_retrieve'
    ),
    path(
        'measurement/<int:pk>/update/', 
        views.measurement_update_api_view, 
        name='measurement_update'
    ),
    path(
        'measurement/<int:pk>/delete/', 
        views.measurement_delete_api_view, 
        name='measurement_delete'
    ),
    
]


