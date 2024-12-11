from django.contrib import admin
from .models import (DashboardButton, DashboardCategoryButton, NextStageDocuments,
                     DashboardSubCategoryButton, ProjectDocumentation, Files)


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

class NextStageDocumentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subcategories_btn', 'project_document', 'name', 'created_at']
    list_display_links = ['project_document', 'name']
    search_fields = ['name', 'project_document']


admin.site.register(NextStageDocuments, NextStageDocumentsAdmin)


class FilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'user', 'files', 'created_at']
    list_display_links = ['document', 'files']
    search_fields = ['created_at', 'files']


admin.site.register(Files, FilesAdmin)