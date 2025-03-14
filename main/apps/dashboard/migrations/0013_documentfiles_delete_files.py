# Generated by Django 4.2.16 on 2025-02-21 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0012_remove_nextstagedocuments_project_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=1000, null=True, verbose_name='Nomi')),
                ('full_name', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Nomi')),
                ('calendar', models.CharField(blank=True, max_length=30, null=True, verbose_name='Hujjat sanasi')),
                ('file_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Hujjat Kodi')),
                ('files', models.FileField(blank=True, null=True, upload_to='', verbose_name='files/%Y/%m/%d')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.nextstagedocuments', verbose_name='Loyiha hujjatlar')),
            ],
            options={
                'verbose_name': 'Fayl',
                'verbose_name_plural': 'Fayllar',
                'db_table': 'document_files',
                'ordering': ('-id',),
            },
        ),
        migrations.DeleteModel(
            name='Files',
        ),
    ]
