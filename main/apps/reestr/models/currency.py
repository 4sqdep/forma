from django.db import models
from main.apps.common.models import BaseMeta, BaseModel



class Currency(BaseModel):
    title = models.CharField(max_length=255, verbose_name="O'lchov nomi")
    

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"