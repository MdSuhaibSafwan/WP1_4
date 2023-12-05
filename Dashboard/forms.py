from django import forms
from django.forms import TextInput, ModelForm
from . models import * 
from MainData.models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from Main.models import *
from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput

class MetricForm(forms.Form):
	"""A form to allow the user to change the metric being displayed on the sub process chart"""

	choice = forms.ChoiceField(choices=METRIC_CHOICES, label='Choice', widget=forms.Select(), required=True)

class AssumedCostForm(forms.Form):
	value = forms.IntegerField(label='Value', widget=forms.TextInput(attrs={'placeholder':'Enter value', 'style':'width:10vw;'})) #assumed cost for automated project

class ManualProjectComparisonForm(forms.Form):
	def __init__(self, user, *args, **kwargs): #passing user to form
		super(ManualProjectComparisonForm, self).__init__(*args, **kwargs)
		projectSet = Project.objects.none()
		projectSet = user.profile.user_company.project_set.all().filter(manual=True) #get all projects within user company manual project set
		self.fields['choice'] = forms.ModelChoiceField(queryset=projectSet, empty_label="Select a Manual Project")  #select manual projects
	
	value = forms.IntegerField(label='Value', widget=forms.TextInput(attrs={'placeholder':'Enter Assumed cost part', 'style':'width:10vw;', 'style':'margin-right:150px;' }), required=True) #assumed cost for manual proejct

class LearningRateForm(forms.Form):
	value = forms.FloatField(label='Value', widget=forms.TextInput(attrs={'placeholder':'Enter Learning Rate', 'style':'width:10vw;'}))



class TimesForm(forms.Form):
	start_date_field = forms.DateField(widget=DatePickerInput)
	end_date_field = forms.DateField(widget=DatePickerInput)


class OEETimesForm(forms.Form):
	start_date = forms.DateField(widget=DatePickerInput)
	end_date= forms.DateField(widget=DatePickerInput)

class OEEForm(forms.Form):
	"""A form to allow the user to change the metric being displayed on the sub process chart"""

	choice = forms.ChoiceField(choices=OEE_CHOICES, label='Choice', widget=forms.Select(), required=True)
	value = forms.DecimalField(label='Value', widget=forms.TextInput(attrs={'placeholder':'Enter Value', 'style':'width:10vw;'}))
