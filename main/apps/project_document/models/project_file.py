import os
from django.utils.timezone import now
from django.db import models
from main.apps.common.models import BaseModel, BaseMeta
from main.apps.project_document.models.project_document_type import ProjectDocumentType
from main.apps.project_document.models.project_section import ProjectSection



def upload_document_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"document_files/{original_name}_{timestamp}{ext}"



class       ProjectDocumentFile(BaseModel):
    project_document_type = models.ForeignKey(ProjectDocumentType, on_delete=models.SET_NULL, verbose_name="Project Document type", blank=True, null=True)
    project_section = models.ForeignKey(ProjectSection, on_delete=models.SET_NULL, verbose_name="Project Section", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    full_name = models.CharField(max_length=1000, blank=True, null=True)
    calendar = models.DateField(blank=True, null=True)
    file_code = models.CharField(max_length=20, blank=True, null=True, )
    file = models.FileField(upload_to=upload_document_files, blank=True, null=True)

    def __str__(self):
        return f"{self.project_document_type} -- {self.name}"

    class Meta(BaseMeta):
        db_table = "project_document_file"
        verbose_name = "Project Document File"
        verbose_name_plural = "Project Document Files"