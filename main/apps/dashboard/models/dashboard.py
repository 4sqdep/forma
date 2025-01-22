from django.db import models
from main.apps.common.models import BaseModel, BaseMeta


class DashboardButton(BaseModel):
    """Dashboard button uchun asosiy button"""
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi", db_index=True)

    def __str__(self):
        return self.name

    class Meta(BaseMeta):
        verbose_name = "Dashboard Button"
        verbose_name_plural = "Asosiy Knopkalar"


class DashboardCategoryButton(BaseModel):
    """Dashboard button uchun Kategoriya button"""
    dashboard_button = models.ForeignKey(DashboardButton, on_delete=models.SET_NULL,
                                         verbose_name="Kinopka", null=True, blank=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi", db_index=True)

    def __str__(self):
        return self.name

    class Meta(BaseMeta):
        verbose_name = "Dashboard Category Button"
        verbose_name_plural = "Kategoriya Knopkalar"


class DashboardSubCategoryButton(BaseModel):
    """Dashboard button uchun SubKategoriya button"""
    dashboard_category_btn = models.ForeignKey(DashboardCategoryButton, on_delete=models.SET_NULL, verbose_name="Categoriya knopka", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi", db_index=True)

    def __str__(self):
        return self.name

    class Meta(BaseMeta):
        verbose_name = "Dashboard Sub Category Button"
        verbose_name_plural = "Obyekt nomlari"