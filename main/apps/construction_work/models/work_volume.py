from django.db import models
from main.apps.common.models import BaseModel, BaseMeta, Currency, Measurement
from main.apps.object_passport.models.object import Object






class WorkType(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta(BaseMeta):
        db_table = "work_type"
        verbose_name = "Work Type"
        verbose_name_plural = "Work Types"



class WorkCategory(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    # work_type = models.ForeignKey(WorkType, on_delete=models.SET_NULL, null=True, blank=True)
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    plan_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    fact_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')

    def __str__(self):
        return self.title

    class Meta(BaseMeta):
        db_table = "work_category"
        verbose_name = "Work Category"
        verbose_name_plural = "Work Categories"



class WorkVolume(BaseModel):
    work_category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, null=True, blank=True)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    fact = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')

    class Meta(BaseMeta):
        db_table = "work_volume"
        verbose_name = "Work Volume"
        verbose_name_plural = "Work Volumes"



class MonthlyWorkVolume(BaseModel):
    work_volume = models.ForeignKey(WorkVolume, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    fact = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    date = models.DateField()

    class Meta(BaseMeta):
        db_table = "monthly_work_volume"
        verbose_name = "Monthly Work Volume"
        verbose_name_plural = "Monthly Work Volumes"
        constraints = [
            models.UniqueConstraint(fields=['work_volume', 'date'], name='unique_monthly_work_volume')
        ]

    
    @property
    def work_category(self):
        return self.work_volume.work_category if self.work_volume else None 
    
    @property
    def work_type(self):
        return self.work_volume.work_type if self.work_volume else None
    

    def delete(self, *args, **kwargs):
        if self.work_volume:
            self.work_volume.plan -= self.plan 
            self.work_volume.fact -= self.fact
            self.work_volume.save()
        super().delete(*args, **kwargs)