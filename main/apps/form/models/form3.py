from django.db import models
from main.apps.account.models.user import User
from main.apps.common.models import BaseMeta, BaseModel
    



class DocumentType(models.TextChoices):
    CREATED = 'created', "Created"
    IN_TRANSIT = 'in_transit', "In Transit"
    DELIVERED = 'delivered', "Delivered"


class Form3(BaseModel):
    inn_number = models.CharField(max_length=255, null=True, blank=True)
    organization_name = models.CharField(max_length=355, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    



    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "industrial_equipment"
        verbose_name = "Industrial Equipment"
        verbose_name_plural = "Industrial Equipment"


    