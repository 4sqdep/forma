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
    object_category = models.ForeignKey(ObjectCategory, on_delete=models.SET_NULL, verbose_name="Kinopka", null=True, blank=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")

    def __str__(self):
        return self.name

    class Meta(BaseMeta):
        db_table = "object_subcategory"
        verbose_name = "Object SubCategory"
        verbose_name_plural = "Object SubCategories"