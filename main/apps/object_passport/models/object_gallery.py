import os
from django.db import models
from main.apps.common.models import BaseModel, BaseMeta
from django.utils.timezone import now
from main.apps.object_passport.models.object import Object



def upload_object_files(instance, filename):
    ext = os.path.splitext(filename)[1]
    original_name = os.path.splitext(filename)[0]
    timestamp = now().strftime("%Y_%m_%d")
    return f"object_files/{original_name}_{timestamp}{ext}"


class Gallery(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Obyekt nomi")
    file = models.FileField(upload_to=upload_object_files, blank=True, null=True, verbose_name="Rasm yoki Video")
    file_type = models.CharField(max_length=20, blank=True, null=True, verbose_name="Fayl turi")
    size = models.CharField(max_length=50, blank=True, null=True, verbose_name="Hajmi")

    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nomi")

    def __str__(self):
        return f"{self.object}"

    class Meta(BaseMeta):
        db_table = "object_gallery"
        verbose_name = "Object Gallery"
        verbose_name_plural = "Objects Gallery"