# Generated by Django 4.2.16 on 2025-04-07 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_communication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeecommunication',
            name='receiver',
        ),
    ]
