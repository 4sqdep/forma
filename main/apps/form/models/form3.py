from django.db import models
from main.apps.account.models.user import User
from main.apps.common.models import BaseMeta, BaseModel, Currency
from main.apps.dashboard.models.dashboard import Object
    



class DocumentType(models.TextChoices):
    CREATED = 'created', "Created"
    IN_TRANSIT = 'in_transit', "In Transit"
    DELIVERED = 'delivered', "Delivered"



class Form3(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    total_amount_year = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    vat = models.PositiveIntegerField()
    
    work_volume_from_construction_beginning = models.PositiveIntegerField()
    current_contract_amount_from_construction_beginning = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    
    work_volume_from_year_beginnging = models.PositiveIntegerField()
    current_contract_amount_from_year_beginnging = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')

    work_volume_for_month = models.PositiveIntegerField()
    current_contract_amount_for_month = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')


    class Meta(BaseMeta):
        db_table = "form3"
        verbose_name = "Form3"
        verbose_name_plural = "Form3"

    