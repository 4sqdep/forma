from django.contrib import admin
from main.apps.equipment.models.hydro_station import HydroStation, FinancialResource


admin.site.register(HydroStation)
admin.site.register(FinancialResource)