# Generated by Django 4.2.16 on 2024-12-03 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile/%Y/%m/%d', verbose_name='Profile Image'),
        ),
    ]
