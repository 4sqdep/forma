import os
from django.db import models
from ..resource.models.equipment import Equipment, EquipmentCategory
from ..resource.models.material import Material, MaterialCategory
from ..common.models import BaseModel, BaseMeta
from django.utils import timezone
from django.utils.text import slugify


def upload_service_images(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"profile/{filename}"


class ServiceCategory(BaseModel):
    title = models.CharField(max_length=255)

    class Meta(BaseMeta):
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories' 

    def __str__(self):
        return self.title 



class Service(BaseModel):
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True)
    picture = models.ImageField(upload_to=upload_service_images, null=True, blank=True)
    title = models.CharField(max_length=255)
    # measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True, blank=True)
    equipment_category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    material_category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True)
    material= models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    service_price = models.DecimalField(max_digits=25, decimal_places=2, default='0.00')
    lead_time = models.DateTimeField()


    class Meta(BaseMeta):
        verbose_name = 'Service'
        verbose_name_plural = 'Services' 
