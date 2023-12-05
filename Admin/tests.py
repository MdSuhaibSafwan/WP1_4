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
	
	def test_amot_admin_url(self):
		url = reverse('admin_start')
		self.assertEqual(resolve(url).func, admin_start)

	def test_request_hardware_url(self):
		url = reverse('admin_request', kwargs={'id':1})
		self.assertEqual(resolve(url).func, admin_request_hard)

	def test_assign_hardware_url(self):
		url = reverse('admin_assign_hardware', kwargs={'id':1})
		self.assertEqual(resolve(url).func, admin_assign_machine)

	def test_edit_process_url(self):
		url = reverse('admin_edit', kwargs={'id':1})
		self.assertEqual(resolve(url).func, admin_edit)

	def test_total_edit_process_url(self):
		url = reverse('admin_total_edit', kwargs={'id':1})
		self.assertEqual(resolve(url).func, admin_total_edit)

	def test_view_all_process_url(self):
		url = reverse('admin_view_all_process', kwargs={'id':1})
		self.assertEqual(resolve(url).func, admin_view_all_process)

	def test_view_process_url(self):
		url = reverse('admin_view_process', kwargs={'id':1})
		self.assertEqual(resolve(url).func, admin_view_process)

	def test_view_sub_process_url(self):
		url = reverse('admin_view_sub', kwargs={'id':1})
		self.assertEqual(resolve(url).func, admin_view_sub)

	def test_edit_repeat_block_url(self):
		url = reverse('admin_edit_repeat_block', kwargs={'id':1})
		self.assertEqual(resolve(url).func, admin_edit_repeat_block)

	def test_update_sub_process_positions_url(self):
		url = reverse('updatePositions', kwargs={'id':1})
		self.assertEqual(resolve(url).func, updatePositions)

	def test_update_process_positions_url(self):
		url = reverse('updateProPositions', kwargs={'id':1})
		self.assertEqual(resolve(url).func, updateProPositions)

