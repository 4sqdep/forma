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
        '<int:object_id>/detail/', 
        hydro_station.hydro_station_detail_api_view, 
        name='hydro_station_retrieve'
    ),
    path(
        '<int:pk>/update/', 
        hydro_station.hydro_station_update_api_view, 
        name='hydro_station_update'
    ),
    path(
        '<int:pk>/delete/', 
        hydro_station.hydro_station_delete_api_view, 
        name='hydro_station_delete'
    )
]


