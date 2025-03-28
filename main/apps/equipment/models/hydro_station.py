from django.db import models
from main.apps.common.models import BaseMeta, BaseModel, Currency
from main.apps.dashboard.models.dashboard import Object
from decimal import Decimal
import os
from django.utils.timezone import now



def upload_hydro_station_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"hydro_station_files/{original_name}_{timestamp}{ext}"



class FinancialResourceType(models.TextChoices):
    FUNDS = "funds", "Funds"
    GES = "ges", "Ges"



class CalculationType(models.TextChoices):
    AMOUNT = 'amount', "Fixed Amount"
    PERCENT = 'percent', "Percentage"



class HydroStation(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, blank=True, null=True)
    supplier_name = models.CharField(max_length=255, null=True, blank=True)
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=upload_hydro_station_files, null=True, blank=True)
    contract_amount = models.DecimalField(max_digits=32, decimal_places=2, default=Decimal("0.00"))
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    calculation_type = models.CharField(max_length=255, choices=CalculationType.choices, default=CalculationType.PERCENT)
    financial_reource_type = models.CharField(max_length=255, choices=FinancialResourceType.choices, default=FinancialResourceType.FUNDS)
    prepayment_from_own_fund = models.DecimalField(max_digits=32, decimal_places=2, default=Decimal("0.00"))
    prepayment_from_foreign_credit_account = models.DecimalField(max_digits=32, decimal_places=2, default=Decimal("0.00"))
    additional_prepayment = models.DecimalField(max_digits=32, decimal_places=2, default=Decimal("0.00"))
    payment_on_completion = models.DecimalField(max_digits=32, decimal_places=2, default=Decimal("0.00"))
    transit_equipment_amount = models.DecimalField(max_digits=32, decimal_places=2, default=Decimal("0.00"))
    delivery_date = models.DateField()
    financial_resource_data = models.JSONField(default=list) 


    class Meta(BaseMeta):
        db_table = "hydro_station"
        verbose_name = "Hydro Station"
        verbose_name_plural = "Hydro Stations"
    

    def __str__(self):
        return f"{self.supplier_name}"



    


    