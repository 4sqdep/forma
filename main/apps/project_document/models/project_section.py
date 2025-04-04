from django.db import models
from main.apps.common.models import BaseModel, BaseMeta
from main.apps.project_document.models.project_document_type import ProjectDocumentType




class ProjectSection(BaseModel):
    project_document_type = models.ForeignKey(ProjectDocumentType, on_delete=models.SET_NULL, verbose_name="Keyingi hujjat", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")

    def __str__(self):
        return f"{self.project_document_type} -- {self.name}"
    
    class Meta(BaseMeta):
        db_table = "project_section"
        verbose_name = "Project Section"
        verbose_name_plural = "Project Sections"

