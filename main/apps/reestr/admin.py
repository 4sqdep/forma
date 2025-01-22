from django.contrib import admin
from main.apps.reestr.models.construction import MonthlyExpense, ConstructionTask, Year, Month



admin.site.register(ConstructionTask)
admin.site.register(MonthlyExpense)
admin.site.register(Year)
admin.site.register(Month)