from django.db import models
from main.apps.common.models import BaseMeta, BaseModel, Currency
from main.apps.project_document.models.project_document_type import ProjectDocumentType




class ConstructionTask(BaseModel):
    project_document_type = models.ForeignKey(ProjectDocumentType, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, verbose_name="Ish nomi")
    total_cost = models.DecimalField(max_digits=32, decimal_places=2, null=True, blank=True, verbose_name="Umumiy xarajat summa")

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "project_construction_task"
        verbose_name = "Project Construction Task"
        verbose_name_plural = "Project ConstructionT asks"



class MonthlyExpense(BaseModel):
    construction_task = models.ForeignKey(
        ConstructionTask, 
        on_delete=models.SET_NULL, 
        related_name="monthly_construction_task", 
        verbose_name="Qurilish ishlari", 
        blank=True, 
        null=True
    )
    spent_amount = models.DecimalField(max_digits=32, decimal_places=2, default=0, verbose_name="Sarflangan summa")
    date = models.DateField()

    class Meta(BaseMeta):
        db_table = "monthly_expense"
        verbose_name = "Monthly Expense"
        verbose_name_plural = "Monthly Expenses"
    


    