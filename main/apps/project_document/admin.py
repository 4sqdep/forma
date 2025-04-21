from django.contrib import admin
from main.apps.project_document.models.project_section import ProjectSection
from main.apps.project_document.models.project_document_type import ProjectDocumentType
from main.apps.project_document.models.project_file import ProjectDocumentFile


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


class ProjectDocumentFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'project_document_type', 'project_section', 'name', 'calendar']
    list_display_links = ['project_document_type', 'project_section', 'name', 'calendar']
    search_fields = ['name']


admin.site.register(ProjectDocumentFile, ProjectDocumentFileAdmin)
