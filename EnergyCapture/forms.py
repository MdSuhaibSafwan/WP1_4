import os
import requests
from django import forms
from .models import *
from .views import *
from django.forms import TextInput, ModelForm
from Dashboard.widget import DatePickerInput, TimePickerInput, DateTimePickerInput
from json import JSONDecodeError


TIME_CHOICES =(
	("default", "----------"),
    ("HR", "Last Hour"),
    ("DAY", "Last 24 Hours"),
    ("WK", "Last Week"),
    ("MTH", "Last Month"),
    ("YR", "Last Year"),
    ("AT", "All Time"),
    ("Custom", "Custom"),
)
  

class AddPowerClampForm(forms.Form):
	def __init__(self, devices, *args, **kwargs):
		super(AddPowerClampForm, self).__init__(*args, **kwargs)
		# devices_qs = self.get_devices_from_shelly()
		# print("Devices QS --> ", devices_qs)
		device_choices = self.get_device_names_for_choice_field()
		# example_qs = [("1", "number1"), ("2", "number2"), ("3", "number3")]
		self.fields['name'] = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'Enter Power Clamp', 'style':'width:8vw;  margin-bottom:20px; display:inline-block'}))
		self.fields['deviceID'] =forms.ChoiceField(choices=device_choices, 
			widget=forms.Select(
				attrs={
					'placeholder':'Enter Value', 
					'style':'width:8vw; display:inline-block'
		}))
		self.fields['name'].label = "Name"
		self.fields['deviceID'].label = "Device ID"

	def get_devices_from_shelly(self):
		AUTH_KEY = os.environ.get('AUTH_KEY')
		s = requests.post('https://shelly-43-eu.shelly.cloud/device/all_status', data={'auth_key':AUTH_KEY})

		try:
			receivedData = s.json() #converting received response into json structure
		except JSONDecodeError:
			print("Failed request! (JSON DECODE ERROR)")
			receivedData= {}
			drilldown = {}
		
		return receivedData
	
	def get_device_names_for_choice_field(self):
		data = self.get_devices_from_shelly()
		# data["data"]["devices_status"][device]["getinfo"]["fw_info"]["device"]
		device_choices = []
		loop_counter = 1
		for device_id in data["data"]["devices_status"].keys():
			# device_data = data["data"]["devices_status"][device_id]
			# try:
			# 	device_name = device_data["getinfo"]["fw_info"]["device"]
			# except KeyError:
			# 	device_name = "device " + str(device_id)
			device_name = f"shellym3-{str(device_id)}"
			device_tuple = (device_id, device_name)
			device_choices.append(device_tuple)
			loop_counter += 1
		
		# print(device_choices)
		return device_choices

class DeletePowerClampForm(forms.Form):
	def __init__(self, powerClamps, *args, **kwargs):
		super(DeletePowerClampForm, self).__init__(*args, **kwargs)
		self.fields['name'] = forms.ModelChoiceField(queryset=powerClamps, widget=forms.Select(attrs={'placeholder':'Enter Value', 'style':'width:8vw;'}))
		self.fields['name'].label = "Clamp"

class AddStationForm(forms.Form):
	name = forms.CharField(label="Station Name", max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Station Name', 'style':'width:13vw;'}))
	name.label = "Station"

class DeleteStationForm(forms.Form):
	def __init__(self, stations, *args, **kwargs):
		super(DeleteStationForm, self).__init__(*args, **kwargs)
		self.fields['station'] = forms.ModelChoiceField(queryset=stations, widget=forms.Select(attrs={'placeholder':'Enter Value', 'style':'width:13vw;'}))
		self.fields['station'].label = "Station"

class AddEquipmentForm(forms.Form):
	name = forms.CharField(label="Equipment Name", max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Equipment Name', 'style':'width:13vw;'}))
	name.label = "Equipment"

class DeleteEquipmentForm(forms.Form):
	def __init__(self, equipment, *args, **kwargs):
		super(DeleteEquipmentForm, self).__init__(*args, **kwargs)
		self.fields['equipment'] = forms.ModelChoiceField(queryset=equipment, widget=forms.Select(attrs={'placeholder':'Enter Value', 'style':'width:13vw;'}))
		self.fields['equipment'].label="Equipment"

class ChooseCO2Form(ModelForm):
	class Meta:
		model = CO2
		fields = ['name']
		labels = {'name':('CO2 choices')}	

class ChooseDateRange(forms.Form):
	start_date_field = forms.DateField(widget=DatePickerInput, label="Start Date")
	end_date_field = forms.DateField(widget=DatePickerInput, label="End Date")

class ChooseTime(forms.Form):
	time_field = forms.ChoiceField(choices = TIME_CHOICES, label="Choose a Time Frame")
