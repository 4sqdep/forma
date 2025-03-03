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
        'category/list/<int:hydro_station_id>/', 
        industrial_equipment.equipment_category_list_api_view, 
        name='equipment_category_list'
    ),
    path(
        'category/detail/<int:pk>/', 
        industrial_equipment.equipment_category_detail_api_view, 
        name='equipment_category_retrieve'
    ),
    path(
        'category/update/<int:pk>/', 
        industrial_equipment.equipment_category_update_api_view, 
        name='equipment_category_update'
    ),
    path(
        'subcategory/delete/<int:pk>/', 
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
        'subcategory/list/<int:equipment_category>/', 
        industrial_equipment.equipment_subcategory_list_api_view, 
        name='equipment_subcategory_list'
    ),
    path(
        'subcategory/detail/<int:pk>/', 
        industrial_equipment.equipment_subcategory_detail_api_view, 
        name='equipment_subcategory_retrieve'
    ),
    path(
        'subcategory/update/<int:pk>/', 
        industrial_equipment.equipment_subcategory_update_api_view, 
        name='equipment_subcategory_update'
    ),
    path(
        'subcategory/delete/<int:pk>/', 
        industrial_equipment.equipment_subcategory_delete_api_view, 
        name='equipment_subcategory_delete'
    ),

    path(
        'asset-create/', 
        industrial_equipment.industrial_asset_create_api_view, 
        name='industrial_asset_create'
    ),
    path(
        'asset-list/<int:equipment_category>/', 
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


