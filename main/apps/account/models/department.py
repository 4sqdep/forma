from django.db import models
from main.apps.common.models import BaseMeta, BaseModel
from django.utils.translation import gettext_lazy as _




class Department(BaseModel):
    user = models.OneToOneField('account.User', on_delete=models.SET_NULL, null=True, related_name="department",
                                      blank=True, verbose_name="Foydalanuvchi")
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name="Nomi")

    class Meta(BaseMeta):
        db_table = "department"
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

    def __str__(self):
        return f"{self.user} -- {self.name}"

    