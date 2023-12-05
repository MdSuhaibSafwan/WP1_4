from django.test import TestCase, Client
from django.db.models import ForeignKey
from datetime import datetime,date,time,timedelta, timezone
from django.urls import reverse, resolve
import json
from django.contrib.auth.models import User, Group
from django.test.utils import setup_test_environment 
from http import HTTPStatus
from .models import *
from .forms import * 
from.views import *


class UrlTests(TestCase):
	
	def test_home_url(self):
		url = reverse('index')
		self.assertEqual(resolve(url).func, index)
		
	def test_show_projects_url(self):
		url = reverse('showProjects')
		self.assertEqual(resolve(url).func, showProjects)
		
	def test_show_process_url(self):
		url = reverse('showProcess', kwargs={'id':1})
		self.assertEqual(resolve(url).func, showProcess)

	def test_show_sub_process_url(self):
		url = reverse('showSub', kwargs={'id':1})
		self.assertEqual(resolve(url).func, showSubProcess)
		
	def test_show_all_process_url(self):
		url = reverse('showAllProcess', kwargs={'id':1})
		self.assertEqual(resolve(url).func, showAllProcess)
		
	def test_show_environ_sensors_url(self):
		url = reverse('showEnvironSensors', kwargs={'id':1})
		self.assertEqual(resolve(url).func, showEnvironSensors)
		
	def test_environ_graph_url(self):
		url = reverse('environGraph', kwargs={'id':1})
		self.assertEqual(resolve(url).func, environGraph)
		
	def test_machine_health_url(self):
		url = reverse('machineHealth', kwargs={'id':1})
		self.assertEqual(resolve(url).func, machineHealth)
		
	def test_show_machine_health_url(self):
		url = reverse('machineHealthShow', kwargs={'id':1})
		self.assertEqual(resolve(url).func, machineHealthShow)
		
	def test_popup_url(self):
		url = reverse('popUp', kwargs={'id':1})
		self.assertEqual(resolve(url).func, popUp)

	def test_system_architecture_url(self):
		url = reverse('systemArchitecture', kwargs={'id':1})
		self.assertEqual(resolve(url).func, systemArchitecture)

	def test_final_inspection_url(self):
		url = reverse('finalInspection', kwargs={'id':1})
		self.assertEqual(resolve(url).func, showSubProcess)		

	def test_final_url(self):
		url = reverse('final', kwargs={'id':1})
		self.assertEqual(resolve(url).func, final)

	def test_part_save_url(self):
		url = reverse('partSave', kwargs={'id':1,'bad':'1'})
		self.assertEqual(resolve(url).func, partSave)		
	
	def test_upload_url(self):
		url = reverse('upload')
		self.assertEqual(resolve(url).func, showSubProcess)		

	# architecture, FI
	
