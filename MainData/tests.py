from django.test import TestCase, Client
from django.db.models import ForeignKey
from datetime import datetime,date,time,timedelta, timezone
from django.urls import reverse, resolve
import json
from django.contrib.auth.models import User, Group
from django.test.utils import setup_test_environment 

from .models import *
from Export import views as v

from.views import *

class ModelTests(TestCase):
	"""Class to test all Main app models"""
	
	def setUp(self):
		"""Set up for all Main tests"""
		self.company = Company.objects.create(company_name = 'Test Company')
		self.project = Project.objects.create(project_name = 'Test Project', company = self.company)
		self.part = Part.objects.create(project=  self.project)
		self.processPart = ProcessPart.objects.create(processName = 'Test Process', part = self.part)
		self.subProcessPart = SubProcessPart.objects.create(subProcessName = 'Test processPart', processPart = self.processPart)
		 
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
		project = Project.objects.create(project_name = 'Test Project', company = self.company)
		project.assumedCost = 4.1
		project.priceKG = 10
		project.priceM2 = 10
		project.materialDensity = 10
		project.techRate = 10
		project.superRate = 10
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

	def test_part_fields(self):
		"""Test if Project fields are saved correctly"""
		part = Part.objects.create( project = self.project)
		
		part.part_id = 5
		part.date = date.today()
		part.labourInput = 10
		part.jobStart = datetime(2022, 8, 10, tzinfo=timezone.utc)
		part.jobEnd = datetime(2022, 8, 10, tzinfo=timezone.utc)
		part.processTime = timedelta(seconds=4)
		part.interfaceTime = timedelta(seconds=5)
		part.cycleTime = timedelta(seconds=6)
		part.popUpStart = datetime(2022, 8, 10, tzinfo=timezone.utc)
		part.popUpEnd= datetime(2022, 8, 10, tzinfo=timezone.utc)
		part.scrapRate = 10
		part.power = 10
		part.preTrimWeight = 10
		part.postTrimWeight = 10

		part.priceKG = 10
		part.priceM2 = 10
		part.materialDensity = 10
		part.techRate = 10
		part.superRate = 10
		part.powerRate = 10

		part.nominalPartWeight = 10
		part.nominalPartLength = 10
		part.nominalPartWidth = 10
		part.nominalPartThickness = 10
		part.actualWeight = 10
		part.weightTolerance = 10
		part.depthTolerance = 10
		part.lengthTolerance = 10
		part.widthTolerance = 10
		part.assumedCost = 4

		part.setUpCost = 10

		part.materialCost = 10
		part.labourCost = 10
		part.powerCost = 10
		part.totalCost = 30

		part.save()

		part_query = Part.objects.get(part_id = part.part_id)
 		
		self.assertEqual(part, part_query)

	def test_part_project_relation(self):
		"""Test if Process to Project relations are created correctly"""
		self.assertEqual(self.part.project, self.project)
	
	def test_processpart_part_relation(self):
		self.assertEqual(self.processPart.part, self.part)

	def test_subprocessPart_part_relation(self):
		self.assertEqual(self.subProcessPart.processPart, self.processPart)	
		
	def test_processpart_fields(self):
		processPart = ProcessPart.objects.create(processName = 'Test processPart', part = self.part)
		
		processPart.date = date.today()
		processPart.labourInput = 10
		processPart.cycle = timedelta(seconds=6)
		processPart.processTime = timedelta(seconds=4)
		processPart.jobStart = datetime(2022, 8, 10, tzinfo=timezone.utc)
		processPart.jobEnd = datetime(2022, 8, 10, tzinfo=timezone.utc)
		processPart.processStart = datetime(2022, 8, 10, tzinfo=timezone.utc)
		processPart.processEnd = datetime(2022, 8, 10, tzinfo=timezone.utc)
		processPart.interfaceTime = timedelta(seconds=4)
		processPart.scrapRate = 40
		processPart.power = 90
		processPart.status = 2
		processPart.processCheck = True
		processPart.qualityCheck = True

		processPart.CO2 = 200

		processPart.materialWastage = 200
		processPart.materialScrap = 200
		processPart.materialPart = 300
		processPart.materialSumCost = 700

		processPart.technicianLabourCost = 20
		processPart.supervisorLabourCost = 30

		processPart.labourSumCost = 50

		processPart.powerCost = 300
		processPart.powerRate=20

		processPart.totalCost = 1000



		processPart.save()
 		
		processPart_query = ProcessPart.objects.get(processName=processPart.processName)
 		
		self.assertEqual(processPart, processPart_query)
		
	def test_subProcesspart_fields(self):
		subProcessPart = SubProcessPart.objects.create(subProcessName = 'Test subProcessPart', processPart = self.processPart)
		
		subProcessPart.date = date.today()
		subProcessPart.labourInput = 10
		subProcessPart.cycle = timedelta(seconds=6)
		subProcessPart.subProcessTime = timedelta(seconds=4)
		subProcessPart.jobStart = datetime(2022, 8, 10, tzinfo=timezone.utc)
		subProcessPart.jobEnd = datetime(2022, 8, 10, tzinfo=timezone.utc)
		subProcessPart.subProcessStart = datetime(2022, 8, 10, tzinfo=timezone.utc)
		subProcessPart.subProcessEnd = datetime(2022, 8, 10, tzinfo=timezone.utc)
		subProcessPart.interfaceTime = timedelta(seconds=4)
		subProcessPart.scrapRate = 40
		subProcessPart.power = 90
		subProcessPart.status = 2
		subProcessPart.subProcessCheck = True
		subProcessPart.qualityCheck = True

		subProcessPart.CO2 = 200

		subProcessPart.materialWastage = 200
		subProcessPart.materialScrap = 200
		subProcessPart.materialPart = 300
		subProcessPart.materialSumCost = 700

		subProcessPart.technicianLabourCost = 20
		subProcessPart.supervisorLabourCost = 30

		subProcessPart.labourSumCost = 50

		subProcessPart.powerCost = 300
		subProcessPart.powerRate=20

		subProcessPart.totalCost = 1000



		subProcessPart.save()
 		
		subProcessPart_query = SubProcessPart.objects.get(id=subProcessPart.id)
 		
		self.assertEqual(subProcessPart, subProcessPart_query)


