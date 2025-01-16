from django.db import models
from main.apps.common.models import BaseMeta, BaseModel
from main.apps.dashboard.models.dashboard import (
    DashboardButton, 
    DashboardCategoryButton, 
    DashboardSubCategoryButton
)
from main.apps.dashboard.models.document import ProjectDocumentation



class ObjectsPassword(BaseModel):
    """Obyektlar uchun paspord modeli"""
    main_btn = models.ForeignKey(DashboardButton, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name="Asosiy knopkalar")
    category_btn = models.ForeignKey(DashboardCategoryButton, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name="Kategoriya knopkalar")
    subcategory_btn = models.ForeignKey(DashboardSubCategoryButton, on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name="Obyekt nomi")
    project_documentation = models.ForeignKey(ProjectDocumentation, on_delete=models.SET_NULL, null=True, blank=True,
                                              verbose_name="Obyekt bo'limi")
    smr_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Qurilish summasi")
    equipment_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Uskunalar summasi")
    investment_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Investitsiya summasi")
    uge_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="UZBEKGIDRO summasi")
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Obyekt umumiy summasi")
    total_power = models.CharField(max_length=200, null=True, blank=True, verbose_name="Umumiy quvvat")

    def __str__(self):
        return self.project_documentation.name

    class Meta(BaseMeta):
        verbose_name = "Obyekt paspord modeli"
        verbose_name_plural = "Obyekt paspordi"


class Files(BaseModel):
    """Obyekt paspotriga tegishli fayllar uchun modeli"""
    obj_password = models.ForeignKey(ObjectsPassword, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name="Obyekt pasporti")
    file = models.FileField(upload_to="objpassword/files/%Y/%m/%d", null=True, blank=True, verbose_name="Fayl")\
    
    class Meta(BaseMeta):
        verbose_name = "Fayl"
        verbose_name_plural = "Fayllar"

    def __str__(self):
        return self.created_at

    