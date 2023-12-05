from django.db import models
from Main.models import Company
import datetime
import django.utils
from zoneinfo import ZoneInfo
# Create your models here.
django.utils.timezone.activate(ZoneInfo("Europe/London"))

class Station(models.Model):
	name = models.CharField(max_length=50, null = True)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, null = True)
	total_power = models.FloatField(default=0, null = True)


	def __str__(self):
		return self.name


class StationTime(models.Model):
	station = models.ForeignKey(Station, on_delete=models.CASCADE, null = True)
	power = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	time=models.DateTimeField(default= django.utils.timezone.now)
	id = models.BigAutoField(primary_key=True)



class Equipment(models.Model):
	name = models.CharField(max_length=50, null = True)
	station = models.ForeignKey(Station, on_delete=models.CASCADE, null = True)
	total_power = models.FloatField(default=0, null = True)

	def __str__(self):
		return self.name

class EquipmentTime(models.Model):
	equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null = True)
	power = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	time=models.DateTimeField(default= django.utils.timezone.now)
	id = models.BigAutoField(primary_key=True)

class PowerClamp(models.Model):
	name = models.CharField(max_length=50, null = True)
	deviceID = models.CharField(max_length=50, null = True)
	equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
	total_power = models.FloatField(default=0, null = True)

	def __str__(self):
		return self.name

class PowerClampTime(models.Model):
	powerClamp = models.ForeignKey(PowerClamp,on_delete=models.CASCADE, null = True)
	power = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	time = models.DateTimeField(default= django.utils.timezone.now)
	id = models.BigAutoField(primary_key=True)

class PossibleDeviceID(models.Model):
	deviceID = models.CharField(max_length=50, null = True)

	def __str__(self):
		return self.deviceID

class CO2(models.Model):

	CO2_CHOICES = [
		('Scope 2', 'Scope 2'),
		('Scope 3 (Generation)', 'Scope 3 (Generation)'),
		('Scope 3 (Transmission and Distribution', 'Scope 3 (Transmission and Distribution'),
		('Total', 'Total'),
		]

	name = models.CharField(max_length=50,choices=CO2_CHOICES, null = True)
	value = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, null = True)
