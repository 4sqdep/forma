from django.contrib import admin
from main.apps.dashboard.models.dashboard import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton
from main.apps.dashboard.models.document import Files, NextStageDocuments, ProjectDocumentation, ProjectSections



class DashboardButtonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(DashboardButton, DashboardButtonAdmin)


class DashboardCategoryButtonAdmin(admin.ModelAdmin):
    list_display = ['id', 'dashboard_button', 'name']
    list_display_links = ['dashboard_button', 'name']
    search_fields = ['name']


admin.site.register(DashboardCategoryButton, DashboardCategoryButtonAdmin)


class DashboardSubCategoryButtonAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'dashboard_category_btn', 'name']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(DashboardSubCategoryButton, DashboardSubCategoryButtonAdmin)

@admin.register(ProjectDocumentation)
class ProjectDocumentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'subcategories_btn', 'name', 'order')


class NextStageDocumentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'subcategories_btn', 'project_document', 'name']
    list_display_links = ['project_document', 'name']
    search_fields = ['name', 'project_document']


admin.site.register(NextStageDocuments, NextStageDocumentsAdmin)


class FilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'created_by', 'files']
    list_display_links = ['document', 'files']


admin.site.register(Files, FilesAdmin)


class ProjectSectionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'next_stage_documents', 'created_by', 'name']
    list_display_links = ['name']
    search_fields = ['name']

admin.site.register(ProjectSections, ProjectSectionsAdmin)