from django.db import models
from account.models import User


class DashboardButton(models.Model):
    """Dashboard button uchun asosiy button"""
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dashboard Button"
        verbose_name_plural = "Dashboard Knopkalar"


class DashboardCategoryButton(models.Model):
    """Dashboard button uchun Kategoriya button"""
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dashboard Category Button"
        verbose_name_plural = "Dashboard Kategoriya Knopkalar"


class DashboardSubCategoryButton(models.Model):
    """Dashboard button uchun SubKategoriya button"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Foydalanuvchi", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dashboard Sub Category Button"
        verbose_name_plural = "Dashboard Pastki Kategoriya Knopkalar"