from django.db import models
from main.apps.account.models.department import Department
from main.apps.common.models import BaseMeta, BaseModel
from django.utils.translation import gettext_lazy as _




class Position(BaseModel):
    name = models.CharField(max_length=50, unique=False, null=False, blank=False, verbose_name="Nomi")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bo'lim")

    class Meta(BaseMeta):
        verbose_name = "Lavozim"
        verbose_name_plural = "Lavozimlar"
    
    def __str__(self):
        return f"{self.department} - {self.name}"
    