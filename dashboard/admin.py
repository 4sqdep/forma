from django.contrib import admin
from .models import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton, ProjectDocumentation


class DashboardButtonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(DashboardButton, DashboardButtonAdmin)


class DashboardCategoryButtonAdmin(admin.ModelAdmin):
    list_display = ['id', 'dashboard_button', 'name', 'created_at']
    list_display_links = ['dashboard_button', 'name']
    search_fields = ['name']


admin.site.register(DashboardCategoryButton, DashboardCategoryButtonAdmin)


class DashboardSubCategoryButtonAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'dashboard_category_btn', 'name', 'created_at']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(DashboardSubCategoryButton, DashboardSubCategoryButtonAdmin)


class ProjectDocumentationAdmin(admin.ModelAdmin):
    list_display = ['id', 'subcategories_btn', 'user', 'name', 'created_at']
    list_display_links = ['subcategories_btn', 'name']
    search_fields = ['name']

admin.site.register(ProjectDocumentation, ProjectDocumentationAdmin)
