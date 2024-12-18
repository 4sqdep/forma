from django.db import models
from main.apps.account.models import User
from main.apps.common.models import BaseMeta, BaseModel
from main.apps.statement.models.statement import Statement




class StatementInformation(BaseModel):
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE, null=True)
    discount_percent = models.DecimalField(max_digits=20, decimal_places=2, default='0.00')
    discount_sum = models.DecimalField(max_digits=30, decimal_places=2, default='0.00')
    duration_date = models.DateTimeField()
    statament_comment = models.TextField(blank=True)
    comment_for_employee = models.TextField(blank=True)

    class Meta(BaseMeta):
        verbose_name = 'Statement Information'
        verbose_name_plural = 'Statement Informations' 

    def __str__(self):
        return self.id