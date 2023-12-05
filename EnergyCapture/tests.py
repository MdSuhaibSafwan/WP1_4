from django.test import TestCase, Client
from django.db.models import ForeignKey
from datetime import datetime,date,time,timedelta, timezone
from django.urls import reverse, resolve
import json
from django.contrib.auth.models import User, Group
from django.test.utils import setup_test_environment 
from http import HTTPStatus
from .models import *
from .forms import * 
from.views import *

# Create your tests here.

class UrlTests(TestCase):
	def test_add_power_clamps_url(self):
		url = reverse('addPowerClamps', kwargs={'id':1})
		self.assertEqual(resolve(url).func, addPowerClamps)

	def test_add_station_url(self):
		url = reverse('addStation')
		self.assertEqual(resolve(url).func, addStation)

	def test_add_equipment_url(self):
		url = reverse('addEquipment', kwargs={'id':1})
		self.assertEqual(resolve(url).func, addEquipment)

	def test_energy_capture_dashboard_url(self):
		url = reverse('energyCaptureDashboard')
		self.assertEqual(resolve(url).func, energyCaptureDashboard)

	def test_overview_hierarchy_url(self):
		url = reverse('overviewHierarchy')
		self.assertEqual(resolve(url).func, overviewHierarchy)

	def test_grab_pie_kwh_station_url(self):
		url = reverse('grab_pie_kWh_station')
		self.assertEqual(resolve(url).func, grab_pie_kWh_station)

	def test_grab_energy_power_clamps_url(self):
		url = reverse('grabEnergy_PowerClamp', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grabEnergy_PowerClamp)

	def test_grab_energy_equipment_url(self):
		url = reverse('grabEnergy_Equipment', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grabEnergy_Equipment)

	def test_grab_energy_station_url(self):
		url = reverse('grabEnergy_Station')
		self.assertEqual(resolve(url).func, grabEnergy_Station)

	def test_grab_co2_station_url(self):
		url = reverse('grabCO2_Station')
		self.assertEqual(resolve(url).func, grabCO2_Station)

	def test_grab_pie_co2_station(self):
		url = reverse('grab_pie_CO2_station')
		self.assertEqual(resolve(url).func, grab_pie_CO2_station)

	def test_grab_line_kwh_all_url(self):
		url = reverse('grab_line_kWh_all')
		self.assertEqual(resolve(url).func, grab_line_kWh_all)

	def test_grab_line_co2_all_url(self):
		url = reverse('grab_line_CO2_all')
		self.assertEqual(resolve(url).func, grab_line_CO2_all)

	def test_populate_bar_chart_url(self):
		url = reverse('populate_bar_chart')
		self.assertEqual(resolve(url).func, populate_bar_chart)

	def test_station_dashboard_url(self):
		url = reverse('viewStationDashboard', kwargs={'id':1})
		self.assertEqual(resolve(url).func, viewStationDashboard)

	def test_grab_energy_station_url(self):
		url = reverse('viewEquipmentDashboard', kwargs={'id':1})
		self.assertEqual(resolve(url).func, viewEquipmentDashboard)

	def test_grab_individual_station_kwh_url(self):
		url = reverse('grab_indiviudal_station_kWh', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grab_indiviudal_station_kWh)

	def test_grab_individual_station_co2_url(self):
		url = reverse('grab_individual_station_CO2', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grab_individual_station_CO2)

	def test_grab_equipment_kwh_co2_url(self):
		url = reverse('grab_equipment_kWh_CO2', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grab_equipment_kWh_CO2)

	def test_grab_equipment_line_kwh_url(self):
		url = reverse('grab_equipment_line_kWh', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grab_equipment_line_kWh)

	def test_garb_equipment_line_co2_url(self):
		url = reverse('grab_equipment_line_CO2', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grab_equipment_line_CO2)

	def test_grab_individual_equipment_kwh_url(self):
		url = reverse('grab_individual_equipment_kWh', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grab_individual_equipment_kWh)

	def test_grab_individual_equipment_co2_url(self):
		url = reverse('grab_individual_equipment_CO2', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grab_individual_equipment_CO2)

	def test_grab_clamps_line_kwh_url(self):
		url = reverse('grab_clamps_line_kWh', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grab_clamps_line_kWh)

	def test_grab_clamps_line_co2_url(self):
		url = reverse('grab_clamps_line_CO2', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grab_clamps_line_CO2)

	def test_grab_clamp_kwh_co2_url(self):
		url = reverse('grab_clamp_kWh_CO2', kwargs={'id':1})
		self.assertEqual(resolve(url).func, grab_clamp_kWh_CO2)

