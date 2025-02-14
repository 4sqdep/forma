from django.db import models
from main.apps.common.models import BaseModel, BaseMeta
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
        verbose_name = "ObjectCategory"
        verbose_name_plural = "Asosiy Knopkalar"



class ObjectSubCategory(BaseModel):
    object_category = models.ForeignKey(ObjectCategory, on_delete=models.SET_NULL,
                                         verbose_name="Kinopka", null=True, blank=True)
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")

    def __str__(self):
        return self.name

    class Meta(BaseMeta):
        db_table = "object_subcategory"
        verbose_name = "Object SubCategory"
        verbose_name_plural = "Kategoriya Knopkalar"



class Object(BaseModel):
    object_category = models.ForeignKey(ObjectCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Asosiy knopkalar")
    object_subcategory = models.ForeignKey(ObjectSubCategory, on_delete=models.SET_NULL, verbose_name="Categoriya knopka", blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")
    project_documentation = models.ForeignKey('dashboard.ProjectDocumentation', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Obyekt bo'limi")
    smr_price = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    equipment_price = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    investment_price = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    uge_price = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    total_price = models.DecimalField(max_digits=32, decimal_places=2, default='0.00')
    total_power = models.CharField(max_length=200, null=True, blank=True, verbose_name="Umumiy quvvat")
    start_date = models.DateField(null=True, blank=True, verbose_name="Qurilish boshlangan vaqti")
    end_date = models.DateField(null=True, blank=True, verbose_name="Qurilish tuganlangan vaqti")

    def __str__(self):
        return self.title

    class Meta(BaseMeta):
        db_table = "object"
        verbose_name = "Object"
        verbose_name_plural = "Obyekt nomlari"