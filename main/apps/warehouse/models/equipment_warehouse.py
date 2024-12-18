from django.db import models
from main.apps.common.models import BaseMeta
from main.apps.resource.models.equipment import Equipment, EquipmentCategory
from main.apps.resource.models.time_measurement import TimeMeasurement
from .base import WarehouseBaseModel




class StatusChoices(models.TextChoices):
    IN_STOCK = 'in stock'
    IN_USE = 'in use'
    UNDER_REPAIR = 'under repair'
    BOOKED = 'booked'
    DEPRECATED = 'deprecated'


class EquipmentWarehouse(WarehouseBaseModel):
    equipment_category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=255, choices=StatusChoices.choices)
    time_measurement = models.ManyToManyField(TimeMeasurement)
    measurement_data = models.JSONField(default=dict)


    class Meta(BaseMeta):
        verbose_name = 'Equipment Warehouse'
        verbose_name_plural = 'Equipment Warehouses' 

    def __str__(self):
        return str(self.equipment) if self.equipment else "No Equipment"
    