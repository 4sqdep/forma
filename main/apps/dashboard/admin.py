from django.contrib import admin
from main.apps.dashboard.models.dashboard import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton
from main.apps.dashboard.models.document import Files, NextStageDocuments, ProjectDocumentation, ProjectSections



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

@admin.register(ProjectDocumentation)
class ProjectDocumentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'subcategories_btn', 'name', 'order', 'created_at')


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


class ProjectSectionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'next_stage_documents', 'user', 'name', 'created_at', 'updated_at']
    list_display_links = ['name']
    search_fields = ['name']

admin.site.register(ProjectSections, ProjectSectionsAdmin)