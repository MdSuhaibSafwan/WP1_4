from django.urls import path, re_path
from .consumers import GraphConsumer, SessionGraphConsumer

ws_urlpatterns = [
	#path("ws/MachineHealth/", GraphConsumer.as_asgi())
	re_path(r"ws/EnergyCapture/(?P<room_name>\w+)/$", GraphConsumer.as_asgi()),
    path("EnergyCapture/graph/", SessionGraphConsumer.as_asgi(), )
]