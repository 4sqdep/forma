# Generated by Django 4.2.16 on 2025-02-13 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0011_rename_dashboard_subbtn_hydrostation_object_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hydrostation',
            name='contract_file',
            field=models.FileField(blank=True, null=True, upload_to='contract_files/.2025-02-13.13-01-18'),
        ),
    ]
