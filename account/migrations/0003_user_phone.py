# Generated by Django 4.2.16 on 2024-12-23 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=11, verbose_name='Telfon raqami'),
        ),
    ]