# Generated by Django 4.2.16 on 2025-01-31 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0004_industrialequipment_industrialasset'),
    ]

    operations = [
        migrations.RenameField(
            model_name='industrialasset',
            old_name='commodity_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='industrialasset',
            old_name='country_of_origin',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='industrialasset',
            old_name='price_per_unit',
            new_name='price',
        ),
    ]
