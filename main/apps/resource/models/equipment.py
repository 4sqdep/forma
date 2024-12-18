from django.db import models
from .measurement import Measurement
from .time_measurement import TimeMeasurement
from ...common.models import BaseModel, BaseMeta




class EquipmentCategory(BaseModel):
    title = models.CharField(max_length=255)

    class Meta(BaseMeta):
        verbose_name = 'Equipment Category '
        verbose_name_plural = 'Equipment Categories' 

    def __str__(self):
        return self.title 


class Equipment(BaseModel):
    equipment_category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    time_measurement = models.ForeignKey(TimeMeasurement, on_delete=models.CASCADE)

    class Meta(BaseMeta):
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment' 

    def __str__(self):
        return self.title 
    