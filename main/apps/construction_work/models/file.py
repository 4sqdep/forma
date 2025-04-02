import os
from django.db import models
from main.apps.common.models import BaseModel, BaseMeta
from django.utils.timezone import now
from ..models.section import ConstructionInstallationSection




def upload_construction_installation_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"construction_installation_files/{original_name}_{timestamp}{ext}"



class ConstructionInstallationFile(BaseModel):
    section = models.ForeignKey(ConstructionInstallationSection, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    file_code = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=upload_construction_installation_files, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "installation_file"
        verbose_name = "Construction Installation File"
        verbose_name_plural = "Construction Installation Files"
