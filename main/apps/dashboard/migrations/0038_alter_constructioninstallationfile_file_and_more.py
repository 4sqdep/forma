# Generated by Django 4.2.16 on 2025-03-19 06:31

from django.db import migrations, models
import main.apps.dashboard.models.construction_installation_work
import main.apps.dashboard.models.dashboard
import main.apps.dashboard.models.document


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0037_alter_documentfiles_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constructioninstallationfile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=main.apps.dashboard.models.construction_installation_work.upload_construction_installation_files),
        ),
        migrations.AlterField(
            model_name='constructioninstallationstatistics',
            name='contract_file',
            field=models.FileField(blank=True, null=True, upload_to=main.apps.dashboard.models.construction_installation_work.upload_contract_files),
        ),
        migrations.AlterField(
            model_name='documentfiles',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to=main.apps.dashboard.models.document.upload_document_files),
        ),
        migrations.AlterField(
            model_name='object',
            name='object_file',
            field=models.FileField(blank=True, null=True, upload_to=main.apps.dashboard.models.dashboard.upload_object_files),
        ),
    ]
