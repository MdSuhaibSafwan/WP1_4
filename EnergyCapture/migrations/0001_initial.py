# Generated by Django 4.2.1 on 2023-11-29 16:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('total_power', models.FloatField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PossibleDeviceID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceID', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PowerClamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('deviceID', models.CharField(max_length=50, null=True)),
                ('total_power', models.FloatField(default=0, null=True)),
                ('equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EnergyCapture.equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('total_power', models.FloatField(default=0, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.company')),
            ],
        ),
        migrations.CreateModel(
            name='StationTime',
            fields=[
                ('power', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EnergyCapture.station')),
            ],
        ),
        migrations.CreateModel(
            name='PowerClampTime',
            fields=[
                ('power', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('powerClamp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EnergyCapture.powerclamp')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentTime',
            fields=[
                ('power', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EnergyCapture.equipment')),
            ],
        ),
        migrations.AddField(
            model_name='equipment',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EnergyCapture.station'),
        ),
        migrations.CreateModel(
            name='CO2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Scope 2', 'Scope 2'), ('Scope 3 (Generation)', 'Scope 3 (Generation)'), ('Scope 3 (Transmission and Distribution', 'Scope 3 (Transmission and Distribution'), ('Total', 'Total')], max_length=50, null=True)),
                ('value', models.DecimalField(decimal_places=5, max_digits=10, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.company')),
            ],
        ),
    ]
