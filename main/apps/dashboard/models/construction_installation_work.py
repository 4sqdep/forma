from django.db import models
from main.apps.dashboard.models.dashboard import Object
from main.apps.common.models import BaseModel, BaseMeta



class Section(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, verbose_name="Loyiha nomi", blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")

    def __str__(self):
        return f"{self.title}"
    
    class Meta(BaseMeta):
        db_table = "sections"
        verbose_name = "Section"
        verbose_name_plural = "Sections"



class ConstructionFile(BaseModel):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, verbose_name="Project Section", blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    file_code = models.CharField(max_length=20, blank=True, null=True, )
    file = models.FileField(upload_to="document_files/", blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "installation_work"
        verbose_name = "Construction File"
        verbose_name_plural = "Construction Files"