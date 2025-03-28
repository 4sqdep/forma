# Generated by Django 4.2.16 on 2025-02-25 14:30

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0016_alter_financialresource_additional_prepayment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hydrostation',
            name='additional_prepayment',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=32),
        ),
        migrations.AddField(
            model_name='hydrostation',
            name='financial_resource_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hydrostation',
            name='payment_on_completion',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=32),
        ),
        migrations.AddField(
            model_name='hydrostation',
            name='percent',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=32),
        ),
        migrations.AddField(
            model_name='hydrostation',
            name='prepayment_from_foreign_credit_account',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=32),
        ),
        migrations.AddField(
            model_name='hydrostation',
            name='prepayment_from_own_fund',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=32),
        ),
    ]
