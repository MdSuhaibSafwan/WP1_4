#Django
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.db.models.fields import NOT_PROVIDED
from django.contrib import messages
from django import template

#Importing local .py files
from .forms import *
from .models import *
from MainData.models import *
from EdgeDetection.forms import *
from EdgeDetection.views import *
#from . helper import *
import django.utils
from zoneinfo import ZoneInfo
#Importing DateTime
from datetime import datetime,date,time,timedelta

import io, os, random, requests, math, environ, json, environ

 
from asgiref.sync import async_to_sync
from django.utils import timezone

# import channels.layers
django.utils.timezone.activate(ZoneInfo("Europe/London"))

def index(response):
	"""View to return home page"""
	if response.user.is_authenticated:
		admin = False
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		#return response and page
		return render(response, 'Main/index.html', {'admin':admin})
	else:
		return redirect('/mylogout/')


def showProcess(response, id):
	"""View to add or remove sub process's from the current process. If trying to access
		through url then all process's shown"""
	#setup
	if response.user.is_authenticated:
		pro = Process.objects.get(id=id)
		orderedSubProList,firstCardID, partID, lastCardID = '', '', '', ''
		subLength = 0
		deletion,addDevice =  False, False

		if pro.project.manual:
			processName = pro.manualName
			form= addManualSubProcess(pro)
		else:
			processName = pro.name
			form= addSubProcess(pro)
		sensor_form = SensorForm(pro)
		machine_form = MachineForm()
		part_instance_form = PartInstanceForm(pro)
		sensorSet = Sensor.objects.none()
		select_sensor_form = SelectSensorForm(sensorSet)
		enter_device_form = EnterDeviceID()
		subProcessPartSet = []
		processPart = None

		if response.user.profile.sequence_choice is None:
			if pro.partinstance_set.first() is not None:
				for part in pro.partinstance_set.first().part_set.all():
					if ProcessPart.objects.filter(part=part, processName=pro.name).exists():
						processPart = ProcessPart.objects.get(part = part, processName=pro.name)
					if processPart is not None:
						for sub in processPart.subprocesspart_set.all():
							subProcessPartSet.append(sub)
						for blank in part.blank_set.all():
							processPart = ProcessPart.objects.get(blank=blank, processName = pro.name)
							for sub in processPart.subprocesspart_set.all():
								subProcessPartSet.append(sub)

			if pro.blankinstance_set.first() is not None:
				for blank in pro.blankinstance_set.first().blank_set.all():
					if ProcessPart.objects.filter(blank=blank, processName=pro.name).exists():
						processPart = ProcessPart.objects.get(blank = blank, processName = pro.name)
					if processPart is not None:
						for sub in processPart.subprocesspart_set.all():
							subProcessPartSet.append(sub)
						# for ply in blank.ply_set.all():					
						# 	processPart = ProcessPart.objects.get(ply=ply)
						# 	for sub in processPart.subprocesspart_set.all():
						# 		subProcessPartSet.append(sub)

			if pro.plyinstance_set.first() is not None:
				for ply in pro.plyinstance_set.first().ply_set.all():
					if ProcessPart.objects.filter(ply=ply, processName=pro.name).exists():
						processPart = ProcessPart.objects.get(ply = ply, processName = pro.name)
					if processPart is not None:
						for sub in processPart.subprocesspart_set.all():
							subProcessPartSet.append(sub)
		else:
			product = ProcessPart.objects.get(id=response.user.profile.sequence_choice)
			active = False

			if product.ply is not None:
				piece = product.ply
				if piece.plyInst is not None:
					active = True
			elif product.blank is not None:
				piece = product.blank
				if piece.blankInstance is not None:
					active = True
			elif product.part is not None:
				piece = product.part
				if piece.partInstance is not None:
					active = True

			if active == True:
				for sub in product.subprocesspart_set.all():
					subProcessPartSet.append(sub)
			else:
				profile = response.user.profile
				profile.sequence_choice = None
				profile.save()

		if len(subProcessPartSet) == 0:
			subLength = 0
		else:
			subLength = 1

		management, technician, supervisor = False, False, False

		if response.user.groups.filter(name='Management').exists():
			management = True
		if response.user.groups.filter(name='Supervisor').exists():
			supervisor = True

		#make sure project is in the user company project set
		if pro.project in response.user.profile.user_company.project_set.all():
			#check group
			if management or supervisor:
				pro.update_subprocess_positions()
				if response.method == 'POST':
					if response.user.has_perm('Main.edit_process'):

						#check what is being returned to stop form.is_valid displaying error on other forms
						if (response.POST.get('addSubProcess') or response.POST.get('deleteSubProcess')):
							#pass response to form
							if pro.project.manual:
								form = addManualSubProcess(pro, response.POST)
							else:
								form = addSubProcess(pro, response.POST)
							if form.is_valid():


								#read in sub process
								if pro.project.manual:
									reqSubProcessDirty = form.cleaned_data['manualName']
									reqSubProcess = SubProcess.manual_sub_process_dict[reqSubProcessDirty]
								else:
									reqSubProcess = form.cleaned_data['name']

								#check what information is being passed
								if response.POST.get('addSubProcess'):
									#check if sub process exists
									if pro.subprocess_set.filter(name=reqSubProcess) or pro.subprocess_set.filter(manualName=reqSubProcess):
											messages.error(response,"This Sub Process already exists!")
									#if sub process doesn't exist create it
									else:
										if pro.project.manual:
											#check if sub process is a 'process task'
											if reqSubProcessDirty == 'material_pressed' or reqSubProcessDirty == 'final_inspection':
												#create sub process and set processCheck
												pro.subprocess_set.create(manualName=reqSubProcess, processCheck=True)
											else:
												#create sub process
												pro.subprocess_set.create(manualName=reqSubProcess)
											#display success
											messages.success(response,"Sub Process sucessfully added!")

										else:
											#check if sub process is a 'process task'
											if reqSubProcess == 'material_pressed' or reqSubProcess == 'final_inspection':
												#create sub process and set processCheck
												pro.subprocess_set.create(name=reqSubProcess, processCheck=True)
											else:
												#create sub process
												pro.subprocess_set.create(name=reqSubProcess)
											#display success
											messages.success(response,"Sub Process sucessfully added!")
											pro.update_subprocess_positions()
								#check what information is being passed
								elif response.POST.get('deleteSubProcess'):
									#if sub process exists delete it
									pName = ""
									try:
										if pro.project.manual:
											p = pro.subprocess_set.get(manualName=reqSubProcess)
											pName = p.manualName
											processName = pro.manualName
										else:
											p = pro.subprocess_set.get(name=reqSubProcess)
											pName = p.name
											processName = pro.name

										if processName == "Form Preform":
											if pName == "Initialisation" or pName == "Material Pressed" or pName == "Final Inspection":
												messages.error(response,"You cannot delete this Sub-Process because it is vital to Form Preform")
											else:
												p.delete()
												messages.success(response,"Sub Process sucessfully deleted!")
									#if sub process doesn't exist display error
									except:
										messages.error(response,'Sub Process does not exist!')


						#check what is being returned to stop form.is_valid displaying error on other forms
						if (response.POST.get('addSensor') or response.POST.get('deleteSensor')):
							sensor_form = SensorForm(pro, response.POST)
							if sensor_form.is_valid():
								#read in cleaned sensor name
								reqSensor = sensor_form.cleaned_data['choice']
								#check response
								if response.POST.get('addSensor'):
									#check if sensor exists
									if not Sensor.objects.all().filter(name = reqSensor.name).exists():
										sensor = pro.sensor_set.create(name=reqSensor.name,process=pro, modelID = "SKXCV"+ str(random.randint(0,999)))
									else:

										sensor = Sensor.objects.get(name=reqSensor.name, modelID=reqSensor.modelID)
										if not sensor in pro.sensor_set.all():
											sensor.process = pro
											sensor.save()
											messages.success(response,"Sensor sucessfully added!")
										else:
											messages.error(response, 'Sensor already exists!')
								#check response
								elif response.POST.get('deleteSensor'):
									#if sensor exists delete it

									sensor = pro.sensor_set.filter(name=reqSensor.name).first()

									if len(pro.sensor_set.filter(name=reqSensor.name)) > 1:
										messages.error(response, "Select a Sensor to delete!")
										sensorSet = pro.sensor_set.filter(name=reqSensor.name)
										deletion = True
										select_sensor_form = SelectSensorForm(sensorSet, response.POST)
									else:
										sensor.delete()

										messages.success(response, 'Sensor successfully deleted!')


						if response.POST.get('addDeviceID'):
							cleaned_data = Sensor.pro_sensor_choices_dict[response.POST['proName']]
							sensor = pro.sensor_set.create(name=cleaned_data,process=pro, modelID = response.POST['name'])
							messages.success(response, sensor.name + " Sucessfully Added!")

						if response.POST.get('deleteSelection'):

							sensor = Sensor.objects.get(modelID=response.POST['choice'])

							sensor.delete()
							messages.success(response,"Sensor successfully deleted!")

						if response.POST.get('requestHardware'):
							data = {}
							data = {
							'isok' : True,

							'machines' : {

								'Ply Cutter':{
									'isok' : True,

									'devices':{

										'Humidity Sensor':{
											'id' :1,
											'isok': True,
											'modelID':'TC-611'
										},

										'Pressure Sensor':{
											'id' :2,
											'isok': False,
											'modelID':'PS-219'
										},

										'VOC':{
											'id' :3,
											'isok': True,
											'modelID':'US-519'
										},
									},

									'tiaBlocks' : {
										'block1' : {
											'id' : 1,
										},

										'block2' : {
											'id' : 2,
										},

										'block3' : {
											'id' : 3,
										},
									},
								},

								'Preforming Cell':{

									'isok' : False,

									'devices':{
										'Thermocouple':{
											'id' :4,
											'isok': True,
											'modelID':'TC-421'
										},

										'Pressure Sensor':{
											'id' :5,
											'isok': True,
											'modelID':'PS-311'
										},

										'Ultrasonic Sensor':{
											'id' :6,
											'isok': True,
											'modelID':'US-109'
										},

										'Power Clamp (Big Cabinet)':{
											'id': 7,
											'isok': True,
											'modelID':'3494546ecb06'
										},

										'Power Clamp (Kuka Robot)':{
											'id': 8,
											'isok': True,
											'modelID':'3494546ed0bd'
										},

										'Power Clamp (CNC Router)':{
											'id': 9,
											'isok': True,
											'modelID':'c8c9a37057ca'
										},
									},

									'tiaBlocks' : {
										'block4' : {
											'id' : 4,
										},

										'block5' : {
											'id' : 5,
										},

										'block6' : {
											'id' : 6,
										},
									},
								},
							},
						}

							for machineKey in data['machines']:
								if not response.user.profile.user_company.machine_set.filter(name=machineKey).exists():
									m = Machine.objects.create(name=machineKey, company=response.user.profile.user_company)
								else:
									m = Machine.objects.get(name=machineKey)

								for device in data['machines'][machineKey]['devices']:
									deviceID = data['machines'][machineKey]['devices'][device]['id']
									modelID = data['machines'][machineKey]['devices'][device]['modelID']
									if not Sensor.objects.filter(id=deviceID).exists():
										s = Sensor.objects.create(name=device,id=deviceID, modelID=modelID)
									else:
										s = Sensor.objects.get(id=deviceID, modelID=modelID)

									s.machine = m
									s.save()

									if m in pro.machine.all():
										if len(pro.possiblesensors_set.filter(name=s.name, machine = m)) == 0:
											pro.possiblesensors_set.create(name = s.name, machine=m, modelID = s.modelID)

						if response.POST.get('changePartInstance'):
							part_instance_form = PartInstanceForm(pro,response.POST)
							if part_instance_form.is_valid():
								reqInputClean = part_instance_form.cleaned_data['choice']

								if "Ply" in reqInputClean:
									plyInstance = pro.plyinstance_set.get(instance_id=int(reqInputClean[len(reqInputClean)-1]))
									product = plyInstance.ply_set.all().first().processpart_set.all().first()

								elif "Blank" in reqInputClean:
									blankInstance = pro.blankinstance_set.get(instance_id=int(reqInputClean[len(reqInputClean)-1]))
									product = blankInstance.blank_set.all().first().processpart_set.all().first()

								elif "Part" in reqInputClean:
									partInstance = pro.partinstance_set.get(instance_id=int(reqInputClean[len(reqInputClean)-1]))
									product = partInstance.part_set.all().first().processpart_set.all().first()

								profile = response.user.profile
								profile.sequence_choice = product.id
								profile.save()
								print(profile.sequence_choice)
								for sub in product.subprocesspart_set.all():
									subProcessPartSet.append(sub)
								
								return redirect('/' + str(pro.id))


						if response.POST.get('play'):
							subProcessID = response.POST['play']
							subProcess = SubProcess.objects.get(id=subProcessID)

							if subProcess.operator != None:
								subProcess.status=1
								subProcess.jobStart = datetime.now().replace(microsecond=0)
								subProcess.updateSubIntervals()
								subProcess.updateSubCosts()
								subProcess.save()
							else:
								messages.error(response, 'Sub process needs and operator!')


					else:
						#show permission error
						messages.error(response,'You do not have permission for this action')




				orderedSubProList = pro.order_subprocess_custom()
				firstCardID = orderedSubProList.first()
				lastCardID = orderedSubProList.last()


				#pass response, page, and dict with var
				return render(response, 'Main/showProcess.html', {'enter_device_form':enter_device_form, 'addDevice':addDevice,  'partID':partID,'deletion':deletion,   'sensorSet':sensorSet, 'select_sensor_form':select_sensor_form,  'subLength':subLength,'processPart':processPart,'subProcessPartSet': subProcessPartSet, 'part_instance_form': part_instance_form, 'lastCardID':lastCardID, 'firstCardID':firstCardID, 'orderedSubProList':orderedSubProList, 'form':form, 'sensor_form':sensor_form, 'Pro' : pro, 'management':management, 'technician':technician,'supervisor': supervisor})
			#if user is a technician
			elif response.user.groups.filter(name='Technician').exists():
				orderedSubProList = pro.order_subprocess()
				firstCard = orderedSubProList.first()
				firstCardID = firstCard.id
				lastCard = orderedSubProList.last()
				lastCardID = lastCard.id
				technician = True
				#return response, page, var
				return render(response, 'Main/showProcess.html', {'partID':partID,'lastCardID':lastCardID, 'firstCardID':firstCardID, 'orderedSubProList':orderedSubProList, 'management':management, 'Pro' : pro, 'technician':technician, 'supervisor': supervisor, 'part_instance_form': part_instance_form})
		#if process doesnt belong to the users company redirect to home page
		return redirect('/')
	else:
		return redirect('/mylogout/')

