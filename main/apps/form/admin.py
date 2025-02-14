from django.contrib import admin
from main.apps.equipment.models.hydro_station import HydroStation, FinancialResource
from main.apps.equipment.models.industrial_equipment import IndustrialEquipment, IndustrialAsset



admin.site.register(HydroStation)
admin.site.register(FinancialResource)
admin.site.register(IndustrialEquipment)
admin.site.register(IndustrialAsset)