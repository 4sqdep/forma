from django.contrib import admin
from .models.equipment import Equipment, EquipmentCategory
from .models.material import Material, MaterialCategory
from .models.measurement import Measurement
from .models.time_measurement import TimeMeasurement



admin.site.register(Equipment)
admin.site.register(EquipmentCategory)
admin.site.register(Material)
admin.site.register(MaterialCategory)
admin.site.register(Measurement)
admin.site.register(TimeMeasurement)