from celery import shared_task, Task
import time
import random
from celery import Celery
from celery.schedules import crontab
from asgiref.sync import async_to_sync, sync_to_async
import channels.layers
import requests
import os
from opcua import *
from django.apps import apps
from datetime import datetime,timedelta
import random
import string
import math
import pytz
from zoneinfo import ZoneInfo
from django.utils import timezone

app = Celery('WP1_4')
BROKER = "redis://localhost:6379"

timezone.activate(ZoneInfo("Europe/London"))

@shared_task
def Master_Scheduler_Station(id):
	Station = apps.get_model(app_label='EnergyCapture', model_name='Station')
	PowerClamp = apps.get_model(app_label='EnergyCapture', model_name='PowerClamp')
	Company = apps.get_model(app_label='Main', model_name='Company')
	company = Company.objects.first()
	station = Station.objects.get(id=id)
	drilldown = company.json

	total = 0
	grandTotal = 0
	if drilldown:
		for equipment in station.equipment_set.all():
			for clamp in equipment.powerclamp_set.all():
				if clamp.deviceID in drilldown.keys():
					clamp.powerclamptime_set.create(power=drilldown[clamp.deviceID]['total_power'], time=timezone.localtime(timezone.now()))
					total+=drilldown[clamp.deviceID]['total_power']
				else:
					rand = random.randint(54,743)
					clamp.powerclamptime_set.create(power=rand, time=timezone.localtime(timezone.now()))
					total+=rand

			equipment.equipmenttime_set.create(power=total, time=timezone.localtime(timezone.now()))
			grandTotal += total
			total = 0
		station.stationtime_set.create(power=grandTotal, time=timezone.localtime(timezone.now()))
		print("success")
			

	else:
		print("fail")
		station.stationtime_set.create(power=0,time=timezone.localtime(timezone.now()))
		for equipment in station.equipment_set.all():
			equipment.equipmenttime_set.create(power=0, time=timezone.localtime(timezone.now()))
			for clamp in equipment.powerclamp_set.all():
				clamp.powerclamptime_set.create(power=0, time=timezone.localtime(timezone.now()))

@shared_task
def Master_Company_Scheduler():
	Company = apps.get_model(app_label='Main', model_name='Company')
	company = Company.objects.first()

	total = 0
	for station in company.station_set.all():
		total += station.stationtime_set.last().power

	company.companytime_set.create(power=total, time=timezone.localtime(timezone.now()))



@shared_task(task_ignore_result = True)
def Schedule():

	s = requests.post('https://shelly-43-eu.shelly.cloud/device/all_status', data={'auth_key':os.environ.get('AUTH_KEY')})

	try:
		receivedData = s.json() #converting received response into json structure
	except JSONDecodeError:
		print("Failed request! (JSON DECODE ERROR)")
		receivedData= {}
		drilldown = {}
	PossibleDeviceID = apps.get_model(app_label='EnergyCapture', model_name='PossibleDeviceID')

	try:
		drilldown=receivedData['data']['devices_status']
	except KeyError:
		print("Failed request (JSON KEY ERROR)!")
		drilldown = {}
		
	Company = apps.get_model(app_label='Main', model_name='Company')
	company = Company.objects.first()
	company.json = drilldown
	company.save()

	if drilldown:
		for temp in drilldown.keys():
	 		PossibleDeviceID.objects.get_or_create(deviceID=temp)

@shared_task(task_ignore_result = True)
def PostData(equipment): #Post data to powerClamp page
	channel_layer = channels.layers.get_channel_layer() #get channel layer form redis so we can get rooms
	data, labels, times =[],[],[]
	total_power=0
	postData = {}
	Equipment = apps.get_model(app_label='EnergyCapture', model_name='Equipment') #Equipment model
	equipment = Equipment.objects.get(id=equipment) #equipment ID specified on creation of this periodic task, so this task will always be related to the channel room 
	for powerClamp in equipment.powerclamp_set.all():
		data.append(float(powerClamp.powerclamptime_set.last().power))
		labels.append(powerClamp.name)
		times.append(float(math.trunc(datetime.timestamp(powerClamp.powerclamptime_set.last().time)*1000))) #grab latest power data and timestamp

	postData = {'data':data, 'labels':labels, 'times':times}

	async_to_sync(channel_layer.group_send)('EnergyCapture_addPowerClamps'+str(equipment.id), {'type':"graph_message", "message":postData}) #throw data to django channel room directly related to this task

