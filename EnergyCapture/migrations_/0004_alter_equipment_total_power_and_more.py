# Generated by Django 4.2.1 on 2023-05-17 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EnergyCapture', '0003_equipment_total_power_powerclamp_total_power_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='total_power',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='powerclamp',
            name='total_power',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='total_power',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=50, null=True),
        ),
    ]
