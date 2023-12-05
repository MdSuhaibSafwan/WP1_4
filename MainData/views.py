from django.shortcuts import render, redirect
#Django
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.db.models.fields import NOT_PROVIDED
from Main.models import Project, Sensor
from MainData.models import *
from datetime import timedelta, datetime
from django.contrib.auth.models import User, Group

from django.contrib import messages

from .forms import *

import io
 
def viewProjectParts(response, id):
	'''View to allow viewing of parts associated with a project '''
	if response.user.is_authenticated:
		#setup	
		project, management, supervisor = Project.objects.get(id=id), False, False
		if response.user.groups.filter(name='Management').exists():	
			management = True	
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True		
			#check project in user company set
		else:
			return redirect('/')
			
		if response.user.profile.user_company != None:
			if project in response.user.profile.user_company.project_set.all():
				if management or supervisor:
					return render(response, 'MainData/viewProjectPart.html', {'project':project, 'management':management, 'supervisor':supervisor})
			else:
				#redirect to home page
				return redirect('/')

		else:#redirect to home page
			return redirect('/')	
		
	else:
		return redirect('/mylogout/')
		
def viewPartDetail(response, id):
	'''View to allow the user to view detail to do with a parts process's'''
	if response.user.is_authenticated:
		management, supervisor = False, False
		part = Part.objects.get(part_id=id)
		partProcessSet = part.processpart_set.all().values_list('processName', flat=True).distinct()
		processSet = [(id,id) for id in partProcessSet]
		# convert list to dict then back to list to remove duplicates
		processPart = part.processpart_set.first()

		process_select_form = selectProcessPartForm(processSet)
		if response.user.groups.filter(name='Management').exists():	
			management = True	
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True	
		#check project in user company set
		if part.project in response.user.profile.user_company.project_set.all():
			if management or supervisor:
				if response.POST.get('processPartSelect'):
					process_select_form = selectProcessPartForm(processSet, response.POST)
					if process_select_form.is_valid():
						processPart = part.processpart_set.get(processName = process_select_form.cleaned_data['choice'])
						messages.success(response, 'Process Successfully Changed!')

				return render(response, 'MainData/viewPartDetail.html', {'part':part, 'management':management, 'supervisor':supervisor, 'process_select_form':process_select_form, 'processPart': processPart})
		else:
			#redirect to home page
			return redirect('/')
		
		#redirect to home page
		return redirect('/')	
	else:
		return redirect('/mylogout/')

def viewBlankDetail(response, id):
	if response.user.is_authenticated:
		blank = Blank.objects.get(blank_id=id)
		management, supervisor = False,False
		blankProcessSet = blank.processpart_set.all().values_list('processName', flat=True).distinct()
		processSet = [(id,id) for id in blankProcessSet]
		processPart = blank.processpart_set.first()

		process_select_form = selectProcessPartForm(processSet)

		if response.user.groups.filter(name='Management').exists():	
			management = True	
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True	
		#check project in user company set
		if blank.project in response.user.profile.user_company.project_set.all():
			if management or supervisor:

				if response.POST.get('processPartSelect'):
					process_select_form = selectProcessPartForm(processSet, response.POST)

					if process_select_form.is_valid():
						if blank.processpart_set.filter(processName = process_select_form.cleaned_data['choice']).exists():
							processPart = blank.processpart_set.get(processName = process_select_form.cleaned_data['choice'])
						messages.success(response, 'Process Successfully Changed!')


				return render(response, 'MainData/viewBlankDetail.html', {'blank':blank, 'management':management, 'supervisor':supervisor, 'processPart':processPart, 'process_select_form':process_select_form })
			else:
				return redirect('/')
		else:
			return redirect('/')
	else:
		return redirect('/')


def viewPlyDetail(response,id):
	if response.user.is_authenticated:
		ply = Ply.objects.get(ply_id=id)
		management, supervisor = False,False
		plyProcessSet = ply.processpart_set.all().values_list('processName', flat=True).distinct()
		processSet = [(id,id) for id in plyProcessSet]
		processPart = ply.processpart_set.first()

		process_select_form = selectProcessPartForm(processSet)

		if response.user.groups.filter(name='Management').exists():	
			management = True	
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True	
		#check project in user company set
		if ply.project in response.user.profile.user_company.project_set.all():
			if management or supervisor:

				if response.POST.get('processPartSelect'):
					process_select_form = selectProcessPartForm(processSet, response.POST)

					if process_select_form.is_valid():
						if ply.processpart_set.filter(processName = process_select_form.cleaned_data['choice']).exists():
							processPart = ply.processpart_set.get(processName = process_select_form.cleaned_data['choice'])
						messages.success(response, 'Process Successfully Changed!')


				return render(response, 'MainData/viewPlyDetail.html', {'ply':ply, 'management':management, 'supervisor':supervisor, 'processPart':processPart, 'process_select_form':process_select_form })
			else:
				return redirect('/')
		else:
			return redirect('/')
	else:
		return redirect('/')
		

