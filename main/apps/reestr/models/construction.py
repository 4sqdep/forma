from django.db import models
from main.apps.account.models.user import User
from main.apps.common.models import BaseMeta, BaseModel, Currency
from main.apps.dashboard.models.document import NextStageDocuments




class ConstructionTask(BaseModel):
    next_stage_document = models.ForeignKey(NextStageDocuments, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ManyToManyField(User, verbose_name='Xodimlar', blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, verbose_name="Ish nomi")
    total_cost = models.DecimalField(max_digits=32, decimal_places=2, null=True, blank=True, verbose_name="Umumiy xarajat summa")

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "construction_task"
        verbose_name = "Construction Task"
        verbose_name_plural = "Construction Tasks"



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
    


    