class UrlTests(TestCase):
	
	def test_view_project_part_url(self):
		url = reverse('viewProjectParts',  kwargs={'id':1})
		self.assertEqual(resolve(url).func, viewProjectParts)
		
	def test_view_part_detail_url(self):
		url = reverse('viewPartDetail', kwargs={'id':1})
		self.assertEqual(resolve(url).func, viewPartDetail)
		
	def test_view_part_sub_detail_url(self):
		url = reverse('viewPartSubDetail', kwargs={'id':1})
		self.assertEqual(resolve(url).func, viewPartSubDetail)

	def test_process_part_sensor_url(self):
		url = reverse('processPartSensor', kwargs={'id':1})
		self.assertEqual(resolve(url).func, processPartSensor)
		
	def test_view_part_sub_sensor_detail_url(self):
		url = reverse('viewPartSubSensorDetail', kwargs={'id':1})
		self.assertEqual(resolve(url).func, viewPartSubSensorDetail)
		



class ViewTests(TestCase):
	
	def setUp(self):
		self.client = Client()
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
		self.prosensor = Sensor.objects.create(process = self.process, name  = "Test Sensor")
		self.subprocess = SubProcess.objects.create(process=self.process, name= 'Test SubProcess')
		self.subsensor = Sensor.objects.create(sub_process=self.subprocess, name = "Test Sub Sensor")

		self.part = Part.objects.create(project = self.project, part_id = 1)
		self.processPart = ProcessPart.objects.create(part=self.part)
		self.subProcessPart = SubProcessPart.objects.create(processPart=self.processPart, subProcessName = "Test Sub Process Parts")
		self.processSensorPart = SensorData.objects.create(sensorName = self.prosensor.name, processPart = self.processPart)
		self.subProcessSensorPart = SensorData.objects.create(sensorName = self.subsensor.name, subProcessPart= self.subProcessPart)

		self.all_parts_url = reverse('viewProjectParts', kwargs={'id':self.project.id})
		self.all_part_detail_url = reverse('viewPartDetail', kwargs={'id':self.part.part_id})
		self.all_process_part_sensor_url = reverse('processPartSensor', kwargs={'id':self.processSensorPart.id})
		self.all_part_sub_detail_url = reverse('viewPartSubDetail', kwargs={'id':self.processPart.id})
		self.all_part_sub_sensor_detail_url = reverse('viewPartSubSensorDetail', kwargs={'id':self.subProcessPart.id})

		self.client.login(username='Test User', password='Test')
		
		
	def test_show_project_page_no_return(self):				
		response = self.client.post(self.all_parts_url)			
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_view_part_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.profile.user_company = self.company
		self.user.save()		
		
		response = self.client.post(self.all_parts_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'MainData/viewProjectPart.html')
		
	def test_project_belong_to_user(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.profile.user_company = self.company
		self.user.save()		
		
		response = self.client.post(self.all_parts_url)
		
		self.assertQuerysetEqual(self.user.profile.user_company.project_set.all().last().part_set.all(), response.context['user'].profile.user_company.project_set.all().last().part_set.all(), transform=lambda 	x: x, ordered=False)
		
	def test_part_page_no_return(self):	
		self.user.save()					
			
		response = self.client.post(self.all_part_detail_url)
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_part_detail_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()			
			
		response = self.client.post(self.all_part_detail_url)
		
		self.assertTemplateUsed(response, 'MainData/viewPartDetail.html')
		self.assertEqual(response.status_code, 200)
				
	def test_part_sub_detail_page_no_return(self):
		self.user.save()
		response = self.client.post(self.all_part_sub_detail_url)
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
	
	def test_sub_part_detail_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()			
			
		response = self.client.post(self.all_part_sub_detail_url)
		
		self.assertTemplateUsed(response, 'MainData/viewPartSubDetail.html')
		self.assertEqual(response.status_code, 200)
	

	def test_process_part_sensor_page_no_return(self):
		self.user.save()
		response = self.client.post(self.all_process_part_sensor_url)
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')

	def test_process_part_sensor_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()			
			
		response = self.client.post(self.all_process_part_sensor_url)
		
		self.assertTemplateUsed(response, 'MainData/processPartSensor.html')
		self.assertEqual(response.status_code, 200)

	def test_sub_part_sensor_detail_page_no_return(self):
		self.user.save()
		response = self.client.post(self.all_part_sub_sensor_detail_url)
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		

	def test_sub_part_detail_sensor_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()			
			
		response = self.client.post(self.all_part_sub_sensor_detail_url)
		
		self.assertTemplateUsed(response, 'MainData/viewPartSubSensorDetail.html')
		self.assertEqual(response.status_code, 200)
				