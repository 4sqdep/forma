# Generated by Django 4.2.16 on 2025-03-08 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_rename_section_constructioninstallationproject_sub_section_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='constructioninstallationproject',
            name='sub_section',
        ),
        migrations.AddField(
            model_name='constructioninstallationproject',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.constructioninstallationsection'),
        ),
    ]
