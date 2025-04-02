# from django.db import models
# from main.apps.common.models import BaseMeta, BaseModel
# from main.apps.dashboard.models.dashboard import (
#     ObjectCategory, 
#     ObjectSubCategory, 
#     Object
# )




# class ObjectsPassword(BaseModel):
#     main_btn = models.ForeignKey(ObjectCategory, on_delete=models.SET_NULL, null=True, blank=True,
#                                     verbose_name="Asosiy knopkalar")
#     category_btn = models.ForeignKey(ObjectSubCategory, on_delete=models.SET_NULL, null=True, blank=True,
#                                      verbose_name="Kategoriya knopkalar")
#     subcategory_btn = models.ForeignKey(Object, on_delete=models.SET_NULL, null=True, blank=True,
#                                         verbose_name="Obyekt nomi")
#     smr_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Qurilish summasi")
#     equipment_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Uskunalar summasi")
#     investment_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Investitsiya summasi")
#     uge_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="UZBEKGIDRO summasi")
#     total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Obyekt umumiy summasi")
#     total_power = models.CharField(max_length=200, null=True, blank=True, verbose_name="Umumiy quvvat")
#     start_date = models.DateField(null=True, blank=True, verbose_name="Qurilish boshlangan vaqti")
#     end_date = models.DateField(null=True, blank=True, verbose_name="Qurilish tuganlangan vaqti")
#
#     def __str__(self):
#         return f"{self.project_documentation}"
#
#     class Meta(BaseMeta):
#         db_table = "objects_password"
#         verbose_name = "Obyekt paspord modeli"
#         verbose_name_plural = "Obyekt paspordi"
#
#
#
# class Files(BaseModel):
#     obj_password = models.ForeignKey(ObjectsPassword, on_delete=models.SET_NULL, null=True, blank=True,
#                                      verbose_name="Obyekt pasporti")
#     file = models.FileField(upload_to="objpassword/files/%Y/%m/%d", null=True, blank=True, verbose_name="Fayl")\
#
#     class Meta(BaseMeta):
#         db_table = "main_files"
#         verbose_name = "Fayl"
#         verbose_name_plural = "Fayllar"
#
#     def __str__(self):
#         return f"{self.created_by}"

    