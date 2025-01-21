from django.contrib import admin
from main.apps.reestr.models.construction import MonthlyExpense, ConstructionTask



admin.site.register(ConstructionTask)
admin.site.register(MonthlyExpense)