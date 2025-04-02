from django.db import models
from main.apps.common.models import BaseModel, BaseMeta
from main.apps.object_passport.models.object import Object




class ProjectDocumentType(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, verbose_name="Loyiha nomi", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")
    is_forma = models.BooleanField(default=False, verbose_name="Forma")
    is_section = models.BooleanField(default=False, verbose_name="Bo'lim")
    is_file = models.BooleanField(default=False, verbose_name="Fayl yuklash")

    def __str__(self):
        return f"{self.name}"

    class Meta(BaseMeta):
        db_table = "project_document_type"
        verbose_name = "Project Document Type"
        verbose_name_plural = "Project Document Types"