from django.test import TestCase
from django.test import TestCase, Client
from django.db.models import ForeignKey
from datetime import datetime,date,time,timedelta, timezone
from django.urls import reverse, resolve
import json
import csv 
import io
from django.contrib.auth.models import User, Group
from django.test.utils import setup_test_environment 
from http import HTTPStatus
from Export import views as v
from Main.models import *
from django.http import FileResponse
from MainData.models import *


class UrlTests(TestCase):
	def test_export_csv_url(self):
		url = reverse('ExpCSV', kwargs={'id':1, 'partID':1})
		self.assertEqual(resolve(url).func, v.exportCSV)
		
	def test_export_pdf_url(self):
		url = reverse('ExpPDF', kwargs={'id':1, 'partID':1})
		self.assertEqual(resolve(url).func, v.exportPDF)

	def test_export_part_pdf_url(self):
		url = reverse('exportPartPDF', kwargs={'id':1})
		self.assertEqual(resolve(url).func, v.exportPartPDF)
		
	def test_export_part_csv_url(self):
		url = reverse('exportPartCSV', kwargs={'id':1})
		self.assertEqual(resolve(url).func, v.exportPartCSV)

	def test_export_sysarch_csv_url(self):
		url = reverse('exportSysArchitectureCSV', kwargs={'id':1})
		self.assertEqual(resolve(url).func, v.exportSysArchitectureCSV)

	def test_export_sysarch_pdf_url(self):
		url = reverse('exportSysArchitecturePDF', kwargs={'id':1})
		self.assertEqual(resolve(url).func, v.exportSysArchitecturePDF)



class ExportTests(TestCase):
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
		self.part = Part.objects.create(part_id=1, project=self.project)
		self.processpart = ProcessPart.objects.create(processName = self.process.name, part = self.part)
		self.subprocesspart = SubProcessPart.objects.create(subProcessName = self.subprocess.name, processPart = self.processpart)
		self.all_export_csv_url = reverse('ExpCSV', kwargs={'id':self.process.id, 'partID':self.part.part_id})
		self.all_export_pdf_url = reverse('ExpPDF', kwargs={'id':self.process.id, 'partID':self.part.part_id})
		self.all_export_part_csv_url = reverse('exportPartCSV', kwargs={'id':self.part.part_id})
		self.all_export_part_pdf_url = reverse('exportPartPDF', kwargs={'id':self.part.part_id})
		self.all_export_sysarch_csv_url = reverse('exportSysArchitectureCSV', kwargs={'id':self.project.id})
		self.all_export_sysarch_pdf_url = reverse('exportSysArchitecturePDF', kwargs={'id':self.project.id})
		self.client.login(username='Test User', password='Test')


	def test_export_csv_function(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		#Testing Manager
		response = self.client.get(self.all_export_csv_url)
		self.assertEqual(response.status_code, 200)

		self.assertEqual(response.get('Content-Disposition'), 'attachment;filename=Management-SubProcessData.csv')

		content = response.content.decode('utf-8')
		cvs_reader = csv.reader(io.StringIO(content))
		body = list(cvs_reader)

		self.assertTrue(any(self.process.name in x for x in body))
		self.assertTrue(any(self.subprocess.name in x for x in body))


		#Testing Supervisor
		self.user.groups.remove(self.mang_group)
		self.user.save()
		response=self.client.get(self.all_export_csv_url)
		self.assertEqual(response.status_code, 200)

		self.assertEqual(response.get('Content-Disposition'), 'attachment;filename=Supervisor-SubProcessData.csv')

		content = response.content.decode('utf-8')
		cvs_reader = csv.reader(io.StringIO(content))
		body = list(cvs_reader)

		self.assertTrue(any(self.process.name in x for x in body))
		self.assertTrue(any(self.subprocess.name in x for x in body))


	def test_export_pdf_function(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		#Testing Manager
		response = self.client.get(self.all_export_pdf_url)
		self.assertEqual(response.status_code, 200)

		self.assertEqual(response.get('Content-Disposition'), 'attachment; filename = "Management-ProcessData.pdf"')

		#Testing Supervisor
		self.user.groups.remove(self.mang_group)
		self.user.save()

		response=self.client.get(self.all_export_pdf_url)
		self.assertEqual(response.status_code, 200)

		self.assertEqual(response.get('Content-Disposition'), 'attachment; filename = "Supervisor-ProcessData.pdf"')

	def test_export_part_csv_function(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()

		#Testing Manager
		response = self.client.get(self.all_export_part_csv_url)
		self.assertEqual(response.status_code, 200)

		self.assertEqual(response.get('Content-Disposition'), 'attachment;filename=Management-PartData.csv')

		content = response.content.decode('utf-8')
		cvs_reader = csv.reader(io.StringIO(content))
		body = list(cvs_reader)

		self.assertTrue(any(self.processpart.processName in x for x in body))
		self.assertTrue(any(self.subprocesspart.subProcessName in x for x in body))

		#Testing Supervisor
		self.user.groups.remove(self.mang_group)
		self.user.save()
		response = self.client.get(self.all_export_part_csv_url)
		self.assertEqual(response.status_code, 200)

		self.assertEqual(response.get('Content-Disposition'), 'attachment;filename=Supervisor-PartData.csv')

		content = response.content.decode('utf-8')
		cvs_reader = csv.reader(io.StringIO(content))
		body = list(cvs_reader)

		self.assertTrue(any(self.processpart.processName in x for x in body))
		self.assertTrue(any(self.subprocesspart.subProcessName in x for x in body))



	def test_export_systemarch_csv_function(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()
		response = self.client.get(self.all_export_sysarch_csv_url)
		self.assertEqual(response.status_code, 200)

		self.assertEquals(
		response.get('Content-Disposition'),
		'attachment;filename=SystemArchitecture.csv'
	)

		content = response.content.decode('utf-8')
		cvs_reader = csv.reader(io.StringIO(content))
		body = list(cvs_reader)

		self.assertTrue(any(self.project.project_name in x for x in body))
		self.assertTrue(any(self.process.name in x for x in body))
		self.assertTrue(any(self.process.name+"-"+self.subprocess.name in x for x in body))







