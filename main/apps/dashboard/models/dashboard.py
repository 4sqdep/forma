from django.db import models
from main.apps.common.models import BaseModel, BaseMeta, Currency
from django.utils.text import slugify




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
    object_category = models.ForeignKey(ObjectCategory, on_delete=models.SET_NULL,
                                         verbose_name="Kinopka", null=True, blank=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")

    def __str__(self):
        return self.name

    class Meta(BaseMeta):
        db_table = "object_subcategory"
        verbose_name = "Object SubCategory"
        verbose_name_plural = "Object SubCategories"



class Object(BaseModel):
    object_category = models.ForeignKey(ObjectCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Obyekt Categoriya")
    object_subcategory = models.ForeignKey(ObjectSubCategory, on_delete=models.SET_NULL, verbose_name="Obyekt Subcategoriya", blank=True, null=True)
    project_documentation = models.ForeignKey('dashboard.ProjectDocumentation', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Obyekt bo'limi")
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")
    construction_work_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    equipment_amount = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    other_expense = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    total_price = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    object_power = models.PositiveIntegerField(null=True, blank=True)
    pressure = models.PositiveIntegerField(null=True, blank=True)
    water_consumption = models.PositiveIntegerField(null=True, blank=True)
    object_file = models.FileField(upload_to="object_files/", null=True)
    start_date = models.DateField(null=True, blank=True, verbose_name="Qurilish boshlangan vaqti")
    end_date = models.DateField(null=True, blank=True, verbose_name="Qurilish tuganlangan vaqti")

    def __str__(self):
        return self.title

    class Meta(BaseMeta):
        db_table = "object"
        verbose_name = "Object"
        verbose_name_plural = "Objects"