def showProjects(response):
	"""View to show the Companies Projects page"""
	#setup
	#check user group
	if response.user.is_authenticated:
		form = CreateNewProject()
		management, supervisor = False,False
		if response.user.groups.filter(name='Management').exists():
			management = True
		if response.user.groups.filter(name='Supervisor').exists():
			supervisor = True
		delform = deleteProject(response.user.profile.user_company)
		if management or supervisor:
			if response.method == 'POST':
				#check permissions
				if response.user.has_perm('Main.edit_project'):
					#check response type
					if response.POST.get('addProject'):
						form = CreateNewProject(response.POST)
						if form.is_valid():
							#get cleaned project name
							n = form.cleaned_data['name']
							if response.POST.get('addProject'):
								#if project exists show error
								if response.user.profile.user_company.project_set.filter(project_name=n).exists():
									messages.error(response, 'Project already in list!')		
								#if project doesnt exist create one and save
								else:
									p = Project.objects.create(project_name=n)
									p.manual = form.cleaned_data['manual']
									p.save()
									response.user.profile.user_company.project_set.add(p)
					elif response.POST.get('deleteProject'):
						delform = deleteProject(response.user.profile.user_company, response.POST)
						if delform.is_valid():
							n = delform.cleaned_data['choice']
							#check response type
							if response.POST.get('deleteProject'):
								#check if project exists and delete
								try:
									if response.user.profile.user_company.project_set.get(project_name=n):
										p = response.user.profile.user_company.project_set.get(project_name=n)
										p.delete()
										messages.success(response, 'Project successfully deleted!')
								#show error if project doesnt exist
								except:
									messages.error(response, 'Project not in list!')
				else:
					#show permission error
					messages.error(response, 'You do not have permission for this action!')
			else:
				#return empty form
				form = CreateNewProject()

			#return response, page and dict of var
			return render(response, 'Main/showProjects.html', {'delform':delform,  'form' : form, 'management':management, 'supervisor':supervisor})
		#technician check
		elif response.user.groups.filter(name='Technician').exists():
			#return response, page and dict of var
			return render(response, 'Main/showProjects.html',{'management':management, 'supervisor':supervisor})
		else:
			#redirect to home page
			return redirect('/')
	else:
		return redirect('/mylogout/')

def showAllProcess(response, id):
	"""View to show all process's and allow the deletion of them"""
	#setup
	if response.user.is_authenticated:
		orderedProList = ''
		project = Project.objects.get(id=id)
		processPart = ''
		if project.manual:
			form = addManualProcess()
		else:
			form = addProcess(project)
		technician, management, supervisor = False, False, False
		material_form = AddMaterialForm()
		project_part_instance_form = ProjectPartInstanceForm(project)
		process_window_form = ProcessWindowForm()
		partInstance = ''

		if response.user.groups.filter(name='Management').exists():
			management = True
			group = 'Management'
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True
			group = 'Supervisor'
		else:
			group = 'Technician'

		const_form = ConstForm(group=group)
		#check project in user company:
		if project in response.user.profile.user_company.project_set.all():
			project.update_process_positions()

			if management or supervisor:
				if response.method == 'POST':
					if response.user.has_perm('Main.edit_process'):
						#check response type
						if response.POST.get('addProcess') or response.POST.get('deleteProcess'):
							if project.manual:
								form = addManualProcess(response.POST)
							else:
								form = addProcess(project, response.POST)
							if form.is_valid():
								#read in and clean process name/manual process name and project type
								if project.manual:
									reqProcessDirty = form.cleaned_data['manualName']
									reqProcess = Process.manual_process_dict[reqProcessDirty]
								else:
									reqProcess = form.cleaned_data['choice']
								#check response type
								if response.POST.get('addProcess'):
									#check if process exists and show error

									if project.process_set.filter(name=reqProcess).exists() or project.process_set.filter(manualName=reqProcess).exists():
										messages.error(response, 'Process already in list!')
									#if process doesnt exist create, save an display success
									else:
										if project.manual:
											pro = project.process_set.create(manualName = reqProcess)
											if reqProcess == "Form Preform":
												pro.subprocess_set.create(manualName= "Initialisation")
												pro.subprocess_set.create(manualName= "Lower Male Tool to create Preform", processCheck=True)
												pro.subprocess_set.create(manualName= "Final Inspection", processCheck=True)
												pro.viable= True
												pro.save()
										else:
											pro = project.process_set.create(name = reqProcess)
											if reqProcess == "Form Preform":
												pro.subprocess_set.create(name= "Initialisation")
												pro.subprocess_set.create(name= "Material Pressed", processCheck=True)
												pro.subprocess_set.create(name= "Final Inspection", processCheck=True)
												pro.viable= True
												pro.save()
										messages.success(response, 'Process sucessfully added!')
								#check response type
								elif response.POST.get('deleteProcess'):
									#if process exists delete it
									if project.process_set.filter(name=reqProcess).exists():
										p = project.process_set.get(name=reqProcess)
										p.delete()
										messages.success(response, 'Process sucessfully deleted!')
									elif project.process_set.filter(manualName=reqProcess).exists():
										p = project.process_set.get(manualName=reqProcess)
										p.delete()
										messages.success(response, 'Process sucessfully deleted!')
									#if process doesnt exist show error
									else:
										messages.error(response, 'Process does not exist!')
						#check response type
						elif response.POST.get('changeConst'):
							const_form = ConstForm(group, response.POST)
							if const_form.is_valid():
								#read in project const choice and its value
								choiceDirty = const_form.cleaned_data['choice']
								if management:
									choiceClean = Project.const_dict_mang[choiceDirty]
									value = const_form.cleaned_data['value']
								elif supervisor:
									choiceClean = Project.const_dict_super[choiceDirty]
									value = const_form.cleaned_data['value']
								else:
									messages.error(response, 'You do not have permission!')
									redirect('/')
								#set project model field with new value and save
								setattr(project, choiceClean, value)
								project.save()
								for process in project.process_set.all():
									for partInst in process.partinstance_set.all():
										part = Part.objects.get(part_id=partInst.instance_id)
										setattr(part, choiceClean, value)
										part.save()
										for processPart in part.processpart_set.all():
											for subProcessPart in processPart.subprocesspart_set.all():
												subProcessPart.updateSubCosts()
												subProcessPart.updateSubCO2()
											processPart.updateProcessCosts()
										part.updatePartCosts()
									for subProcess in process.subprocess_set.all():
										if subProcess.operator is not None:
											subProcess.updateSubCosts()
											subProcess.updateSubCO2()
										else:
											messages.error(response, 'not all sub process have an operator calcs incomplete please solve this and re enter')
									process.updateProcessCosts()
								project.updateProjectCosts()

						if response.POST.get('status'): #if user clicks on the Thumbs up button
							 processID = response.POST['status']
							 process = Process.objects.get(id=processID)

							 process.status=2
							 process.save()

						if response.POST.get('stopStatus'): #if user clicks the Stop button
							processID = response.POST['stopStatus']
							process = Process.objects.get(id=processID)

							process.status=3
							process.save()
						if response.POST.get('play'): #if User clicks the play button
							processID = response.POST['play']
							process = Process.objects.get(id=processID)

							process.status=1
							process.save()


						if response.POST.get('selectPartInstance'):
							project_part_instance_form = ProjectPartInstanceForm(project, response.POST)

							if project_part_instance_form.is_valid():
								partInstance = project_part_instance_form.cleaned_data['choice']
							else:
								messages.error(response, 'Some error please help')

						if response.POST.get('material'):
							material_form = AddMaterialForm(response.POST)

							if material_form.is_valid():

								if Material.objects.filter(name=material_form.cleaned_data['name']).exists():
									material = Material.objects.get(name=material_form.cleaned_data['name'])
									project.material = material_form.cleaned_data['name']
									project.priceKG = material.priceKG
									project.priceM2 = material.priceM2
									project.materialDensity = material.materialDensity
								else:
									material = Material.objects.create(name = material_form.cleaned_data['name'], priceKG = 10, priceM2 = 20, materialDensity = 2)
									project.material = material_form.cleaned_data['name']
									project.priceKG = material.priceKG
									project.priceM2 = material.priceM2
									project.materialDensity = material.materialDensity

								project.save()


						if response.POST.get('processWindow'):
							process_window_form = ProcessWindowForm(response.POST)
							if process_window_form.is_valid():
								value = process_window_form.cleaned_data['value']
								project.processWindow = value
								project.save()


						if response.POST.get('AutoFill'): #if user clicks the autofill data button, populate all processes/sub-process within that project with dummy data
							sName = ""
							messages.success(response, "Data successfully auto-filled!")
							project.superRate = 75
							project.techRate = 52
							project.powerRate = 0.23
							project.priceKG = 10
							project.nominalPartWidth = 1300
							project.nominalPartLength = 1900
							project.nominalPartThickness = 15
							project.widthTolerance = 0.02
							project.lengthTolerance = 0.02
							project.depthTolerance = 0.02
							project.nominalPartWeight = 3.75
							project.weightTolerance = 0.15
							project.nominalVolumeWrinkling = 3.50
							project.preformWrinklingTolerance = 2.5
							project.CO2PerPower = 0.233
							project.setUpCost = 2000

							count = 0
							project.save()
							company = response.user.profile.user_company
							newset = Profile.objects.all().filter(user_company=company)

							if not project.manual:
								for process in project.process_set.all():
									timeList = []
									for subpro in process.order_subprocess():

										if project.manual:
											sName = subpro.manualName
										else:
											sName = subpro.name

										subpro.operator = newset.get(username="Technician").username

										subpro.processCheck = False

										if sName == "Initialisation":
											subpro.operator = newset.get(username="Supervisor").username
											subpro.power = 6.3
											subpro.startPoint = True
											subpro.preTrimWeight = float(10)

											subpro.labourInput = 100
										elif sName == "Final Inspection":
											subpro.labourInput = 100
											subpro.preTrimWeight = 3.8
											subpro.postTrimWeight = 3.75
											subpro.operator = newset.get(username="Supervisor").username
											subpro.power = 6.8
											subpro.actualWeight = 3.71
											subpro.processCheck = True
											subpro.endPoint = True


										elif sName == "Material loaded in machine":
											subpro.save()
											subpro.power = 5.4

											subpro.labourInput = 50
											count += 1

										elif sName == "Platten at initial location":
											subpro.power = 5.4
											subpro.labourInput = 50
											count += 1

										elif sName == "Material and Tool Inside Press":
											subpro.power = 5.6

											subpro.labourInput = 50
											count += 1

										elif sName == "Material Pressed":
											subpro.power = 6.9
											subpro.processCheck = True
											subpro.labourInput = 50
											count += 1
										elif sName == "Material Released from Tool":
											subpro.power = 5.1

											subpro.labourInput = 50
											subpro.centrePosT = 1.5
											subpro.centrePosMT = 1.5
											subpro.tolerance = 0.25
											count += 1

										elif sName == "Machine Returns To Initial Locations":
											subpro.power = 5.3

											subpro.labourInput = 50
											count += 1

										elif sName == "Removal End effector actuated":
											subpro.power = 5.6

											subpro.verticalEffector = 34
											subpro.tolerancex2 = 2

											subpro.labourInput = 50
											count += 1

										elif sName == "Preform leaves Tool":
											subpro.power = 5.4
											subpro.labourInput = 50
											count += 1


										subpro.CO2 = float(subpro.power) * subpro.process.project.CO2PerPower

										if subpro.plyTask:
											subpro.batchSize = 6
										if subpro.blankTask:
											subpro.batchSize = 2
			
										if subpro.partTask:
											subpro.batchSize = 1
										subpro.status = 0
										subpro.labourInput = 100
										subpro.save()

										subpro.updateSubIntervals()
										subpro.process.updateProcessStartEnd()
										subpro.updateSubCosts()
										subpro.process.updateProcessCosts()
										subpro.save()
										project.updateProjectCosts()
							else:
								project.setUpCost = 0
								for process in project.process_set.all():
									process.operator=newset.get(username="Technician").username
									timeList = []
									for subpro in process.order_subprocess():


										subpro.operator = newset.get(username="Technician").username
										subpro.status = 0

										if subpro.manualName == "Initialisation":
											subpro.power = 6.3
											subpro.labourInput = 100
											subpro.jobStart = datetime.now().replace(microsecond=0)
											subpro.save()
											subpro.jobEnd = datetime.now().replace(microsecond=0)
											subpro.jobEnd = subpro.jobEnd + timedelta(minutes=5)
											timeList.append(subpro.jobEnd)
											subpro.startPoint = True

										elif subpro.manualName == "Material loaded in female tool":
											subpro.jobStart = timeList[count]
											subpro.save()
											subpro.jobEnd = subpro.jobStart + timedelta(seconds=600)
											timeList.append(subpro.jobEnd)
											subpro.power = 5.4

											subpro.labourInput = 50
											count += 1
										elif subpro.manualName == "Male Tool Lifted In Position":
											subpro.jobStart = timeList[count]
											subpro.save()
											subpro.jobEnd = subpro.jobStart + timedelta(seconds=600)
											timeList.append(subpro.jobEnd)
											subpro.power = 5.4

											subpro.labourInput = 50
											count += 1
										elif subpro.manualName == "Lower Male Tool to create Preform":
											subpro.jobStart = timeList[count]
											subpro.save()
											subpro.jobEnd = subpro.jobStart + timedelta(seconds=9000)
											timeList.append(subpro.jobEnd)
											subpro.power = 6.9

											subpro.labourInput = 15
											count += 1
										elif subpro.manualName == "Remove Male Tool":
											subpro.jobStart = timeList[count]
											subpro.save()
											subpro.jobEnd = subpro.jobStart + timedelta(seconds=1200)
											timeList.append(subpro.jobEnd)
											subpro.power = 5.1

											subpro.labourInput = 50
											count += 1

										elif subpro.manualName == "Release Preform from Female Tool":
											subpro.jobStart = timeList[count]
											subpro.save()
											subpro.jobEnd = subpro.jobStart + timedelta(seconds=2400)
											timeList.append(subpro.jobEnd)
											subpro.power = 5.4

											subpro.labourInput = 50
											count += 1

										elif subpro.manualName == "Final Inspection":
											subpro.jobStart = timeList[count]
											subpro.save()
											subpro.jobEnd = subpro.jobStart + timedelta(seconds=4800)
											subpro.power = 6.8
											subpro.preTrimWeight = 3.8
											subpro.postTrimWeight = 3.75
											timeList.append(subpro.jobEnd)
											subpro.operator = newset.get(username="Supervisor").username

											subpro.labourInput = 100
											count += 1
											subpro.endPoint = True



										subpro.save()
										subpro.updateSubIntervals()
										subpro.process.updateProcessStartEnd()
										subpro.updateSubCosts()
										subpro.process.updateProcessCosts()
										subpro.save()
										project.updateProjectCosts()


					else:
						#show permission error
						messages.error(response, 'You do not have permission for this action!')

				orderedProList = project.order_process_custom()
				lastProcess = orderedProList.last()
				return render(response, 'Main/showAllProcess.html', {'lastProcess':lastProcess, 'process_window_form':process_window_form, 'material_form':material_form, 'project_part_instance_form':project_part_instance_form, 'partInstance':partInstance, 'orderedProList':orderedProList, 'form': form, 'const_form':const_form, 'selected_project' : project, 'management':management, 'technician':technician, 'supervisor':supervisor})
			elif response.user.groups.filter(name='Technician').exists():
				technician=True
				orderedProList = project.order_process()
				return render(response, 'Main/showAllProcess.html', {'project_part_instance_form':project_part_instance_form, 'partInstance':partInstance, 'orderedProList':orderedProList, 'management':management,'selected_project':project, 'technician':technician, 'supervisor':supervisor})
		#redirect to home page
		return redirect('/')
	else:
		return redirect('/mylogout/')