class ModelTests(TestCase):
	"""Class to test all Main app models"""
	
	def setUp(self):
		"""Set up for all Main tests"""
		self.company = Company.objects.create(company_name = 'Test Company')
		self.project = Project.objects.create(project_name = 'Test Project', company = self.company)
		self.process = Process.objects.create(name = 'Test Process', project = self.project)
		self.manualProcess = Process.objects.create(manualName = 'Test Process', project = self.project)
		self.subProcess = SubProcess.objects.create(name = 'Test SubProcess', process = self.process)
		 
	def test_company_creation(self):
		"""Test if Companies are created correctly"""
		company = Company.objects.get(id=self.company.id)
		self.assertEqual(self.company, company)
		
	def test_project_creation(self):		
		"""Test if Projects are created correctly"""
		project = Project.objects.get(id=self.project.id)
		self.assertEqual(self.project, project)
	
	def test_project_company_relation(self):
		"""Test if Project to Company relations are created correctly"""
		self.assertEqual(self.company, self.project.company)		
		
	def test_project_fields(self):
		"""Test if Project fields are saved correctly"""
		project = self.project
		
		project.priceKG = 10
		project.priceM2 = 10
		project.materialDensity = 10
		project.techRate = 10
		project.superRate = 10
		project.assumedCost = 4.1
		project.powerRate = 10
		project.manual = True
		project.nominalPartWeight = 10
		project.nominalPartLength = 10
		project.nominalPartWidth = 10
		project.nominalPartThickness = 10
		project.setupCost = 10

 		
		project.save()
 		
		project_query = Project.objects.get(id=project.id)
 		
		self.assertEqual(project, project_query)

	def test_process_fields(self):
		"""Test if Project fields are saved correctly"""
		process = Process.objects.create(name = 'Test Process', project = self.project)
		
		process.operator = 'test operator'
		process.labourInput = 10
		process.cycle = timedelta(seconds=4)
		process.processTime = timedelta(seconds=4)
		process.jobStart = datetime(2022, 8, 10, tzinfo=timezone.utc)
		process.jobEnd = datetime(2022, 8, 10, tzinfo=timezone.utc)
		process.processStart = datetime(2022, 8, 10, tzinfo=timezone.utc)
		process.processEnd = datetime(2022, 8, 10, tzinfo=timezone.utc)
		process.interfaceTime = timedelta(seconds=4)
		process.badPart = True
		process.scrapRate = 40
		process.minBatchSize = 70
		process.maxBatchSize = 70
		process.power = 90
		process.status = 2
		process.processCheck = True
		process.qualityCheck = True

		process.save()
 		
		process_query = Process.objects.get(id=process.id)
 		
		self.assertEqual(process, process_query)

	def test_process_project_realtion(self):
		"""Test if Process to Project relations are created correctly"""
		self.assertEqual(self.process.project, self.project)
 		
	def test_manual_process_project_realtion(self):
		"""Test if Manual Process to Project relations are created correctly"""
		self.assertEqual(self.manualProcess.project, self.project)
	
	def test_subprocess_process_realtion(self):
		"""Test if SubProcess to Process relations are created correctly"""
		self.assertEqual(self.subProcess.process, self.process)	
		
	def test_subprocess_fields(self):
		subProcess = SubProcess.objects.create(name = 'Test SubProcess', process = self.process)
		
		subProcess.operator = 'test operator'
		subProcess.labourInput = 10
		subProcess.cycle = datetime(2022, 8, 10, tzinfo=timezone.utc)
		subProcess.processTime = timedelta(seconds=4)
		subProcess.jobStart = datetime(2022, 8, 10, tzinfo=timezone.utc)
		subProcess.jobEnd = datetime(2022, 8, 10, tzinfo=timezone.utc)
		subProcess.processStart = datetime(2022, 8, 10, tzinfo=timezone.utc)
		subProcess.processEnd = datetime(2022, 8, 10, tzinfo=timezone.utc)
		subProcess.interfaceTime = timedelta(seconds=4)
		subProcess.badPart = True
		subProcess.scrapRate = 40
		subProcess.minBatchSize = 70
		subProcess.maxBatchSize = 70
		subProcess.power = 90
		subProcess.status = 2
		subProcess.processCheck = True
		subProcess.qualityCheck = True

		subProcess.save()
 		
		subProcess_query = SubProcess.objects.get(id=subProcess.id)
 		
		self.assertEqual(subProcess, subProcess_query)
		
