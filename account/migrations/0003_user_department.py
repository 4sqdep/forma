# Generated by Django 4.2.16 on 2024-11-07 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_permission_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.department', verbose_name="Bo'lim nomi"),
        ),
    ]