def viewPartSubDetail(response, id):
	'''View to allow the user to access the detail of the sub process related to the part'''
	#setup
	if response.user.is_authenticated:
		proPart, management, supervisor = ProcessPart.objects.get(id=id), False, False
		part, ply, blank = False,False,False
		if response.user.groups.filter(name='Management').exists():	
			management = True	
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True	
		if proPart.part is not None:
			checkVar = proPart.part
			part = True
		elif proPart.blank is not None:
			checkVar = proPart.blank
			blank = True
		elif proPart.ply is not None:
			checkVar = proPart.ply
			ply = True
			
		#check project in user company set
		if checkVar.project in response.user.profile.user_company.project_set.all():
			if management or supervisor:
				orderedSubProcessPartList = proPart.subprocesspart_set.all()
				lastCardID = orderedSubProcessPartList.last()
				return render(response, 'MainData/viewPartSubDetail.html', {'part':part, 'ply':ply, 'blank':blank,  'proPart':proPart,  'management':management, 'supervisor':supervisor, 'lastCardID': lastCardID})
		else:
			#redirect to home page
			return redirect('/')
			
		#redirect to home page
		return redirect('/')	
	else:
		return redirect('/mylogout/')
		
def viewPartSubSensorDetail(response, id):
	'''view to allow user to access sensor detail related to the part'''
	#setup		
	if response.user.is_authenticated:
		subProPart, management, supervisor = SubProcessPart.objects.get(id=id), False, False
		if response.user.groups.filter(name='Management').exists():	
			management = True	
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True	
		#check project in user company set
		if subProPart.processPart.part.project in response.user.profile.user_company.project_set.all():
			if management or supervisor:
				return render(response, 'MainData/viewPartSubSensorDetail.html', {'subProPart' : subProPart,  'management':management, 'supervisor':supervisor})
		else:
			#redirect to the home page		
			return redirect('/')	
		
		#redirect to home page
		return redirect('/')	
	else:
		return redirect('/mylogout/')
		

def processPartSensor(response, id):
	#setup		
	if response.user.is_authenticated:
		sensorData, management, supervisor, processPart, subProcessPart, error, project = SensorData.objects.get(id=id), False, False, False, False, '',''
		if sensorData.processPart is not None:
			project = sensorData.processPart.part.project
			processPart = True
		elif sensorData.subProcessPart is not None:
	  		project = sensorData.subProcessPart.processPart.part.project
	  		subProcessPart = True

		if response.user.groups.filter(name='Management').exists():	
			management = True	
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True
		
			
		if project in response.user.profile.user_company.project_set.all():
			if management or supervisor:
				return render(response, 'MainData/processPartSensor.html', {'sensorData' : sensorData,  'management':management, 'supervisor':supervisor, 'processPart':processPart, 'subProcessPart':subProcessPart })
		else:
			#redirect to the home page		
			return redirect('/')	
			
		#redirect to home page
		return redirect('/')	
	else:
		return redirect('/mylogout/')
	

def updateProcessGraph(response, id):
	#part data sensor graphs
	if response.user.is_authenticated:
		sensor, data, labels, date = SensorData.objects.get(id=id), [], [], []
		#get all sensortime data for sensors and append it to data and labels for graph plotting
		for instance in sensor.sensortimedata_set.all():
			if sensor.sensorName == "Thermocouple":
				data.append(instance.temp) 
				format_data = "%H:%M:%S"
				labels.append(datetime.strftime(instance.time, format_data))

			elif sensor.sensorName == "Accelerometer":
				data.append(instance.acceleration)
				format_data = "%H:%M:%S"
				labels.append(datetime.strftime(instance.time, format_data))

			elif sensor.sensorName == "Pressure Sensor":
				data.append(instance.pressure)
				format_data = "%H:%M:%S"
				labels.append(datetime.strftime(instance.time, format_data))

			elif sensor.sensorName == "Motor Driver":
				data.append(instance.torque)
				format_data = "%H:%M:%S"
				labels.append(datetime.strftime(instance.time, format_data))

			elif sensor.sensorName == "Microphone":
				data.append(instance.noise)
				format_data = "%H:%M:%S"
				labels.append(datetime.strftime(instance.time, format_data))

			format_data = "%m/%d/%Y"
			date = datetime.strftime(instance.time, format_data)



		return JsonResponse(data={'data':data, 'labels':labels, 'date': date,})
	else:
		return redirect('/')

		