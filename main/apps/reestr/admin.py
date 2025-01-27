from django.contrib import admin
from main.apps.reestr.models.construction import MonthlyExpense, ConstructionTask
from main.apps.reestr.models.currency import Currency



admin.site.register(ConstructionTask)
admin.site.register(MonthlyExpense)
admin.site.register(Currency)