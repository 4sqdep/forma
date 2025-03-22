from django.db import models
from main.apps.dashboard.models.dashboard import Object
from main.apps.common.models import BaseModel, BaseMeta, Currency
from decimal import Decimal
import os
from django.utils.timezone import now



def upload_contract_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"contract_files/{original_name}_{timestamp}{ext}"


def upload_construction_installation_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"construction_installation_files/{original_name}_{timestamp}{ext}"




class ConstructionInstallationSection(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, verbose_name="Loyiha nomi", blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")
    is_forma = models.BooleanField(default=False, verbose_name="Forma")
    is_file = models.BooleanField(default=False, verbose_name="Fayl yuklash")

    def __str__(self):
        return f"{self.title}"
    
    class Meta(BaseMeta):
        db_table = "construction_installation_section"
        verbose_name = "Construction Installation Section"
        verbose_name_plural = "Construction Installation Sections"



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



class ConstructionInstallationFile(BaseModel):
    section = models.ForeignKey(ConstructionInstallationSection, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    file_code = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=upload_construction_installation_files, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "installation_file"
        verbose_name = "Construction Installation File"
        verbose_name_plural = "Construction Installation Files"



class ConstructionInstallationProject(BaseModel):
    section = models.ForeignKey(ConstructionInstallationSection, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    allocated_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "construction_installation_project"
        verbose_name = "Construction Installation Project"
        verbose_name_plural = "Construction Installation Projects"



class MonthlyCompletedTask(BaseModel):
    construction_installation_project = models.ForeignKey(
        ConstructionInstallationProject, 
        on_delete=models.SET_NULL,  
        related_name="monthly_tasks", 
        blank=True, 
        null=True
    )
    date = models.DateField(blank=True, null=True)
    monthly_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')

    class Meta(BaseMeta):
        db_table = "monthly_completed_task"
        verbose_name = "Monthly Completed Task"
        verbose_name_plural = "Monthly Completed Tasks"