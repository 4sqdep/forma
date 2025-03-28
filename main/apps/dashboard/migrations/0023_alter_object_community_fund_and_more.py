from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_object_community_fund_object_foreign_loan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='community_fund',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='UZBEKGIDRO summasi'),
        ),
        migrations.AlterField(
            model_name='object',
            name='construction_work_amount',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='Qurilish ishlar summasi'),
        ),
        migrations.AlterField(
            model_name='object',
            name='equipment_amount',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='Uskunalar summasi'),
        ),
        migrations.AlterField(
            model_name='object',
            name='foreign_loan',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='Xorijiy kredit'),
        ),
        migrations.AlterField(
            model_name='object',
            name='object_file',
            field=models.FileField(null=True, upload_to='object_files/', verbose_name='Obyekt pasporti fayli'),
        ),
        migrations.AlterField(
            model_name='object',
            name='object_power',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Obyekt umumiy quvvat'),
        ),
        migrations.AlterField(
            model_name='object',
            name='other_expense',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='Boshqa xarajatlar'),
        ),
        migrations.AlterField(
            model_name='object',
            name='pressure',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Bosim'),
        ),
        migrations.AlterField(
            model_name='object',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=32, verbose_name='Obyekt umumiy summasi'),
        ),
        migrations.AlterField(
            model_name='object',
            name='water_consumption',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Suv sarfi'),
        ),
    ]
