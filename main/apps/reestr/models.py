from django.db import models


class Year(models.Model):
    year = models.IntegerField(verbose_name="Yil")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")
    amount = models.DecimalField(max_digits=24, decimal_places=2, null=True, blank=True, verbose_name="Yillik Miqdori")

    def __str__(self):
        return str(self.year)
    class Meta:
        verbose_name = "Yil"
        verbose_name_plural = "Yillar"


class Month(models.Model):
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, related_name="months", blank=True, null=True,
                             verbose_name="Yil")
    month = models.CharField(max_length=20, verbose_name="Oy")
    work = models.ForeignKey('DynamicWork', on_delete=models.SET_NULL, related_name="monthly_data",
                             verbose_name="Oylik ma'lumotlar", blank=True, null=True)
    spent_amount = models.DecimalField(max_digits=24, decimal_places=2, default=0, verbose_name="Sarflangan summa")
    amount = models.DecimalField(max_digits=24, decimal_places=2, null=True, blank=True, verbose_name="Miqdori")

    def __str__(self):
        return f"{self.month} ({self.year.year})"

    class Meta:
        verbose_name = "Oy"
        verbose_name_plural = "Oylar"


class DynamicWork(models.Model):
    no = models.IntegerField(verbose_name="Ish raqami")
    work_name = models.CharField(max_length=255, verbose_name="Ish nomi", db_index=True)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Umumiy xarajat summa")
    total_fact = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Jami fakt summa")
    difference = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Farq summa")
    year_data = models.ManyToManyField(Year, related_name="works", verbose_name="Yearly Data")

    def __str__(self):
        return f"{self.no}: {self.work_name}"

    class Meta:
        verbose_name = "Farq"
        verbose_name_plural = "Farqil"