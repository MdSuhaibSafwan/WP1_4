from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from Main.models import Profile,Company
from django.contrib.auth.models import User, Group

class RegisterForm(UserCreationForm):
	"""Form to allow a user to register"""
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Enter email'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password1 = forms.CharField(label='Password' ,widget=forms.TextInput(attrs={'placeholder':'Passsword', 'type':'password'}))
	password2 = forms.CharField(label='Password Confirmation',widget=forms.TextInput(attrs={'placeholder':'Confirm Password', 'type':'password'}))
	
	
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		#widgets = {
#			'username': forms.TextInput(attrs={'class': 'usernameBox'}),
#		}

class RegisterFormProfile(ModelForm):	
	
	class Meta:
		model = Company
		fields = ['company_name']

class ContactForm(forms.Form):
	"""Form to allow a user to send an email to host email specified in settings"""
	form_email = forms.EmailField(required=True, label='Email', widget=forms.TextInput(attrs={'placeholder':'Enter email', 'style':'display:block;'}))
	subject = forms.CharField(required=True, label='Subject', widget=forms.TextInput(attrs={'placeholder':'Subject', 'style':'display:block;'}))
	message = forms.CharField(required = True, label='Message', widget=forms.Textarea(attrs={'placeholder':'Write your message here...', 'style':'display:block'}))
        

class EditProfile(UserChangeForm):
	"""class that uses and slight edits standard user change form"""
	password = None
		
	class Meta:
		model = User
		fields = ['username', 'email'] 

class PasswordProtectForm(forms.Form):
	password = forms.CharField(required=True, widget=forms.PasswordInput())

class SelectUserGroup(forms.Form):
	def __init__(self, *args, **kwargs):
		super(SelectUserGroup, self).__init__(*args, **kwargs) #passing company name to form so model choice field can access all profiles within company
		self.fields['choice'] = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Choose a Group")
		
		
		