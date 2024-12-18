from django.db import models
from ...common.models import BaseModel, BaseMeta
from .measurement import Measurement



class MaterialCategory(BaseModel):
    title = models.CharField(max_length=255)

    class Meta(BaseMeta):
        verbose_name = 'Material Category'
        verbose_name_plural = 'Material Categories' 

    def __str__(self):
        return self.title


class Material(BaseModel):
    material_category = models.ForeignKey(MaterialCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)

    class Meta(BaseMeta):
        verbose_name = 'Material'
        verbose_name_plural = 'Materials' 

    def __str__(self):
        return self.title