from django.test import TestCase
from django.test import TestCase, Client
from django.db.models import ForeignKey
from datetime import datetime,date,time,timedelta, timezone
from django.urls import reverse, resolve
import json
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import *
from django.test.utils import setup_test_environment 

from .forms import * 
from Main.models import *
from.views import *
from WP1_4.urls import *

class UrlTests(TestCase):
	def test_register_url(self):
		url = reverse('register')
		self.assertEqual(resolve(url).func, register)

	def test_user_edit_view_url(self):
		url = reverse('edit_profile')
		self.assertEqual(resolve(url).func, UserEditView)

	def test_user_edit_password_url(self):
		url = reverse('edit_password')
		self.assertEqual(resolve(url).func, change_password)

	def test_contact_url(self):
		url = reverse('contact')
		self.assertEqual(resolve(url).func, contact)

	def test_faq_url(self):
		url = reverse('faq')
		self.assertEqual(resolve(url).func, faq)
		

class ViewTests(TestCase):
	
	def setUp(self):
		self.client = Client()
		self.register_url = reverse('register')
		self.edit_profile_url = reverse('edit_profile')
		self.change_password_url = reverse('edit_password')
		self.contact_url = reverse('contact')
		self.faq_url = reverse('faq')
		self.user = User.objects.create_user(username='Test User', email='test@test.com', password='Test')
		self.client.login(username='Test User', password='Test')
		
	def test_register_page_return(self):				
		response = self.client.post(self.register_url)			
	
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Login/register.html')

	def test_edit_profile_return(self):
		response = self.client.post(self.edit_profile_url)

		self.assertEqual(str(response.context['user']), 'Test User')	
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'registration/edit_profile.html')

	def test_edit_password_return(self):
		response = self.client.post(self.change_password_url)

		self.assertEqual(str(response.context['user']), 'Test User')	
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Login/edit_password.html')

	def test_contact_return(self):
		response = self.client.post(self.contact_url)

		self.assertEqual(str(response.context['user']), 'Test User')	
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Login/contact.html')

	def test_faq_return(self):
		response = self.client.post(self.faq_url)

		self.assertEqual(str(response.context['user']), 'Test User')	
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Login/faq.html')


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
		self.client.login(username='Test User', password='Test')

	def test_register_form(self):
		self.form = RegisterForm(data={"email": "test@test.com", "username": "TestMrMan", "password1":"TestMr!$""!$JDF", "password2":"TestMr!$""!$JDF"})
		
		self.assertTrue(self.form.is_valid())
		self.assertTrue(self.form['email'].value() == "test@test.com" and self.form['username'].value()=="TestMrMan" and 
			self.form['password1'].value() == "TestMr!$""!$JDF" and self.form['password2'].value() == "TestMr!$""!$JDF")

		self.testuser = User.objects.create_user(username=self.form['username'].value(), email = self.form['email'].value(), password=self.form['password1'].value())
		self.assertTrue(self.testuser.username == self.form['username'].value() and self.testuser.email == self.form['email'].value()) 

	def test_register_form_profile(self):
		self.form = RegisterFormProfile(data={"company_name":"test_comp"})
		self.assertTrue(self.form.is_valid())

		self.assertEqual(self.form['company_name'].value(), "test_comp")

	def test_contact_form(self):
		self.form = ContactForm(data={"form_email": "test@test.com", "subject":"test Subject", "message": "test message"})
		self.assertTrue(self.form.is_valid())

		self.assertTrue(self.form['form_email'].value() == "test@test.com" and self.form['subject'].value() == "test Subject" and self.form['message'].value() == "test message")

	def test_edit_profile_form(self):
		self.form = EditProfile(data={"username":"testman", "email":"test@test.com"})
		self.assertTrue(self.form.is_valid())

		self.assertTrue(self.form['username'].value() == "testman" and self.form['email'].value() == "test@test.com")