def showSubProcess(response, id):
	"""View to show and allow the addition or deletion of components"""
	#setup
	#check sub pro belongs to user company
	if response.user.is_authenticated:
		sub_pro = SubProcess.objects.get(id=id)
		deletion,final = False, False
		name  = response.user.profile.user_company.company_name
		if sub_pro.name == "Final Inspection" or sub_pro.manualName == "Final Inspection":
			final = True
		sName = ""
		if sub_pro.process.project.manual:
			sName = sub_pro.manualName
		else:
			sName = sub_pro.name
		#setup
		weightForm = EnterPartWeight()
		input_form = addManualInfo()
		input_time_form = addManualTimeInfo()
		sensor_form = SensorForm(sub_pro.process)
		machine_form = MachineForm()
		prev_material_form = PreviousMaterialForm()
		imageForm = ImageUploadForm()
		fileForm = FileUploadForm()
		if sub_pro.process.project.manual:
			sub_master_form = SubMasterForm(sub_pro.manualName)
		else:
			sub_master_form = SubMasterForm(sub_pro.name)
		operator_form = operatorForm(name)
		management, supervisor = False, False

		if deletion == False:
			sensorSet = Sensor.objects.none()
			select_sensor_form = SelectSensorForm(sensorSet)


		if response.user.groups.filter(name='Management').exists():
			management = True
		if response.user.groups.filter(name='Supervisor').exists():
			supervisor = True
		if sub_pro.process.project.company == response.user.profile.user_company:
			if management or supervisor:
				if response.method == 'POST':
					#permission check
					if response.user.has_perm('Main.edit_sub_process'):
						#check response type
						if sub_pro.partInstance != None or sub_pro.startPoint:
							if response.POST.get('addPreCost'):
								prev_material_form = PreviousMaterialForm(response.POST)
								if prev_material_form.is_valid():
									sub_pro.materialWastageCost = prev_material_form.cleaned_data['value']
									sub_pro.save()
							if response.POST.get('addManual'):
								if User.objects.filter(username=sub_pro.operator).exists():
									input_form = addManualInfo(response.POST)
									if input_form.is_valid():
										#read and clean input
										reqInputDirty = input_form.cleaned_data['task']
										reqInput = SubProcess.manual_input_dict[reqInputDirty]
										inputValue = input_form.cleaned_data['value']

										#save to model
										setattr(sub_pro,reqInput,inputValue)
										sub_pro.save()
										messages.success(response, "Value Successfully changed!")

										#update parent process values
										if reqInputDirty == 'BAT':
											sub_pro.process.updateBatchSize()

										elif reqInputDirty == 'SCR':
											sub_pro.process.updateScrapRate()

										elif reqInputDirty == 'LAB':
											sub_pro.process.updateLabourInput()

										elif reqInputDirty == 'POR':
											sub_pro.updateSubCO2()
											sub_pro.process.updatePowerCon()

										#update intervals and assign interface or process time  depending on processCheck field
										sub_pro.updateSubIntervals()
										#sets start and end times for process (min and max of sub process's)
										sub_pro.process.updateProcessStartEnd()

										#update costs
										sub_pro.updateSubCosts()
										sub_pro.process.updateProcessCosts()
									else:
										messages.error(response,"Invalid input!")
								else:
									messages.error(response, 'Sub Process needs operator')
						#check response type
							if response.POST.get('addManualTime'):
								if User.objects.filter(username=sub_pro.operator).exists():
									input_time_form = addManualTimeInfo(response.POST)
									if input_time_form.is_valid():
										#read and clean task and value
										reqInputDirty = input_time_form.cleaned_data['task']
										reqInput = sub_pro.manual_input_time_dict[reqInputDirty]
										inputValue = datetime.now().replace(microsecond=0)
										valid = False

										#set to model and save
										if sub_pro.jobStart == None or sub_pro.jobEnd == None:
											valid = True
										else:
											if inputValue.timestamp() - sub_pro.jobStart.timestamp() < 0:
												messages.error(response, "You cannot end the job before Job Start!")
												sub_pro.jobStart = None
												sub_pro.jobEnd = None
												sub_pro.save()
												valid=False

											if sub_pro.jobEnd != None:
												valid = True

										if valid == True:
											setattr(sub_pro,reqInput,inputValue)
											#save changes
											sub_pro.save()

											#update intervals and assign interface or process time  depending on processCheck field
											sub_pro.updateSubIntervals()

											#sets start and end times for process (min and max of sub process's)
											sub_pro.process.updateProcessStartEnd()

											#update costs
											sub_pro.updateSubCosts()
											sub_pro.process.updateProcessCosts()

											if final == True:
												return redirect('/finalInspection'+str(sub_pro.id))
											else:
												return redirect('/c'+str(sub_pro.id))
								else:
									messages.error(response, 'Sub Process needs operator')
						else:
							messages.error(response,"Warning: This Sub-Process is not active!")
							#check to stop sensorform.is_valid displaying error on other form
						if (response.POST.get('addSensor') or response.POST.get('deleteSensor')):
							sensor_form = SensorForm(sub_pro.process, response.POST)
							if sensor_form.is_valid():
								#read in and clean sensor name
								reqSensor = sensor_form.cleaned_data['choice']

								#check response type
								if response.POST.get('addSensor'):
									#check if sensor exists and show error

									s = Sensor.objects.get(name=reqSensor.name, modelID = reqSensor.modelID)

									if not s in sub_pro.sensor_set.all():
										sub_pro.sensor_set.add(s)
										messages.success(response, 'Sensor successfully added!')
									else:
										messages.error(response, 'Sensor already exists!')
								#check response type
								elif response.POST.get('deleteSensor'):
									#if sensor exists delete
									try:
										sensor = sub_pro.sensor_set.filter(name=reqSensor.name).first()

										if len(sub_pro.sensor_set.filter(name=reqSensor.name)) > 1:
											messages.error(response, "Select a Sensor to delete!")
											sensorSet = sub_pro.sensor_set.filter(name=reqSensor.name)
											deletion = True
											select_sensor_form = SelectSensorForm(sensorSet, response.POST)
										else:
											sensor.delete()

											messages.success(response, 'Sensor successfully deleted!')
									except:
										messages.error(response,"Sensor does not exist!")
								#if sensor doesnt exist show error

										#messages.error(response, 'Sensor does not exist!')

						#check to stop machineform.is_valid displaying error on other form
						if (response.POST.get('addMachine') or response.POST.get('delMachine')):
							machine_form = MachineForm(response.POST)
							if machine_form.is_valid():
								#read in machine name
								reqMachineDirty = machine_form.cleaned_data['name']
								reqMachine = Machine.machine_choices_dict[reqMachineDirty]
								process = sub_pro.process
								#check response type
								if response.POST.get('addMachine'):
									if Machine.objects.filter(name=reqMachine).exists():
									#if machine exists show error
										if sub_pro.plyCutter != None and sub_pro.plyCutter.name == reqMachine:
											#error2 = "Ply cutter already exists! \n"
											messages.error(response, 'Ply Cutter has already been assigned!')
										elif sub_pro.sortPickAndPlace != None and sub_pro.sortPickAndPlace.name == reqMachine:
											messages.error(response, "Pick and Place (sorts) already exists!")
										elif sub_pro.blanksPickAndPlace != None and sub_pro.blanksPickAndPlace.name == reqMachine:
											messages.error(response, "Pick and Place (blanks) already exists!")
										elif sub_pro.preformCell != None and sub_pro.preformCell.name == reqMachine:
											messages.error(response,"Preforming Cell already exists!")
										else:
											if(reqMachine=="Ply Cutter"):
												setattr(sub_pro, 'plyCutter', Machine.objects.get(name=reqMachine))
											elif(reqMachine == "Pick and Place (sort)"):
												setattr(sub_pro, 'sortPickAndPlace', Machine.objects.get(name=reqMachine))
											elif(reqMachine == "Pick and Place (blanks)"):
												setattr(sub_pro, 'blanksPickAndPlace', Machine.objects.get(name=reqMachine))
											elif(reqMachine == "Preforming Cell"):
												setattr(sub_pro, 'preformCell', Machine.objects.get(name=reqMachine))
											sub_pro.save()
											messages.success(response, 'Machine successfully added!')

									else:

									#if machine doesnt exist create and show success


										Machine.objects.create(name=reqMachine)

										if(reqMachine=="Ply Cutter"):
											setattr(sub_pro, 'plyCutter', Machine.objects.get(name=reqMachine))
										elif(reqMachine == "Pick and Place (sort)"):
											setattr(sub_pro, 'sortPickAndPlace', Machine.objects.get(name=reqMachine))
										elif(reqMachine == "Pick and Place (blanks)"):
											setattr(sub_pro, 'blanksPickAndPlace', Machine.objects.get(name=reqMachine))
										elif(reqMachine == "Preforming Cell"):
											setattr(sub_pro, 'preformCell', Machine.objects.get(name=reqMachine))
										sub_pro.save()

										messages.success(response, 'Machine successfully added!')
								#check response type
								elif response.POST.get('delMachine'):

									#if machine exists delete
									try:
										Machine.objects.get(name=reqMachine).delete()
										messages.success(response, 'Machine successfully deleted!')
										return redirect('/'+str(process.id))
									except:
										messages.error(response,"Machine does not exist!")
						if response.POST.get('ChangeOP'):

							operator_form = operatorForm(name, response.POST)
							choiceDirty=  ""
							if operator_form.is_valid():
								choice=operator_form.cleaned_data['choice']

							setattr(sub_pro, 'operator', choice.user.username)
							sub_pro.save()

							#update intervals and assign interface or process time  depending on processCheck field
							sub_pro.updateSubIntervals()

							#sets start and end times for process (min and max of sub process's)
							sub_pro.process.updateProcessStartEnd()

							#update costs
							sub_pro.updateSubCosts()
							sub_pro.process.updateProcessCosts()

							if final == True:
								return redirect('/finalInspection'+str(sub_pro.id))
							else:
								return redirect('/c'+str(sub_pro.id))

						if response.POST.get('deleteSelection'):

							sensor = Sensor.objects.get(modelID=response.POST['choice'])

							sensor.delete()
							messages.success(response,"Sensor successfully deleted!")


						if response.POST.get('ChangeSubMaster'): #used to change specific subprocess fields within components page
							if sub_pro.process.project.manual:
								name = sub_pro.manualName
							else:
								name = sub_pro.name
							sub_master_form = SubMasterForm(name, response.POST)
							if sub_master_form.is_valid():
								choiceDirty = sub_master_form.cleaned_data['choice']
								if sub_pro.manualName == "Material Pressed Inside Press":
									choiceClean = SubProcess.material_in_press_dict[choiceDirty]
								elif sub_pro.manualName == "Material Pressed":
									choiceClean = SubProcess.material_pressed_dict[choiceDirty]
								elif sub_pro.manualName == "Removal End effector actuated":
									choiceClean = SubProcess.removal_effector_dict[choiceDirty]
								elif sub_pro.manualName == "Final Inspection" or sub_pro.name == "Final Inspection":
									choiceClean = SubProcess.trimming_dict[choiceDirty]

								value = sub_master_form.cleaned_data['value']

								setattr(sub_pro, choiceClean, value)
								sub_pro.save()
								sub_pro.updateSubCosts()
								sub_pro.process.updateProcessCosts()

								if final == True:
									return redirect('/finalInspection'+str(sub_pro.id))
								else:
									return redirect('/c'+str(sub_pro.id))

						#check to stop machineform.is_valid displaying error on other form
						if response.POST.get('addWeight'):
							weightForm = EnterPartWeight(response.POST)
							if weightForm.is_valid():
								weight = weightForm.cleaned_data['value']
								sub_pro.preTrimWeight = weight
								sub_pro.save()
								scale = sub_pro.sensor_set.get(name='Scale')
								scale.preTrimWeight = weight
								scale.save()

						if response.POST.get('addFile'):
							file_upload_view(response, sub_pro)

						if response.POST.get('addImage'):
							image_upload_view(response, sub_pro)



					else:
						#show permission error
						messages.error(response, 'You do not have permission for this action!')
				if final == True:

					return render(response, 'Main/finalInspection.html', {'deletion':deletion, 'imageForm':imageForm, 'fileForm':fileForm, 'select_sensor_form':select_sensor_form,  'sensorSet':sensorSet,'sub_pro':sub_pro, 'input_form':input_form, 'input_time_form':input_time_form, 'sensor_form':sensor_form, 'machine_form':machine_form, 'weightForm' : weightForm, 'management':management, 'supervisor':supervisor, 'sub_master_form': sub_master_form, 'operator_form': operator_form})
				else:
					return render(response, 'Main/components.html', {'deletion':deletion,  'select_sensor_form':select_sensor_form,  'sensorSet':sensorSet,  'sub_pro':sub_pro,'input_form':input_form, 'input_time_form':input_time_form, 'sensor_form':sensor_form, 'machine_form':machine_form, 'weightForm' : weightForm, 'management':management, 'supervisor':supervisor, 'sub_master_form': sub_master_form, 'operator_form': operator_form})
			elif response.user.groups.filter(name='Technician').exists():
				return render(response, 'Main/components.html', {'sub_pro':sub_pro})
			else:
				#redirect to home page
				redirect('/')
		#if sub process isnt in user company group redirect to home
		return HttpResponseRedirect('/')
	else:
		return redirect('/mylogout/')



