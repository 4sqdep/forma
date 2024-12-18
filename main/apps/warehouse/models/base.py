from django.db import models
from main.apps.common.models import BaseMeta, BaseModel
from main.apps.resource.models.measurement import Measurement



class WarehouseBaseModel(BaseModel):
    quantity = models.PositiveIntegerField(default=1)
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True  
