from django.db import models
from main.apps.common.models import BaseMeta, BaseModel, Measurement
from main.apps.equipment.models.hydro_station import HydroStation
from django.db.models import Sum

from main.apps.object_passport.models.object import Object



class EquipmentStatus(models.TextChoices):
    CREATED = 'created', "Created"
    IN_TRANSIT = 'in_transit', "In Transit"
    DELIVERED = 'delivered', "Delivered"



class EquipmentCategory(BaseModel):
    hydro_station = models.ForeignKey(HydroStation, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    has_subcategories = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "equipment_category"
        verbose_name = "Equipment Category"
        verbose_name_plural = "Equipment Categories"


class EquipmentSubCategory(BaseModel):
    equipment_category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "equipment_subcategory"
        verbose_name = "Equipment SubCategory"
        verbose_name_plural = "Equipment SubCategories"



class IndustrialAsset(BaseModel):
    equipment_category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True)
    equipment_subcategory = models.ForeignKey(EquipmentSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, null=True, blank=True)
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True)
    text = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    country = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    total_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    delivered_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    status = models.CharField(max_length=20, choices=EquipmentStatus.choices, default=EquipmentStatus.CREATED, verbose_name="Holati")
    date = models.DateField()

    class Meta(BaseMeta):
        db_table = "industrial_asset"
        verbose_name = "Industrial Asset"
        verbose_name_plural = "Industrial Assets"

    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        super().save(*args, **kwargs)
        if self.equipment_category:
            self.update_equipment_category_total_cost()
        
    
    def delete(self, *args, **kwargs):
        equipment_category = self.equipment_category
        super().delete(*args, **kwargs)
        if equipment_category:
            equipment_category.total_cost = equipment_category.industrialasset_set.aggregate(total=Sum('total_amount'))['total'] or 0
            equipment_category.save()
        
    
    def update_equipment_category_total_cost(self):
        total_cost = self.equipment_category.industrialasset_set.aggregate(total=Sum('total_amount'))['total'] or 0
        self.equipment_category.total_cost = total_cost
        self.equipment_category.save()



    