def showEnvironSensors(response, id):
	if response.user.is_authenticated:
		management, supervisor = False, False,
		process = Process.objects.get(id=id)
		time_form = ChangeGraphTime()
		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True
		if process.project in response.user.profile.user_company.project_set.all():
			if management or supervisor:
				if response.POST.get('changeVOCGraph'):
					time_form = ChangeGraphTime(response.POST)
					if time_form.is_valid():
						if process.sensor_set.all().filter(name="VOC Sensor").exists():
							sensor = process.sensor_set.all().get(name="VOC Sensor")
							sensor.averageTime = response.POST['time']
							sensor.save()

				if response.POST.get('changeTempGraph'):
					time_form = ChangeGraphTime(response.POST)
					if time_form.is_valid():
						if process.sensor_set.all().filter(name="Thermocouple").exists():
							sensor = process.sensor_set.all().get(name="Thermocouple")
							sensor.averageTime = response.POST['time']
							sensor.save()

				if response.POST.get('changeHumidityGraph'):
					time_form = ChangeGraphTime(response.POST)
					if time_form.is_valid():
						if process.sensor_set.all().filter(name="Humidity Sensor").exists():
							sensor = process.sensor_set.all().get(name="Humidity Sensor")
							sensor.averageTime = response.POST['time']
							sensor.save()

				if response.POST.get('changeDustGraph'):
					time_form = ChangeGraphTime(response.POST)
					if time_form.is_valid():
						if process.sensor_set.all().filter(name="Dust Sensor").exists():
							sensor = process.sensor_set.all().get(name="Dust Sensor")
							sensor.averageTime = response.POST['time']
							sensor.save()

				return render(response, 'Main/showEnvironSensors.html', {'time_form':time_form,'management':management, 'supervisor':supervisor, 'process':process})
			else:
				#redirect to the home page
				return redirect('/')
		else:
			#redirect to the home page
			return redirect('/')
	else:
		return redirect('/mylogout/')

def environGraph(response, id):
	if response.user.is_authenticated:
		Proc, management, supervisor = Process.objects.get(id=id), False, False
		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True

		if Proc.project in response.user.profile.user_company.project_set.all():
			if management or supervisor:

				#default variables
				requiredField, labels, tempData, tempLabels, vocData, vocLabels, dustData, dustLabels, humidityData, humidityLabels,  = '', [], [],[],[],[],[],[],[], []
				data = {'Temp':0, 'VOC':0, 'Dust': 0, 'Humidity':0}
				minV = {'Temp':-5, 'VOC':-10, 'Dust': 2, 'Humidity':2} #min lines for each graph
				maxV = {'Temp':50, 'VOC':15, 'Dust': 25, 'Humidity':20} #max lines for each graph

				for sensor in Proc.sensor_set.all():
					avgList = []
					average = 0
					if sensor.name == "Thermocouple":
						tempLabels.append(sensor.name + "-" +sensor.modelID) #add sensor name and corresponding model ID
						tempLabels.append("Average Temperature Over The last "+ str(sensor.averageTime)+" Seconds")
						sensor.sensortime_set.create(temp = random.randint(0,40), time=datetime.now())
						if len(sensor.sensortime_set.all()) >= sensor.averageTime:
							sensor.sensortime_set.first().delete()
						if len(sensor.sensortime_set.all()) != 0: #if sensor is receiving data (sensortime data)
							tempData.append(sensor.sensortime_set.all().last().temp) #append temperature attribute from sensortime attribute
							for each in sensor.sensortime_set.all():
								avgList.append(each.temp)

							average = sum(avgList) / len(sensor.sensortime_set.all())
							tempData.append(average)
							#-Un-comment this to see cool graph lines-#
							#tempData.append(random.randint(0,40))
						else:
							tempData.append(0)

					if sensor.name == "VOC Sensor":
						vocLabels.append(sensor.name + "-" + sensor.modelID)#add sensor name and corresponding model ID
						vocLabels.append("Average VOC Over The last "+ str(sensor.averageTime)+" Seconds")
						sensor.sensortime_set.create(VOC = random.randint(0,10), time=datetime.now())
						if len(sensor.sensortime_set.all()) >= sensor.averageTime:
							sensor.sensortime_set.first().delete()
						if len(sensor.sensortime_set.all()) != 0:#if sensor is receiving data (sensortime data)
							vocData.append(sensor.sensortime_set.all().last().VOC)#append VOC attribute from sensortime attribute
							for each in sensor.sensortime_set.all():
								avgList.append(each.VOC)

							average = sum(avgList) / len(sensor.sensortime_set.all())
							vocData.append(average)
							#vocData.append(random.randint(0, 10))
						else:
							vocData.append(0)

					if sensor.name == "Humidity Sensor":
						humidityLabels.append(sensor.name + "-" + sensor.modelID)#add sensor name and corresponding model ID
						humidityLabels.append("Average Humidity Over The last "+ str(sensor.averageTime)+" Seconds")
						sensor.sensortime_set.create(humidity = random.randint(5,15), time=datetime.now())
						if len(sensor.sensortime_set.all()) >= sensor.averageTime:
							sensor.sensortime_set.first().delete()
						if len(sensor.sensortime_set.all()) != 0:#if sensor is receiving data (sensortime data)
							humidityData.append(sensor.sensortime_set.all().last().humidity)#append humidity attribute from sensortime attribute
							for each in sensor.sensortime_set.all():
								avgList.append(each.humidity)

							average = sum(avgList) / len(sensor.sensortime_set.all())
							humidityData.append(average)
							#humidityData.append(random.randint(5,15))
						else:
							humidityData.append(0)

					if sensor.name == "Dust Sensor":
						dustLabels.append(sensor.name + "-" + sensor.modelID)#add sensor name and corresponding model ID
						dustLabels.append("Average Dust Over The last "+ str(sensor.averageTime)+" Seconds")
						sensor.sensortime_set.create(dust = random.randint(5,20), time=datetime.now())
						if len(sensor.sensortime_set.all()) >= sensor.averageTime:
							sensor.sensortime_set.first().delete()
						if len(sensor.sensortime_set.all()) != 0:#if sensor is receiving data (sensortime data)
							dustData.append(sensor.sensortime_set.all().last().dust)#append dust attribute from sensortime attribute
							for each in sensor.sensortime_set.all():
								avgList.append(each.dust)

							average = sum(avgList) / len(sensor.sensortime_set.all())
							dustData.append(average)
							#dustData.append(random.randint(5,20))
						else:
							dustData.append(0)

				return JsonResponse(data={'data':data, 'tempData':tempData, 'tempLabels':tempLabels, 'vocData':vocData, 'vocLabels':vocLabels, 'dustData':dustData, 'dustLabels':dustLabels, 'humidityData':humidityData, 'humidityLabels':humidityLabels, 'labels':labels, 'maxV':maxV, 'minV':minV})
	else:
		return redirect('/mylogout/')


