import os
from django.utils.timezone import now
from django.db import models
from main.apps.common.models import BaseModel, BaseMeta, Measurement



def upload_construction_files(instance, filename):
    ext = os.path.splitext(filename)[1]  
    original_name = os.path.splitext(filename)[0]  
    timestamp = now().strftime("%Y_%m_%d") 
    return f"message_files/{original_name}_{timestamp}{ext}"



class WorkType(BaseModel):
    object = models.ForeignKey(object, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True, blank=True)
    plan = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    fact = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')

    def __str__(self):
        return self.title

    class Meta(BaseMeta):
        db_table = "work_category"
        verbose_name = "Work Category"
        verbose_name_plural = "Work Categories"



class WorkSubCategory(BaseModel):
    work_category = models.ForeignKey(WorkType, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta(BaseMeta):
        db_table = "work_subcategory"
        verbose_name = "Work SubCategory"
        verbose_name_plural = "Work SubCategories"



class WorkProgress(BaseModel):
    work_category = models.ForeignKey(WorkType, on_delete=models.SET_NULL, null=True, blank=True)
    work_subcategory = models.ForeignKey(WorkSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    total_volume = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    date = models.DateField(null=True, blank=True)
    remained_volume = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    completed_volume = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    file = models.FileField(upload_to=upload_construction_files, null=True, blank=True)
    contractor = models.CharField(max_length=255, null=True, blank=True)


    class Meta(BaseMeta):
        db_table = "work_progress"
        verbose_name = "Work Progress"
        verbose_name_plural = "Work Progress"



class MonthlyWorkVolume(BaseModel):
    work_progress = models.ForeignKey(WorkProgress, on_delete=models.SET_NULL, null=True, blank=True)
    plan = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    fact = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    date = models.DateField()

    def __str__(self):
        return self.work_progress.title

    class Meta(BaseMeta):
        db_table = "monthly_work_volume"
        verbose_name = "Monthly Work Volume"
        verbose_name_plural = "Monthly Work Volumes"