from django.contrib import admin
from main.apps.warehouse.models.equipment_warehouse import EquipmentWarehouse
from main.apps.warehouse.models.material_warehouse import MaterialWarehouse



admin.site.register(EquipmentWarehouse)
admin.site.register(MaterialWarehouse)
