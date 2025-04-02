from django.db import models
from main.apps.common.models import BaseModel, BaseMeta, Currency
from main.apps.construction_work.models.section import ConstructionInstallationSection





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
