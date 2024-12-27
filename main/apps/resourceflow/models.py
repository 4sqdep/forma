from django.db import models
from main.apps.account.models import User
from main.apps.resource.models.equipment import Equipment, EquipmentCategory
from main.apps.resource.models.material import Material, MaterialCategory
from main.apps.resource.models.measurement import Measurement
from ..common.models import BaseModel, BaseMeta



class StatusChoices(models.TextChoices):
    NEW = 'new'
    IN_PROGRESS = 'in progress'
    RESOLVED = 'resolved'
    REJECTED = 'rejected'
    CLOSED = 'closed'



class ResourceRequest(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resource_request_sender')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resource_ruest_receiver')    
    request_for = models.BooleanField(default=False)
    text = models.TextField(null=True, blank=True)
    equipment_category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True)
    material_category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    pickup_time = models.DateTimeField()
    return_time = models.DateTimeField()
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.NEW)
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True)

    class Meta(BaseMeta):
        verbose_name = 'Resource Request'
        verbose_name_plural = 'Resource Requests' 



class ResourceReturn(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_return_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_return_receiver')    
    request_for = models.BooleanField(default=False)
    text = models.TextField(null=True, blank=True)
    equipment_category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True)
    material_category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    pickup_time = models.DateTimeField()
    return_time = models.DateTimeField()
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.NEW)
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True)

    class Meta(BaseMeta):
        verbose_name = 'Resource Return'
        verbose_name_plural = 'Resource Returns' 

    

