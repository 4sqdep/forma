from django.db import models
from ...common.models import BaseModel, BaseMeta




class Measurement(BaseModel):
    title = models.CharField(max_length=255)
    short_title = models.CharField(max_length=255)

    class Meta(BaseMeta):
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurements' 

    def __str__(self):
        return self.short_title