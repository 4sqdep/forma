# Generated by Django 4.2.16 on 2025-04-01 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.apps.object_passport.models.object


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Nomi')),
                ('construction_work_amount', models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='Qurilish ishlar summasi')),
                ('equipment_amount', models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='Uskunalar summasi')),
                ('other_expense', models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='Boshqa xarajatlar')),
                ('total_price', models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='Obyekt umumiy summasi')),
                ('object_power', models.FloatField(blank=True, null=True, verbose_name='Obyetk umumiy quvvati')),
                ('annual_electricity_production', models.FloatField(blank=True, null=True, verbose_name='Yillik elektr ishlab chiqarish')),
                ('pressure', models.FloatField(blank=True, null=True, verbose_name='Bosim')),
                ('water_consumption', models.FloatField(blank=True, null=True, verbose_name='Suv sarfi')),
                ('community_fund', models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='UZBEKGIDRO summasi')),
                ('foreign_loan', models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='Xorijiy kredit')),
                ('object_file', models.FileField(blank=True, null=True, upload_to=main.apps.object_passport.models.object.upload_object_files)),
                ('useful_work_coefficient', models.FloatField(blank=True, max_length=30, null=True, verbose_name='Foydali ish koeffitsiyenti')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Kenglik')),
                ('longtitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Uzunlik')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Qurilish boshlangan vaqti')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Qurilish tuganlangan vaqti')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.currency')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('object_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.objectcategory', verbose_name='Obyekt Categoriya')),
                ('object_subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.objectsubcategory', verbose_name='Obyekt Subcategoriya')),
            ],
            options={
                'verbose_name': 'Object',
                'verbose_name_plural': 'Objects',
                'db_table': 'object',
                'ordering': ('-id',),
            },
        ),
    ]
