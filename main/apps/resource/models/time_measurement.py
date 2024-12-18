from django.db import models
from ...common.models import BaseModel, BaseMeta




class TimeMeasurement(BaseModel):
    title = models.CharField(max_length=255)

    class Meta(BaseMeta):
        verbose_name = 'Time Measurement'
        verbose_name_plural = 'Time Measurements' 

    def __str__(self):
        return self.title
