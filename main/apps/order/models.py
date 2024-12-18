from django.db import models
from ..common.models import BaseModel, BaseMeta
from ..checklist.models import CheckList




class Order(BaseModel):
    checklist = models.ForeignKey(CheckList, on_delete=models.SET_NULL, null=True)
    profitability_of_order = models.DecimalField(max_digits=25, decimal_places=2, default='0.00')
    total_lead_time = models.CharField(max_length=255, null=True, blank=True) 
    order_comment = models.TextField(null=True, blank=True)
    employee_note = models.TextField(null=True, blank=True)    


    class Meta(BaseMeta):
        verbose_name = 'Order'
        verbose_name_plural = 'Orders' 
