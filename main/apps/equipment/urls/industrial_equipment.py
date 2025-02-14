from django.urls import path
from ..views import industrial_equipment



urlpatterns = [
    path(
        'create/', 
        industrial_equipment.industrial_equipment_create_api_view, 
        name='industrial_equipment_create'
    ),
    path(
        'list/<int:hydro_station_id>/', 
        industrial_equipment.industrial_equipment_list_api_view, 
        name='industrial_equipment_list'
    ),
    path(
        'detail/<int:pk>/', 
        industrial_equipment.industrial_equipment_detail_api_view, 
        name='industrial_equipment_retrieve'
    ),
    path(
        'update/<int:pk>/', 
        industrial_equipment.industrial_equipment_update_api_view, 
        name='industrial_equipment_update'
    ),
    path(
        'delete/<int:pk>/', 
        industrial_equipment.industrial_equipment_delete_api_view, 
        name='industrial_equipment_delete'
    ),
    path(
        'asset-create/', 
        industrial_equipment.industrial_asset_create_api_view, 
        name='industrial_asset_create'
    ),
    path(
        'asset-list/<int:industrial_equipment_id>/<int:hydro_station_id>/', 
        industrial_equipment.industrial_asset_list_api_view, 
        name='industrial_asset_list'
    ),
    path(
        'asset-detail/<int:pk>/', 
        industrial_equipment.industrial_asset_detail_api_view, 
        name='industrial_asset_retrieve'
    ),
    path(
        'asset-update/<int:pk>/', 
        industrial_equipment.industrial_asset_update_api_view, 
        name='industrial_asset_update'
    ),
    path(
        'asset-delete/<int:pk>/', 
        industrial_equipment.industrial_asset_delete_api_view, 
        name='industrial_asset_delete'
    ),
]