class ModelTests(TestCase):
	"""Class to test all EnergyCapture app models"""
	def setUp(self):
		"""Set up for all EnergyCapture tests"""
		self.company = Company.objects.create(company_name = 'Test Company')
		self.station = Station.objects.create(name = 'Test Station', company = self.company)
		self.equipment = Equipment.objects.create(name = 'Test Equipment', station = self.station)
		self.powerclamp = PowerClamp.objects.create(name = 'Test Power Clamp', equipment = self.equipment)
		self.stationtime = StationTime.objects.create(power = 1, id = 1, station = self.station)
		self.equipmenttime = EquipmentTime.objects.create(power = 1, id = 1, equipment = self.equipment)
		self.powerclamptime = PowerClampTime.objects.create(power = 1, id = 1, powerClamp = self.powerclamp)

	def test_station_creation(self):
		station = Station.objects.get(id=self.station.id)
		self.assertEqual(self.station, station)	

	def test_equipment_creation(self):
		equipment = Equipment.objects.get(id=self.equipment.id)
		self.assertEqual(self.equipment, equipment)

	def test_powerclamp_creation(self):
		powerclamp = PowerClamp.objects.get(id=self.powerclamp.id)
		self.assertEqual(self.powerclamp, powerclamp)

	def test_stationtime_creation(self):
		stationtime = StationTime.objects.get(id=self.stationtime.id)
		self.assertEqual(self.stationtime, stationtime)

	def test_eqipmenttime_creation(self):
		equipmenttime = EquipmentTime.objects.get(id=self.equipmenttime.id)
		self.assertEqual(self.equipmenttime, equipmenttime)

	def test_powerclamptime_creation(self):
		powerclamptime = PowerClampTime.objects.get(id=self.powerclamptime.id)
		self.assertEqual(self.powerclamptime, powerclamptime)

class FormTests(TestCase):

	def setUp(self):
		self.company = Company.objects.create(company_name = 'Test Company')
		self.station = Station.objects.create(name = 'Test Station', company = self.company)
		self.equipment = Equipment.objects.create(name = 'Test Equipment', station = self.station)
		self.powerclamp = PowerClamp.objects.create(name = 'Test Power Clamp', equipment = self.equipment)
		self.stationtime = StationTime.objects.create(power = 1, id = 1, station = self.station)
		self.equipmenttime = EquipmentTime.objects.create(power = 1, id = 1, equipment = self.equipment)
		self.powerclamptime = PowerClampTime.objects.create(power = 1, id = 1, powerClamp = self.powerclamp)
		self.possibleID = PossibleDeviceID.objects.create(deviceID = 'test')

	def test_add_powerclamp(self):
		self.form = AddPowerClampForm(PossibleDeviceID.objects.all(), data={'name': 'powerclamp', 'deviceID': self.possibleID})
		self.assertTrue(self.form.is_valid())
		self.assertTrue(self.possibleID in PossibleDeviceID.objects.all())
		self.powerclamp = PowerClamp.objects.create(name = self.form.cleaned_data['name'])

		self.assertEqual(self.powerclamp, PowerClamp.objects.get(name = self.form['name'].value()))

	def test_delete_powerclamp(self):
		self.form = AddPowerClampForm(PossibleDeviceID.objects.all(), data={'name': 'powerclamp', 'deviceID': self.possibleID})
		self.assertTrue(self.form.is_valid())
		self.assertTrue(self.possibleID in PossibleDeviceID.objects.all())
		self.powerclamp = PowerClamp.objects.create(name = self.form.cleaned_data['name'])

		self.assertEqual(self.powerclamp, PowerClamp.objects.get(name = self.form['name'].value()))

		self.powerclamp.delete()
		self.assertFalse(PowerClamp.objects.all().filter(name = self.form.cleaned_data['name']).exists())

	def test_add_station(self):
		self.form = AddStationForm(data={'name': 'test'})	
		self.assertTrue(self.form.is_valid())
		self.station = Station.objects.create(name = self.form.cleaned_data['name'])

		self.assertEqual(self.station, Station.objects.get(name = self.form['name'].value()))

	def test_delete_station(self):
		self.form = AddStationForm(data={'name': 'test'})	
		self.assertTrue(self.form.is_valid())
		self.station = Station.objects.create(name = self.form.cleaned_data['name'])

		self.assertEqual(self.station, Station.objects.get(name = self.form['name'].value()))

		self.station.delete()
		self.assertFalse(Station.objects.all().filter(name=self.form.cleaned_data['name']).exists())		

	def test_add_equipment(self):
		self.form = AddEquipmentForm(data = {'name': 'test'})
		self.assertTrue(self.form.is_valid())
		self.equipment = Equipment.objects.all().create(name = self.form.cleaned_data['name'])

		self.assertEqual(self.equipment, Equipment.objects.get(name = self.form['name'].value()))

	def test_delete_equipment(self):
		self.form = AddEquipmentForm(data = {'name': 'test'})
		self.assertTrue(self.form.is_valid())
		self.equipment = Equipment.objects.all().create(name = self.form.cleaned_data['name'])

		self.assertEqual(self.equipment, Equipment.objects.get(name = self.form['name'].value()))

		self.equipment.delete()
		self.assertFalse(Equipment.objects.all().filter(name = self.form.cleaned_data['name']).exists())

	def test_choose_co2(self):
		self.form = ChooseCO2Form(data = {'name': 'Scope 2'})
		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.form.cleaned_data['name'],'Scope 2')

	def test_choose_date_range(self):
		self.form = ChooseDateRange(data = {'start_date_field': '01/01/1000', 'end_date_field': '02/01/1000'})
		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.form.cleaned_data['start_date_field'], datetime.date(1000, 1, 1))

	def test_choose_time(self):
		self.form = ChooseTime(data = {'time_field': 'HR'})
		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.form.cleaned_data['time_field'], 'HR')

