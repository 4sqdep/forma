from django.db import models
from main.apps.resource.models.time_measurement import TimeMeasurement
from main.apps.service.models import Service, ServiceCategory
from main.apps.statement.models.statement import Statement
from ..resource.models.equipment import Equipment, EquipmentCategory
from ..common.models import BaseModel, BaseMeta



class BuildingTypeChoices(models.TextChoices):
    COTTAGE = 'cottage'
    FLAT = 'flat'
    OFFICE = 'office'
    INDUSTRIAL_PREMISES = 'industrial premises'
    SHOP = 'shop'
    SHOPPING_MALL = 'shopping mall'



class CheckList(BaseModel):
    statement = models.ForeignKey(Statement, on_delete=models.SET_NULL, null=True, related_name="order_statements")
    building_type = models.CharField(max_length=255, choices=BuildingTypeChoices.choices)
    building_area = models.PositiveIntegerField()
    service_category = models.ManyToManyField(ServiceCategory, null=True, blank=True)
    service = models.ManyToManyField(Service, null=True, blank=True)
    service_total_price = models.DecimalField(max_digits=25, decimal_places=2, default='0.00')
    equipment_category = models.ManyToManyField(EquipmentCategory, null=True)
    equipment = models.ManyToManyField(Equipment, null=True)
    measurement = models.ForeignKey(TimeMeasurement, on_delete=models.SET_NULL, null=True)
    equipment_total_price = models.DecimalField(max_digits=25, decimal_places=2, default='0.00') 
    payment_for_employment = models.DecimalField(max_digits=25, decimal_places=2, default='0.00')
    payment_from_client = models.DecimalField(max_digits=25, decimal_places=2, default='0.00')
    discount_percent = models.DecimalField(max_digits=25, decimal_places=2)
    discount_sum = models.DecimalField(max_digits=25, decimal_places=2)
   

    class Meta(BaseMeta):
        verbose_name = 'CheckList'
        verbose_name_plural = 'CheckLists' 
    

