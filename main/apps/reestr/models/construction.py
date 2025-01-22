from django.db import models
from main.apps.account.models.user import User
from main.apps.common.models import BaseMeta, BaseModel
from main.apps.dashboard.models.document import NextStageDocuments
from main.apps.reestr.models.currency import Currency
from main.apps.reestr.models.time_period import Month, Year



class ConstructionTask(BaseModel):
    next_stage_document = models.ForeignKey(NextStageDocuments, on_delete=models.SET_NULL, null=True)
    employee = models.ManyToManyField(User, verbose_name='Xodimlar', blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, verbose_name="Ish nomi")
    total_cost = models.DecimalField(max_digits=32, decimal_places=2, null=True, blank=True, verbose_name="Umumiy xarajat summa")

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        verbose_name = "Construction Task"
        verbose_name_plural = "Construction Tasks"



class MonthlyExpense(BaseModel):
    year = models.ManyToManyField(
        Year, 
        related_name="monthly_expenses", 
        blank=True, 
        verbose_name="Yil"
    )
    month = models.ForeignKey(
        Month, 
        on_delete=models.SET_NULL, 
        related_name="monthly_expenses", 
        blank=True, 
        null=True, 
        verbose_name="Oy"
    )
    construction_task = models.ForeignKey(
        ConstructionTask, 
        on_delete=models.SET_NULL, 
        related_name="monthly_construction_task", 
        verbose_name="Qurilish ishlari", 
        blank=True, 
        null=True
    )
    spent_amount = models.DecimalField(max_digits=32, decimal_places=2, default=0, verbose_name="Sarflangan summa")
    amount = models.DecimalField(max_digits=32, decimal_places=2, null=True, blank=True, verbose_name="Miqdori")
    total_year = models.DecimalField(max_digits=32, decimal_places=2, null=True, blank=True, verbose_name="Jami yil summa")
    total_fact = models.DecimalField(max_digits=32, decimal_places=2, null=True, blank=True, verbose_name="Jami fakt summa")
    total_fact_amount = models.DecimalField(max_digits=32, decimal_places=2, null=True, blank=True, verbose_name="Jami fakt summa")
    difference_amount = models.DecimalField(max_digits=32, decimal_places=2, null=True, blank=True, verbose_name="Farq summa")
    total_difference_amount = models.DecimalField(max_digits=32, decimal_places=2, null=True, blank=True, verbose_name="Jami Farq summa")

    def __str__(self):
        return f"{self.month.title}, {self.construction_task.title}"

    class Meta(BaseMeta):
        verbose_name = "Monthly Expense"
        verbose_name_plural = "Monthly Expenses"
    


    