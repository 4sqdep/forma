from django.contrib import admin
from main.apps.equipment.models.hydro_station import HydroStation
from main.apps.equipment.models.industrial_equipment import EquipmentCategory, EquipmentSubCategory, IndustrialAsset



class AdminEquipmentCategory(admin.ModelAdmin):
    list_display = ['id', 'hydro_station', 'title', 'total_cost', 'has_subcategories']
    list_display_links = ['hydro_station', 'title', 'total_cost', 'has_subcategories']
    search_fields = ['title']

admin.site.register(EquipmentCategory, AdminEquipmentCategory)


class AdminEquipmentSubCategory(admin.ModelAdmin):
    list_display = ['id', 'equipment_category', 'title']
    list_display_links = ['equipment_category', 'title']
    search_fields = ['title']

admin.site.register(EquipmentSubCategory, AdminEquipmentSubCategory)


class AdminHydroStation(admin.ModelAdmin):
    list_display = ['id', 'object', 'supplier_name', 'contract_number', 'delivery_date']
    list_display_links = ['object', 'supplier_name', 'contract_number', 'delivery_date']
    search_fields = ['supplier_name', 'contract_number', ]

admin.site.register(HydroStation, AdminHydroStation)


class AdminIndustrialAsset(admin.ModelAdmin):
    list_display = ['id', 'object', 'equipment_category',
                    'equipment_subcategory', 'quantity',
                    'country', 'code']
    list_display_links = ['object', 'equipment_category',
                    'equipment_subcategory', 'quantity',
                    'country', 'code']
    search_fields = ['object', 'equipment_category', 'equipment_subcategory', 'quantity', 'code']

admin.site.register(IndustrialAsset, AdminIndustrialAsset)