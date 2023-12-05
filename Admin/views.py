from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.db.models.fields import NOT_PROVIDED
from django.contrib import messages
from django import template

from Main.models import *
from Main.forms import *
from .forms import *

import requests
import json
import random


def admin_start(response):
	"""View to show the Companies Projects page"""
	#check user group
	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
		if admin:
			form = CreateNewProject()
			delform = deleteProject(response.user.profile.user_company)
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
							#check response type
					elif response.POST.get('deleteProject'):
						delform = deleteProject(response.user.profile.user_company, response.POST)
						if delform.is_valid():
							n = delform.cleaned_data['choice']
							#check response type
							if response.POST.get('deleteProject'):
								#check if project exists and delete
								if response.user.profile.user_company.project_set.filter(project_name=n).exists():
									p = response.user.profile.user_company.project_set.get(project_name=n)
									p.delete()
									messages.success(response, 'Project successfully deleted!')
								#show error if project doesnt exist
								else:
									messages.error(response, 'Project not in list!')
				else:
					#show permission error
					messages.error(response, 'You do not have permission for this action!')
			else:
				#return empty form
				form = CreateNewProject()
			
			#return response, page and dict of var
			return render(response, 'Admin/showProjects.html', {'delform':delform, 'form' : form, 'admin':admin})
		else:
			#redirect to home page
			return redirect('/')
	else:
		return redirect('/mylogout/')

