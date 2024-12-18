from django.db import models
from main.apps.common.models import BaseMeta
from main.apps.resource.models.material import Material, MaterialCategory
from .base import WarehouseBaseModel



class MaterialWarehouse(WarehouseBaseModel):
    material_category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)
    price_per_unit = models.DecimalField(max_digits=25, decimal_places=2, default='0.00')
    total_price = models.DecimalField(max_digits=25, decimal_places=2, default='0.00')


    class Meta(BaseMeta):
        verbose_name = 'Material Warehouse'
        verbose_name_plural = 'Material Warehouses' 

    def __str__(self):
        return str(self.material_category) if self.material_category else "No Category"


    def save(self, *args, **kwargs):
        self.total_price = self.price_per_unit * self.quantity
        super().save(*args, **kwargs)