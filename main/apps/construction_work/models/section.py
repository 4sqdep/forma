from django.db import models
from main.apps.common.models import BaseModel, BaseMeta
from main.apps.object_passport.models.object import Object




class ConstructionInstallationSection(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, verbose_name="Loyiha nomi", blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")
    is_forma = models.BooleanField(default=False, verbose_name="Forma")
    is_file = models.BooleanField(default=False, verbose_name="Fayl yuklash")

    def __str__(self):
        return f"{self.title}"
    
    class Meta(BaseMeta):
        db_table = "construction_installation_section"
        verbose_name = "Construction Installation Section"
        verbose_name_plural = "Construction Installation Sections"