def admin_request_hard(response, id):

	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
			return redirect('/')
		if admin:
			data = {}
			deviceList = []
			requested,saved = False,False
			project = Project.objects.get(id=id)
			if project in response.user.profile.user_company.project_set.all():
				if response.method == 'POST':
					if response.POST.get('requestHardware') or response.POST.get('saveRequest'):
						requested = True
						# make request to IPC here
						# data = requests.post()
						# here for practice
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

										'Dust Sensor':{
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

						if response.POST.get('saveRequest'):
							for machineKey in data['machines']:
								if not response.user.profile.user_company.machine_set.filter(name=machineKey).exists():
									m = Machine.objects.create(name=machineKey, company=response.user.profile.user_company)
								else: 
									m = Machine.objects.get(name=machineKey, company=response.user.profile.user_company)

								if not project.possibleprojectmachines_set.filter(name=machineKey).exists():
									pm = PossibleProjectMachines.objects.create(name=machineKey, project=project, machine=m)
								else:
									pm = PossibleProjectMachines.objects.get(name = machineKey, project=project, machine = m)

								for device in data['machines'][machineKey]['devices']:
									deviceID = data['machines'][machineKey]['devices'][device]['id']
									modelID = data['machines'][machineKey]['devices'][device]['modelID']
									
									if not Sensor.objects.all().filter(id=deviceID).exists():
										s = Sensor.objects.create(name=device,id=deviceID, modelID=modelID, machine = m, status=1)
									else:
										s =Sensor.objects.get(id=deviceID, modelID = modelID)

									s.machine = m
									s.save()
								for tiaBlock in data['machines'][machineKey]['tiaBlocks']:
									tiaID = data['machines'][machineKey]['tiaBlocks'][tiaBlock]['id']
									if not TiaBlocks.objects.filter(id=tiaID).exists():
										t = TiaBlocks.objects.create(machine=m, id=tiaID, name=tiaBlock)
										t.project.add(project)
									else:
										t = TiaBlocks.objects.get(id=tiaID)
										t.machine = m
										t.save()

							return redirect(f'/adminAssignHardware{id}', permanent=True)


					return render(response, 'Admin/requestHardware.html', {'data' : data, 'admin':admin, 'deviceList':deviceList, 'requested':requested, 'project':project, 'saved':saved})

				else:
					return render(response, 'Admin/requestHardware.html', {'data' : data, 'admin':admin, 'deviceList':deviceList, 'requested':requested, 'project':project, 'saved':saved})
			else:
				#redirect to home page
				return redirect('/')
	else:
		return redirect('/mylogout/')

def admin_assign_machine(response, id):

	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
			return redirect('/')
		if admin:
			project = Project.objects.get(id=id)
			company = Company.objects.get(company_name=response.user.profile.user_company)
			machineForm = SelectMachines(id)
			possibleProForm = PossibleProForm(id)
			if project in response.user.profile.user_company.project_set.all():
				if project.editStatus != 0:					#what is editStatus used for?
					project.process_set.all().delete()
				if response.method == 'POST':
					project.editStatus = 0
					project.save()
					if response.POST.get('addMachine') or response.POST.get('removeMachine'):
						if not project.machineConfirmed:				#what is machineConfirmed used for?
							machineForm = SelectMachines(id, response.POST)
							if machineForm.is_valid():
								posMachine = machineForm.cleaned_data['machine']
								if response.POST.get('addMachine'):
									if project.machine_set.filter(name=posMachine.machine).exists():		#CAN YOU EXPLAIN HERE TO
										messages.error(response, "Machine already added")
									else:
										posMachine.machine.projects.add(project)
										posMachine.save()
										for sensor in posMachine.machine.sensor_set.all():
											PossibleProjectSensors.objects.create(name=sensor.name, project=project, machine=posMachine.machine, modelID = sensor.modelID)

										for block in posMachine.machine.tiablocks_set.all():
											PossibleProjectTia.objects.create(name=block.name, project=project, machine=posMachine.machine)
										messages.success(response, "Machine added")								#HERE

								elif response.POST.get('removeMachine'):
									if project.machine_set.filter(name=posMachine.machine).exists():
										machineDel = project.machine_set.get(name=posMachine.machine)
										for sensor in machineDel.possibleprojectsensors_set.filter(project=project):
											print(sensor)
											project.possibleprojectsensors_set.get(name=sensor.name).delete()
										for block in machineDel.possibleprojecttia_set.filter(project=project):
											project.possibleprojecttia_set.get(name=block.name).delete()
										machineDel.projects.remove(project)
									else:
										messages.error(response, "machine not in project")

						else:
							messages.error(response, 'Machines already confirmed')

					if response.POST.get('machineConfirm'):
						if project.machine_set.first() is not None:
							if not project.machineConfirmed:
								project.machineConfirmed = True
								project.save()
								for machine in project.machine_set.all():
									if machine.name == 'Ply Cutter':
										for process in project.PLY_CUTTER_LIST:
											if not PossibleProjectProcess.objects.filter(name=process,project=project, machine=machine).exists():
												PossibleProjectProcess.objects.create(name=process, project=project, machine=machine)



									# if machine.name == 'Press':

									if machine.name == 'Preforming Cell':
										for process in project.PRE_CELL_LIST:
											if not PossibleProjectProcess.objects.filter(name=process,project=project, machine=machine).exists():
												PossibleProjectProcess.objects.create(name=process, project=project, machine=machine)

								if not project.possibleprojectprocess_set.all().exists():
									project.noSuggested = True
									project.save()
									return redirect(f'/adminTotalEditProcess{id}', permanent=True)
							else:  
								messages.error(response,"Machines already confirmed")
						else:
							messages.error(response,"Please add a machine")

					if (response.POST.get('addProcess') or response.POST.get('removeProcess')) and project.machineConfirmed :
						#need checks for manual here too
						possibleProForm = PossibleProForm(id, response.POST)

						if possibleProForm.is_valid():
							process = possibleProForm.cleaned_data['process']
							if response.POST.get('addProcess'):
								project.order_process()
								project.save()
								if not project.manual:
									if project.process_set.filter(name=process).exists():
										messages.error(response, "Process already added")
									else:
										posPro = project.possibleprojectprocess_set.get(name=process)
										createdPro = Process.objects.create(name=process.name, project=project)
										createdPro.machine.add(posPro.machine)
										createdPro.save()
										messages.success(response, "Process added")
								else:
									if project.process_set.filter(manualName=process).exists():
										messages.error(response, "Process already added")
									else:
										Process.objects.create(manualName=process.name, project=project)
										messages.success(response, "Process added")

							elif response.POST.get('removeProcess'):
								if not project.manual:
									if project.process_set.filter(name=process).exists():
										project.process_set.get(name=process).delete()
										messages.success(response, "Process removed")
									else:
										messages.error(response, "Process not available to delete")
								else:
									if project.process_set.filter(manualName=process).exists():
										project.process_set.get(manualName=process).delete()
										messages.success(response, "Process removed")
									else:
										messages.error(response, "Process not available to delete")

					if response.POST.get('confirmProcess') and project.machineConfirmed:
						if project.process_set.filter().exists():
							for process in project.process_set.all():
								subset = []
								if process.name == "Cut Plies":
									for subpro in Process.CUT_PLIES_SUB_LIST:
										if not PossibleSubProcesses.objects.filter(name = subpro, process = process).exists():			#GO THROUGH THIS
											PossibleSubProcesses.objects.create(name = subpro, process = process)

									if len(process.subprocess_set.all()) == 0:
										subset.append(process.subprocess_set.create(name="Cut Initialisation"))
										subset.append(process.subprocess_set.create(name="Backer Removal"))
										subset.append(process.subprocess_set.create(name="Vail Addition"))
										subset.append(process.subprocess_set.create(name="Cut Ply"))
										subset.append(process.subprocess_set.create(name="Unload Ply"))
										for subprocess in subset:
											if subprocess.name in SubProcess.PLY_LIST:
												subprocess.plyTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()
											elif subprocess.name in SubProcess.BLANKS_LIST:
												subprocess.blankTask = True 
												subprocess.save()

											# if here as need over lap between consolidation and other lists
											if subprocess.name in SubProcess.CONSOLIDATION_LIST:
												subprocess.consolidationCheck = True
												subprocess.save()																			#TO HERE

								elif process.name == "Create Blanks":
									for subpro in Process.CREATE_BLANKS_SUB_LIST:
										if not  PossibleSubProcesses.objects.filter(name = subpro, process = process).exists():
											PossibleSubProcesses.objects.create(name = subpro, process = process)
									if len(process.subprocess_set.all()) == 0:
										subset.append(process.subprocess_set.create(name="Blanks Initialisation"))
										subset.append(process.subprocess_set.create(name="Pickup Initial Ply"))
										subset.append(process.subprocess_set.create(name="Pickup Ply"))
										subset.append(process.subprocess_set.create(name="Weld"))
										subset.append(process.subprocess_set.create(name="Unload Blank"))
										for subprocess in subset:
											if subprocess.name in SubProcess.BLANKS_LIST:
												subprocess.blankTask = True
												subprocess.save()

											elif subprocess.name in SubProcess.PLY_LIST:
												subprocess.plyTask = True 
												subprocess.save()

											# if here as need over lap between consolidation and other lists
											if subprocess.name in SubProcess.CONSOLIDATION_LIST:
												subprocess.consolidationCheck = True
												subprocess.save()

								elif process.name == "Prep Material For Press":
									for subpro in Process.PREP_FOR_PRESS_SUB_LIST:
										if not PossibleSubProcesses.objects.filter(name = subpro, process = process).exists():
											PossibleSubProcesses.objects.create(name = subpro, process = process)
									if len(process.subprocess_set.all()) == 0:
										subset.append(process.subprocess_set.create(name="Lay Bottom Casette"))
										subset.append(process.subprocess_set.create(name="Lay Blank"))
										subset.append(process.subprocess_set.create(name="Lay Top Casette"))
										subset.append(process.subprocess_set.create(name="Unload Casette"))
										for subprocess in subset:
											if subprocess.name in SubProcess.BLANKS_LIST:
												subprocess.blankTask = True
												subprocess.save()

											elif subprocess.name in SubProcess.PLY_LIST:
												subprocess.plyTask = True 
												subprocess.save()

											elif subprocess.name in SubProcess.PART_LIST:
												subprocess.partTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()

											# if here as need over lap between consolidation and other lists
											if subprocess.name in SubProcess.CONSOLIDATION_LIST:
												subprocess.consolidationCheck = True
												subprocess.save()
								elif process.name == "Form Preform":
									for subpro in Process.FORM_PREFORM_SUB_LIST:
										if not PossibleSubProcesses.objects.filter(name = subpro, process = process).exists():
											PossibleSubProcesses.objects.create(name = subpro, process = process)
									if len(process.subprocess_set.all()) == 0:
										subset.append(process.subprocess_set.create(name="Initialisation"))
										subset.append(process.subprocess_set.create(name="Material Pressed"))
										subset.append(process.subprocess_set.create(name="Final Inspection"))
										for subprocess in subset:
											if subprocess.name in SubProcess.PART_LIST:
												subprocess.partTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()
											elif subprocess.name in SubProcess.PLY_LIST:
												subprocess.plyTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()
											elif subprocess.name in SubProcess.BLANKS_LIST:
												subprocess.blankTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()

											elif subprocess.name in SubProcess.BLANKS_LIST:
												subprocess.blankTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()

											# if here as need over lap between consolidation and other lists
											if subprocess.name in SubProcess.CONSOLIDATION_LIST:
												subprocess.consolidationCheck = True
												subprocess.save()

								elif process.name == "Pre Heat":
									for subpro in Process.PRE_HEAT_SUB_LIST:
										if not PossibleSubProcesses.objects.filter(name = subpro, process = process).exists():
											PossibleSubProcesses.objects.create(name = subpro, process = process)
									if len(process.subprocess_set.all()) == 0:
										subset.append(process.subprocess_set.create(name="Load"))
										subset.append(process.subprocess_set.create(name="Heating"))
										subset.append(process.subprocess_set.create(name="Unload"))
										for subprocess in subset:
											if subprocess.name in SubProcess.PART_LIST:
												subprocess.partTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()
											elif subprocess.name in SubProcess.PLY_LIST:
												subprocess.plyTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()
											elif subprocess.name in SubProcess.BLANKS_LIST:
												subprocess.blankTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()

											elif subprocess.name in SubProcess.BLANKS_LIST:
												subprocess.blankTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()

											# if here as need over lap between consolidation and other lists
											if subprocess.name in SubProcess.CONSOLIDATION_LIST:
												subprocess.consolidationCheck = True
												subprocess.save()
								elif process.name == "Destination":
									for subpro in Process.DESTINATION_SUB_LIST:
										if not PossibleSubProcesses.objects.filter(name = subpro, process = process).exists():
											PossibleSubProcesses.objects.create(name = subpro, process = process)
									if len(process.subprocess_set.all()) == 0:
										subset.append(process.subprocess_set.create(name="Mould moves to loading"))
										subset.append(process.subprocess_set.create(name="Inserts Heated"))
										subset.append(process.subprocess_set.create(name="Mould loaded"))
										subset.append(process.subprocess_set.create(name="Mould moves into press"))
										for subprocess in subset:
											if subprocess.name in SubProcess.PART_LIST:
												subprocess.partTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()
											elif subprocess.name in SubProcess.PLY_LIST:
												subprocess.plyTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()
											elif subprocess.name in SubProcess.BLANKS_LIST:
												subprocess.blankTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()

											elif subprocess.name in SubProcess.BLANKS_LIST:
												subprocess.blankTask = True
												# repeat saves as one didnt work for some sub pros (for no reason)
												subprocess.save()

											# if here as need over lap between consolidation and other lists
											if subprocess.name in SubProcess.CONSOLIDATION_LIST:
												subprocess.consolidationCheck = True
												subprocess.save()
							project.processConfirmed = True
							project.save()
							project.update_process_positions()
							for process in project.process_set.all():
								process.update_subprocess_positions()
							return redirect(f'/adminViewAllProcess{id}', permanent=True)
						else:
							messages.error(response, 'No process added!')
				
				return render(response, 'Admin/assignHardware.html', {'project':project, 'machineForm':machineForm, 'possibleProForm':possibleProForm})
			else:
				redirect('/')
	else:
		redirect('mylogout/')

def admin_edit(response, id):
	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
			return redirect('/')
		
		if admin:
			project = Project.objects.get(id=id)
			possibleProForm = PossibleProForm(id)
			UserProForm = UserDefineProSub()
			count = 0
			if project.machineConfirmed:
				if project in response.user.profile.user_company.project_set.all():
					if project.editStatus != 1:
						project.process_set.all().delete()
						project.editStatus = 1
						project.save()
					if response.method == 'POST':
						if (response.POST.get('addProcess') or response.POST.get('removeProcess')) and project.machineConfirmed :
							#need checks for manual here too
							possibleProForm = PossibleProForm(id, response.POST)

							if possibleProForm.is_valid():
								process = possibleProForm.cleaned_data['process']
								if response.POST.get('addProcess'):
									if not project.manual:
										if project.process_set.filter(name=process).exists():
											messages.error(response, "Process already added")
										else:
											Process.objects.create(name=process.name, project=project)
											count = 0
											for each in project.order_process():
												each.position = count
												each.save()
												count+=1
											messages.success(response, "Process added")
									else:
										if project.process_set.filter(manualName=process).exists():
											messages.error(response, "Process already added")
										else:
											Process.objects.create(manualName=process.name, project=project)
											count = 0
											for each in project.order_process():
												each.position = count
												each.save()
												count+=1
											messages.success(response, "Process added")

								elif response.POST.get('removeProcess'):
									if not project.manual:
										if project.process_set.filter(name=process).exists():
											project.process_set.get(name=process).delete()
											messages.success(response, "Process removed")
										else:
											messages.error(response, "Process not available to delete")
									else:
										if project.process_set.filter(manualName=process).exists():
											project.process_set.get(manualName=process).delete()
											messages.success(response, "Process removed")
										else:
											messages.error(response, "Process not available to delete")

						if response.POST.get('confirmProcess') and project.machineConfirmed:
							if project.process_set.filter().exists():
								for process in project.process_set.all():
									if process.name == "Cut Plies":
										for subpro in Process.CUT_PLIES_SUB_LIST:
											PossibleSubProcesses.objects.create(name = subpro, process = process)
									elif process.name == "Create Blanks":
										for subpro in Process.CREATE_BLANKS_SUB_LIST:
											PossibleSubProcesses.objects.create(name = subpro, process = process)
									elif process.name == "Prep Material For Press":
										for subpro in Process.PREP_FOR_PRESS_SUB_LIST:
											PossibleSubProcesses.objects.create(name = subpro, process = process)
									elif process.name == "Form Preform":
										for subpro in Process.FORM_PREFORM_SUB_LIST:
											PossibleSubProcesses.objects.create(name = subpro, process = process)
								project.processConfirmed = True
								project.editStatus = 1
								project.save()
								return redirect(f'/adminViewAllProcess{id}', permanent=True)
							else:
								messages.error(response, 'No process added!')

						if response.POST.get('addUserProcess') or response.POST.get('removeUserProcess'):
							UserProForm = UserDefineProSub(response.POST)
							if UserProForm.is_valid():
								#get cleaned project name
								n = UserProForm.cleaned_data['name']
								if response.POST.get('addUserProcess'):
									#if project exists show error
									if project.process_set.filter(name=n).exists():
										messages.error(response, 'Process already in list!')
									#if project doesnt exist create one and save
									else:
										p = Process.objects.create(name=n, project=project, editProcess=True)
										for each in project.process_set.all():
												each.position = count
												each.save()
												count+=1
										p.save()
								#check response type
								elif response.POST.get('removeUserProcess'):
									#check if project exists and delete
									if project.process_set.filter(name=n).exists():
										p = project.process_set.get(name=n)
										p.delete()
										messages.success(response, 'Process successfully deleted!')
									#show error if project doesnt exist
									else:
										messages.error(response, 'Process not in list!')

					return render(response, 'Admin/editProcess.html', {'project':project, 'possibleProForm':possibleProForm, 'UserProForm':UserProForm})
				else:
					redirect('/')
			else:
				redirect('/')
	else:
		redirect('mylogout/')

def admin_total_edit(response, id):
	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
			return redirect('/')
		
		if admin:
			project = Project.objects.get(id=id)
			UserProForm = UserDefineProSub()
			if project in response.user.profile.user_company.project_set.all():
				if project.editStatus != 2:
					project.process_set.all().delete()
				if response.method == 'POST':
					project.editStatus = 2
					project.save()
					if response.POST.get('confirmProcess') and project.machineConfirmed:
						if project.process_set.filter().exists():
							for process in project.process_set.all():
								if process.name == "Cut Plies":
									for subpro in Process.CUT_PLIES_SUB_LIST:
										PossibleSubProcesses.objects.create(name = subpro, process = process)
								elif process.name == "Create Blanks":
									for subpro in Process.CREATE_BLANKS_SUB_LIST:
										PossibleSubProcesses.objects.create(name = subpro, process = process)
								elif process.name == "Prep Material For Press":
									for subpro in Process.PREP_FOR_PRESS_SUB_LIST:
										PossibleSubProcesses.objects.create(name = subpro, process = process)
								elif process.name == "Form Preform":
									for subpro in Process.FORM_PREFORM_SUB_LIST:
										PossibleSubProcesses.objects.create(name = subpro, process = process)
							project.processConfirmed = True
							project.editStatus = 2
							project.save()
							return redirect(f'/adminViewAllProcess{id}', permanent=True)
						else:
							messages.error(response, 'No process added!')

					if response.POST.get('addUserProcess') or response.POST.get('removeUserProcess'):
						UserProForm = UserDefineProSub(response.POST)
						if UserProForm.is_valid():
							#get cleaned project name
							n = UserProForm.cleaned_data['name']
							if response.POST.get('addUserProcess'):
								#if project exists show error
								if project.process_set.filter(name=n).exists():
									messages.error(response, 'Process already in list!')
								#if project doesnt exist create one and save
								else:
									p = Process.objects.create(name=n, project=project, editProcess=True)
									p.save()
							#check response type
							elif response.POST.get('removeUserProcess'):
								#check if project exists and delete
								if project.process_set.filter(name=n).exists():
									p = project.process_set.get(name=n)
									p.delete()
									messages.success(response, 'Process successfully deleted!')
								#show error if project doesnt exist
								else:
									messages.error(response, 'Process not in list!')

				return render(response, 'Admin/totalEditProcess.html', {'project':project, 'UserProForm':UserProForm})
			else:
				redirect('/')
	else:
		redirect('mylogout/')

def admin_view_all_process(response, id):
	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
			return redirect('/')
		if admin:
			project = Project.objects.get(id=id)
			if project.machineConfirmed:
				if project in response.user.profile.user_company.project_set.all():
					return render(response, 'Admin/adminViewAllProcess.html', {'project':project})
				else:
					redirect('/')
			else:
				redirect('/')
	else:
		redirect('/mylogout')

def admin_view_process(response, id):
	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
			return render('/')
		if admin:
			if Process.objects.filter(id=id).exists():
				process = Process.objects.get(id=id)
			else:
				return redirect('/')
			project = process.project
			UserSubForm = UserDefineProSub()
			repeat_block_form = AddRepeatBlock(process)
			if project.machineConfirmed:
				if project.manual:
					addSubForm = addManualSubProcess()
				else:
					addSubForm = PossibleSubProForm(id)
				addSensorForm = SensorForm(project, process.machine.first())
				deletion = False
				if deletion == False:				#whats the point?
					sensorSet = Sensor.objects.none()			#what does .none() do?
					select_sensor_form = SelectSensorFormAdmin(sensorSet)
				if process.project in response.user.profile.user_company.project_set.all():		#not just do if project?
					if response.method == 'POST':
						if response.POST.get('addSubProcess') or response.POST.get('removeSubProcess'):
							if project.manual:
								addSubForm = addManualSubProcess(response.POST)
							else:
								addSubForm = PossibleSubProForm(id, response.POST)
							if addSubForm.is_valid():
								if project.manual:
									reqSubProcessDirty = addSubForm.cleaned_data['manualName']
									reqSubProcess = SubProcess.manual_sub_process_dict[reqSubProcessDirty]			#why do we do this for manuel forms?
								else:
									reqSubProcessDirty = addSubForm.cleaned_data['name']
									reqSubProcess= addSubForm.cleaned_data['name']
								
								weighPoint = addSubForm.cleaned_data['weightPoint']  			#is it weightpoint or weighpoint?
								finalWeighPoint = addSubForm.cleaned_data['finalWeighPoint']

								if weighPoint and finalWeighPoint:
									messages.error(response, "Can't be a weigh point and final weigh point!")
								else:
									#check what information is being passed
									if response.POST.get('addSubProcess'):
										#check if sub process exists
										if process.subprocess_set.filter(name=reqSubProcess) or process.subprocess_set.filter(manualName=reqSubProcess):
											messages.error(response,"This Sub Process already exists!")
										#if sub process doesn't exist create it
										else:
											if process.project.manual:
												#check if sub process is a 'process task'
												if reqSubProcessDirty == 'material_pressed' or reqSubProcessDirty == 'final_inspection':
													#create sub process and set processCheck
													process.subprocess_set.create(manualName=reqSubProcess, processCheck=True, weighPoint=weighPoint, finalWeighPoint=finalWeighPoint)				#what does processCheck do?
												else:
													#create sub process
													process.subprocess_set.create(manualName=reqSubProcess, weighPoint=weighPoint, finalWeighPoint=finalWeighPoint)

												#display success
												messages.success(response,"Sub Process sucessfully added!")
												process.update_subprocess_positions()

											else:
												#check if sub process is a 'process task'
												if reqSubProcessDirty == 'material_pressed' or reqSubProcessDirty == 'final_inspection':
													#create sub process and set processCheck
													process.subprocess_set.create(name=reqSubProcess, processCheck=True, weighPoint=weighPoint, finalWeighPoint=finalWeighPoint)
												else:
													#create sub process
													process.subprocess_set.create(name=reqSubProcess, weighPoint=weighPoint, finalWeighPoint=finalWeighPoint)

												if reqSubProcess.name in SubProcess.PLY_LIST:
													subPro = process.subprocess_set.get(name=reqSubProcess)				#could this be taken out the if statement?
													subPro.plyTask = True
													# repeat saves as one didnt work for some sub pros (for no reason)
													subPro.save()

												elif reqSubProcess.name in SubProcess.BLANKS_LIST:
													subPro = process.subprocess_set.get(name=reqSubProcess)
													subPro.blankTask = True
													subPro.save()

												elif reqSubProcess.name in SubProcess.PART_LIST:
													subPro = process.subprocess_set.get(name=reqSubProcess)
													subPro.partTask = True
													subPro.save()

												# if here as need over lap between consolidation and other lists
												if reqSubProcess.name in SubProcess.CONSOLIDATION_LIST:
													subPro = process.subprocess_set.get(name=reqSubProcess)
													subPro.consolidationCheck = True
													subPro.save()

												process.update_subprocess_positions()
												#display success
												messages.success(response,"Sub Process sucessfully added!")

									if response.POST.get('removeSubProcess'):
										#if sub process exists delete it
										pName = ""
										if process.subprocess_set.filter(manualName=reqSubProcess).exists() or process.subprocess_set.filter(name=reqSubProcess).exists():
											if process.project.manual:
												p = process.subprocess_set.get(manualName=reqSubProcess)
												pName = p.manualName
												processName = process.manualName
											else:	
												p = process.subprocess_set.get(name=reqSubProcess)
												pName = p.name
												processName = process.name
											
											if processName == "Form Preform":
												if pName == "Initialisation" or pName == "Material Pressed" or pName == "Final Inspection":
													messages.error(response,"You cannot delete this Sub-Process because it is vital to Form Preform")
												else:
													p.delete()
													messages.success(response,"Sub Process sucessfully deleted!")
											else:
												p.delete()
												messages.success(response,"Sub Process sucessfully deleted!")

										#if sub process doesn't exist display error
										else:
											messages.error(response,'Sub Process does not exist!')


						#check to stop sensorform.is_valid displaying error on other form
						if (response.POST.get('addSensor') or response.POST.get('removeSensor')):
							addSensorForm = SensorForm(project, process.machine.first(), response.POST)
							if addSensorForm.is_valid():
								#read in and clean sensor name
								reqSensorDirty = addSensorForm.cleaned_data['sensor']
								# reqSensor = Sensor.sensor_choices_dict[reqSensorDirty]

								#check response type
								if response.POST.get('addSensor'):
									#check if sensor exists and show error
									if process.sensor_set.filter(name=reqSensorDirty).exists():
										messages.error(response, 'Sensor Already added!')			#why does the response need to be passed through here?
									else:
										name = project.possibleprojectsensors_set.get(name=reqSensorDirty)
										s = Sensor.objects.get(name=name, modelID=name.modelID)
										process.sensor_set.add(s)
										messages.success(response, 'Sensor successfully added!')
								#check response type
								elif response.POST.get('removeSensor'):
									#if sensor exists delete
									if process.sensor_set.filter(name=reqSensorDirty).exists():
										sensor = process.sensor_set.filter(name=reqSensorDirty).first()
										
										if len(process.sensor_set.filter(name=reqSensorDirty)) > 1:
											messages.error(response, "Select a Sensor to delete!")
											sensorSet = process.sensor_set.filter(name=reqSensorDirty)
											deletion = True
											select_sensor_form = SelectSensorFormAdmin(sensorSet, response.POST)
										else:
											process.sensor_set.remove(sensor)

											messages.success(response, 'Sensor successfully deleted!')
									else:
										messages.error(response,"Sensor does not exist!")

								
						if response.POST.get('addRepeatBlock'):				#run through this
							repeat_block_form = AddRepeatBlock(process, response.POST)

							if repeat_block_form.is_valid():
								start, end = False,False

								start_sub_pro = repeat_block_form.cleaned_data['start']
								end_sub_pro = repeat_block_form.cleaned_data['end']
								iterations = repeat_block_form.cleaned_data['value']

								
								repeat_block = process.repeatblock_set.create(number_of_iterations = iterations, iteration = 0)

								startPos = start_sub_pro.position
								endPos = end_sub_pro.position + 1

								for instance in range(startPos, endPos):
									if instance == startPos:
										start = True
									elif instance == endPos - 1:
										end = True
									else:
										start,end=False,False

									sub_pro = process.subprocess_set.get(position=instance)
									sub_pro.repeat = True 
									sub_pro.save()
									repeat_block.repeatblocksubprocesses_set.create(sub_process = sub_pro, start=start, end=end)


						if response.POST.get('addUserSubProcess') or response.POST.get('removeUserSubProcess'):
							UserSubForm = UserDefineProSub(response.POST)
							if UserSubForm.is_valid():
								#get cleaned project name
								n = UserSubForm.cleaned_data['name']
								weighPoint = UserSubForm.cleaned_data['weightPoint']
								finalWeighPoint = UserSubForm.cleaned_data['finalWeighPoint']
								partTask = UserSubForm.cleaned_data['partTask']
								plyTask = UserSubForm.cleaned_data['plyTask']
								blankTask = UserSubForm.cleaned_data['blankTask']
								consolidationCheck = UserSubForm.cleaned_data['consolidationCheck']
								if response.POST.get('addUserSubProcess'):
									if weighPoint and finalWeighPoint:
										messages.error(response, "Can't be a weigh point and final weigh point!")
									elif (partTask == False and plyTask == False and blankTask == False) or (partTask and plyTask) or (partTask and blankTask) or (plyTask and blankTask) or (partTask and plyTask and blankTask):
										messages.error(response, 'One type of Task needs to be chosen!')

									else:
										#if sub process exists show error
										if process.subprocess_set.filter(name=n).exists():
											messages.error(response, 'Sub Process already in list!')
										#if sub process doesnt exist create one and save
										else:
											p = SubProcess.objects.create(name=n, process=process, weighPoint=weighPoint, finalWeighPoint=finalWeighPoint)
											p.save()
								#check response type
								elif response.POST.get('removeUserSubProcess'):
									#check if sub process exists and delete
									if process.subprocess_set.filter(name=n).exists():
										p = process.subprocess_set.get(name=n)
										p.delete()
										messages.success(response, 'Sub Process successfully deleted!')
									#show error if project doesnt exist
									else:
										messages.error(response, 'Sub Process not in list!')
							UserSubForm = UserDefineProSub()
					return render(response, 'Admin/adminViewProcess.html', {'repeat_block_form':repeat_block_form,  'process':process, 'addSubForm':addSubForm, 'addSensorForm':addSensorForm, 'select_sensor_form':select_sensor_form, 'deletion':deletion, 'UserSubForm':UserSubForm})
				else:
					redirect('/')
			else:
				redirect('/')
		else:
			return redirect('/')
	else:
		redirect('/mylogout')


def admin_view_sub(response, id):

	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
			return redirect('/')
		if admin:
			if SubProcess.objects.filter(id=id).exists():
				subProcess = SubProcess.objects.get(id=id)
			else:
				return redirect('/')
			addSensorForm = SensorForm(subProcess.process.project, subProcess.process.machine.first())
			addBlockForm = AddTiaBlock(subProcess.process.project, subProcess.process.machine.first())
			editCriterionForm = EditCriterionForm()
			processCheckForm = ProcessCheckForm()
			if subProcess.process.project in response.user.profile.user_company.project_set.all():
				if response.method == 'POST':
					#check to stop sensorform.is_valid displaying error on other form
					if (response.POST.get('addSensor') or response.POST.get('removeSensor')):
						addSensorForm = SensorForm(subProcess.process.project, subProcess.process.machine.first(), response.POST)
						if addSensorForm.is_valid():
							#read in and clean sensor name
							reqSensorDirty = addSensorForm.cleaned_data['sensor']

							#check response type
							if response.POST.get('addSensor'):
								#check if sensor exists and show error
								if subProcess.sensor_set.filter(name=reqSensorDirty).exists():
									messages.error(response, 'Sensor Already added!')
								else:
									s = Sensor.objects.get(name=reqSensorDirty, modelID = reqSensorDirty.modelID)
									
									s.name=reqSensorDirty
									# not needed i dont think?
									# s.subProcess=subProcess
									subProcess.sensor_set.add(s)
									messages.success(response, 'Sensor successfully added!')
							#check response type
							elif response.POST.get('removeSensor'):
								#if sensor exists delete
								if subProcess.sensor_set.filter(name=reqSensorDirty).exists():
									sensor= subProcess.sensor_set.filter(name=reqSensorDirty).first()
									if len(subProcess.sensor_set.filter(name=reqSensorDirty)) > 1:
										messages.error(response, "Select a Sensor to delete!")
										sensorSet = subProcess.sensor_set.filter(name=reqSensorDirty)
										deletion = True
										select_sensor_form = SelectSensorFormAdmin(sensorSet, response.POST)
									else:
										subProcess.sensor_set.remove(sensor)

										messages.success(response, 'Sensor successfully deleted!')
								else:
									messages.error(response,"Sensor does not exist!")

					if response.POST.get('addTia') or response.POST.get('removeTia'):
						addBlockForm = AddTiaBlock(subProcess.process.project, subProcess.process.machine.first(), response.POST)
						if addBlockForm.is_valid():
							choice=addBlockForm.cleaned_data['choice']
							if response.POST.get('addTia'):
								if subProcess.tiablocks_set.filter(name=choice).exists():
									messages.error(response, 'Block already assigned')
								else:
									block = TiaBlocks.objects.get(name=choice)
									subProcess.tiablocks_set.add(block)
									block.save()
							elif response.POST.get('removeTia'):
								if subProcess.tiablocks_set.filter(name=choice).exists():
									block = TiaBlocks.objects.get(name=choice)
									subProcess.tiablocks_set.remove(block)
								else:
									messages.error(response, 'Block doesnt exist')

					if response.POST.get('submitCriterion'):
						editCriterionForm = EditCriterionForm(response.POST)

						if editCriterionForm.is_valid():
							criterion = editCriterionForm.cleaned_data['criterion']
							subProcess.criterion = criterion
							subProcess.save()
					
					if response.POST.get('submitProcessCheck'):
						processCheckForm = ProcessCheckForm(response.POST)

						if processCheckForm.is_valid():
							value = processCheckForm.cleaned_data['process_check']
							subProcess.processCheck = value 
							subProcess.save()


				return render(response, 'Admin/adminViewSub.html', {'processCheckForm':processCheckForm, 'editCriterionForm':editCriterionForm, 'addSensorForm':addSensorForm, 'subProcess':subProcess, 'addBlockForm':addBlockForm})
	else:
		redirect('/mylogout')


def updatePositions(response, id):

	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
			return redirect('/')
		if admin:
			pro  = Process.objects.get(id=id)
			if pro.project in response.user.profile.user_company.project_set.all():
				x = response.POST.dict()
				positions,order = [], []
				count = 0
				#--get current positions--#
				for subPro in pro.order_subprocess_custom():
					positions.append(subPro.position)

				#--get positions after movement--#
				positions.insert(int(x['index']), positions.pop(int(x['old'])))				#explain pls
				#--get new order of subpros--#
				for i in range(0,len(positions)):
					order.append(pro.subprocess_set.all().get(position=positions[i]))

				#--set new positions using order--#
				for instance in order:
					instance.position = count
					instance.save()
					count+=1

				#--start and end point assigning--#
				count = 0
				for every in pro.order_subprocess_custom():
					if every.position == 0 and every.process.initialised is False:
						every.startPoint = True
						every.endPoint = False
					elif every.position == len(pro.order_subprocess_custom())-1:
						every.endPoint = True
						every.startPoint = False
					elif every.position == 1 and every.process.initialised is True:
						every.startPoint = True 
						every.endPoint = False
					else:
						every.startPoint = False
						every.endPoint = False
					every.save()

				return redirect('/'+str(pro.id))
			else:
				return redirect('/')
	else:
		return redirect('/')

def updateProPositions(response, id):
	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
			return redirect('/')
		if admin:
			project  = Project.objects.get(id=id)
			if project in response.user.profile.user_company.project_set.all():
				x = response.POST.dict()
				positions,order = [], []
				count = 0
				#--get current positions--#
				for pro in project.order_process():
					positions.append(pro.position)

				#--get positions after movement--#
				positions.insert(int(x['index']), positions.pop(int(x['old'])))
				#--get new order of subpros--#
				for i in range(0,len(positions)):
					order.append(project.process_set.all().get(position=positions[i]))

				#--set new positions using order--#
				for instance in order:
					instance.position = count
					instance.save()
					count+=1

				return redirect('/adminViewAllProcess'+str(project.id))
			else:
				return redirect('/')
	else:
		return redirect('/')

def admin_edit_repeat_block(response, id):
	if response.user.is_authenticated:
		if response.user.groups.filter(name='Admin').exists():
			admin = True
		else:
			admin = False
			return redirect('/')
		if admin:
			repeat_block = RepeatBlock.objects.get(id=id)
			process=repeat_block.process
			repeat_block_form = AddRepeatBlock(process)

			startSub = repeat_block.repeatblocksubprocesses_set.get(start=True).sub_process
			endSub = repeat_block.repeatblocksubprocesses_set.get(end=True).sub_process

			if response.POST.get('addRepeatBlock'):
				repeat_block_form = AddRepeatBlock(process, response.POST)

				if repeat_block_form.is_valid():
					start, end = False,False

					start_sub_pro = repeat_block_form.cleaned_data['start']
					end_sub_pro = repeat_block_form.cleaned_data['end']
					iterations = repeat_block_form.cleaned_data['value']

					repeat_block.repeatblocksubprocesses_set.delete()
					repeat_block.number_of_iterations = iterations 
					repeat_block.iteration = 0

					repeat_block.save()

					startPos = start_sub_pro.position
					endPos = end_sub_pro.position + 1

					for instance in range(startPos, endPos):
						if instance == startPos:
							start = True
						elif instance == endPos - 1:
							end = True
						else:
							start,end=False,False

						sub_pro = process.subprocess_set.get(position=instance)
						sub_pro.repeat = True 
						sub_pro.save()
						repeat_block.repeatblocksubprocesses_set.create(sub_process = sub_pro, start=start, end=end)
					return redirect('/adminEditRepeatBlock'+str(repeat_block.id))

	return render(response, 'Admin/adminEditRepeatBlock.html', {'repeat_block_form':repeat_block_form,'process':process, 'repeat_block':repeat_block, 'startSub':startSub, 'endSub':endSub})

	