def popUp(response, id):
	#setup
	if response.user.is_authenticated:
		subpro = SubProcess.objects.get(id=id)
		initialTempTime, initialTempData, initialPressureData, initialPressureTime, cleanPressureData, cleanTempData = [],[],[],[],[],[]
		temperatureData, pressureData = {},{}
		tempReached, pressureReached, jobEnd = False, False, False
		thermo, pressSensor,  temp = None, None, None
		tempReachedTime, pressureReachedTime, firstPressure = "00:00:00", "00:00:00", "00:00:00"
		total, tMaxTemp, tMinTemp, pMaxPressure, pMinPressure, refreshRate, seconds,cleanedTempReachedTime, cleanedPressureReachedTime =  0, 0, 10, 10, 0, 1500, 0, 0,0
		ellipseSupport, ellipseSupportPressure,  = "", ""
		time = ""
		currentTime = datetime.now()
		time = currentTime.strftime("%H:%M:%S")

		if subpro.sensor_set.filter(name="Thermocouple").exists(): #initialise thermocouple
			thermo = subpro.sensor_set.get(name="Thermocouple")
			tempReached = thermo.temperatureReached
			tempReachedTime = thermo.tempReachedTime
			tMaxTemp = thermo.maxTemp
			tMinTemp = thermo.minTemp
		if subpro.sensor_set.filter(name="Pressure Sensor").exists(): #initialise pressure sensor
			pressSensor = subpro.sensor_set.get(name="Pressure Sensor")
			pressureReached = pressSensor.pressureReached
			pMaxPressure= pressSensor.maxPressure
			pMinPressure = pressSensor.minPressure
			pressureReachedTime = pressSensor.pressureReachedTime

		if subpro.jobEnd != None and subpro.jobStart != None:
			jobEnd = True
		if subpro.jobEnd == None and subpro.jobStart != None: #if task is ongoing

			if thermo != None: #if thermocouple exists
				thermo.sensortime_set.create(time=datetime.now(), temp=random.randint(3,5)) #create sensortime data

			if pressSensor != None: #if pressure sensor exists
				pressSensor.sensortime_set.create(time=datetime.now(), pressure=random.randint(6,8))

			if tempReached == True: # if temperature reached set value
				thermo.tempReachedTime = time
				temp = currentTime + timedelta(seconds=3)
				ellipseSupport = temp.strftime("%H:%M:%S")
				thermo.temperatureReached = False
				tempReached = True
				thermo.save()
				tempReachedTime = thermo.tempReachedTime


			if pressureReached == True: # if pressure reached set value
				pressSensor.pressureReachedTime = time
				pressSensor.pressureReached = False
				temp = currentTime + timedelta(seconds=3)
				ellipseSupportPressure = temp.strftime("%H:%M:%S")
				pressureReached = True
				pressureReachedTime = pressSensor.pressureReachedTime
				pressSensor.save()


			if thermo != None:
				for each in thermo.sensortime_set.all():
					currentTime = each.time
					time = currentTime.strftime("%H:%M:%S")
					initialTempData.append({'x':time, 'y':each.temp})

				if thermo.tempReachedTime != None:
					r = datetime.strptime(thermo.tempReachedTime, '%H:%M:%S')
					temp = r + timedelta(seconds=3)
					ellipseSupport=temp.strftime("%H:%M:%S")

			if pressSensor!= None:
				for each in pressSensor.sensortime_set.all():
					currentTime = each.time
					time = currentTime.strftime("%H:%M:%S")
					initialPressureData.append({'x':time, 'y':each.pressure})

				if pressSensor.pressureReachedTime != None:
					r = datetime.strptime(pressSensor.pressureReachedTime, '%H:%M:%S')
					temp = r + timedelta(seconds=3)
					ellipseSupportPressure=temp.strftime("%H:%M:%S")

			currentTime = datetime.now()
			time = currentTime.strftime("%H:%M:%S")


		if subpro.jobStart != None and subpro.jobEnd != None: # if task is finished
			if thermo != None:
				for each in thermo.sensortime_set.all():
					currentTime = each.time


					time = currentTime.strftime("%H:%M:%S")
					initialTempData.append({'x':time, 'y':each.temp})


				if len(initialTempData) > 0:
					firstTemp = initialTempData[0]['x']
					lastTemp = initialTempData[-1]['x']

					k = datetime.strptime(firstTemp, '%H:%M:%S')
					z = datetime.strptime(lastTemp, '%H:%M:%S')

					dif = z - k


					reachedDif = z-datetime.strptime(thermo.tempReachedTime, '%H:%M:%S')

					cleanedTempReachedTime=0


					total = int(dif.total_seconds())
					cleanedTempReachedTime = total - int(reachedDif.total_seconds())
					newList = list(range(0,int(total)))



					initialTempData = []
					count = 0
					for each in thermo.sensortime_set.all():
						if count >= len(newList):
							break
						else:
							initialTempData.append({'x': str(newList[count]), 'y': each.temp})
							count+=1



			if pressSensor!= None:
				for each in pressSensor.sensortime_set.all():
					currentTime = each.time
					time = currentTime.strftime("%H:%M:%S")
					initialPressureData.append({'x':time, 'y':each.pressure})

				if len(initialPressureData) > 0:
					firstPressure = initialPressureData[0]['x']
					lastPressure = initialPressureData[-1]['x']

					k = datetime.strptime(firstPressure, '%H:%M:%S')
					z = datetime.strptime(lastPressure, '%H:%M:%S')

					dif = z - k

					reachedDif = z-datetime.strptime(pressSensor.pressureReachedTime, '%H:%M:%S')

					cleanedPressureReachedTime = 0

					total = int(dif.total_seconds())
					cleanedPressureReachedTime = total - int(reachedDif.total_seconds())
					newList = list(range(0,int(total)))



					initialPressureData = []
					count = 0
					for each in pressSensor.sensortime_set.all():
						if count >= len(newList):
							break
						else:
							initialPressureData.append({'x': str(newList[count]), 'y': each.pressure})

							count+=1



		if subpro.jobStart != None and subpro.jobEnd == None:

			management = False
			supervisor = False
			if response.user.groups.filter(name='Management').exists():
				management = True
			elif response.user.groups.filter(name='Supervisor').exists():
				supervisor = True


			if subpro.process.project in response.user.profile.user_company.project_set.all():
				if management or supervisor:
					if thermo != None:
						if len(thermo.sensortime_set.all()) == 0:
							temperatureData.update({str(id): 0, 'maxTemp':thermo.maxTemp, 'minTemp':thermo.minTemp})
						else:
							temperatureData.update({str(id): thermo.sensortime_set.all().last().temp, 'time':time , 'maxTemp':thermo.maxTemp, 'minTemp':thermo.minTemp})#if thermocouple exists within sub process, display popup real-time temperature graph
					if pressSensor != None:

						if len(pressSensor.sensortime_set.all()) == 0:
							pressureData.update({str(id): 0, 'maxPressure':pressSensor .maxPressure, 'minPressure':pressSensor .minPressure})
						else:
							pressureData.update({str(id): pressSensor.sensortime_set.all().last().pressure, 'time':time,  'maxPressure':pressSensor.maxPressure, 'minPressure':pressSensor.minPressure})#if pressure sensor exists within sub process, display popup real-time pressure graph

					return JsonResponse(data={'refreshRate':refreshRate, 'ellipseSupportPressure':ellipseSupportPressure ,'ellipseSupport' : ellipseSupport,'jobEnd':jobEnd,'pressureReachedTime': pressureReachedTime, 'pressureReached':pressureReached, 'tempReachedTime':tempReachedTime ,'tempReached':tempReached, 'pressureReached': pressureReached,'initialTempData':initialTempData , 'initialPressureData':initialPressureData,'temperatureData':temperatureData, 'pressureData': pressureData,})
		elif subpro.jobStart != None and subpro.jobEnd != None:
			refreshRate = 100000000

			#pressureReachedTime = middle['x']
			#tempReachedTime = middle['x']

			temperatureData.update({str(id): 0, 'maxTemp':tMaxTemp, 'minTemp':tMinTemp})
			pressureData.update({str(id): 0, 'maxPressure':pMaxPressure ,'minPressure':pMinPressure})
			return JsonResponse(data={ 'ellipseSupportPressure':ellipseSupportPressure ,'ellipseSupport' : ellipseSupport, 'cleanedPressureReachedTime':cleanedPressureReachedTime,  'cleanedTempReachedTime': cleanedTempReachedTime,'jobEnd':jobEnd,'refreshRate':refreshRate,'firstPressure':firstPressure, 'total':total,   'pressureReachedTime': pressureReachedTime, 'tempReachedTime': tempReachedTime, 'pressureReached':pressureReached, 'tempReached':tempReached, 'pressureReached': pressureReached, 'initialTempData':initialTempData , 'initialPressureData':initialPressureData, 'temperatureData':temperatureData, 'pressureData': pressureData})
		elif subpro.jobStart == None and subpro.jobEnd == None:
			refreshRate = 10000
			temperatureData.update({str(id): 0, 'maxTemp':tMaxTemp, 'minTemp':tMinTemp})
			pressureData.update({str(id): 0, 'maxPressure':pMaxPressure ,'minPressure':pMinPressure})
			return JsonResponse(data={ 'ellipseSupportPressure':ellipseSupportPressure ,'ellipseSupport' : ellipseSupport,'jobEnd':jobEnd,'refreshRate':refreshRate,'firstPressure':firstPressure, 'total':total,   'pressureReachedTime': pressureReachedTime, 'tempReachedTime': tempReachedTime, 'pressureReached':pressureReached, 'tempReached':tempReached, 'pressureReached': pressureReached,'initialTempData':initialTempData , 'initialPressureData':initialPressureData, 'temperatureData':temperatureData, 'pressureData': pressureData})
	else:
		return redirect('/mylogout/')

def machineHealthShow(response, id):
	process = Process.objects.get(id=id)
	if response.user.is_authenticated:
		management = False
		supervisor = False
		time_form = ChangeGraphTime()
		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True
		if process.project in response.user.profile.user_company.project_set.all():
			if management or supervisor:
				if response.POST.get('changeEnergyGraph'):
					time_form = ChangeGraphTime(response.POST)
					if time_form.is_valid():
						if process.sensor_set.all().filter(name="Power Clamp (Big Oven)").exists():
							ovenSensor = process.sensor_set.all().get(name="Power Clamp (Big Oven)")

						if process.sensor_set.all().filter(name="Power Clamp (Big Cabinet)").exists():
							cabinetSensor = process.sensor_set.all().get(name="Power Clamp (Big Cabinet)")

						if process.sensor_set.all().filter(name="Power Clamp (Kuka Robot)").exists():
							kukaSensor = process.sensor_set.all().get(name="Power Clamp (Kuka Robot)")

						if process.sensor_set.all().filter(name="Power Clamp (CNC Router)").exists():
							cncSensor = process.sensor_set.all().get(name="Power Clamp (CNC Router)")

						ovenSensor.averageEnergyTime = response.POST['time']
						cabinetSensor.averageEnergyTime = response.POST['time']
						kukaSensor.averageEnergyTime = response.POST['time']
						cncSensor.averageEnergyTime = response.POST['time']

						ovenSensor.save()
						cabinetSensor.save()
						kukaSensor.save()
						cncSensor.save()
				if response.POST.get('changeStrainGraph'):
					time_form = ChangeGraphTime(response.POST)
					if time_form.is_valid():
						if process.sensor_set.all().filter(name="Strain Gauge").exists():
							sensor = process.sensor_set.all().get(name="Strain Gauge")
							sensor.averageTime = response.POST['time']
							sensor.save()
				if response.POST.get('changeNoiseGraph'):
					time_form = ChangeGraphTime(response.POST)
					if time_form.is_valid():
						if process.sensor_set.all().filter(name="Microphone").exists():
							sensor = process.sensor_set.all().get(name="Microphone")
							sensor.averageTime = response.POST['time']
							sensor.save()
				if response.POST.get('changeAccelerationGraph'):
					time_form = ChangeGraphTime(response.POST)
					if time_form.is_valid():
						if process.sensor_set.all().filter(name="Accelerometer").exists():
							sensor = process.sensor_set.all().get(name="Accelerometer")
							sensor.averageTime = response.POST['time']
							sensor.save()

				#open Machine Health Page
				return render(response, 'Main/showMachineHealth.html', {'time_form':time_form, 'management':management, 'supervisor':supervisor, 'process':process})
		else:
			#redirect to the home page
			return redirect('/')
	else:
		return redirect('/mylogout/')



