from django.db import models
from main.apps.common.models import BaseModel, BaseMeta, Currency
from django.utils.text import slugify
import os
from django.utils.timezone import now



def upload_object_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"object_files/{original_name}_{timestamp}{ext}"



class ObjectCategory(BaseModel):
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")
    slug_name = models.SlugField(unique=True, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.name:
            self.slug_name = slugify(self.name).replace('-', '_')
        super(ObjectCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta(BaseMeta):
        db_table = "object_category"
        verbose_name = "Object Category"
        verbose_name_plural = "Object Categories"



class ObjectSubCategory(BaseModel):
    object_category = models.ForeignKey(ObjectCategory, on_delete=models.SET_NULL,
                                         verbose_name="Kinopka", null=True, blank=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")

    def __str__(self):
        return self.name

    class Meta(BaseMeta):
        db_table = "object_subcategory"
        verbose_name = "Object SubCategory"
        verbose_name_plural = "Object SubCategories"



class Object(BaseModel):
    object_category = models.ForeignKey(ObjectCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Obyekt Categoriya")
    object_subcategory = models.ForeignKey(ObjectSubCategory, on_delete=models.SET_NULL, verbose_name="Obyekt Subcategoriya", blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")
    construction_work_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00', verbose_name="Qurilish ishlar summasi")
    equipment_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00', verbose_name="Uskunalar summasi")
    other_expense = models.DecimalField(max_digits=32, decimal_places=2, default='0.00', verbose_name="Boshqa xarajatlar")
    total_price = models.DecimalField(max_digits=32, decimal_places=2, default='0.00', verbose_name="Obyekt umumiy summasi")
    object_power = models.FloatField(null=True, blank=True, verbose_name='Obyetk umumiy quvvati')
    annual_electricity_production = models.FloatField(null=True, blank=True, verbose_name='Yillik elektr ishlab chiqarish')
    pressure = models.FloatField(null=True, blank=True, verbose_name='Bosim')
    water_consumption = models.FloatField(null=True, blank=True, verbose_name="Suv sarfi")
    community_fund = models.DecimalField(max_digits=32, decimal_places=2, default='0.00', verbose_name="UZBEKGIDRO summasi")
    foreign_loan = models.DecimalField(max_digits=32, decimal_places=2, default='0.00', verbose_name="Xorijiy kredit")
    object_file = models.FileField(upload_to=upload_object_files, blank=True, null=True)
    useful_work_coefficient = models.FloatField(max_length=30, null=True, blank=True, verbose_name="Foydali ish koeffitsiyenti")
    latitude = models.CharField(max_length=25, verbose_name="Kenglik", null=True, blank=True)
    longitude = models.CharField(max_length=25, verbose_name="Uzunlik", null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, verbose_name="Qurilish boshlangan vaqti")
    end_date = models.DateField(null=True, blank=True, verbose_name="Qurilish tuganlangan vaqti")

    def __str__(self):
        return self.title

    class Meta(BaseMeta):
        db_table = "object"
        verbose_name = "Object"
        verbose_name_plural = "Objects"