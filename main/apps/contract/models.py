from django.db import models
from ..common.models import BaseModel, BaseMeta
from ..checklist.models import CheckList




class Contract(BaseModel):
    checklist = models.ForeignKey(CheckList, on_delete=models.SET_NULL, null=True)
    subject_of_contract = models.TextField(null=True, blank=True)
    contract_amount = models.DecimalField(max_digits=25, decimal_places=2, default='0.00')
    date = models.DateField()
 

    class Meta(BaseMeta):
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts' 

    def __str__(self):
        return self.contract_number 