def machineHealth(response, id):
	if response.user.is_authenticated:

		management = False
		supervisor = False
		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True

		Proc = Process.objects.get(id=id)
		if Proc.project in response.user.profile.user_company.project_set.all():
			if management or supervisor:

				#setup
				energyData, energyLabels, microphoneData, microphoneLabels, torqueData, torqueLabels, accelerationData, accelerationLabels, labels = [],[],[],[],[],[],[],[],[]
				maxV, minV = [15,15,15],[-5,-5,-5] #default min and max lines
				bigCabinetPower, bigOvenPower, kukaRobotPower, cncPower = 0,0,0,0
				kWh = False
				bigOven, bigCabinet, kuka, CNC = {},{},{},{}

				#request call to shelly API for all power clamp data
				s = requests.post('https://shelly-43-eu.shelly.cloud/device/all_status', data={'auth_key':os.environ.get('AUTH_KEY')})
				receivedData = s.json() #converting received response into json structure
				print(receivedData)
				if Proc.sensor_set.all().filter(name = "Power Clamp (Big Oven)").exists():
					try:
						bigOven = receivedData['data']['devices_status'][Proc.sensor_set.all().get(name="Power Clamp (Big Oven)").modelID] #getting big oven device data
					except KeyError:
						bigOven['total_power'] = 0
				else:
					bigOven['total_power'] = 0

				if Proc.sensor_set.all().filter(name = "Power Clamp (Big Cabinet)").exists():
					try:
						bigCabinet = receivedData['data']['devices_status'][Proc.sensor_set.all().get(name="Power Clamp (Big Cabinet)").modelID] #getting big cabinet device data
					except KeyError:
						bigCabinet['total_power'] = 0
				else:
					bigCabinet['total_power'] = 0

				if Proc.sensor_set.all().filter(name = "Power Clamp (Kuka Robot)").exists():
					try:
						kuka = receivedData['data']['devices_status'][Proc.sensor_set.all().get(name="Power Clamp (Kuka Robot)").modelID] #getting kuka robot device data
					except KeyError:
						kuka['total_power'] = 0
				else:
					kuka['total_power'] = 0

				if Proc.sensor_set.all().filter(name = "Power Clamp (CNC Router)").exists():
					try:
						CNC = receivedData['data']['devices_status'][Proc.sensor_set.all().get(name="Power Clamp (CNC Router)").modelID]
					except KeyError:
						CNC['total_power'] = 0
				else:
					CNC['total_power'] = 0

				if bigOven['total_power'] > 1000: #if watts per hour exceeds 1000, set measurement to kWh instead
					kWh = True
				else:
					kWh = True

				#assigning power values
				bigOvenPower = bigOven['total_power']
				bigCabinetPower = bigCabinet['total_power']
				kukaRobotPower = kuka['total_power']
				cncPower = CNC['total_power']

				print(bigOvenPower)

				energySensors = []

				if Proc.sensor_set.all().filter(name="Power Clamp (Big Oven)").exists():
					ovenSensor = Proc.sensor_set.all().get(name="Power Clamp (Big Oven)")
					ovenSensor.sensortime_set.create(energy=bigOvenPower, time = datetime.now())
					if len(ovenSensor.sensortime_set.all()) >= ovenSensor.averageEnergyTime:
						ovenSensor.sensortime_set.first().delete()

					energySensors.append(ovenSensor)

				if Proc.sensor_set.all().filter(name="Power Clamp (Big Cabinet)").exists():
					cabinetSensor = Proc.sensor_set.all().get(name="Power Clamp (Big Cabinet)")
					cabinetSensor.sensortime_set.create(energy=bigCabinetPower, time = datetime.now())
					if len(cabinetSensor.sensortime_set.all()) >= cabinetSensor.averageEnergyTime:
						cabinetSensor.sensortime_set.first().delete()

					energySensors.append(cabinetSensor)

				if Proc.sensor_set.all().filter(name="Power Clamp (Kuka Robot)").exists():
					kukaSensor = Proc.sensor_set.all().get(name="Power Clamp (Kuka Robot)")
					kukaSensor.sensortime_set.create(energy=kukaRobotPower, time = datetime.now())
					if len(kukaSensor.sensortime_set.all()) >= kukaSensor.averageEnergyTime:
						kukaSensor.sensortime_set.first().delete()

					energySensors.append(kukaSensor)

				if Proc.sensor_set.all().filter(name="Power Clamp (CNC Router)").exists():
					cncSensor = Proc.sensor_set.all().get(name="Power Clamp (CNC Router)")
					cncSensor.sensortime_set.create(energy=cncPower, time = datetime.now())
					if len(cncSensor.sensortime_set.all()) >= cncSensor.averageEnergyTime:
						cncSensor.sensortime_set.first().delete()
					energySensors.append(cncSensor)

				# x,p,k = None,None,None
				# #if power is returning a negative value, invert it into a positive
				# if bigOven['total_power'] < 0:
				# 	bigOvenPower = x['total_power'] * -1		#Huh?

				# if bigCabinet['total_power'] < 0:
				# 	bigCabinetPower = p['total_power'] * -1

				# if kuka['total_power'] < 0:
				# 	kukaRobotPower = k['total_power'] * -1

				if kWh == False: #assign in watts per hour
					energyLabels.append("Big Oven (Watts)")
					energyLabels.append("Big Cabinet (Watts)")
					energyLabels.append("Kuka Robot (Watts)")
					energyLabels.append("CNC Router (Watts)")
					energyLabels.append("Total Power Consumption (Watts)")
					energyData.append(bigOvenPower)
					energyData.append(bigCabinetPower)
					energyData.append(kukaRobotPower)
					energyData.append(cncPower)
					energyData.append(bigOvenPower + bigCabinetPower + kukaRobotPower+cncPower)

				else: #assign in kWh
					energyLabels.append("Big Oven (kWh) ")
					energyLabels.append("Big Cabinet (kWh) ")
					energyLabels.append("Kuka Robot (kWh)")
					energyLabels.append("CNC Router (kWh)")
					energyLabels.append("Total Power Consumption (kWh)")
					energyData.append(bigOvenPower / 1000)
					energyData.append(bigCabinetPower / 1000)
					energyData.append(kukaRobotPower / 1000)
					energyData.append(cncPower/1000)
					energyData.append((bigOvenPower + bigCabinetPower + kukaRobotPower+ cncPower) / 1000)

				CO2perKWH = (((bigOvenPower / 1000) + (bigCabinetPower/ 1000) + (kukaRobotPower/ 1000) + (cncPower/1000))) * float(Proc.project.CO2PerPower) #CO2 per KWH calculation

				avgList = []
				for instance in energySensors:
					for power in instance.sensortime_set.all():
						avgList.append(power.energy)
				try:
					average = (sum(avgList) / len(avgList)) / 1000
				except:
					average = 0

				energyLabels.append("Average Power Consumption in the last " +str(energySensors[0].averageEnergyTime)+  " seconds")
				energyData.append(average)

				#assigning real-time microphone, torque and acceleration data to graphs
				for sensor in Proc.sensor_set.all():
					average = 0
					avgList = []
					if sensor.name == "Microphone":
						microphoneLabels.append(sensor.name + "-" +sensor.modelID)
						microphoneLabels.append("Average Noise Over The last "+ str(sensor.averageTime)+" Seconds")
						sensor.sensortime_set.create(noise = random.randint(1,10), time=datetime.now())
						if len(sensor.sensortime_set.all()) >= sensor.averageTime:
							sensor.sensortime_set.first().delete()
						if len(sensor.sensortime_set.all()) != 0:
							microphoneData.append(sensor.sensortime_set.all().last().noise)
							#microphoneData.append(random.randint(5,10))
							for each in sensor.sensortime_set.all():
								avgList.append(each.noise)

							average = sum(avgList) / len(sensor.sensortime_set.all())
							microphoneData.append(average)
						else:
							microphoneData.append(random.randint(5,10))

					if sensor.name == "Strain Gauge":
						torqueLabels.append(sensor.name + "-" + sensor.modelID)
						torqueLabels.append("Average Strain Over The last "+ str(sensor.averageTime)+" Seconds")
						sensor.sensortime_set.create(torque = random.randint(1,10), time=datetime.now())
						if len(sensor.sensortime_set.all()) >= sensor.averageTime:
							sensor.sensortime_set.first().delete()

						if len(sensor.sensortime_set.all()) != 0:
							torqueData.append(sensor.sensortime_set.all().last().torque)
							for each in sensor.sensortime_set.all():
								avgList.append(each.torque)
							average = sum(avgList) / len(sensor.sensortime_set.all())
							torqueData.append(average)
							#torqueData.append(random.randint(0,10))

						else:
							torqueData.append(random.randint(0,10))

					if sensor.name == "Accelerometer":
						accelerationLabels.append(sensor.name + "-" + sensor.modelID)
						accelerationLabels.append("Average Acceleration Over The last "+ str(sensor.averageTime)+" Seconds")
						sensor.sensortime_set.create(acceleration = random.randint(1,10), time=datetime.now())
						if len(sensor.sensortime_set.all()) >= sensor.averageTime:
							sensor.sensortime_set.first().delete()

						if len(sensor.sensortime_set.all()) != 0:
							accelerationData.append(sensor.sensortime_set.all().last().acceleration)

							for each in sensor.sensortime_set.all():
								avgList.append(each.acceleration)
							average = sum(avgList) / len(sensor.sensortime_set.all())
							accelerationData.append(average)
							#accelerationData.append(random.randint(5,10))
						else:
							accelerationData.append(random.randint(5,10))

				return JsonResponse(data={'CO2perKWH':CO2perKWH, 'accelerationLabels':accelerationLabels, 'accelerationData':accelerationData, 'torqueLabels':torqueLabels, 'torqueData':torqueData, 'microphoneData':microphoneData, 'microphoneLabels':microphoneLabels, 'labels':labels, 'energyData': energyData, 'energyLabels': energyLabels, 'minV':minV, 'maxV':maxV})
		else:
			return redirect('/')
	else:
		return redirect('/mylogout/')

def final(response, id):
	
	if response.user.is_authenticated:
		sub_pro = SubProcess.objects.get(id=id)
		management = False
		supervisor = False
		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True
		if sub_pro.process.project in response.user.profile.user_company.project_set.all():
			if management or supervisor:

				#assigning nominal and actual values
				nominalThickness = sub_pro.process.project.nominalPartThickness
				actualThickness = sub_pro.actualThickness
				nominalWeight= sub_pro.process.project.nominalPartWeight
				actualWeight = sub_pro.postTrimWeight

				data = {}
				dataThickness = {}
				data.update({'Nominal Weight': nominalWeight})
				data.update({'Actual Weight': actualWeight})
				dataThickness.update({'Nominal Thickness': nominalThickness})
				dataThickness.update({'Actual Thickness': actualThickness})

				#data returned as json response for graph data on final inspection page


				return JsonResponse(data={'data':data, 'dataThickness':dataThickness})
	else:
		return redirect('/mylogout/')


def systemArchitecture(response, id):
	if response.user.is_authenticated:
		project = Project.objects.get(id=id)
		management = False
		supervisor = False
		technician = False
		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True
		elif response.user.groups.filter(name='Technician').exists():
			technician = True
		if project in response.user.profile.user_company.project_set.all():
			if management or supervisor or technician:

				#open system architecture page
				return render(response, 'Main/showSystemArchitecture.html', {'technician':technician, 'management':management, 'supervisor':supervisor, 'selected_project':project})
			else:
				return redirect('/')
		else:
			#redirect to the home page
			return redirect('/')
	else:
		return redirect('/mylogout/')

def part_start(response, id):
	
	if response.user.is_authenticated:
		subPro = SubProcess.objects.get(id=id)
		process = subPro.process
		project = subPro.process.project
		management, supervisor, admin = False, False, False
		orderedSubProList = process.order_subprocess_custom()
		indexList = list(orderedSubProList)
		index = indexList.index(subPro)
		try:
			nextSub = orderedSubProList[index + 1] #the next sub process in sequence	
		except IndexError:
			if not process.endPoint: # if not final process
				nextProcess = project.process_set.get(position = process.position + 1) #get next process
				nextSub = nextProcess.order_subprocess_custom().first() #get next sub process

		if project.manual:
			nextName = subPro.manualName
			pname= process.manualName
		else:
			nextName = subPro.name
			pname = process.name

		if subPro.partTask:
			attr = 'partInstance'
			nextAttr = 'partInstance'

		elif subPro.blankTask and not subPro.consolidationCheck:
			attr = 'blankInstance'
			nextAttr = 'blankInstance'

		elif subPro.blankTask and subPro.consolidationCheck:
			attr = 'blankInstance'
			nextAttr = 'partInstance'

		elif subPro.plyTask and not subPro.consolidationCheck:
			attr = 'plyInstance'
			nextAttr = 'plyInstance'

		elif subPro.plyTask and subPro.consolidationCheck:
			attr = 'plyInstance'
			nextAttr = 'blankInstance'

		if not  process.startPoint and subPro.startPoint:
			currentInstance = process.instancequeue_set.first().instance_id
			setattr(subPro, attr, currentInstance)
			subPro.save()
			process.instancequeue_set.first().delete()
		else:
			currentInstance = getattr(subPro, attr) 

		if not subPro.endPoint:
			nextInstance = getattr(nextSub, nextAttr)
		else:
			nextInstance = None

		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True
		elif response.user.groups.filter(name='Admin').exists():
			admin = True

		if subPro.operator == None:
			messages.error(response, "Sub Process needs operator")
		# elif (subPro.partInstance != None and subPro.partTask) or (subPro.blankInstance != None and subPro.blankTask) or (subPro.plyInstance != None and subPro.plyTask) and not subPro.startPoint: #if part instance doesn't exist
		# 	messages.error(response,'This Sub proces is already active!')#sub pro is full
		elif not subPro.endPoint and nextInstance != None and currentInstance != None:
			messages.error(response,"You cannot submit this part until " + nextName + " has been submitted!") # you cannot submit this sub process part until the next sub process has been submitted
		else:
			subPro.jobStart =  timezone.localtime(timezone.now()).replace(microsecond=0)
			subPro.status = 1
			subPro.save()
			if (subPro.partTask and not Part.objects.all()) or (subPro.blankTask and not Blank.objects.all()) or (subPro.plyTask and not Ply.objects.all()):
				ID = 1
			else:
				if subPro.partTask:
					lastPart = Part.objects.latest('part_id') #get last part and set ID to last part + 1
					ID = lastPart.part_id + 1
				elif subPro.blankTask:
					lastBlank = Blank.objects.latest('blank_id') #get last part and set ID to last part + 1
					ID = lastBlank.blank_id + 1
				elif subPro.plyTask:
					lastPly = Ply.objects.latest('ply_id') #get last part and set ID to last part + 1
					ID = lastPly.ply_id + 1			


			if subPro.startPoint == True and process.startPoint == True:
				if subPro.partTask:
					if not PartInstance.objects.all():
						instID = 1
					else:
						instID = PartInstance.objects.latest('instance_id').instance_id + 1

					part = Part.objects.create(part_id=ID, project=project,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0), techRate=project.techRate, superRate=project.superRate,
								powerRate=project.powerRate,CO2PerPower = project.CO2PerPower, setUpCost=project.setUpCost) #create part
					processPart = ProcessPart.objects.create(part = part, processName = pname,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0)) #create process part
					subPro.process.partinstance_set.create(instance_id = instID) #create part instance
					subPro.partInstance = instID
					partInst = PartInstance.objects.get(instance_id = subPro.partInstance)
					partInst.part_set.add(part)
					subPro.save()
				elif subPro.blankTask:
					if not BlankInstance.objects.all():
						instID = 1
					else:
						instID = BlankInstance.objects.latest('instance_id').instance_id + 1

					for i in range(int(subPro.batchSize)):							
						blank = Blank.objects.create(blank_id=ID, project=project,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0), techRate=project.techRate, superRate=project.superRate,
								powerRate=project.powerRate,CO2PerPower = project.CO2PerPower, setUpCost=project.setUpCost) #create blank
						processPart = ProcessPart.objects.create(blank = blank, processName = pname,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0)) #create process part

						if subPro.process.blankinstance_set.filter(instance_id=instID).exists():
							localInst = subPro.process.blankinstance_set.get(instance_id=instID)
							localInst.blank_set.add(blank)
						else:
							subPro.process.blankinstance_set.create(instance_id=instID)
							localInst = subPro.process.blankinstance_set.get(instance_id=instID)
						blank.blankInstance = localInst
						blank.save()
						ID += 1
				
					subPro.blankInstance = instID
					subPro.save()
				elif subPro.plyTask:
					if not PlyInstance.objects.all():
						instID = 1
					else:
						instID = PlyInstance.objects.latest('instance_id').instance_id + 1

					for i in range(int(subPro.batchSize)):							
						ply = Ply.objects.create(ply_id=ID, project=project,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0), techRate=project.techRate, superRate=project.superRate,
							powerRate=project.powerRate,CO2PerPower = project.CO2PerPower, setUpCost=project.setUpCost) #create blank
						processPart = ProcessPart.objects.create(ply = ply, processName = pname,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0)) #create process part
				
						if subPro.process.plyinstance_set.filter(instance_id=instID).exists():
							localInst = subPro.process.plyinstance_set.get(instance_id=instID)
							localInst.ply_set.add(ply)
						else:
							subPro.process.plyinstance_set.create(instance_id = instID) #create ply instance
							localInst = subPro.process.plyinstance_set.get(instance_id=instID)
						ply.plyInst = localInst
						ply.save()
						ID += 1 
			

					subPro.plyInstance = instID
					subPro.save() 
			elif subPro.startPoint == True and process.startPoint == False:
				if subPro.partTask:
					partInst = PartInstance.objects.get(instance_id = subPro.partInstance)
					if subPro.batchSize != len(partInst.part_set.all()):
						messages.error(response, 'Batch size does not match active batch!')
					else:
						for part in partInst.part_set.all():
							processPart = ProcessPart.objects.create(part = part, processName = pname,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0)) #create process part
				if subPro.blankTask:
					blankInst = BlankInstance.objects.get(instance_id = subPro.blankInstance)
					if subPro.batchSize != len(blankInst.blank_set.all()):
						messages.error(response, 'Batch size does not match active batch!')
					else:
						for blank in blankInst.blank_set.all():
							processPart = ProcessPart.objects.create(blank = blank, processName = pname,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0)) #create process part
				if subPro.plyTask:
					plyInst = PlyInstance.objects.get(instance_id = subPro.plyInstance)
					if subPro.batchSize != len(plyInst.ply_set.all()):
						messages.error(response, 'Batch size does not match active batch!')
					else:
						for ply in plyInst.ply_set.all():
							processPart = ProcessPart.objects.create(ply = ply, processName = pname,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0)) #create process part

			if subPro.partTask:
				localInst = PartInstance.objects.get(instance_id = subPro.partInstance)
				products = localInst.part_set.all()
			elif subPro.blankTask:
				localInst = BlankInstance.objects.get(instance_id = subPro.blankInstance)
				products = localInst.blank_set.all()
			elif subPro.plyTask:
				localInst = PlyInstance.objects.get(instance_id = subPro.plyInstance)
				products = localInst.ply_set.all()
			else:
				products = []

			for product in products:	
				product.updateWholePart() #update products and set to submitted
				product.updatePrimaryValues(project)

		return redirect('/'+str(process.id))
	else:
		return redirect('/')


