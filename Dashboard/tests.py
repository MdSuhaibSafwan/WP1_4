from django.test import TestCase, Client
from django.db.models import ForeignKey
from datetime import datetime,date,time,timedelta, timezone
from django.urls import reverse, resolve
import json
from django.contrib.auth.models import User, Group
from django.test.utils import setup_test_environment 

from .models import *
from MainData.models import *
from Main.models import *
from .forms import *

from.views import *

class UrlTests(TestCase):
	
	def test_view_project_dashboard(self):
		url = reverse('projectDash')
		self.assertEqual(resolve(url).func, project_dash)
		
	def test_view_dash_url(self):
		url = reverse('dashboard', kwargs={'id':1})
		self.assertEqual(resolve(url).func, dashboard)
		
	def test_view_part_graph_url(self):
		url = reverse('partGraph')
		self.assertEqual(resolve(url).func, part_graph)

	def test_view_pie_chart_url(self):
		url = reverse('pieChart', kwargs={'id':1})
		self.assertEqual(resolve(url).func, pie_chart)
		
	def test_view_subChart_url(self):
		url = reverse('subChart', kwargs={'id':1, 'choice':'test'})
		self.assertEqual(resolve(url).func, sub_chart)
		
	def test_view_cost_model_chart_url(self):
		url = reverse('costModelChart', kwargs={'id':1, 'error':'test', 'mID':1})
		self.assertEqual(resolve(url).func, cost_model_chart)

class ViewTests(TestCase):
	
	def setUp(self):
		self.client = Client()
		self.project_url = reverse('projectDash')
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
		
		

		self.all_dash_url = reverse('dashboard', kwargs={'id':self.project.id})
	

		self.client.login(username='Test User', password='Test')
		
		
	def test_show_dashboard_projects_return(self):				
		response = self.client.post(self.project_url)			
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_view_dashboard_projects_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()		
		
		response = self.client.post(self.project_url)
		
		self.assertEqual(str(response.context['user']), 'Test User')		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Dashboard/selectProjectDash.html')
		
	def test_project_belong_to_user(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()		
		
		response = self.client.post(self.project_url)
		
		self.assertQuerysetEqual(self.user.profile.user_company.project_set.all(), response.context['user'].profile.user_company.project_set.all(), transform=lambda 	x: x, ordered=False)
		
	def test_dash_no_return(self):	
		self.user.save()					
			
		response = self.client.post(self.all_dash_url)
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')
		
	def test_dash_page_return(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()			
			
		response = self.client.post(self.all_dash_url)
		
		self.assertTemplateUsed(response, 'Dashboard/dashboard.html')
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
		self.user.profile.user_company = self.company
		self.failureCompany = Company.objects.create(company_name = 'Failure Company')
		self.project = Project.objects.create(company=self.company, project_name='Test Project')
		self.manualProject = Project.objects.create(company=self.company, project_name='Test Manual Project', manual=True)
		self.failureProject= Project.objects.create(company=self.company, project_name='Failure Project')
		self.process = Process.objects.create(project = self.project, name = "Test Process")
		self.subprocess = SubProcess.objects.create(process=self.process, name= 'Test SubProcess')
		self.manualProcess = Process.objects.create(project = self.manualProject, manualName = "Test Manual Process")
		self.manualSubProcess = SubProcess.objects.create(process=self.manualProcess, manualName= 'Test Manual SubProcess')
		self.all_process_url = reverse('showAllProcess', kwargs={'id':self.project.id})
		self.all_manual_process_url = reverse('showAllProcess', kwargs={'id':self.manualProject.id})
		self.all_sub_process_url = reverse('showProcess', kwargs={'id':self.process.id})
		self.all_manual_sub_process_url = reverse('showProcess', kwargs={'id':self.manualProcess.id})
		self.all_sub_process_detail_url = reverse('showSub', kwargs={'id':self.subprocess.id})
		self.client.login(username='Test User', password='Test')

	def test_metric_form(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	
		self.form = MetricForm(data={"choice": "CYT"})

		self.assertTrue(self.form.is_valid())
		self.assertEqual("CYT", self.form['choice'].value())

	def test_assumed_cost_form(self):
		self.user.groups.add(self.mang_group, self.super_group)
		self.user.save()	
		self.form = AssumedCostForm(data={"value": 4})

		self.assertTrue(self.form.is_valid())
		self.assertEqual(4, self.form['value'].value())

		