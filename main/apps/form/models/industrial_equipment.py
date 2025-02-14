from django.db import models
from main.apps.common.models import BaseMeta, BaseModel, Measurement
from main.apps.equipment.models.hydro_station import HydroStation
from django.db.models import Sum




class IndustrialEquipment(BaseModel):
    hydro_station = models.ForeignKey(HydroStation, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "industrial_equipment"
        verbose_name = "Industrial Equipment"
        verbose_name_plural = "Industrial Equipment"



class IndustrialAsset(BaseModel):
    industrial_equipment = models.ForeignKey(IndustrialEquipment, on_delete=models.SET_NULL, null=True)
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True)
    text = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    country = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    total_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    delivered_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    delivered_in_percent = models.PositiveIntegerField()
    remaining_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    remaining_in_percent = models.PositiveIntegerField()
    expected_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    date = models.DateField()

    class Meta(BaseMeta):
        db_table = "industrial_asset"
        verbose_name = "Industrial Asset"
        verbose_name_plural = "Industrial Assets"

    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        super().save(*args, **kwargs)
        if self.industrial_equipment:
            self.update_industrial_equipment_total_cost()
        
    
    def delete(self, *args, **kwargs):
        industrial_equipment = self.industrial_equipment
        super().delete(*args, **kwargs)
        if industrial_equipment:
            industrial_equipment.total_cost = industrial_equipment.industrialasset_set.aggregate(total=Sum('total_amount'))['total'] or 0
            industrial_equipment.save()
        
    
    def update_industrial_equipment_total_cost(self):
        total_cost = self.industrial_equipment.industrialasset_set.aggregate(total=Sum('total_amount'))['total'] or 0
        self.industrial_equipment.total_cost = total_cost
        self.industrial_equipment.save()



    