from django.db import models
from django.conf import settings
from .utils import upload_file


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='%(app_label)s_%(class)s_created_by'
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='%(app_label)s_%(class)s_deleted_by'
    )

    class Meta:
        abstract = True


class BaseMeta(object):
    ordering = ("-id",)



class Currency(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Pul o'lchov birligi")
    
    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "currency"
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"



class Measurement(BaseModel):
    title = models.CharField(max_length=255, verbose_name="O'lchov nomi")

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "measurement"
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"



class Template(BaseModel):
    file = models.FileField(upload_to="templates/", null=True)

    class Meta(BaseMeta):
        db_table = "template"
        verbose_name = "Template"
        verbose_name_plural = "Templates"