from django.db import models

class Nocapitelni(models.Model):
    file = models.FileField(upload_to='nocapitelni', null=True, blank=True, verbose_name='Fayl')

    def __str__(self):
        return str(self.file)
    class Meta:
        verbose_name = 'Nocapitelni'
        verbose_name_plural = 'Nocapitelni'