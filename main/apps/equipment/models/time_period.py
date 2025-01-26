from django.db import models
from main.apps.account.models.user import User
from main.apps.common.models import BaseMeta, BaseModel




class Year(BaseModel):
    title = models.CharField(max_length=255)


    def __str__(self):
        return self.title
    
    class Meta(BaseMeta):
        verbose_name = "Yil"
        verbose_name_plural = "Yillar"



class Month(BaseModel):
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, related_name="months", blank=True, null=True, verbose_name="Yil")
    title = models.CharField(max_length=255, verbose_name="Oy")

    def __str__(self):
        return f"{self.title} ({self.year.title})"

    class Meta(BaseMeta):
        verbose_name = "Oy"
        verbose_name_plural = "Oylar"
