from django import forms
from django.forms import TextInput, ModelForm
from Main.models import *
#from . choices import * 
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group

class selectProcessPartForm(forms.Form):
	def __init__(self, processSet, *args, **kwargs): #passing process set so use can pick process part corresponding with project
		super(selectProcessPartForm, self).__init__(*args, **kwargs)
		self.fields['choice'] = forms.ChoiceField(choices=processSet,  label='Choice', widget=forms.Select(), required=True)