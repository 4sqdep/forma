# Generated by Django 4.2.16 on 2025-03-04 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0021_hydrostation_financial_reource_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industrialasset',
            name='delivered_in_percent',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='industrialasset',
            name='remaining_in_percent',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
