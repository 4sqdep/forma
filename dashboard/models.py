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
    dashboard_button = models.ForeignKey(DashboardButton, on_delete=models.SET_NULL, verbose_name="Kinopka", null=True, blank=True)
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
    dashboard_category_btn = models.ForeignKey(DashboardCategoryButton, on_delete=models.SET_NULL, verbose_name="Categoriya knopka", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dashboard Sub Category Button"
        verbose_name_plural = "Dashboard Pastki Kategoriya Knopkalar"


class ProjectDocumentation(models.Model):
    """Loyiha hujjatlar Qurilish montaj ishlari Uskunalar uchun model"""
    subcategories_btn = models.ForeignKey(DashboardSubCategoryButton, on_delete=models.SET_NULL,
                                          verbose_name="Loyiha nomi", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Foydalanuvchi", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")
    def __str__(self):
        return f"{self.subcategories_btn} -- {self.name}"

    class Meta:
        verbose_name = "Loyiha hujjati"
        verbose_name_plural = "Loyiha hujjatlari"


class NextStageDocuments(models.Model):
    """Keyingi bosqich uchun qabul qilinadigan hujjatlar uchun model"""
    project_document = models.ForeignKey(ProjectDocumentation, on_delete=models.SET_NULL, verbose_name="Loyiha hujjatlar"
                                         , blank=True, null=True)
    subcategories_btn = models.ForeignKey(DashboardSubCategoryButton, on_delete=models.SET_NULL,
                                          verbose_name="Loyiha nomi", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Foydalanuvchi", blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return f"{self.project_document} -- {self.name}"

    class Meta:
        verbose_name = "Keyingi hujjat"
        verbose_name_plural = "Keyingi hujjatlari"


class Files(models.Model):
    document = models.ForeignKey(NextStageDocuments, on_delete=models.SET_NULL, verbose_name="Loyiha hujjatlar",
                                 blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Foydalanuvchi", blank=True, null=True)
    files = models.FileField(verbose_name="files/%Y/%m/%d", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return f"{self.document}"

    class Meta:
        verbose_name = "Fayl"
        verbose_name_plural = "Fayllar"