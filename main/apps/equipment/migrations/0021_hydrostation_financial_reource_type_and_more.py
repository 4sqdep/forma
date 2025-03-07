# Generated by Django 4.2.16 on 2025-03-01 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0020_equipmentcategory_equipmentsubcategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hydrostation',
            name='financial_reource_type',
            field=models.CharField(choices=[('funds', 'Funds'), ('ges', 'Ges')], default='funds', max_length=255),
        ),
        migrations.AlterField(
            model_name='hydrostation',
            name='calculation_type',
            field=models.CharField(choices=[('amount', 'Fixed Amount'), ('percent', 'Percentage')], default='percent', max_length=255),
        ),
    ]
