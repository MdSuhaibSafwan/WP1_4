# Generated by Django 4.2.1 on 2023-05-17 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EnergyCapture', '0002_possibledeviceid_equipment_station_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='total_power',
            field=models.DecimalField(decimal_places=3, max_digits=50, null=True),
        ),
        migrations.AddField(
            model_name='powerclamp',
            name='total_power',
            field=models.DecimalField(decimal_places=3, max_digits=50, null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='total_power',
            field=models.DecimalField(decimal_places=3, max_digits=50, null=True),
        ),
    ]