class ViewTests(TestCase):
	
	def setUp(self):
		self.client = Client()
		self.project_url = reverse('showProjects')
		self.mang_group = Group(name='Management')
		self.mang_group.save() 
		self.super_group = Group(name='Supervisor')
		self.super_group.save()
		self.company = Company.objects.create(company_name = 'Test Company')
		self.user = User.objects.create_user(username='Test User', email='test@test.com', password='Test')
		self.user.profile.user_company = self.company
		self.failureCompany = Company.objects.create(company_name = 'Failure Company')
		self.project = Project.objects.create(company=self.company, project_name='Test Project')
		self.failureProject= Project.objects.create(company=self.company, project_name='Failure Project')
		self.process = Process.objects.create(project=self.project, name= 'Test Process')
		self.subprocess = SubProcess.objects.create(process=self.process, name= 'Test SubProcess')
		self.finalInspection = SubProcess.objects.create(process=self.process, name= 'Final Inspection', id=2)
		self.all_process_url = reverse('showAllProcess', kwargs={'id':self.project.id})
		self.all_sub_process_url = reverse('showProcess', kwargs={'id':self.process.id})
		self.all_sub_process_detail_url = reverse('showSub', kwargs={'id':self.subprocess.id})
		self.system_architecture_url = reverse('systemArchitecture', kwargs={'id':1})
		self.final_inspection_url = reverse('finalInspection', kwargs={'id':2})
		self.client.login(username='Test User', password='Test')
		
		
	def test_show_project_page_no_return(self):				
		response = self.client.post(self.project_url)			
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_show_project_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()		
		
		response = self.client.post(self.project_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Main/showProjects.html')
		
	def test_project_belong_to_user(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()		
		
		response = self.client.post(self.project_url)
		
		self.assertQuerysetEqual(self.user.profile.user_company.project_set.all(), response.context['user'].profile.user_company.project_set.all(), transform=lambda 	x: x, ordered=False)
		
	def test_process_page_no_return(self):	
		self.user.save()					
			
		response = self.client.post(self.all_process_url)
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_process_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()			
			
		response = self.client.post(self.all_process_url)
		
		self.assertTemplateUsed(response, 'Main/showAllProcess.html')
		self.assertEqual(response.status_code, 200)
		
	#def test_process_page_func(self):
#		self.user.groups.add(self.mang_group, self.super_group)
#		self.user.save()			
#		
#		response = self.client.post(self.all_process_url, {})
		
				
	def test_subprocess_page_no_return(self):
		self.user.save()
		response = self.client.post(self.all_sub_process_url)
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
	
	def test_subprocess_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()			
			
		response = self.client.post(self.all_sub_process_url)
		
		self.assertTemplateUsed(response, 'Main/showProcess.html')
		self.assertEqual(response.status_code, 200)
	
	def test_subprocess_detail_page_no_return(self):
		self.user.save()
		response = self.client.post(self.all_sub_process_detail_url)
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_subprocess_detail_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()			
			
		response = self.client.post(self.all_sub_process_detail_url)
		
		self.assertTemplateUsed(response, 'Main/components.html')
		self.assertEqual(response.status_code, 200)
		
	def test_system_architecture_page_no_return(self):
		self.user.save()
		response = self.client.post(self.system_architecture_url)
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_system_architecture_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()			
			
		response = self.client.post(self.system_architecture_url)
		
		self.assertTemplateUsed(response, 'Main/showSystemArchitecture.html')
		self.assertEqual(response.status_code, 200)

	def test_final_inspection_page_no_return(self):
		self.user.save()
		response = self.client.post(self.final_inspection_url)
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_final_inspection_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()			
			
		response = self.client.post(self.final_inspection_url)
		
		self.assertTemplateUsed(response, 'Main/finalInspection.html')
		self.assertEqual(response.status_code, 200)


class FormTests(TestCase):

	def setUp(self):
		self.client = Client()
		self.project_url = reverse('showProjects')
		self.mang_group = Group(name='Management')
		self.mang_group.save() 
		self.super_group = Group(name='Supervisor')
		self.super_group.save()
		self.company = Company.objects.create(company_name = 'Test Company')
		self.user = User.objects.create_user(username='Test User', email='test@test.com', password='Test')
		self.user_mang = User.objects.create_user(username='Management', email='mang@mang.com', password='Manage')
		self.user_sup = User.objects.create_user(username='Supervisor', email='sup@sup.com', password='Super')
		self.user.profile.user_company = self.company
		self.failureCompany = Company.objects.create(company_name = 'Failure Company')
		self.project = Project.objects.create(company=self.company, project_name='Test Project')
		self.manualProject = Project.objects.create(company=self.company, project_name='Test Manual Project', manual=True)
		self.failureProject= Project.objects.create(company=self.company, project_name='Failure Project')
		self.process = Process.objects.create(project = self.project, name = "Test Process")
		self.formPreform = Process.objects.create(project=self.project, name = "Form Preform")
		self.subprocess = SubProcess.objects.create(process=self.process, name= 'Test SubProcess', position = 0)
		self.finalsubprocess = SubProcess.objects.create(process=self.process, name= 'Test SubProcess', position = 1)
		self.manualProcess = Process.objects.create(project = self.manualProject, manualName = "Test Manual Process")
		self.manualSubProcess = SubProcess.objects.create(process=self.manualProcess, manualName= 'Test Manual SubProcess')
		self.sensor = Sensor.objects.create(process = self.process, name = "Test Sensor", modelID= 1)
		self.all_process_url = reverse('showAllProcess', kwargs={'id':self.project.id})
		self.all_manual_process_url = reverse('showAllProcess', kwargs={'id':self.manualProject.id})
		self.all_sub_process_url = reverse('showProcess', kwargs={'id':self.process.id})
		self.all_manual_sub_process_url = reverse('showProcess', kwargs={'id':self.manualProcess.id})
		self.all_sub_process_detail_url = reverse('showSub', kwargs={'id':self.subprocess.id})
		self.client.login(username='Test User', password='Test')
		self.partinstance = PartInstance.objects.create(process=self.process)
		self.machine = Machine.objects.create(company=self.company, name="Preforming Cell", status =1)
		self.machine.projects.add(self.project)
		self.machine.save()

	def test_create_project(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	
		self.form = CreateNewProject(data={"name": "a project"})

		self.assertTrue(self.form.is_valid())
		self.assertEqual("a project", self.form['name'].value())

		self.project = Project.objects.create(project_name = self.form.cleaned_data['name'], manual = False)

		self.assertEqual(self.project, Project.objects.get(project_name=self.form['name'].value()))

		response = self.client.post(self.project_url, {'form': self.form,  'selected_project' :self.project, 'management':True, 'technician':False, 'supervisor':True})
		self.assertEqual(response.status_code, HTTPStatus.OK)
	
	def test_delete_project(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	
		self.form = CreateNewProject(data={"name": "a project"})

		self.assertTrue(self.form.is_valid())
		self.assertEqual("a project", self.form['name'].value())

		self.project = Project.objects.create(project_name = self.form.cleaned_data['name'], manual = False)

		self.assertEqual(self.project, Project.objects.get(project_name=self.form['name'].value()))

		self.project.delete()

		self.assertFalse(Project.objects.all().filter(project_name=self.form.cleaned_data['name']).exists())


	def test_add_process(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	

		for process in self.project.PRE_CELL_LIST:
			if not PossibleProjectProcess.objects.filter(name=process,project=self.project, machine=self.machine).exists():
				PossibleProjectProcess.objects.create(name=process, project=self.project, machine=self.machine)

		self.form = addProcess(self.project, data={"choice": self.project.possibleprojectprocess_set.first()})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.project.possibleprojectprocess_set.first(), self.form.cleaned_data['choice'])

		self.process = self.project.process_set.create(name=self.form.cleaned_data['choice'].name)
		self.assertEqual(self.process, Process.objects.get(name=self.form.cleaned_data['choice'].name))

		response = self.client.post(self.all_process_url, {'process': self.process, 'form': self.form,  'selected_project' :self.project, 'management':True, 'technician':False, 'supervisor':True})
		self.assertEqual(response.status_code, HTTPStatus.OK)

	def test_add_manual_process(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	
		self.form = addManualProcess(data={"manualName": "incoming_goods"})

		self.assertTrue(self.form.is_valid())
		self.assertEqual("incoming_goods", self.form['manualName'].value())

		self.manualProcess = self.manualProject.process_set.create(manualName=self.form.cleaned_data['manualName'])
		self.assertEqual(self.manualProcess, self.manualProject.process_set.get(manualName=self.form['manualName'].value()))

		response = self.client.post(self.all_manual_process_url, {'process': self.manualProcess, 'form': self.form,  'selected_project' :self.manualProject, 'management':True, 'technician':False, 'supervisor':True})
		self.assertEqual(response.status_code, HTTPStatus.OK)

	def test_delete_process(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	
		
		for process in self.project.PRE_CELL_LIST:
			if not PossibleProjectProcess.objects.filter(name=process,project=self.project, machine=self.machine).exists():
				PossibleProjectProcess.objects.create(name=process, project=self.project, machine=self.machine)

		self.form = addProcess(self.project, data={"choice": self.project.possibleprojectprocess_set.first()})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.project.possibleprojectprocess_set.first(), self.form.cleaned_data['choice'])

		self.process = self.project.process_set.create(name=self.form.cleaned_data['choice'].name)
		self.assertEqual(self.process, Process.objects.get(name=self.form.cleaned_data['choice'].name))

		self.process.delete()

		self.assertFalse(Process.objects.all().filter(name=self.form.cleaned_data['choice'].name).exists()) 

	def test_manual_delete_process(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	
		self.form = addManualProcess(data={"manualName": "incoming_goods"})

		self.assertTrue(self.form.is_valid())
		self.assertEqual("incoming_goods", self.form['manualName'].value())

		self.manualProcess = self.manualProject.process_set.create(manualName=self.form.cleaned_data['manualName'])
		self.assertEqual(self.manualProcess, self.manualProject.process_set.get(manualName=self.form['manualName'].value()))

		self.manualProcess.delete()

		self.assertFalse(Process.objects.all().filter(manualName=self.form.cleaned_data['manualName']).exists()) 

	def test_add_sub_process(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	

		for subpro in self.process.FORM_PREFORM_SUB_LIST:
			if not PossibleSubProcesses.objects.filter(name=self.process.name,process=self.process).exists():
				PossibleSubProcesses.objects.create(name=self.process.name,process=self.process)

		self.form = addSubProcess(self.process, data={"name": self.process.possiblesubprocesses_set.last()})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.process.possiblesubprocesses_set.first(), self.form.cleaned_data['name'])

		self.process = self.process.subprocess_set.create(name=self.form.cleaned_data['name'].name)
		self.assertEqual(self.process, SubProcess.objects.get(name=self.form.cleaned_data['name'].name))

		response = self.client.post(self.all_sub_process_url, {'sub_pro':self.subprocess, 'Pro':self.process, 'form': self.form,'management':True, 'technician':False, 'supervisor':True})
		self.assertEqual(response.status_code, HTTPStatus.OK)


	def test_delete_sub_process(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	
		for subpro in self.process.FORM_PREFORM_SUB_LIST:
			if not PossibleSubProcesses.objects.filter(name=self.process.name,process=self.process).exists():
				PossibleSubProcesses.objects.create(name=self.process.name,process=self.process)

		self.form =  addSubProcess(self.process, data={"name": self.process.possiblesubprocesses_set.last()})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.process.possiblesubprocesses_set.first(), self.form.cleaned_data['name'])

		self.process = self.process.subprocess_set.create(manualName=self.form.cleaned_data['name'].name)
		self.assertEqual(self.process, SubProcess.objects.get(manualName=self.form.cleaned_data['name'].name))

		self.process.delete()

		self.assertFalse(SubProcess.objects.all().filter(name=self.form.cleaned_data['name']).exists())

	def test_add_sub_manual_process(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	

		for subpro in self.process.FORM_PREFORM_SUB_LIST:
			if not PossibleSubProcesses.objects.filter(name=self.process.name,process=self.process).exists():
				PossibleSubProcesses.objects.create(name=self.process.name,process=self.process)

		self.form =  addManualSubProcess(self.process, data={"name": self.process.possiblesubprocesses_set.last()})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.process.possiblesubprocesses_set.first(), self.form.cleaned_data['name'])

		self.process = self.process.subprocess_set.create(manualName=self.form.cleaned_data['name'].name)
		self.assertEqual(self.process, SubProcess.objects.get(manualName=self.form.cleaned_data['name'].name))

	def test_delete_sub_manual_process(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	
		for subpro in self.process.FORM_PREFORM_SUB_LIST:
			if not PossibleSubProcesses.objects.filter(name=self.process.name,process=self.process).exists():
				PossibleSubProcesses.objects.create(name=self.process.name,process=self.process)

		self.form =  addManualSubProcess(self.process, data={"name": self.process.possiblesubprocesses_set.last()})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.process.possiblesubprocesses_set.first(), self.form.cleaned_data['name'])

		self.process = self.process.subprocess_set.create(manualName=self.form.cleaned_data['name'].name)
		self.assertEqual(self.process, SubProcess.objects.get(manualName=self.form.cleaned_data['name'].name))

		self.process.delete()

		self.assertFalse(SubProcess.objects.all().filter(name=self.form.cleaned_data['name']).exists())
		
	def test_add_manual_input(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()
		form_data = {"task": "LAB", "value": 123}
		self.form = addManualInfo(data=form_data)

		self.assertTrue(self.form.is_valid())
		self.assertTrue(self.form['task'].value()=="LAB" and self.form['value'].value()==123)
		
		reqInputDirty = self.form['task'].value()
		reqInput = SubProcess.manual_input_dict[reqInputDirty]
		inputValue = self.form['value'].value()

		setattr(self.subprocess,reqInput,inputValue)

		self.subprocess.save()

		self.assertTrue(self.subprocess.labourInput == inputValue)

	def test_add_manual_time_info(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		form_data = {"task": "JBS"}
		self.form = addManualTimeInfo(data=form_data)

		self.assertTrue(self.form.is_valid())

		self.assertEqual(self.form['task'].value(), form_data['task'])

		reqInputDirty = self.form['task'].value()
		reqInput = SubProcess.manual_input_time_dict[reqInputDirty]
		inputValue = datetime(2022, 8, 10, tzinfo=timezone.utc)

		setattr(self.subprocess, reqInput, inputValue)

		self.subprocess.save()

		self.assertEqual(self.subprocess.jobStart, inputValue)

	def test_edit_component(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		form_data = {"name": 'Test'}
		self.form = EditComponent(data=form_data)

		self.assertTrue(self.form.is_valid())

		self.assertEqual(self.form['name'].value(), form_data['name'])

	def test_operator_form(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		self.form = operatorForm(self.company.company_name,data={'choice': self.user.username})
		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.form['choice'].value(), self.user.username)

		reqInput = "operator"
		inputValue = self.form['choice'].value()

		setattr(self.subprocess, reqInput, inputValue)

		self.subprocess.save()

		self.assertEqual(self.subprocess.operator, self.form['choice'].value())

	# def test_sensor_form(self):
	# 	self.user.groups.add(self.mang_group, self.super_group)
	# 	self.user.save()

	# 	form_data = {"name":"thermocouple"}
	# 	self.form = SensorForm(data=form_data)

	# 	self.assertTrue(self.form.is_valid())
	# 	self.assertEqual(self.form['name'].value(), form_data['name'])

	# 	self.sensor = Sensor.objects.create(sub_process=self.subprocess, name=self.form['name'].value())
	# 	self.assertEqual(self.sensor.name, self.form['name'].value())

	def test_machine_form(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		form_data = {"name":"ply_cutter"}
		self.form = MachineForm(data=form_data)

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.form['name'].value(), form_data['name'])

		self.machine = Machine.objects.create(name=self.form['name'].value())
		self.assertEqual(self.machine.name, self.form['name'].value())

	def test_const_form_mang(self):
		self.user.groups.add(self.mang_group )
		self.user.save()

		name = self.mang_group.name

		form_data = {"choice":"PWR", "value":0.2}
		self.form = ConstForm(data=form_data, group=name)

		self.assertTrue(self.form.is_valid())
		self.assertTrue(self.form['choice'].value() == form_data['choice'] and self.form['value'].value() == form_data['value'])

		choiceClean = Project.const_dict_mang[self.form['choice'].value()]
		value = self.form['value'].value()

		setattr(self.project, choiceClean, value)

		self.project.save()

		self.assertEqual(self.project.powerRate, self.form['value'].value())

	def test_const_form_sup(self):
		self.user.groups.add(self.super_group )
		self.user.save()

		name = self.super_group.name

		form_data = {"choice":"NPW", "value":123}
		self.form = ConstForm(data=form_data, group=name)

		self.assertTrue(self.form.is_valid())
		self.assertTrue(self.form['choice'].value() == form_data['choice'] and self.form['value'].value() == form_data['value'])

		choiceClean = Project.const_dict_super[self.form['choice'].value()]
		value = self.form['value'].value()

		setattr(self.project, choiceClean, value)

		self.project.save()

		self.assertEqual(self.project.nominalPartWeight, self.form['value'].value())

	def test_sub_master_form(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		self.form = SubMasterForm("Final Inspection", data={"choice":"AT", "value":25})
		self.assertTrue(self.form.is_valid())
		self.assertTrue(self.form['choice'].value()=="AT" and self.form['value'].value()==25)

		choiceClean = SubProcess.trimming_dict[self.form['choice'].value()]
		value = self.form['value'].value()

		setattr(self.subprocess, choiceClean, value)
		self.subprocess.save()

		self.assertEqual(self.subprocess.actualThickness, self.form['value'].value())

	def test_part_instance_form(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		form = PartInstanceForm(self.process, data={'choice':self.partinstance})

		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data['choice'], self.partinstance)

	def test_change_graph_time_form(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		form_data = {"time": '10'}
		self.form = ChangeGraphTime(data=form_data)

		self.assertTrue(self.form.is_valid())

		self.assertEqual(self.form['time'].value(), form_data['time'])
		
	def test_enter_device_id_form(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		form_data = {"name": 'Test'}
		self.form = EnterDeviceID(data=form_data)

		self.assertTrue(self.form.is_valid())

		self.assertEqual(self.form['name'].value(), form_data['name'])

	def test_possible_sensor_form(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()
		self.form = PossibleSensorForm(data={"name":"incoming_goods"})

		self.assertTrue(self.form.is_valid())
		self.assertEqual("incoming_goods", self.form['name'].value())

	def test_select_sensor_form(self):
		self.user.groups.add(self.super_group)
		self.user.save()

		self.form = SelectSensorForm(self.process.sensor_set.all(), data={"choice":self.sensor.modelID})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.sensor.modelID, self.form["choice"].value())






