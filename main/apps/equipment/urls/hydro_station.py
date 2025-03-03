from django.urls import path
from ..views import hydro_station

app_name = 'hydro_station'


urlpatterns = [
    path(
        'create/', 
        hydro_station.hydro_station_create_api_view, 
        name='hydro_station_create'
    ),
    path(
        'list/', 
        hydro_station.hydro_station_list_api_view, 
        name='hydro_station_list'
    ),
    path(
        'detail/<int:object_id>/', 
        hydro_station.hydro_station_detail_api_view, 
        name='hydro_station_retrieve'
    ),
    path(
        'update/<int:pk>/', 
        hydro_station.hydro_station_update_api_view, 
        name='hydro_station_update'
    ),
    path(
        'delete/<int:pk>/', 
        hydro_station.hydro_station_delete_api_view, 
        name='hydro_station_delete'
    ),
    path(
        'financial-resource-create/', 
        hydro_station.financial_resource_create_api_view, 
        name='financial_resource_create'
    ),
    path(
        'financial-resource-list/', 
        hydro_station.financial_resource_list_api_view, 
        name='financial_resource_list'
    ),
    path(
        'financial-resource-detail/<int:pk>/', 
        hydro_station.financial_resource_detail_api_view, 
        name='financial_resource_retrieve'
    ),
    path(
        'financial-resource-update/<int:pk>/', 
        hydro_station.financial_resource_update_api_view, 
        name='financial_resource_update'
    ),
    path(
        'financial-resource-delete/<int:pk>/', 
        hydro_station.financial_resource_delete_api_view, 
        name='financial_resource_delete'
    ),
    
]


