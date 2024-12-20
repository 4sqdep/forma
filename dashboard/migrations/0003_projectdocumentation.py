# Generated by Django 4.2.16 on 2024-12-07 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_dashboardcategorybutton_dashboard_button_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectDocumentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=1000, null=True, verbose_name='Nomi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Kiritilgan vaqti')),
                ('subcategories_btn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.dashboardsubcategorybutton', verbose_name='Loyiha nomi')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Loyiha hujjati',
                'verbose_name_plural': 'Loyiha hujjatlari',
            },
        ),
    ]
