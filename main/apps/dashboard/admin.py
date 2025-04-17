from django.contrib import admin
from main.apps.dashboard.models.dashboard import ObjectCategory, ObjectSubCategory



class ObjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug_name']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(ObjectCategory, ObjectCategoryAdmin)


class ObjectSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'object_category', 'name']
    list_display_links = ['object_category', 'name']
    search_fields = ['name']


admin.site.register(ObjectSubCategory, ObjectSubCategoryAdmin)


class ObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'object_subcategory', 'title']
    list_display_links = ['title']
    search_fields = ['title']

