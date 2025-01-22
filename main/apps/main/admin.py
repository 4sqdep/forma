from django.contrib import admin
from .models import ObjectsPassword


class ObjectsPasswordAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'main_btn', 'category_btn', 'subcategory_btn', 'project_documentation', 'smr_price',
                    'equipment_price', 'investment_price', 'uge_price', 'total_price', 'total_power']
    list_display_links = ['main_btn', 'category_btn', 'subcategory_btn', 'project_documentation', 'total_price']
    search_fields = ['main_btn__name', 'category_btn__name', 'subcategory_btn__name', 'project_documentation__name',
                     'smr_price', 'equipment_price', 'investment_price', 'uge_price', 'total_price', 'total_power']

admin.site.register(ObjectsPassword, ObjectsPasswordAdmin)