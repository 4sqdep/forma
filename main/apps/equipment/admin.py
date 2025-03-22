from django.contrib import admin
from main.apps.equipment.models.hydro_station import HydroStation
from main.apps.equipment.models.industrial_equipment import EquipmentCategory, EquipmentSubCategory, IndustrialAsset



admin.site.register(HydroStation)
admin.site.register(EquipmentCategory)
admin.site.register(EquipmentSubCategory)
admin.site.register(IndustrialAsset)