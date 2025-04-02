import os
from django.db import models
from main.apps.common.models import BaseModel, BaseMeta
from decimal import Decimal
from django.utils.timezone import now
from main.apps.object_passport.models.object import Object



def upload_contract_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"contract_files/{original_name}_{timestamp}{ext}"
    


class ConstructionInstallationStatistics(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, blank=True, null=True)
    installation_work_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    date = models.DateField(null=True, blank=True)
    remanied_work_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    cost_of_performed_work = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    contract_file = models.FileField(upload_to=upload_contract_files, blank=True, null=True)
    contractor = models.CharField(max_length=255, null=True, blank=True)

    class Meta(BaseMeta):
        db_table = "construction_installation_statistics"
        verbose_name = "Construction Installation Statistics"
        verbose_name_plural = "Construction Installation Statistics"

    def save(self, *args, **kwargs):
        self.installation_work_amount = self.installation_work_amount or Decimal("0.00")
        self.cost_of_performed_work = self.cost_of_performed_work or Decimal("0.00")
        self.remanied_work_amount = self.installation_work_amount - self.cost_of_performed_work
        super().save(*args, **kwargs)

    