class ViewTests(TestCase):
	
	def setUp(self):
		self.client = Client()
		self.amot_admin_url = reverse('admin_start')
		self.mang_group = Group(name='Management')
		self.mang_group.save() 
		self.super_group = Group(name='Supervisor')
		self.super_group.save()
		self.admin_group = Group(name="Admin")
		self.admin_group.save()
		self.company = Company.objects.create(company_name = 'Test Company')
		self.user = User.objects.create_user(username='Test User', email='test@test.com', password='Test')
		self.user.profile.user_company = self.company
		self.profile = self.user.profile
		self.profile.user_company = self.company 
		self.profile.save()
		self.failureCompany = Company.objects.create(company_name = 'Failure Company')
		self.project = Project.objects.create(company=self.company, project_name='Test Project')
		self.failureProject= Project.objects.create(company=self.company, project_name='Failure Project')
		self.process = Process.objects.create(project=self.project, name= 'Test Process')
		self.subprocess = SubProcess.objects.create(process=self.process, name= 'Test SubProcess', position = 0)
		self.finalInspection = SubProcess.objects.create(process=self.process, name= 'Final Inspection', id=2, position = 1)
		self.repeat_block = RepeatBlock.objects.create(process=self.process)
		self.repeat_block.repeatblocksubprocesses_set.create(sub_process = self.subprocess, start=True)
		self.repeat_block.repeatblocksubprocesses_set.create(sub_process = self.finalInspection, end = True)
		self.amot_hardware_request_url = reverse('admin_request', kwargs={'id':self.project.id})
		self.amot_hardware_assign_url = reverse('admin_assign_hardware', kwargs={'id':self.project.id})
		self.amot_edit_process_url  = reverse('admin_edit', kwargs={'id':self.project.id})
		self.amot_total_edit_url = reverse('admin_total_edit', kwargs={'id':self.project.id})
		self.amot_view_all_process_url = reverse('admin_view_all_process', kwargs={'id':self.project.id})
		self.amot_view_process_url = reverse('admin_view_process', kwargs={'id':self.project.id})
		self.amot_view_sub_url= reverse('admin_view_sub', kwargs={'id':self.project.id})
		self.amot_edit_repeat_block_url = reverse('admin_edit_repeat_block', kwargs={'id':self.process.id})
		self.amot_update_sub_positions_url = reverse('updatePositions', kwargs={'id':self.process.id})
		self.amot_update_pro_positions_url = reverse('updateProPositions', kwargs={'id':self.project.id})

		self.client.login(username='Test User', password='Test')
		
	def test_amot_admin_page_no_return(self):				
		response = self.client.post(self.amot_admin_url)			
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_amot_admin_page_return(self):
		self.user.groups.add(self.admin_group)
		self.user.save()		
		
		response = self.client.post(self.amot_admin_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Admin/showProjects.html')

	def test_request_hardware_page_no_return(self):				
		response = self.client.post(self.amot_hardware_request_url)			
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_request_hardware_page_return(self):
		self.user.groups.add(self.admin_group)
		self.user.save()		
		
		response = self.client.post(self.amot_hardware_request_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Admin/requestHardware.html')

	def test_assign_hardware_page_no_return(self):				
		response = self.client.post(self.amot_hardware_assign_url)			
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_assign_hardware_page_return(self):
		self.user.groups.add(self.admin_group)
		self.user.save()		
		
		response = self.client.post(self.amot_hardware_assign_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Admin/assignHardware.html')

	def test_edit_process_no_return(self):				
		response = self.client.post(self.amot_edit_process_url)		
		self.project.machineConfirmed=False 
		self.project.save()	
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_edit_process_page_return(self):
		self.user.groups.add(self.admin_group)
		self.user.save()		
		self.project.machineConfirmed= True 
		self.project.save()
		
		response = self.client.post(self.amot_edit_process_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Admin/editProcess.html')

	def test_total_edit_process_no_return(self):				
		response = self.client.post(self.amot_total_edit_url)		
		self.project.machineConfirmed=False 
		self.project.save()	
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_total_edit_process_page_return(self):
		self.user.groups.add(self.admin_group)
		self.user.save()		
		self.project.machineConfirmed= True 
		self.project.save()
		
		response = self.client.post(self.amot_total_edit_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Admin/totalEditProcess.html')

	def test_view_all_process_no_return(self):				
		response = self.client.post(self.amot_view_all_process_url)		
		self.project.machineConfirmed=False 
		self.project.save()	
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_view_all_process_page_return(self):
		self.user.groups.add(self.admin_group)
		self.user.save()		
		self.project.machineConfirmed= True 
		self.project.save()
		
		response = self.client.post(self.amot_view_all_process_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Admin/adminViewAllProcess.html')

	def test_view_sub_process_no_return(self):				
		response = self.client.post(self.amot_view_sub_url)		
		self.project.machineConfirmed=False 
		self.project.save()	
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_view_sub_process_page_return(self):
		self.user.groups.add(self.admin_group)
		self.user.save()		
		self.project.machineConfirmed= True 
		self.project.save()
		
		response = self.client.post(self.amot_view_sub_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Admin/adminViewSub.html')

	def test_edit_repeat_block_no_return(self):				
		response = self.client.post(self.amot_edit_repeat_block_url)		
		self.project.machineConfirmed=False 
		self.project.save()	
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_edit_repeat_block_process_page_return(self):
		self.user.groups.add(self.admin_group)
		self.user.save()		
		self.project.machineConfirmed= True 
		self.project.save()
		
		response = self.client.post(self.amot_edit_repeat_block_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Admin/adminEditRepeatBlock.html')

class FormTests(TestCase):

	def setUp(self):
		self.client = Client()
		self.amot_admin_url = reverse('admin_start')
		self.mang_group = Group(name='Management')
		self.mang_group.save() 
		self.super_group = Group(name='Supervisor')
		self.super_group.save()
		self.admin_group = Group(name="Admin")
		self.admin_group.save()
		self.company = Company.objects.create(company_name = 'Test Company')
		self.user = User.objects.create_user(username='Test User', email='test@test.com', password='Test')
		self.user.profile.user_company = self.company
		self.profile = self.user.profile
		self.profile.user_company = self.company 
		self.profile.save()
		self.failureCompany = Company.objects.create(company_name = 'Failure Company')
		self.project = Project.objects.create(company=self.company, project_name='Test Project')
		self.failureProject= Project.objects.create(company=self.company, project_name='Failure Project')
		self.process = Process.objects.create(project=self.project, name= 'Test Process')
		self.subprocess = SubProcess.objects.create(process=self.process, name= 'Test SubProcess', position = 0)
		self.finalInspection = SubProcess.objects.create(process=self.process, name= 'Final Inspection', id=2, position = 1)
		self.repeat_block = RepeatBlock.objects.create(process=self.process)
		self.repeat_block.repeatblocksubprocesses_set.create(sub_process = self.subprocess, start=True)
		self.repeat_block.repeatblocksubprocesses_set.create(sub_process = self.finalInspection, end = True)

		self.machine = Machine.objects.create(name="Preforming Cell", company=self.company)


		self.amot_hardware_request_url = reverse('admin_request', kwargs={'id':self.project.id})
		self.amot_hardware_assign_url = reverse('admin_assign_hardware', kwargs={'id':self.project.id})
		self.amot_edit_process_url  = reverse('admin_edit', kwargs={'id':self.project.id})
		self.amot_total_edit_url = reverse('admin_total_edit', kwargs={'id':self.project.id})
		self.amot_view_all_process_url = reverse('admin_view_all_process', kwargs={'id':self.project.id})
		self.amot_view_process_url = reverse('admin_view_process', kwargs={'id':self.project.id})
		self.amot_view_sub_url= reverse('admin_view_sub', kwargs={'id':self.project.id})
		self.amot_edit_repeat_block_url = reverse('admin_edit_repeat_block', kwargs={'id':self.process.id})
		self.amot_update_sub_positions_url = reverse('updatePositions', kwargs={'id':self.process.id})
		self.amot_update_pro_positions_url = reverse('updateProPositions', kwargs={'id':self.project.id})

		self.client.login(username='Test User', password='Test')


	def test_create_project(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	
		self.form = CreateNewProject(data={"name": "a project", "manual":False})

		self.assertTrue(self.form.is_valid())
		self.assertEqual("a project", self.form['name'].value())
		self.project = Project.objects.create(project_name = self.form.cleaned_data['name'], manual=False)

		self.assertEqual(self.project, Project.objects.get(project_name=self.form['name'].value()))


	def test_select_machines_form(self):
		self.user.groups.add(self.admin_group)
		self.user.save()
		self.possibleprojectmachine = PossibleProjectMachines.objects.create(project=self.project, machine=self.machine)

		self.form = SelectMachines(self.project.id, data={"machine":self.possibleprojectmachine})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.machine, self.form.cleaned_data['machine'].machine)

		self.project.machine_set.add(self.form.cleaned_data['machine'].machine)
		self.assertTrue(self.form.cleaned_data['machine'].machine in self.project.machine_set.all())


	def test_possible_pro_form(self):
		self.user.groups.add(self.admin_group)
		self.user.save()
		self.possibleprojectprocess = PossibleProjectProcess.objects.create(machine = self.machine, project=self.project, name = "Form Preform")


		self.form = PossibleProForm(self.project.id, data={'process':self.possibleprojectprocess})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.possibleprojectprocess, self.form.cleaned_data['process'])

		self.process = self.project.process_set.create(name=self.form.cleaned_data['process'].name)

		self.assertTrue(self.form.cleaned_data['process'].name == self.process.name)

	def test_possible_sub_pro_form(self):
		self.user.groups.add(self.admin_group)
		self.user.save()
		self.possiblesubprocess= PossibleSubProcesses.objects.create(process = self.process, name ="Initialisation")

		self.form = PossibleSubProForm(self.process.id, data={'name':self.possiblesubprocess})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.possiblesubprocess, self.form.cleaned_data['name'])

		self.process = self.project.process_set.create(name=self.form.cleaned_data['name'])

		self.assertTrue(self.form.cleaned_data['name'] == self.process.name)

	def test_sensor_form(self):
		self.user.groups.add(self.admin_group)
		self.user.save()
		self.possibleprojectsensor = PossibleProjectSensors.objects.create(name="Thermocouple", project=self.project, machine = self.machine, modelID = "Test-123")

		self.form = SensorForm(self.project,self.machine, data={'sensor': self.possibleprojectsensor})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.possibleprojectsensor, self.form.cleaned_data['sensor'])

		self.sensor = self.process.sensor_set.create(name = self.form.cleaned_data['sensor'].name, machine=self.form.cleaned_data['sensor'].machine)

		self.assertTrue(self.sensor in self.process.sensor_set.all())

	def test_user_define_pro_sub(self):

		self.form = UserDefineProSub(data={"name":"Test Process"})

		self.assertTrue(self.form.is_valid())

		self.subprocess = self.process.subprocess_set.create(name=self.form.cleaned_data['name'])

		self.assertEqual(self.subprocess.name,self.form.cleaned_data['name'])
		self.assertTrue(self.subprocess in self.process.subprocess_set.all())

	def test_add_tia_block(self):

		self.possibleprojecttia = PossibleProjectTia.objects.create(name = "block test", project=self.project, machine=self.machine)

		self.form = AddTiaBlock(self.project, self.machine, data={"choice": self.possibleprojecttia})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(self.form.cleaned_data['choice'], self.possibleprojecttia)

		self.tiablock = TiaBlocks.objects.create(name=self.form.cleaned_data['choice'], subProcess=self.subprocess, project=self.project, machine=self.machine )

		self.assertTrue(self.tiablock in self.subprocess.tiablocks_set.all())

	def test_add_repeat_block(self):

		self.form = AddRepeatBlock(self.process, data={"start":self.subprocess, "end":self.finalInspection, "value":2})

		self.assertTrue(self.form.is_valid())
		self.assertTrue(self.form.cleaned_data['start'] == self.subprocess and self.form.cleaned_data['end'] == self.finalInspection and self.form.cleaned_data['value'] == 2)

		self.repeatblock = RepeatBlock.objects.create(process = self.process, number_of_iterations = self.form.cleaned_data['value'])

		self.start = self.repeatblock.repeatblocksubprocesses_set.create(sub_process=self.form.cleaned_data['start'], start=True)
		self.end = self.repeatblock.repeatblocksubprocesses_set.create(sub_process=self.form.cleaned_data['end'], end=True)

		self.assertTrue(self.start in self.repeatblock.repeatblocksubprocesses_set.all())
		self.assertTrue(self.end in self.repeatblock.repeatblocksubprocesses_set.all())

	def test_edit_criterion(self):
		self.form = EditCriterionForm(data={"criterion": "Test Criterion"})

		self.assertTrue(self.form.is_valid())
		self.subprocess.criterion = self.form.cleaned_data['criterion']
		self.subprocess.save()

		self.assertEqual(self.subprocess.criterion, self.form.cleaned_data['criterion'])

	def test_process_check(self):
		self.form = ProcessCheckForm(data={"process_check": True})

		self.assertTrue(self.form.is_valid())
		self.subprocess.processCheck = self.form.cleaned_data['process_check']

		self.subprocess.save()

		self.assertEqual(self.subprocess.processCheck, self.form.cleaned_data['process_check'])

		self.assertTrue(self.subprocess.processCheck)



