from django.urls import path
from ..views import industrial_equipment



urlpatterns = [
    # Equipment Category
    path(
        'category/create/', 
        industrial_equipment.equipment_category_create_api_view, 
        name='equipment_category_create'
    ),
    path(
        'category/<int:hydro_station_id>/list/', 
        industrial_equipment.equipment_category_list_api_view, 
        name='equipment_category_list'
    ),
    path(
        'category/<int:pk>/detail/', 
        industrial_equipment.equipment_category_detail_api_view, 
        name='equipment_category_retrieve'
    ),
    path(
        'category/<int:pk>/update/', 
        industrial_equipment.equipment_category_update_api_view, 
        name='equipment_category_update'
    ),
    path(
        'category/<int:pk>/delete/', 
        industrial_equipment.equipment_category_delete_api_view, 
        name='equipment_category_delete'
    ),

    # Equipment Subcategory
    path(
        'subcategory/create/', 
        industrial_equipment.equipment_subcategory_create_api_view, 
        name='equipment_subcategory_create'
    ),
    path(
        'subcategory/<int:equipment_category>/list/', 
        industrial_equipment.equipment_subcategory_list_api_view, 
        name='equipment_subcategory_list'
    ),
    path(
        'subcategory/<int:pk>/detail/', 
        industrial_equipment.equipment_subcategory_detail_api_view, 
        name='equipment_subcategory_retrieve'
    ),
    path(
        'subcategory/<int:pk>/update/', 
        industrial_equipment.equipment_subcategory_update_api_view, 
        name='equipment_subcategory_update'
    ),
    path(
        'subcategory/<int:pk>/delete/', 
        industrial_equipment.equipment_subcategory_delete_api_view, 
        name='equipment_subcategory_delete'
    ),

    # Industrial Asset
    path(
        'asset-create/', 
        industrial_equipment.industrial_asset_create_api_view, 
        name='industrial_asset_create'
    ),
    path(
        'asset/<int:equipment_category>/list/', 
        industrial_equipment.industrial_asset_list_api_view, 
        name='industrial_asset_list'
    ),
    path(
        'asset/<int:pk>/detail/', 
        industrial_equipment.industrial_asset_detail_api_view, 
        name='industrial_asset_retrieve'
    ),
    path(
        'asset/<int:pk>/update/', 
        industrial_equipment.industrial_asset_update_api_view, 
        name='industrial_asset_update'
    ),
    path(
        'asset/<int:pk>/delete/', 
        industrial_equipment.industrial_asset_delete_api_view, 
        name='industrial_asset_delete'
    ),
    path(
        'all-asset/<int:obj>/list/', 
        industrial_equipment.all_industrial_asset_list_api_view, 
        name='all_industrial_asset_list'
    ),
]