@shared_task(task_ignore_result = True)
def PostData_Equipment(station): #Post data to equipment page
	channel_layer = channels.layers.get_channel_layer() #getting channel layer from redis so we can get rooms
	data, labels, times =[],[],[]
	total_power=0
	postData = {}
	Station = apps.get_model(app_label='EnergyCapture', model_name='Station') #Get station model
	station = Station.objects.get(id=station) #got our station now as this task can only be created with station ID specified
	for equipment in station.equipment_set.all():
		data.append(float(equipment.equipmenttime_set.last().power)) #get latest power and time stamp, then throw to django channel room
		labels.append(equipment.name)
		times.append(float(math.trunc(datetime.timestamp(equipment.equipmenttime_set.last().time)*1000)))

	postData = {'data':data, 'labels':labels, 'times':times}

	async_to_sync(channel_layer.group_send)('EnergyCapture_addEquipment'+str(station.id), {'type':"graph_message", "message":postData}) #beautiful code that sends our data straight to channel room



@shared_task(task_ignore_result = True)
def PostData_Station(company): #Post data to setup overview page
	channel_layer = channels.layers.get_channel_layer()  #getting channel layer from redis so we can get rooms
	data, labels, times =[],[],[]
	total_power=0
	
	CO2 = []
	postData = {}
	Company = apps.get_model(app_label='Main', model_name='Company') #get company model
	company = Company.objects.get(id=company)
	CO2PerKWH= company.co2_choice #we got company so we can get CO2 choice for kg co2e
	for station in company.station_set.all():
		data.append(float(station.stationtime_set.last().power))
		CO2.append((float(station.stationtime_set.last().power)/1000) * float(CO2PerKWH)) #getting kg CO2e and timestamp (latest)
		labels.append(station.name+str(" (Wh)"))
		times.append(float(math.trunc(datetime.timestamp(station.stationtime_set.last().time)*1000)))


	postData = {'data':data, 'labels':labels, 'times':times, 'CO2':CO2}

	async_to_sync(channel_layer.group_send)('EnergyCapture_addStation', {'type':"graph_message", "message":postData}) #throwing data to our channel room and into graph

@shared_task(task_ignore_result = True)
def PostData_Dashboard(company): #Post data to dashboard overview page
	channel_layer = channels.layers.get_channel_layer() #redis channel layer for rooms
	data, labels, times =[],[],[]
	total_power=0
	CO2 = []
	postData = {}
	Company = apps.get_model(app_label='Main', model_name='Company')
	company = Company.objects.get(id=company) #company specified on this periodic task creation (See equipment setup page view for details)
	CO2PerKWH = company.co2_choice
	total_power = company.total_power
	total_CO2 = company.total_power * float(CO2PerKWH)  #getting latest total kwh/co2 #TODO: Kind of redundant now but could be implemented in future, review nathan
	for station in company.station_set.all():
		data.append(float(station.stationtime_set.last().power)/1000) #CO2, timestamps etc to be thrown into channel room
		CO2.append((float(station.stationtime_set.last().power)/1000) *float(CO2PerKWH))
		labels.append(station.name+str(" (kWh)"))
		times.append(float(math.trunc(datetime.timestamp(station.stationtime_set.last().time)*1000)))


	postData = {'data':data, 'labels':labels, 'times':times, 'CO2':CO2, 'total_power':total_power, 'total_CO2':total_CO2}

	async_to_sync(channel_layer.group_send)('EnergyCapture_energyCaptureDashboard', {'type':"graph_message", "message":postData}) #data launched into room and into graph (magic)

