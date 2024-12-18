from django.contrib import admin
from .models import Country, Region, District


admin.site.register(Country)
admin.site.register(Region)
admin.site.register(District)