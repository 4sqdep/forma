from django.db import models
from django.core.files.storage import FileSystemStorage
from account.models import User


class OriginalNameFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)  # Fayl mavjud bo'lsa, o'chirish
        return name

original_storage = OriginalNameFileSystemStorage()


# Qurulish obyekt nomlari uchun model
class ObjectName(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Obyekt nomi", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Obyekt nomi"
        verbose_name_plural = "Obyekt nomlari"


#     Birlamchi hujjatlar uchun model
class PrimaryDocuments(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Foydalanuvchi")
    object_name = models.ForeignKey(ObjectName, verbose_name="Obyekt nomi", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Obyekt nomi")
    file_code = models.CharField(max_length=30, verbose_name="Hujjat kodi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return f"{self.object_name} {self.name}"

    class Meta:
        verbose_name = "Birlamchi hujjat"
        verbose_name_plural = "Birlamchi hujjatlar"


# Birlamchi hujjatlar uchun fayllar modeli
class PrimaryFiles(models.Model):
    primary_document = models.ForeignKey(PrimaryDocuments, verbose_name="Birlamchi hujjatlar",
                                         on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='primaryfiles', verbose_name="Fayllar", storage=original_storage)

    def __str__(self):
        return f"{self.primary_document}"
    class Meta:
        verbose_name = "Birlamchi Fayl"
        verbose_name_plural = "Birlamchi Fayllar"













class Post(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title
