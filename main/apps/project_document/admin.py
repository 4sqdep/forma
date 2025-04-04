from django.contrib import admin
from main.apps.project_document.models.project_section import ProjectSection
from main.apps.project_document.models.project_document_type import ProjectDocumentType


admin.site.register(ProjectSection)
admin.site.register(ProjectDocumentType)