def part_approve(response, id):
	if response.user.is_authenticated:
		sub_pro = SubProcess.objects.get(id=id)
		process = sub_pro.process
		project = process.project
		processPartSet = []
		management, supervisor = False, False
		repeat_block = None

		if sub_pro.jobStart is not None:
			###---Getting next Sub Process---###
			orderedSubProList = process.order_subprocess_custom()
			indexList = list(orderedSubProList)
			index = indexList.index(sub_pro)
			try:
				nextSub = orderedSubProList[index + 1] #the next sub process in sequence	
			except IndexError: #if there is no next sub process
				if not process.endPoint: #if it is not the last process in sequence
					nextProcess = project.process_set.get(position = process.position + 1) #get first sub process of next process
					nextSub = nextProcess.order_subprocess_custom().first()

			if response.user.groups.filter(name="Management").exists():
				management = True 
			elif response.user.groups.filter(name="Supervisor").exists():
				supervisor = True

			if management or supervisor:
				###---General ply/blank/part Setup---###
				if sub_pro.partTask:
					attr = 'partInstance'
					nextAttr = 'partInstance'

				elif sub_pro.blankTask and not sub_pro.consolidationCheck:
					attr = 'blankInstance'
					nextAttr = 'blankInstance'

				elif sub_pro.blankTask and sub_pro.consolidationCheck:
					attr = 'blankInstance'
					nextAttr = 'partInstance'

				elif sub_pro.plyTask and not sub_pro.consolidationCheck:
					attr = 'plyInstance'
					nextAttr = 'plyInstance'

				elif sub_pro.plyTask and sub_pro.consolidationCheck:
					attr = 'plyInstance'
					nextAttr = 'blankInstance'


				if sub_pro.repeat and process.repeatblock_set.all().filter(finished=False).exists():
					repeat_block = process.repeatblock_set.all().filter(finished=False).first()
					for sub in repeat_block.repeatblocksubprocesses_set.all():
						if sub.sub_process == sub_pro and sub.end and repeat_block.iteration != repeat_block.number_of_iterations:
							nextSub = repeat_block.repeatblocksubprocesses_set.all().get(start=True).sub_process

				if not sub_pro.endPoint: #if sub process is not the final in sequence, then get the next sub process instance
					nextInstance = getattr(nextSub, nextAttr)
				else:
					nextInstance = None #set to none for now
				currentInstance = getattr(sub_pro, attr) #current instance is the current part/ply/blank instance

				if nextInstance is None: #if next sub process has been submitted / is inactive

					if not sub_pro.consolidationCheck and not sub_pro.endPoint:
						setattr(nextSub, nextAttr, currentInstance) #pass instance to next sub process
						nextSub.save()
						
					elif sub_pro.consolidationCheck and not sub_pro.endPoint: #if consolidation subprocess
						if (sub_pro.plyTask and not Blank.objects.all()) or (sub_pro.blankTask and not Part.objects.all()): #settings IDs to lowest primary key possible
							ID = 1
						elif sub_pro.plyTask:
							ID = Blank.objects.latest('blank_id').blank_id + 1
						elif sub_pro.blankTask:
							ID = Part.objects.latest('part_id').part_id + 1

						if sub_pro.plyTask: #if subprocess is a ply task
							if not BlankInstance.objects.all():
								instID = 1
							else:
								instID = BlankInstance.objects.latest('instance_id').instance_id + 1
							setattr(nextSub, nextAttr, instID)
							plyInst = PlyInstance.objects.get(instance_id=currentInstance) #get ply instance
							blankInst = sub_pro.process.blankinstance_set.create(instance_id = instID) # create blank instance
							for i in range(int(nextSub.batchSize)):	
								blank = Blank.objects.create(project=project,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0), techRate=project.techRate, superRate=project.superRate,
		 									powerRate=project.powerRate,CO2PerPower = project.CO2PerPower, setUpCost=project.setUpCost) #create blank
								
								blankInst.blank_set.add(blank) # add blank to blank instance
								processNames, subProcessNames = [],[]

								for index, ply in enumerate(plyInst.ply_set.all()): #for each ply in the ply instance set
									if index+1 <= plyInst.ply_set.all().count() / nextSub.batchSize and i == 0:
										blank.ply_set.add(ply)	#add plies to blank ply set
										for processPart in ply.processpart_set.all():
											if processPart.processName not in processNames:
												processNames.append(processPart.processName)
											for subProcessPart in processPart.subprocesspart_set.all():
												if (subProcessPart.subProcessName, processPart.processName) not in subProcessNames:
													subProcessNames.append((subProcessPart.subProcessName, processPart.processName))

									elif index+1 > plyInst.ply_set.all().count() / nextSub.batchSize and i ==1:
										blank.ply_set.add(ply)	#add plies to blank ply set
										for processPart in ply.processpart_set.all():
											if processPart.processName not in processNames:
												processNames.append(processPart.processName)
											for subProcessPart in processPart.subprocesspart_set.all():
												if (subProcessPart.subProcessName, processPart.processName) not in subProcessNames:
													subProcessNames.append((subProcessPart.subProcessName, processPart.processName))
									print(f"Index of ply set: {index}   i of batch size: {i}")

								for processPartName in processNames:
									processPart = blank.consolidate_process_parts(processPartName)#consolidate process parts
								
								for nameTuple in subProcessNames:
									consolidatedSubProcessPart = blank.consolidate_sub_process_parts(nameTuple[0], nameTuple[1])


								sub_pro.jobEnd = timezone.localtime(timezone.now()).replace(microsecond=0) #set job end
								sub_pro.save()

								sub_pro.updateSubIntervals()
								processNames, subProcessNames = [],[]

	
						elif sub_pro.blankTask:
							if not PartInstance.objects.all():
								instID = 1
							else:
								instID = PartInstance.objects.latest('instance_id').instance_id + 1
							setattr(nextSub, nextAttr, instID) #set next sub process attribute to specified next attribute
							part = Part.objects.create(part_id = ID,project=project,date = date.today(), jobStart = timezone.localtime(timezone.now()).replace(microsecond=0), techRate=project.techRate, superRate=project.superRate,
										powerRate=project.powerRate,CO2PerPower = project.CO2PerPower, setUpCost=project.setUpCost) #create part
							partInst = sub_pro.process.partinstance_set.create(instance_id = instID) #get part instance
							partInst.part_set.add(part) # add part to part instance set
							blankInst = BlankInstance.objects.get(instance_id=currentInstance)
							processNames, subProcessNames = [],[]
							for blank in blankInst.blank_set.all(): # for each blank in currrent instance blank set
								part.blank_set.add(blank)	# add blanks to part set
								# blank.processpart_set.add(ply.processpart_set.last())
							for blank in blankInst.blank_set.all(): #for each ply in the ply instance set
								part.blank_set.add(blank)	#add plies to blank ply set
								for processPart in blank.processpart_set.all():
									if processPart.processName not in processNames:
										processNames.append(processPart.processName)
									for subProcessPart in processPart.subprocesspart_set.all():
										if (subProcessPart.subProcessName, processPart.processName) not in subProcessNames:
											subProcessNames.append((subProcessPart.subProcessName, processPart.processName))

							for processPartName in processNames:
								processPart = part.consolidate_process_parts(processPartName)#consolidate process parts
									
							for nameTuple in subProcessNames:
								consolidatedSubProcessPart = part.consolidate_sub_process_parts(nameTuple[0], nameTuple[1])

							sub_pro.jobEnd = timezone.localtime(timezone.now()).replace(microsecond=0) #set job end
							sub_pro.save()

							sub_pro.updateSubIntervals()
							

						nextSub.save()

					is_blank, is_part = False, False
					if sub_pro.partTask:
						localInst = PartInstance.objects.get(instance_id=currentInstance) # get current local instance
						for part in localInst.part_set.all(): #for each part in localinst set
							product = Part.objects.get(part_id = part.part_id) #get the part
							processPartSet.append(ProcessPart.objects.get(part=product, processName=process.name)) #append product to process part set
					elif sub_pro.blankTask:
						localInst = BlankInstance.objects.get(instance_id=currentInstance)
						for blank in localInst.blank_set.all():
							product = Blank.objects.get(blank_id = blank.blank_id) # get each blank
							processPartSet.append(ProcessPart.objects.get(blank=product, processName=process.name))#append blanks to process part set
						if sub_pro.consolidationCheck:
							localInst.delete() #delete instance if consolidated
							
					elif sub_pro.plyTask:
						localInst = PlyInstance.objects.get(instance_id=currentInstance)
						for ply in localInst.ply_set.all(): #for each ply in local inst set
							product = Ply.objects.get(ply_id = ply.ply_id) #get ply from ply instance
							processPartSet.append(ProcessPart.objects.get(ply=product, processName=process.name)) #append plies to process part set
						if sub_pro.consolidationCheck:
							localInst.delete() #delete instance if conslidated
							

					
					###---General Setup End---#

					###---Start-Intermediary Saving---###
					if sub_pro.repeat and repeat_block is not None:
						if sub_pro == repeat_block.repeatblocksubprocesses_set.last().sub_process:
							if repeat_block.iteration != repeat_block.number_of_iterations:
								repeat_block.iteration +=1
								repeat_block.save()
							else:
								repeat_block.finished = True 
								repeat_block.save()
								messages.success(response, 'Repeat Block Completed!')

					if not sub_pro.endPoint:

						sub_pro.jobEnd = timezone.localtime(timezone.now()).replace(microsecond=0) #set job end
						sub_pro.save()

						process.update_subprocess_positions() #update current subprocess positions

						interval = timedelta()
						interval = sub_pro.jobEnd.replace(tzinfo=None) - sub_pro.jobStart.replace(tzinfo=None) #get cycle time between job start and end

						#sub_pro.calcWastedTime(indexList, processPart)
						#make sure costs are up to date
						sub_pro.updateSubCosts()
						process.updateProcessCosts()
						project.updateProjectCosts()
						#print(sub_pro.technicianLabourCost)

						#if not sub_pro.consolidationCheck:
						for processPart in processPartSet: #for all process parts appended earlier
							#create subprocess part
							if sub_pro.plyTask:
								subProcessPart = processPart.subprocesspart_set.create(subProcessName=sub_pro.name, date=datetime.today(), jobStart = sub_pro.jobStart, jobEnd = sub_pro.jobEnd, processTime=sub_pro.processTime, interfaceTime=sub_pro.interfaceTime, ply=processPart.ply)
							elif sub_pro.blankTask:
								subProcessPart = processPart.subprocesspart_set.create(subProcessName=sub_pro.name, date=datetime.today(), processTime=sub_pro.processTime, jobStart = sub_pro.jobStart, jobEnd = sub_pro.jobEnd, interfaceTime=sub_pro.interfaceTime, blank=processPart.blank)
							elif sub_pro.partTask:
								subProcessPart = processPart.subprocesspart_set.create(subProcessName=sub_pro.name, date=datetime.today(), processTime=sub_pro.processTime, jobStart = sub_pro.jobStart, jobEnd = sub_pro.jobEnd, interfaceTime=sub_pro.interfaceTime, part=processPart.part)
							subProcessPart.mirrorAttributes(sub_pro) #mirror attributes from sub_pro to subprocesspart
							subProcessPart.updateIntervals() #update intervals
							processPart.updateProcessCosts() #updates costs
							processPart.updateWholeProcessPart() # update all processpart values

							for sensor in sub_pro.sensor_set.all(): #for all sensors in sub process set
								sensorData = SensorData.objects.create(sensorName=sensor.name, subProcessPart=subProcessPart, status=sensor.status) #create sensor data object
								sensorData.mirrorSensorAttributes(sensor) #mirror attributes from sensor/sensortime to sensorData/senosrtimeData

							for sensor in sub_pro.process.sensor_set.all():
								sensorData = SensorData.objects.create(sensorName=sensor.name, processPart=processPart, status=sensor.status) #create sensor data object
								sensorData.mirrorSensorAttributes(sensor) #mirror attributes from sensor/sensortime to sensorData/senosrtimeData

						if sub_pro.consolidationCheck:
							if sub_pro.plyTask:
								for blank in blankInst.blank_set.all():
									consolidated = blank.consolidate_sub_process_parts(sub_pro.name, sub_pro.process.name)
									consolidated.jobEnd = sub_pro.jobEnd
									consolidated.save()
							elif sub_pro.blankTask:
								for part in partInst.part_set.all():
									consolidated = part.consolidate_sub_process_parts(sub_pro.name, sub_pro.process.name)
									consolidated.jobEnd = sub_pro.jobEnd
									consolidated.save()

						



						messages.success(response, "Part Data successfully submitted!")

						sub_pro.resetAttributes() #setting attributes to default

						sub_pro.status = 2 #approve colour green implemented
						if sub_pro.startPoint is True and "Initialisation" in sub_pro.name:
							#process.initialised = True
							process.save()
							
						sub_pro.save()

					###---Block END---###

					elif sub_pro.endPoint: 
						sub_pro.jobEnd = timezone.localtime(timezone.now()).replace(microsecond=0) #setting job end
						sub_pro.save()
						###---Approval of sub-processes that are the End Point---###	

						interval = timedelta()
						interval = sub_pro.jobEnd - sub_pro.jobStart #get difference between job end and job start
						index = indexList.index(sub_pro)
						sub_pro.updateSubCosts()
						process.updateProcessCosts()
						project.updateProjectCosts()
							
						sub_pro.save()
						#create sub process part and assign values to fields
						for processPart in processPartSet: #for all process parts appended earlier
							#create subprocess part
							if sub_pro.plyTask:
								subProcessPart = processPart.subprocesspart_set.create(subProcessName=sub_pro.name, date=datetime.today(), jobStart = sub_pro.jobStart, jobEnd = sub_pro.jobEnd, processTime=sub_pro.processTime, interfaceTime=sub_pro.interfaceTime, ply=processPart.ply)
							elif sub_pro.blankTask:
								subProcessPart = processPart.subprocesspart_set.create(subProcessName=sub_pro.name, date=datetime.today(), processTime=sub_pro.processTime, jobStart = sub_pro.jobStart, jobEnd = sub_pro.jobEnd, interfaceTime=sub_pro.interfaceTime, blank=processPart.blank)
							elif sub_pro.partTask:
								subProcessPart = processPart.subprocesspart_set.create(subProcessName=sub_pro.name, date=datetime.today(), processTime=sub_pro.processTime, jobStart = sub_pro.jobStart, jobEnd = sub_pro.jobEnd, interfaceTime=sub_pro.interfaceTime, part=processPart.part)
							subProcessPart.mirrorAttributes(sub_pro) #mirror attributes from sub_pro to subprocesspart
							subProcessPart.updateIntervals() #update intervals
							processPart.updateProcessCosts() #updates costs
							processPart.updateWholeProcessPart() # update all processpart values

							for sensor in sub_pro.sensor_set.all(): #for all sensors in sub process set
								sensorData = SensorData.objects.create(sensorName=sensor.name, subProcessPart=subProcessPart, status=sensor.status) #create sensor data object
								sensorData.mirrorSensorAttributes(sensor) #mirror attributes from sensor/sensortime to sensorData/senosrtimeData

							for sensor in sub_pro.process.sensor_set.all():
								sensorData = SensorData.objects.create(sensorName=sensor.name, processPart=processPart, status=sensor.status) #create sensor data object
								sensorData.mirrorSensorAttributes(sensor) #mirror attributes from sensor/sensortime to sensorData/senosrtimeData
							

						products = None
						 #get needed products based on ply/blank/part conditiosn
						if sub_pro.partTask:
							products = localInst.part_set.all()
						elif sub_pro.blankTask:
							products = localInst.blank_set.all()
						elif sub_pro.plyTask:
							products = localInst.ply_set.all()
						for product in products:
							product.updatePrimaryValues(project)
							product.updateWholePart() #update products and set to submitted
							product.submitted = True
							product.save()
							
						if Material.objects.filter(name=product.project.material).exists():
							material = Material.objects.get(name=product.project.material) #setting material if defined
						else:
							material = None
						#get needed products based on ply/blank/part conditiosn
						sub_pro.resetAttributes()

						for each in process.repeatblock_set.all():
							each.iteration = 0
							each.finished = False
							each.save()


						messages.success(response, "Part Data successfully submitted!")
						sub_pro.status = 2
						sub_pro.save()
						process_set = project.order_process_custom()

						if process_set.filter(position=process.position+1).exists():
							nextProcess = process_set.get(position = process.position+1) #passing part instance to next process (first sub process)
							nextProcess.update_subprocess_positions() #update their positions
							if sub_pro.plyTask:
								plyInst = PlyInstance.objects.get(instance_id=currentInstance)
								plyInst.process = nextProcess   
								plyInst.save()
							elif sub_pro.blankTask:
								blankInst = BlankInstance.objects.get(instance_id=currentInstance)
								blankInst.process = nextProcess 
								blankInst.save()

							if not nextProcess.initialised:
								nextSub = nextProcess.order_subprocess_custom().first() # if initalisation hasn't run on next process

							else:
								nextSub = nextProcess.subprocess_set.get(position=1) # if initialisation has run on next process

							if not sub_pro.consolidationCheck:
								nextProcess.instancequeue_set.create(instance_id=currentInstance)

							else:
								if sub_pro.plyTask:
									newInstance = ply.blank.blank_id
									
								elif sub_pro.blankTask:
									newInstance = blank.part.part_id

								nextProcess.instancequeue_set.create(instance_id=newInstance)
						else:
							if sub_pro.partTask:
								PartInstance.objects.get(instance_id=currentInstance).delete() #delete part instance now that all part data has been saved
							elif sub_pro.blankTask:
								BlankInstance.objects.get(instance_id=currentInstance).delete()
							elif sub_pro.plyTask:
								PlyInstance.objects.get(instance_id=currentInstance).delete()
							pass
				###---End Block---###
				
					
				else:
					messages.error(response, "The Next Sub Process Needs to be Approved before continuing!")
					return redirect('/'+str(process.id))
				return redirect('/'+str(process.id))
			else:
				return redirect('/')
		else:
			return redirect('/')
	else:
		messages.error(response, "You have not started this Sub Process!")


