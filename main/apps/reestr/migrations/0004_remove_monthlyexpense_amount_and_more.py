import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reestr', '0003_alter_constructiontask_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthlyexpense',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='monthlyexpense',
            name='difference_amount',
        ),
        migrations.RemoveField(
            model_name='monthlyexpense',
            name='month',
        ),
        migrations.RemoveField(
            model_name='monthlyexpense',
            name='total_difference_amount',
        ),
        migrations.RemoveField(
            model_name='monthlyexpense',
            name='total_fact',
        ),
        migrations.RemoveField(
            model_name='monthlyexpense',
            name='total_fact_amount',
        ),
        migrations.RemoveField(
            model_name='monthlyexpense',
            name='total_year',
        ),
        migrations.RemoveField(
            model_name='monthlyexpense',
            name='year',
        ),
        migrations.AddField(
            model_name='monthlyexpense',
            name='date',
            field=models.DateField(default=datetime.datetime(2025, 1, 23, 5, 57, 42, 236005, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
