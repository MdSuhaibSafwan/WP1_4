import os
import requests
import json
from asgiref.sync import async_to_sync, sync_to_async


def request_to_shelly_cloud():
	AUTH_KEY = os.environ.get('AUTH_KEY')
	s = requests.post('https://shelly-43-eu.shelly.cloud/device/all_status', data={'auth_key':AUTH_KEY})

	try:
		receivedData = s.json() #converting received response into json structure
	except JSONDecodeError:
		print("Failed request! (JSON DECODE ERROR)")
		receivedData= {}

	return receivedData
	

@sync_to_async
def get_device_data(device_id):
	data = request_to_shelly_cloud()
	if data == {}:
		return None

	device_data = data["data"]["devices_status"][device_id]
	return device_data

