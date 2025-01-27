from django.db import models
from main.apps.common.models import BaseMeta, BaseModel
from main.apps.reestr.models.currency import Currency



class HydroStation(BaseModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    supplier_name = models.CharField(max_length=255, null=True, blank=True)
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    contract_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    delivery_date = models.DateField()
    

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
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
        verbose_name = "Financial Resource"
        verbose_name_plural = "Financial Resources"

    


    