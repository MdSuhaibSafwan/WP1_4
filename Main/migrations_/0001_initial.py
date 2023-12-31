# Generated by Django 4.1.6 on 2023-03-31 10:12

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(choices=[('airborne', 'Airborne'), ('test_comp', 'Test Company')], max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('ply_cutter', 'Ply Cutter'), ('pick_place_sort', 'Pick and Place (sort)'), ('pick_place_blanks', 'Pick and Place (blanks)'), ('preform_cell', 'Preforming Cell')], max_length=50)),
                ('status', models.IntegerField(default=0)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.company')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('test', 'Test One'), ('test2', 'Test Two')], max_length=30, null=True)),
                ('optimumTime', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('optimumTemp', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('optimumPressure', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('priceKG', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('priceM2', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialDensity', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('manualName', models.CharField(max_length=50, null=True)),
                ('viable', models.BooleanField(default=False)),
                ('operator', models.CharField(max_length=50, null=True)),
                ('labourInput', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('cycleTime', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('processTime', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('jobStart', models.DateTimeField(default=None, null=True)),
                ('jobEnd', models.DateTimeField(default=None, null=True)),
                ('processStart', models.DateTimeField(default=None, null=True)),
                ('processEnd', models.DateTimeField(default=None, null=True)),
                ('interfaceTime', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('badPart', models.BooleanField(default=False)),
                ('scrapRate', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('minBatchSize', models.DecimalField(decimal_places=0, default=50, max_digits=50)),
                ('maxBatchSize', models.DecimalField(decimal_places=0, default=350, max_digits=50)),
                ('power', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('status', models.IntegerField(default=0)),
                ('qualityCheck', models.BooleanField(default=False, null=True)),
                ('CO2', models.DecimalField(decimal_places=5, default=0, max_digits=50)),
                ('cycleCostRatio', models.DecimalField(decimal_places=3, default=0, max_digits=50)),
                ('wastedTime', models.DurationField(null=True)),
                ('editProcess', models.BooleanField(default=False)),
                ('materialWastage', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialScrap', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialPart', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialWastageCost', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('materialScrapCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialPartCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialSumCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('technicianLabour', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('supervisorLabour', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('technicianLabourCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('supervisorLabourCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('labourSumCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('powerCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('totalCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('processCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('partCreated', models.BooleanField(default=False)),
                ('position', models.IntegerField(default=None, null=True)),
                ('startPoint', models.BooleanField(default=False)),
                ('endPoint', models.BooleanField(default=False)),
                ('initialised', models.BooleanField(default=False)),
                ('machine', models.ManyToManyField(to='Main.machine')),
            ],
            options={
                'permissions': [('edit_process', 'create or delete process')],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50)),
                ('techRate', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('superRate', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('powerRate', models.DecimalField(decimal_places=5, default=0, max_digits=10)),
                ('manual', models.BooleanField(default=False)),
                ('setUpCost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('CO2PerPower', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('baselinePartNo', models.IntegerField(default=0)),
                ('badPartCounter', models.IntegerField(default=0)),
                ('goodPartCounter', models.IntegerField(default=0)),
                ('startDate', models.DateField(null=True)),
                ('OEEstartDate', models.DateField(null=True)),
                ('endDate', models.DateField(null=True)),
                ('OEEendDate', models.DateField(null=True)),
                ('priceKG', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('priceM2', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialDensity', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('weightTolerance', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('lengthTolerance', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('widthTolerance', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('depthTolerance', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('preformWrinklingTolerance', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('thicknessTolerance', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('nominalVolumeWrinkling', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('nominalPartWeight', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('nominalPartArea', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('nominalPartLength', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('nominalPartWidth', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('nominalPartThickness', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('totalShiftTime', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('plannedDownTime', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('allDownTime', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('allStopTime', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('theoreticalCycleTime', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('defectAmount', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('material', models.CharField(max_length=50, null=True)),
                ('learningRate', models.FloatField(default=0.88)),
                ('machineConfirmed', models.BooleanField(default=False)),
                ('processConfirmed', models.BooleanField(default=False)),
                ('editStatus', models.IntegerField(default=0)),
                ('noSuggested', models.BooleanField(default=False)),
                ('processWindow', models.BooleanField(default=False)),
                ('technicianLabour', models.DurationField(null=True)),
                ('supervisorLabour', models.DurationField(null=True)),
                ('technicianLabourCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('supervisorLabourCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('assumedCost', models.FloatField(default=1, null=True)),
                ('materialCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('powerCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('labourCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('totalCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.company')),
            ],
            options={
                'permissions': [('edit_project', 'create or delete project')],
            },
        ),
        migrations.CreateModel(
            name='RepeatBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iteration', models.IntegerField(null=True)),
                ('number_of_iterations', models.IntegerField(null=True)),
                ('finished', models.BooleanField(default=False)),
                ('process', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.process')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('proName', models.CharField(max_length=50, null=True)),
                ('status', models.IntegerField(default=0)),
                ('averageEnergyTime', models.IntegerField(default=5)),
                ('averageTime', models.IntegerField(default=5)),
                ('temperatureReached', models.BooleanField(default=False)),
                ('tempReachedTime', models.CharField(max_length=50, null=True)),
                ('pressureReached', models.BooleanField(default=False)),
                ('pressureReachedTime', models.CharField(max_length=50, null=True)),
                ('maxTemp', models.IntegerField(default=10, null=True)),
                ('minTemp', models.IntegerField(default=0, null=True)),
                ('maxPressure', models.IntegerField(default=0, null=True)),
                ('minPressure', models.IntegerField(default=10, null=True)),
                ('maxVOC', models.IntegerField(default=10, null=True)),
                ('minVOC', models.IntegerField(default=0, null=True)),
                ('maxHumid', models.IntegerField(default=10, null=True)),
                ('minHumid', models.IntegerField(default=0, null=True)),
                ('maxDust', models.IntegerField(default=10, null=True)),
                ('minDust', models.IntegerField(default=0, null=True)),
                ('maxNoise', models.IntegerField(default=0, null=True)),
                ('minNoise', models.IntegerField(default=0, null=True)),
                ('maxTorque', models.IntegerField(default=0, null=True)),
                ('minTorque', models.IntegerField(default=0, null=True)),
                ('minAccel', models.IntegerField(default=0, null=True)),
                ('maxAccel', models.IntegerField(default=0, null=True)),
                ('tolerance', models.IntegerField(default=10, null=True)),
                ('distance', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('posCheck', models.BooleanField(default=False, null=True)),
                ('actualWeight', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('thickness', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('partPresent', models.BooleanField(default=False, null=True)),
                ('partDimX', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('partDimY', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('encoderPos', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('timerCheck', models.BooleanField(default=False, null=True)),
                ('serviceDate', models.DateTimeField(null=True)),
                ('contactNum', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True)),
                ('dateInstalled', models.DateTimeField(null=True)),
                ('modelID', models.CharField(max_length=50, null=True)),
                ('warrentExp', models.DateTimeField(null=True)),
                ('machine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.machine')),
                ('process', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.process')),
            ],
        ),
        migrations.CreateModel(
            name='SubProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('manualName', models.CharField(max_length=50, null=True)),
                ('repeat', models.BooleanField(default=False)),
                ('operator', models.CharField(max_length=50, null=True)),
                ('labourInput', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('processTime', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('jobStart', models.DateTimeField(default=None, null=True)),
                ('jobEnd', models.DateTimeField(default=None, null=True)),
                ('date', models.DateTimeField(default=None, null=True)),
                ('position', models.IntegerField(null=True)),
                ('startPoint', models.BooleanField(default=False)),
                ('endPoint', models.BooleanField(default=False)),
                ('interfaceTime', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('badPart', models.BooleanField(default=False)),
                ('scrapRate', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('batchSize', models.DecimalField(decimal_places=0, default=5, max_digits=50)),
                ('power', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('status', models.IntegerField(default=0)),
                ('processCheck', models.BooleanField(default=False, null=True)),
                ('qualityCheck', models.BooleanField(default=False, null=True)),
                ('CO2', models.DecimalField(decimal_places=5, default=0, max_digits=50)),
                ('cycleCostRatio', models.DecimalField(decimal_places=3, default=0, max_digits=50)),
                ('preSubCost', models.DecimalField(decimal_places=3, default=0, max_digits=50)),
                ('wastedTime', models.DurationField(default=datetime.timedelta(0))),
                ('criterion', models.CharField(max_length=800, null=True)),
                ('image', models.ImageField(null=True, upload_to='images')),
                ('file', models.FileField(null=True, upload_to='files')),
                ('weighPoint', models.BooleanField(default=False)),
                ('finalWeighPoint', models.BooleanField(default=False)),
                ('postTrimWeight', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('preTrimWeight', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('actualThickness', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('actualWidth', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('actualLength', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('centrePosT', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('centrePosMT', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('tolerance', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('temperature', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('time', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('pressure', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('verticalEffector', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('tolerancex2', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialWastage', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialScrap', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialPart', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialWastageCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialScrapCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialPartCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialSumCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('technicianLabour', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('supervisorLabour', models.DurationField(default=datetime.timedelta(0), null=True)),
                ('technicianLabourCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('supervisorLabourCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('labourSumCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('powerCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('totalCost', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('partInstance', models.IntegerField(default=None, null=True)),
                ('blankInstance', models.IntegerField(default=None, null=True)),
                ('plyInstance', models.IntegerField(default=None, null=True)),
                ('partTask', models.BooleanField(default=False)),
                ('blankTask', models.BooleanField(default=False)),
                ('plyTask', models.BooleanField(default=False)),
                ('consolidationCheck', models.BooleanField(default=False)),
                ('plySurfaceArea', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('plyPerimeter', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('totalSumOfPerimeter', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('totalSurfaceArea', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('totalOffcutArea', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('powerUsage', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialRateArea', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialRateWeight', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('materialDensity', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('blankArea', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('blanksPickAndPlace', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_blanksPickAndPlace', to='Main.machine')),
                ('plyCutter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_plyCutter', to='Main.machine')),
                ('preformCell', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_preformCell', to='Main.machine')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.process')),
                ('sortPickAndPlace', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_sortPickAndPlace', to='Main.machine')),
            ],
            options={
                'permissions': [('edit_sub_process', 'create or delete sub process')],
            },
        ),
        migrations.CreateModel(
            name='TiaBlocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('machine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.machine')),
                ('project', models.ManyToManyField(to='Main.project')),
                ('subProcess', models.ManyToManyField(to='Main.subprocess')),
            ],
        ),
        migrations.CreateModel(
            name='SubProcessWeights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=4, default=0, max_digits=10, null=True)),
                ('subProPart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.subprocess')),
            ],
        ),
        migrations.CreateModel(
            name='SensorTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('distance', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('pressure', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('noise', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('energy', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('VOC', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('dust', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('humidity', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('torque', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('acceleration', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('time', models.DateTimeField(default=None)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.sensor')),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='sub_process',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.subprocess'),
        ),
        migrations.CreateModel(
            name='RepeatBlockSubProcesses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.BooleanField(default=False)),
                ('end', models.BooleanField(default=False)),
                ('repeat_block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.repeatblock')),
                ('sub_process', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.subprocess')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('username', models.CharField(default='anonymous', max_length=50, primary_key=True, serialize=False)),
                ('sequence_choice', models.IntegerField(default=None, null=True)),
                ('user', models.OneToOneField(default='default', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.company')),
            ],
        ),
        migrations.AddField(
            model_name='process',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.project'),
        ),
        migrations.CreateModel(
            name='PossibleSubProcesses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.process')),
            ],
        ),
        migrations.CreateModel(
            name='PossibleSensors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('modelID', models.CharField(max_length=50, null=True)),
                ('machine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.machine')),
                ('process', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.process')),
            ],
        ),
        migrations.CreateModel(
            name='PossibleProjectTia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('machine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.machine')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.project')),
            ],
        ),
        migrations.CreateModel(
            name='PossibleProjectSensors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('modelID', models.CharField(max_length=50, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.machine')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.project')),
            ],
        ),
        migrations.CreateModel(
            name='PossibleProjectProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('machine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.machine')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.project')),
            ],
        ),
        migrations.CreateModel(
            name='PossibleProjectMachines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.machine')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.project')),
            ],
        ),
        migrations.CreateModel(
            name='PlyInstance',
            fields=[
                ('instance_id', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('process', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.process')),
            ],
        ),
        migrations.CreateModel(
            name='PartInstance',
            fields=[
                ('instance_id', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('process', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.process')),
            ],
        ),
        migrations.AddField(
            model_name='machine',
            name='projects',
            field=models.ManyToManyField(to='Main.project'),
        ),
        migrations.CreateModel(
            name='InstanceQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_id', models.IntegerField(null=True)),
                ('process', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.process')),
            ],
        ),
        migrations.CreateModel(
            name='BlankInstance',
            fields=[
                ('instance_id', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('process', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.process')),
            ],
        ),
    ]
