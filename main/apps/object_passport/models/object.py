import os
from django.db import models
from main.apps.common.models import BaseModel, BaseMeta, Currency
from django.utils.timezone import now
from main.apps.dashboard.models.dashboard import ObjectCategory, ObjectSubCategory



def upload_object_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"object_files/{original_name}_{timestamp}{ext}"


class StatusType(models.TextChoices):
    NEW = "new", "Istiqbolli loyihalar"
    IN_PROGRESS = "in_progress", "Amalga oshirilayotgan loyihalar"
    COMPLETED = "completed", "Qurilishi yakunlangan loyihalar"



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
    latitude = models.DecimalField(max_digits=30, decimal_places=20, null=True, blank=True, verbose_name="Kenglik")
    longitude = models.DecimalField(max_digits=30, decimal_places=20, null=True, blank=True, verbose_name="Uzunlik")
    start_date = models.DateField(null=True, blank=True, verbose_name="Qurilish boshlangan vaqti")
    end_date = models.DateField(null=True, blank=True, verbose_name="Qurilish tuganlangan vaqti")
    status_type = models.CharField(max_length=255, blank=True, null=True, choices=StatusType.choices, default=StatusType.NEW)

    def __str__(self):
        return self.title

    class Meta(BaseMeta):
        db_table = "object"
        verbose_name = "Object"
        verbose_name_plural = "Objects"