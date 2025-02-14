from django.db import models
from main.apps.common.models import BaseMeta, BaseModel, Currency
from main.apps.dashboard.models.dashboard import Object
from main.apps.common.utils import upload_file




class HydroStation(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, null=True)
    supplier_name = models.CharField(max_length=255, null=True, blank=True)
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to="contract_files/", null=True)
    contract_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    transit_equipment_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    delivery_date = models.DateField()

    class Meta(BaseMeta):
        db_table = "hydro_station"
        verbose_name = "Hydro Station"
        verbose_name_plural = "Hydro Stations"



class FinancialResource(BaseModel):
    hydro_station = models.ForeignKey(HydroStation, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    prepayment_from_own_fund = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    prepayment_from_foreign_credit_account = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    additional_prepayment = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    payment_on_completion = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "financial_resource"
        verbose_name = "Financial Resource"
        verbose_name_plural = "Financial Resources"

    


    