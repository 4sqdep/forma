# Generated by Django 4.2.16 on 2025-03-26 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_objectspassword_category_btn_and_more'),
        ('dashboard', '0038_alter_constructioninstallationfile_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='project_documentation',
        ),
        migrations.DeleteModel(
            name='ProjectDocumentation',
        ),
    ]
