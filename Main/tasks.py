from celery import shared_task, Task
import time
import random
from celery import Celery
from celery.schedules import crontab
from asgiref.sync import async_to_sync, sync_to_async
import channels.layers
import requests
import os
# from opcua import *
from django.apps import apps

app = Celery('WP1_4')
BROKER = "redis://localhost:6379"

@shared_task
def Schedule(pro):
	channel_layer = channels.layers.get_channel_layer()
	energyData = []
	bigCabinetPower=0
	bigOvenPower = 0
	kukaRobotPower = 0
	kWh = False

	bigOven = {}
	bigCabinet = {}
	kuka = {}

	#request call to shelly API for all power clamp data
	s = requests.post('https://shelly-43-eu.shelly.cloud/device/all_status', data={'auth_key':os.environ.get('AUTH_KEY')})
	receivedData = s.json() #converting received response into json structure
	try:
		bigOven = receivedData['data']['devices_status']['c45bbe7888f4'] #getting big oven device data
	except KeyError:
		bigOven['total_power'] = 0

	try:
		bigCabinet = receivedData['data']['devices_status']['3494546ecb06'] #getting big cabinet device data
	except KeyError:
		bigCabinet['total_power'] = 0

	try:
		kuka = receivedData['data']['devices_status']['3494546ed0bd'] #getting kuka robot device data
	except KeyError:
		kuka['total_power'] = 0

	if bigOven['total_power'] > 1000: #if watts per hour exceeds 1000, set measurement to kWh instead
		kWh = True 
	else:
		kWh = False


	#assigning power values
	bigOvenPower = bigOven['total_power']
	bigCabinetPower = bigCabinet['total_power']
	kukaRobotPower = kuka['total_power']

	#if power is returning a negative value, invert it into a positive
	if bigOven['total_power'] < 0:
		bigOvenPower = x['total_power'] * -1

	if bigCabinet['total_power'] < 0:
		bigCabinetPower = p['total_power'] * -1

	if kuka['total_power'] < 0:
		kukaRobotPower = k['total_power'] * -1

	if kWh == False: #assign in watts per hour
		energyData.append(bigOvenPower)
		energyData.append(bigCabinetPower)
		energyData.append(kukaRobotPower)
		energyData.append(bigOvenPower + bigCabinetPower + kukaRobotPower)

	else: #assign in kWh
		energyData.append(bigOvenPower / 1000)
		energyData.append(bigCabinetPower / 1000)
		energyData.append(kukaRobotPower / 1000)
		energyData.append((bigOvenPower + bigCabinetPower + kukaRobotPower) / 1000)


	CO2perKWH = (((bigOvenPower / 1000) + (bigCabinetPower/ 1000) + (kukaRobotPower/ 1000))) * float(0.233) #CO2 per KWH calculation
	data = {'message':random.randint(1,50), 'CO2perKWH':CO2perKWH, 'energyData':energyData}

	async_to_sync(channel_layer.group_send)('Main_machineHealthShow' + str(pro['pk']), {'type':"graph_message", "message":data})


# @shared_task
# def opc_test():
# 	try:
# 		client = Client("opc.tcp://192.168.0.2:4840")

# 		client.connect()

# 		node = client.get_node('ns=3;s="tensionHomeSW"')

# 		value = node.get_value()

# 		Sensor = apps.get_model(app_label='Main', model_name='Sensor')
# 		sensor = Sensor.objects.get(id=3)
# 		sensor.posCheck = value

# 		if value:
# 			sensor.status = 2
# 		else:
# 			sensor.status = 3

# 		sensor.save()
		
# 	finally:
# 		client.disconnect()


@shared_task()
def erp_listener():
	erp_schedule = apps.get_model(app_label='Main', model_name='ERP_Schedule')
	erp = erp_schedule.objects.first()
	if erp.changed == True:
		print('True')
		erp.changed = False
		erp.save()

@shared_task()
def test():
	print('hello')

