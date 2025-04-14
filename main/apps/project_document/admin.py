from django.contrib import admin
from main.apps.project_document.models.project_section import ProjectSection
from main.apps.project_document.models.project_document_type import ProjectDocumentType


class ProjectSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'project_document_type', 'name']
    list_display_links = ['project_document_type', 'name']
    search_fields = ['name']
admin.site.register(ProjectSection, ProjectSectionAdmin)


class ProjectDocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'object', 'name', 'is_forma', 'is_section', 'is_file']
    list_display_links = ['object', 'name', 'is_forma', 'is_section', 'is_file']
    search_fields = ['name']


admin.site.register(ProjectDocumentType, ProjectDocumentTypeAdmin)
