from channels.generic.websocket import AsyncWebsocketConsumer 
import json 
from random import randint
from asyncio import sleep
import requests 
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async

users_online = []

class GraphConsumer(AsyncWebsocketConsumer):
	
	async def connect(self):

		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = "Main_%s" % self.room_name

		if len(users_online) == 0:
			users_online.append([self.room_name, self.scope['user']])

		else:
			for i in range(0,len(users_online)):
				if users_online[i][0] == self.room_name:
					users_online[i].append(self.scope['user'])
				else:
					if i == len(users_online)-1:
						users_online.append([self.room_name, self.scope['user']])
		
		
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
		print(PeriodicTask.objects.get(name=self.room_name))
		return PeriodicTask.objects.get(name=self.room_name)

	@database_sync_to_async
	def saveSchedule(self, x):
		x.save()
		