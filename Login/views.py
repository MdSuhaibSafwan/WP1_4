from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm,RegisterFormProfile,ContactForm,EditProfile, PasswordProtectForm ,SelectUserGroup
from django.views import generic
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.core.mail import send_mail, BadHeaderError
from Main.models import Company,Profile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Group, Permission
# Create your views here.

def register(response):
	"""View to allow user to register. Checks input is ok and redirects to login page""" 
	if response.method == 'POST':
		#pass response into forms
		user_form= RegisterForm(response.POST)		
		profile_form = RegisterFormProfile(response.POST)
		#check if forms are valid
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			#reload the user so they are not anonymous
			user.refresh_from_db()  
			#get password
			raw_password = user_form.cleaned_data.get('password1')
			# login user after signing up
			user = authenticate(username=user.username, password=raw_password)
			login(response, user)			
			
			#read in company selection and clean it		
			companyDirty = profile_form.cleaned_data['company_name'] 
			company_name = Company.company_choices_dict[companyDirty]
			
			#test if company exists and create relation to user
			if Company.objects.filter(company_name=company_name).exists():
				found_company = Company.objects.get(company_name=company_name)
			else:
				found_company = Company.objects.create(company_name=company_name)
			
			#save company to associated user profile
			user_profile = user.profile
			user_profile.user_company = found_company
			user_profile.save()
			
			#redirect to home page
			return redirect('/')
		
	else:
		#load empty forms
		user_form = RegisterForm()
		profile_form = RegisterFormProfile()
	
	#return response, page and forms 
	return render(response, 'Login/register.html', {'user_form': user_form, 'profile_form' : profile_form})
		
def logout(response):
	"""View to allow user to log out"""
	#return response and logout page
	return render(response, "Login/logout.html", {})
		
def UserEditView(response):
	"""View to allow user to change their details"""
	#setup	

	if response.user.is_authenticated:
		error = ''
		
		if response.method == 'POST':
			#pass response and instance to form
			form = EditProfile(response.POST, instance=response.user)
			#check form is valid
			if form.is_valid():
				#save changes
				form.save()
				#pass success
				error = 'edit made'
			else:
				#pass error
				error = 'something wrong'
		else:
			#pass instance to form to auto fill fields
			form = EditProfile(instance=response.user)
		#return page, form and var
		return render(response, 'registration/edit_profile.html', {'form':form, 'error':error})
	else:
		return redirect('/mylogout/')

def change_password(response):
	"""View to allow the user to change their password"""
	if response.user.is_authenticated:
		if response.method == 'POST':
			#pass response to form 
			form = PasswordChangeForm(response.user, response.POST)
			#check form valid
			if form.is_valid():
				#save changes
				user = form.save()
				#log user back in with new password
				update_session_auth_hash(response, user)
				messages.success(response, 'successful reset')
			else:
				#show visual error
				messages.error(response, 'There is an error')
		else:
			#pass required argument to django standard form
			form = PasswordChangeForm(response.user)
		return render(response, 'Login/edit_password.html', {'form':form})
	else:
		return redirect('/mylogout/')
	
def contact(response):
	"""View to allow user to complete the contact form"""
	#setup
	form = ContactForm(initial = {'form_email':response.user.email})
	error =''
	if response.user.is_authenticated:
		if response.method == 'POST':
			#pass response to form
			form = ContactForm(response.POST)
			#check form valid
			if form.is_valid():
				#read in inputs 
				subject = form.cleaned_data['subject']
				form_email = form.cleaned_data['form_email']
				message = form.cleaned_data['message']
				
				#try to send email
				try:
					#send email 
					send_mail(subject, form_email +' said: '+ message, form_email, ['t.knight@airborne.com'])
					#show email sent
					error = 'Your email has successfully sent. We will never get back to you'
					#return response, page, var and form 
					return render(response, 'Login/contact.html', {'error':error, 'form':form})
				except BadHeaderError:
					#display error
					error = 'failure'
		else:
			#pass empty form
			form = ContactForm(initial = {'form_email':response.user.email})
		
		#return response, page and form 
		return render(response, 'Login/contact.html', {'form':form})
	else:
		return redirect('/mylogout/')

def faq(response):
	"""View to allow user to complete the contact form"""
	#setup
	if response.user.is_authenticated:
		return render(response, 'Login/faq.html')
	else:
		return redirect('/mylogout/')


def edit_user_group(response):
	if response.user.is_authenticated:
		if response.user.groups.filter(name="Admin").exists():
			authenticated = False
			password_protect_form = PasswordProtectForm()
			select_group_form = SelectUserGroup()

			if response.POST.get('enterPassword'):
				password_protect_form = PasswordProtectForm(response.POST)

				if password_protect_form.is_valid():
					if check_password(password_protect_form.cleaned_data['password'], response.user.password):
						authenticated = True
					else:
						messages.error(response, "Incorrect Password!")

			if response.POST.get('enterGroup'):
				select_group_form = SelectUserGroup(response.POST)

				if select_group_form.is_valid():
					group = select_group_form.cleaned_data['choice']
					response.user.groups.clear()
					adminG = Group.objects.get(name="Admin")
					response.user.groups.add(group, adminG)
					response.user.save()
					messages.success(response, 'Group successfully Assigned!')

			return render(response, 'Login/edit_user_group.html', {'select_group_form': select_group_form,'password_protect_form':password_protect_form, 'authenticated':authenticated})
		else:
			return redirect('/')
	else:
		return redirect('/')

def auto_creation(response):
	admin_group, admin_created = Group.objects.get_or_create(name="Admin")
	manager_group, manager_created = Group.objects.get_or_create(name="Management")
	supervisor_group, supervisor_created = Group.objects.get_or_create(name="Supervisor")
	technician_group, technician_created = Group.objects.get_or_create(name="Technician")
	energy_group, energy_created = Group.objects.get_or_create(name="Energy")

	company, created = Company.objects.get_or_create(company_name="Airborne")

	if not User.objects.filter(username="Admin").exists():
		admin_user = User.objects.create_user(username="Admin", email="Admin@airborne.com", password="Admin1")
		profile = admin_user.profile
		profile.user_company = company
		profile.save()
		admin_user.groups.add(admin_group, manager_group, supervisor_group, technician_group, energy_group)
		admin_user.is_superuser = True 
		admin_user.is_staff = True
		admin_user.save()

	if not User.objects.filter(username="Management").exists():
		manager = User.objects.create_user(username="Management", email="Management@airborne.com", password="Hello1")
		profile = manager.profile
		profile.user_company = company
		profile.save()
		manager.groups.add(manager_group)
		manager.save()

	if not User.objects.filter(username="Supervisor").exists():
		supervisor = User.objects.create_user(username="Supervisor", email="Supervisor@airborne.com", password="Hello1")
		profile = supervisor.profile
		profile.user_company = company
		profile.save()
		supervisor.groups.add(supervisor_group)
		supervisor.save()

	if not User.objects.filter(username="Technician").exists():
		technician = User.objects.create_user(username="Technician", email="Techy@airborne.com", password="Hello1")
		profile = technician.profile
		profile.user_company = company
		profile.save()
		technician.groups.add(technician_group)
		technician.save()

	if not User.objects.filter(username="Energy").exists():
		energy = User.objects.create_user(username="Energy", email="Energy@airborne.com", password="Hello1")
		profile = energy.profile
		profile.user_company = company
		profile.save()
		energy.groups.add(energy_group)
		energy.save()

	return redirect('/login')
