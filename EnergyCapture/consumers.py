import json 
import secrets
import requests 
from random import randint
from asyncio import sleep
from django.utils import timezone
from datetime import timedelta
from channels.generic.websocket import AsyncWebsocketConsumer 
from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from django_celery_beat.models import PeriodicTask, CrontabSchedule, ClockedSchedule
from .utils import get_device_data

users_online = []

class GraphConsumer(AsyncWebsocketConsumer):
	
	async def connect(self):

		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = "EnergyCapture_%s" % self.room_name

		self.x = await self.get_name()
		self.x.enabled = True
		await self.saveSchedule(self.x)

		if len(users_online) == 0:
			users_online.append([self.room_name, self.scope['user']])

		else:
			for i in range(0,len(users_online)):
				if users_online[i][0] == self.room_name:
					users_online[i].append(self.scope['user'])
				else:
					if i == len(users_online)-1:
						users_online.append([self.room_name, self.scope['user']])
		
		print(users_online)
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		await self.accept()

	async def disconnect(self, close_code):
		
		for i in range(0,len(users_online)):
			if users_online[i][0] == self.room_name:
				if len(users_online[i])==2:
					self.x = await self.get_name()
					self.x.enabled = False
					await self.saveSchedule(self.x)
					users_online.remove(users_online[i])
					print("Removed room+user")

				else:
					users_online[i].remove(self.scope['user'])
					print("removed user")

		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

	async def receive(self, text_data):
		
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		await self.channel_layer.group_send(self.room_group_name, {"type": 'graph_message', "message":message})

	async def graph_message(self, event):
		message = event["message"]
		await self.send(text_data=json.dumps({"message":message}))

	@database_sync_to_async
	def get_name(self):
		from django_celery_beat.models import PeriodicTask
		print(PeriodicTask.objects.get(name=self.room_group_name))
		return PeriodicTask.objects.get(name=self.room_group_name)

	@database_sync_to_async
	def saveSchedule(self, x):
		x.save()


class SessionGraphConsumer(AsyncConsumer):

	async def websocket_connect(self, event):
		print(event)
		session = self.scope["session"]
		await self.send({
			"type": "websocket.accept"
		})

		room_name = f"room_{session.session_key}"
		print("Room name ", room_name)
		await self.channel_layer.group_add(
			room_name,
			self.channel_name
		)

	async def websocket_receive(self, event):
		data = json.loads(event["text"])
		print(data)

		command = data.get("command", None)
		if command is None:
			return None
		
		command_list = {
			"initiate_celery": self.initiate_celery,
			"get_device_updates": self.get_device_data
		}
		await command_list[command](data)

	async def get_device_data(self, data):
		print("getting device data")
		device_data = await get_device_data(data.get("device_id"))
		if device_data == None:
			return None

		await self.send({
			"type": "websocket.send",
			"text": json.dumps(device_data)
		})


	async def initiate_celery(self, data):
		print("INITIATING CELERY ")
		device_id = data.get("device_id")
		task = await self.create_periodic_task(device_id)


	@database_sync_to_async
	def create_periodic_task(self, device_id):
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
	
	async def send_message(self, event):
		print("Sending Message")
		data = event["data"]
		await self.send({
			"type": "websocket.send",
			"text": json.dumps(data)
		})
		return True

	async def websocket_disconnect(self, event):
		print(event)
