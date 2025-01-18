from django.urls import path
from ..views import currency



urlpatterns = [
    path(
        'create/', 
        currency.currency_create_api_view, 
        name='currency_create'
    ),
    path(
        'list/', 
        currency.currency_list_api_view, 
        name='currency_list'
    ),
    path(
        'detail/<int:pk>/', 
        currency.currency_detail_api_view, 
        name='currency_retrieve'
    ),
    path(
        'update/<int:pk>/', 
        currency.currency_update_api_view, 
        name='currency_update'
    ),
    path(
        'delete/<int:pk>/', 
        currency.currency_delete_api_view, 
        name='currency_delete'
    ),
    
]


