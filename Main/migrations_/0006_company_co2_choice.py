# Generated by Django 4.2.1 on 2023-05-25 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_alter_company_total_power'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='co2_choice',
            field=models.DecimalField(decimal_places=5, max_digits=10, null=True),
        ),
    ]
