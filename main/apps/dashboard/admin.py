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
    list_display = ['id', 'created_by_full_name', 'subcategories_btn', 'project_document', 'name',
                    'is_file', 'is_forma', 'is_section']
    list_display_links = ['project_document', 'name']
    search_fields = ['name', 'project_document']


    def created_by_full_name(self, obj):
        if obj.created_by:  # created_by mavjudligini tekshiramiz
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return "No user assigned"


admin.site.register(NextStageDocuments, NextStageDocumentsAdmin)


class FilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'project_section', 'created_by', 'files']
    list_display_links = ['document', 'files']


admin.site.register(Files, FilesAdmin)


class ProjectSectionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'next_stage_documents', 'created_by', 'name']
    list_display_links = ['name']
    search_fields = ['name']

admin.site.register(ProjectSections, ProjectSectionsAdmin)