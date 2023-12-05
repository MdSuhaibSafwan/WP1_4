from django import forms
from django.forms import TextInput, ModelForm
from Main.models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group


class CreateNewProject(forms.Form):
	"""A form to allow the user to create a new process"""

	name = forms.CharField(label='Name', max_length = 200, widget=forms.TextInput(attrs={'placeholder':'Enter Project Name', 'style':'width:30vw;'}))
	manual = forms.BooleanField(required=False)

class deleteProject(forms.Form):
	def __init__(self, company, *args, **kwargs):
		super(deleteProject, self).__init__(*args, **kwargs)
		self.fields['choice'] = forms.ModelChoiceField(queryset=company.project_set.all(), empty_label="Select Project Name", widget=forms.Select(attrs={'style':'height:2vw;'}))

class SelectMachines(forms.Form):
	"""Form to select the machines to add to a project"""
	def __init__(self, projectID, *args, **kwargs):
		super(SelectMachines, self).__init__(*args, **kwargs) #passing company name to form so model choice field can access all machines within a company
		projectInst = Project.objects.get(id=projectID)
		self.fields['machine'] = forms.ModelChoiceField(queryset=projectInst.possibleprojectmachines_set.all(), empty_label='Choose machine to add to project') 


class PossibleProForm(forms.Form):
	def __init__(self, projectID, *args, **kwargs):
		super(PossibleProForm, self).__init__(*args,**kwargs)
		project = Project.objects.get(id=projectID)
		self.fields['process'] = forms.ModelChoiceField(queryset=project.possibleprojectprocess_set.all(), empty_label="Select Process")

class PossibleSubProForm(forms.Form):
	def __init__(self, processID, *args, **kwargs):
		super(PossibleSubProForm, self).__init__(*args,**kwargs)
		process = Process.objects.get(id=processID)
		self.fields['name'] = forms.ModelChoiceField(queryset=process.possiblesubprocesses_set.all(), empty_label="Select Name")

	weightPoint = forms.BooleanField(required=False)
	finalWeighPoint = forms.BooleanField(required=False)

class addSubProcess(ModelForm):
	"""A form to allow the user to add a prespecified subprocess"""
	class Meta:
		model = SubProcess
		fields = ['name']

class addManualSubProcess(ModelForm):
	"""A form to allow the user to add a prespecified subprocess"""
	class Meta:
		model = SubProcess
		fields = ['manualName']

class SensorForm(forms.Form):
	def __init__(self, project, machine, *args, **kwargs):
		super(SensorForm,self).__init__(*args, **kwargs)
		self.fields['sensor'] = forms.ModelChoiceField(queryset=project.possibleprojectsensors_set.filter(machine=machine), empty_label="Select Sensor", required=True)


class SelectSensorFormAdmin(forms.Form):
	def __init__(self, sensorSet, *args, **kwargs): #passing sensor set for selection to be deleted (using model ID)
		super(SelectSensorFormAdmin, self).__init__(*args, **kwargs)
		self.fields['choice']=forms.ModelChoiceField(queryset=sensorSet, empty_label="Select A Sensor to delete!", required=True)


class UserDefineProSub(forms.Form):

	name = forms.CharField(label='Name', max_length = 200, widget=forms.TextInput(attrs={'placeholder':'Enter Process Name', 'style':'width:50%; border-radius:10px; display:block'}))
	weightPoint = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={}))
	finalWeighPoint = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={}))
	partTask = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={}))
	blankTask = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={}))
	plyTask = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={}))
	consolidationCheck = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={}))
	# will be needed later
	# manual = forms.BooleanField(required=False)

class AddTiaBlock(forms.Form):
	def __init__(self, project, machine, *args, **kwargs):
		super(AddTiaBlock, self).__init__(*args, **kwargs)
		self.fields['choice'] = forms.ModelChoiceField(queryset=project.possibleprojecttia_set.filter(machine=machine), empty_label="Select function block", required=True)

class AddRepeatBlock(forms.Form):
	def __init__(self, process, *args, **kwargs): #passing sensor set for selection to be deleted (using model ID)
		super(AddRepeatBlock, self).__init__(*args, **kwargs)
		self.fields['start']=forms.ModelChoiceField(queryset=process.subprocess_set.all(), empty_label="Select A Start Sub Process", required=True)
		self.fields['end']=forms.ModelChoiceField(queryset=process.subprocess_set.all(), empty_label="Select A Start End Process", required=True)
		self.fields['value'] = forms.IntegerField(label='Iterations', widget=forms.TextInput(attrs={'placeholder':'Iterations', 'style':'width:20vw;'}))

class EditCriterionForm(forms.Form):
	criterion = forms.CharField(label='Criterion', max_length = 800, widget=forms.TextInput(attrs={'placeholder':'Enter Criterion', 'style':'width:100%; margin-bottom:10px;'}))

class ProcessCheckForm(forms.Form):
	process_check = forms.BooleanField(required=False)