def part_bad(response, id):
	
	if response.user.is_authenticated: #and (supervisor or admin):
		#DEFINING
		management, supervisor, admin = False, False, False
		sub_pro = SubProcess.objects.get(id=id)
		process = sub_pro.process
		processPartName = process.name
		orderedSubProList = process.order_subprocess_custom()
		indexList = list(orderedSubProList)
		index = indexList.index(sub_pro)
		project = sub_pro.process.project
		processPartList = []
		productList = []

		#ASSIGNING USER GROUP
		if response.user.groups.filter(name="Management").exists():
			management = True 
		elif response.user.groups.filter(name="Supervisor").exists():
			supervisor = True
		elif response.user.groups.filter(name="Admin").exists():
			admin = True
		#DEFINING THE NEXT SUB-PROCESS/PROCESS IN THE PROCESS/PROJECT
		try:
			nextSub = orderedSubProList[index + 1] #the next sub process in sequence	
		except IndexError:
			if not process.endPoint:
				nextProcess = project.process_set.get(position = process.position + 1)
				nextSub = nextProcess.order_subprocess_custom().first()
		sub_pro.jobEnd = datetime.now().replace(microsecond=0)
		sub_pro.save()
		#DEFINING THE CURRENT INSTANCE ATTR AS A PART, PLY OR BLANK
		if sub_pro.partTask:
			attr = 'partInstance'

		elif sub_pro.blankTask:
			attr = 'blankInstance'

		elif sub_pro.plyTask:
			attr = 'plyInstance'

		currentInstance = getattr(sub_pro, attr)

		if currentInstance == None: 
			messages.error(response, 'No parts to be made bad') #ERROR HANDLING
		else: #FINDING THE TASK SO WE CAN CREATE LISTS FOR SAVING DATA
			if sub_pro.partTask:
				partInst = PartInstance.objects.get(instance_id=currentInstance)
				for part in partInst.part_set.all():
					productList.append(part)
					processPartList.append(part.processpart_set.get(processName=processPartName))
			elif sub_pro.blankTask:
				blankInst = BlankInstance.objects.get(instance_id=sub_pro.blankInstance)
				for blank in blankInst.blank_set.all():
					productList.append(blank)
					processPartList.append(blank.processpart_set.get(processName=processPartName))
			elif sub_pro.plyTask:
				plyInst = PlyInstance.objects.get(instance_id=currentInstance)
				for ply in plyInst.ply_set.all():
					productList.append(ply)
					processPartList.append(ply.processpart_set.get(processName=processPartName))
			#LOOPING THROUGH PROCESS PARTS SAVING SENSOR DATA	
			for processPart in processPartList:
				#save sensor data related to process
				sensorName = ""
				for sensor in process.sensor_set.all(): #loop through sensor fields and mirror to sensor data
					sensorData = processPart.sensordata_set.create(sensorName=sensor.name, status=sensor.status)
					sensorData.mirrorSensorAttributes(sensor)


				try: 
					previousSub = processPart.subprocesspart_set.last() #get previous sub from previous sub process
					sub_pro.wastedTime = sub_pro.jobStart - previousSub.jobEnd #get wasted time
				except:
					sub_pro.wastedTime = timedelta()
					
				sub_pro.save()
				#create sub process part and assign values to fields
				subProcessPart =  SubProcessPart.objects.create(subProcessName=sub_pro.name, processPart=processPart, date=date.today(), processTime = sub_pro.processTime, interfaceTime = sub_pro.interfaceTime)

				subProcessPart.mirrorAttributes(sub_pro)

				subProcessPart.updateIntervals()

				processPart.updateProcessPartMachines(sub_pro.process)
				processPart.updateWholeProcessPart()
				processPart.save()

				#iterate through sensors associated with sub process's
				for sensor in sub_pro.sensor_set.all():
					#create sensor data object and assign values to fields
					sensorData = SensorData.objects.create(sensorName=sensor.name, subProcessPart=subProcessPart, status=sensor.status)
					sensorData.mirrorSensorAttributes(sensor)
			#LOOPING THROUGH THE PRODUCTS SAVING THE MATERIAL THATS BEEN USED
			for product in productList:
			
				for attr in project._meta.fields: #loop through project attributes and assign to part
					if "Cost" in attr.name or attr.name == "part" or attr.name == "date" or attr.name == "plyCutter" or attr.name == "sortPickAndPlace" or attr.name == "blanksPickAndPlace" or attr.name == "preformCell" or attr.name == "id":
						pass
					else:
						value = getattr(project, attr.name)
						setattr(product, attr.name, value)

				product.updateWholePart()
				product.submitted = True
				product.badPart = True
				product.save()

			
			sub_pro.resetAttributes()

			# for each in process.repeatblock_set.all():
			# 	each.iteration = 0
			# 	each.finished = False
			# 	each.save()

			messages.success(response, "Part Data successfully submitted!")
			sub_pro.status = 3
			sub_pro.save()
			process_set = project.order_process_custom()
			#RESET CURRENT INSTANCE
			if sub_pro.partTask:
				partInstance = PartInstance.objects.get(instance_id=currentInstance)
				partInstance.delete()
			elif sub_pro.plyTask:
				plyInstance = PlyInstance.objects.get(instance_id=currentInstance)
				plyInstance.delete()
			elif sub_pro.blankTask:
				blankInstance = BlankInstance.objects.get(instance_id=currentInstance)
				blankInstance.delete()
			
		return redirect('/'+str(process.id))
	return redirect('/')

def viewImages(response,id):
	if response.user.is_authenticated:
		management = False
		supervisor = False
		technician = False

		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True
		elif response.user.groups.filter(name='Technician').exists():
			technician = True

		if management or supervisor or technician:
			project = Project.objects.get(id=id)
			return render(response, 'Main/viewImages.html', {'selected_project':project})
		else:
			return redirect('/')
	else:
		return redirect('/')

def viewImagesDetail(response,id):

	if response.user.is_authenticated:
		management = False
		supervisor = False

		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True

		if management or supervisor:
			project = Project.objects.get(id=id)
			return render(response, 'Main/viewImagesDetail.html', {'selected_project':project})
		else:
			return redirect('/')
	else:
		return redirect('/')

def viewImageSpecific(response,id, part):
	if response.user.is_authenticated:
		management = False
		supervisor = False

		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True

		if management or supervisor:
			if part == 0:
				subpro = SubProcess.objects.get(id=id)
				project = subpro.process.project
			else:
				subpro = SubProcessPart.objects.get(id=id)
				project = subpro.processPart.part.project

			return render(response, 'Main/viewImageSpecific.html', {'sub_pro':subpro, 'project':project})
		else:
			return redirect('/')
	else:
		return redirect('/')


def viewFiles(response,id):
	if response.user.is_authenticated:
		project = Project.objects.get(id=id)
		management = False
		supervisor = False

		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True

		if management or supervisor:
			return render(response, 'Main/viewFiles.html', {'project':project})
		else:
			return redirect('/')
	else:
		return redirect('/')


def downloadFile(response,id,part):

	if response.user.is_authenticated:
		if part == 0:
			sub_pro = SubProcess.objects.get(id=id)
		else:
			sub_pro = SubProcessPart.objects.get(id=id)

		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True

		if management or supervisor:

			filename = sub_pro.file.name.split('/')[-1]
			response = HttpResponse(sub_pro.file, content_type='text/plain')
			response['Content-Disposition'] = 'attachment; filename=%s' % filename

			return response
		else:
			return redirect('/')
	else:
		return redirect('/')