@shared_task(task_ignore_result = True)
def PostData_Dashboard_Station_Level(station): #Post data to Dashboard station page
	channel_layer = channels.layers.get_channel_layer() #Redis channel layer with rooms - basically a database exists within redis that stores the rooms we create with the daphne on-connect django channels function
	data, labels, times =[],[],[]
	total_power=0
	CO2 = []
	
	postData = {}
	Station = apps.get_model(app_label='EnergyCapture', model_name='Station') #station with "station" ID that we specify when creating this periodic task
	station = Station.objects.get(id=station)
	CO2PerKWH= station.company.co2_choice
	total_power = station.total_power #REDUNDANT PROBABLY REVIEW NUTHON
	total_CO2 = station.total_power * float(CO2PerKWH)
	for equipment in station.equipment_set.all():
		data.append(float(equipment.equipmenttime_set.last().power)/1000)
		CO2.append((float(equipment.equipmenttime_set.last().power)/1000) *float(CO2PerKWH))
		labels.append(equipment.name+str(" (kWh)"))
		times.append(float(math.trunc(datetime.timestamp(equipment.equipmenttime_set.last().time)*1000))) #Data with timestamp to be launched


	postData = {'data':data, 'labels':labels, 'times':times, 'CO2':CO2, 'total_power':total_power, 'total_CO2':total_CO2}

	async_to_sync(channel_layer.group_send)('EnergyCapture_stationDashboard'+str(station.id), {'type':"graph_message", "message":postData}) #Low orbit ion cannoned into station dashboard page with specified ID 

@shared_task(task_ignore_result = True)
def PostData_Dashboard_Equipment_Level(equipment): #Post data to Equipmetn dashboard page
	channel_layer = channels.layers.get_channel_layer() #Redis channel layer with rooms
	data, labels, times =[],[],[]
	total_power=0
	CO2 = []
	postData = {}
	Equipment = apps.get_model(app_label='EnergyCapture', model_name='Equipment')
	equipment = Equipment.objects.get(id=equipment)
	CO2PerKWH = equipment.station.company.co2_choice #CO2 per KWH from company object
	total_power = equipment.total_power #redundantly reminding myself that this is redundant
	total_CO2 = equipment.total_power * float(CO2PerKWH)
	for clamp in equipment.powerclamp_set.all():
		data.append(float(clamp.powerclamptime_set.last().power)/1000) #Data to be launched
		CO2.append((float(clamp.powerclamptime_set.last().power)/1000) *float(CO2PerKWH))
		labels.append(clamp.name+str(" (kWh)"))
		times.append(float(math.trunc(datetime.timestamp(clamp.powerclamptime_set.last().time)*1000)))


	postData = {'data':data, 'labels':labels, 'times':times, 'CO2':CO2, 'total_power':total_power, 'total_CO2':total_CO2}

	async_to_sync(channel_layer.group_send)('EnergyCapture_equipmentDashboard'+str(equipment.id), {'type':"graph_message", "message":postData}) #Data given to equipment dashboard page to populate real time graph (epic)

@shared_task()
def object_listener():
	Process = apps.get_model(app_label='Main', model_name='Process')
	p = Process.objects.first()

	if not p.CO2 == p.cached_CO2:
		p.cached_CO2=p.CO2 
		p.save()
		print("updated!")

@shared_task
def send_data_to_session(session_id, device_id):
	AUTH_KEY = os.environ.get('AUTH_KEY')
	s = requests.post('https://shelly-43-eu.shelly.cloud/device/all_status', data={'auth_key':AUTH_KEY})

	try:
		receivedData = s.json() #converting received response into json structure
	except JSONDecodeError:
		print("Failed request! (JSON DECODE ERROR)")
		receivedData= {}
	
	execution_time = timezone.now()
	clocked_obj, created = ClockedSchedule.objects.get_or_create(clocked_time=execution_time)
	session = self.scope["session"]
	task = PeriodicTask.objects.create(
		name=f"send-data-for-session-{session.session_key}-{secrets.token_hex(8)}",
		task="Main.tasks.get_device_data_and_send_update_real_time",
		clocked=clocked_obj,
		one_off=True,
		kwargs=json.dumps({"device_id": device_id, "session_key": session.session_key})
	)
	return task





# @shared_task
# def opc_test():
# 	try:
# 		client = Client("opc.tcp://192.168.0.2:4840")

# 		client.connect()
# 		print("sucess")

# 		# node = client.get_node('ns=3;s="tensionHomeSW"')

# 		# value = node.get_value()

# 		# Sensor = apps.get_model(app_label='Main', model_name='Sensor')
# 		# sensor = Sensor.objects.get(id=3)
# 		# sensor.posCheck = value

# 		# if value:
# 		# 	sensor.status = 2
# 		# else:
# 		# 	sensor.status = 3

# 		# print(sensor.status)
# 		# sensor.save()
		
# 	finally:
# 		client.disconnect()
