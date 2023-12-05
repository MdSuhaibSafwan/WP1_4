from django import forms
from django.forms import TextInput, ModelForm
from Main.models import *
from MainData.models import *
#from . choices import * 
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from django.forms import ModelChoiceField

class CreateNewProject(forms.Form):
	"""A form to allow the user to create a new process"""

	name = forms.CharField(label='Name', max_length = 200, widget=forms.TextInput(attrs={'placeholder':'Enter Project Name', 'style':'width:30vw;'}))
	manual = forms.BooleanField(required=False)

class deleteProject(forms.Form):
	def __init__(self, company, *args, **kwargs):
		super(deleteProject, self).__init__(*args, **kwargs)
		self.fields['choice'] = forms.ModelChoiceField(queryset=company.project_set.all(), empty_label="Select Project Name", widget=forms.Select(attrs={'style':'height:2vw;'}))
	
class addManualInfo(forms.Form):
	"""A form to allow the user to add a manual input"""

	task = forms.ChoiceField(choices=SubProcess.MANUAL_INPUT_CHOICES, label='Task', widget=forms.Select(), required=True)
	value = forms.CharField(label='Value', max_length = 200, widget=forms.TextInput(attrs={'placeholder':'Enter Value', 'style':'width:13vw;'}))

	def clean(self): #error handling for incorrect data
		super(addManualInfo , self).clean()
		error_message = ''

		if self.cleaned_data['value'] == "0":
			error_message = 'Value should not be zero!'
			raise forms.ValidationError(error_message)

		try:
			error_message = "Value should be numeric!"
			float(self.cleaned_data['value']) #try convert input to float, if it fails then the user entered a non-numeric value
		except:
			raise forms.ValidationError(error_message)

		return self.cleaned_data

class addManualTimeInfo(forms.Form):
	"""A form to allow the user to add a manual input"""

	task = forms.ChoiceField(choices=SubProcess.MANUAL_INPUT_TIME_CHOICES, label='Task', widget=forms.Select(), required=True)

class EditComponent(forms.Form):
	"""Form to allow the editing of a component"""	
	
	name = forms.CharField(label='Name', max_length = 200, widget=forms.TextInput(attrs={'placeholder':'Enter Component', 'style':'width:30vw;'}))	

class ChangeGraphTime(forms.Form):
	time = forms.IntegerField(label='time', widget=forms.TextInput(attrs={'placeholder':'Enter Time in Seconds', 'style':'width:35vw;'}))

class EnterDeviceID(forms.Form): 
	name = forms.CharField(label='Device ID', max_length = 200, widget=forms.TextInput(attrs={'placeholder':'Enter Device ID', 'style':'width:30vw;'}))	
	
class addProcess(forms.Form):
	def __init__(self, project, *args, **kwargs): #passing process into form so model choice field can access all part instances within process
		super(addProcess, self).__init__(*args, **kwargs)
		self.fields['choice'] = forms.ModelChoiceField(queryset=PossibleProjectProcess.objects.all().filter(project=project))

class addManualProcess(ModelForm):
	"""A form to allow the user to add a prespecified process"""
	class Meta:
		model = Process
		fields = ['manualName']
		lables = {
			'manualName' : _('Name'),		
		}		
		widgets = {
				'manualName': forms.Select(attrs={
				'placeholder':'Process'
				})	
		}
		
class operatorForm(forms.Form):
	def __init__(self, name, *args, **kwargs):
		super(operatorForm, self).__init__(*args, **kwargs) #passing company name to form so model choice field can access all profiles within company
		company = Company.objects.get(company_name=name)
		newset = Profile.objects.all().filter(user_company=company)
		self.fields['choice'] = forms.ModelChoiceField(queryset=newset, empty_label="Choose a User")

class PartInstanceForm(forms.Form):
	def __init__(self, process, *args, **kwargs): #passing process into form so model choice field can access all part instances within process
		super(PartInstanceForm, self).__init__(*args, **kwargs)
		choices = []
		if process.partinstance_set.all():
			for inst in PartInstance.objects.all().filter(process=process):
				choices.append(('Part' + str(inst),'Part Instance: ' + str(inst.instance_id)))
		if process.blankinstance_set.all():
			for inst in BlankInstance.objects.all().filter(process=process):
				choices.append(('Blank' + str(inst),'Blank Instance: ' + str(inst.instance_id)))
		if process.plyinstance_set.all():
			for inst in PlyInstance.objects.all().filter(process=process):
				choices.append(('Ply' + str(inst),'Ply Instance: ' + str(inst.instance_id)))

		#print(choices)
		self.fields['choice'] = forms.ChoiceField(choices=choices, label='Choice', widget=forms.Select())

class PlyInstanceForm(forms.Form):
	def __init__(self, process, *args, **kwargs): #passing process into form so model choice field can access all part instances within process
		super(PlyInstanceForm, self).__init__(*args, **kwargs)
		self.fields['choice'] = forms.ModelChoiceField(queryset=Ply.objects.all().filter(submitted=False), empty_label="Choose a Ply")

class BlankInstanceFrom(forms.Form):
	def __init__(self, process, *args, **kwargs): #passing process into form so model choice field can access all part instances within process
		super(BlankInstanceForm, self).__init__(*args, **kwargs)
		self.fields['choice'] = forms.ModelChoiceField(queryset=Blank.objects.all().filter(submitted=False), empty_label="Choose a Blank")



class ProjectPartInstanceForm(forms.Form):
	def __init__(self, project, *args, **kwargs): #passing process into form so model choice field can access all part instances within process
		super(ProjectPartInstanceForm, self).__init__(*args, **kwargs)
		self.fields['choice'] = forms.ModelChoiceField(queryset=project.part_set.filter(submitted=False), empty_label="Choose a Part")

class addSubProcess(forms.Form):
	"""A form to allow the user to add a prespecified subprocess"""
	def __init__(self, process, *args, **kwargs): #passing process into form so model choice field can access all part instances within process
		super(addSubProcess, self).__init__(*args, **kwargs)
		self.fields['name'] = forms.ModelChoiceField(queryset=PossibleSubProcesses.objects.all().filter(process=process))

class addManualSubProcess(forms.Form):
	"""A form to allow the user to add a prespecified subprocess"""
	def __init__(self, process, *args, **kwargs): #passing process into form so model choice field can access all part instances within process
		super(addManualSubProcess, self).__init__(*args, **kwargs)
		self.fields['name'] = forms.ModelChoiceField(queryset=PossibleSubProcesses.objects.all().filter(process=process))

class SensorForm(forms.Form):
	def __init__(self, process, *args, **kwargs): #passing process into form so model choice field can access all part instances within process
		super(SensorForm, self).__init__(*args, **kwargs)
		self.fields['choice'] = forms.ModelChoiceField(queryset=PossibleSensors.objects.all().filter(process=process))

class PossibleSensorForm(ModelForm): 
	class Meta:
		model = PossibleSensors
		fields = ['name']

class ProcessSensorForm(ModelForm): 
	
	class Meta:
		model = Sensor
		fields = ['proName']
		labels = {
			'proName': ('Name'),		
		}
		
class MachineForm(ModelForm):
	
	class Meta:
		model = Machine
		fields = ['name']

class SelectSensorForm(forms.Form): #needs to be tested
	def __init__(self, sensorSet, *args, **kwargs): #passing sensor set for selection to be deleted (using model ID)
		super(SelectSensorForm, self).__init__(*args, **kwargs)

		self.fields['choice']=forms.ModelChoiceField(queryset=sensorSet.values_list('modelID', flat=True), empty_label="Select A Sensor to delete!", required=True)
		
class ConstForm(forms.Form):
	"""A form to allow the user to add a Project constant value"""
	def __init__(self, group, *args, **kwargs):
		super(ConstForm, self).__init__(*args, **kwargs) 
		#passing user group to form so model choice field can choose which choice feild to use
		if group == "Management":
			self.fields['choice'] = forms.ChoiceField(choices=Project.CONST_CHOICES_MANG, label='Choice', widget=forms.Select(), required=True)
		elif group == "Supervisor":
			self.fields['choice'] = forms.ChoiceField(choices=Project.CONST_CHOICES_SUPER, label='Choice', widget=forms.Select(), required=True)
		self.fields['value'] = forms.DecimalField(label='Value', widget=forms.TextInput(attrs={'placeholder':'Enter value', 'style':'width:35vw;'}))
  
	def clean(self):
		super(ConstForm , self).clean()
		error_message = ''

		try:
			error_message = "Value should be numeric!"
			float(self.cleaned_data['value'])
		except:
			raise forms.ValidationError(error_message)


		return self.cleaned_data


class PreviousMaterialForm(forms.Form):
	"""A form to allow the user to add a Project constant value"""

#	choice = forms.ChoiceField(choices=Project.PREV_MATERIAL_CHOICES, label='Choice', widget=forms.Select(), required=True)
	value = forms.DecimalField(label='Value', widget=forms.TextInput(attrs={'placeholder':'Enter value', 'style':'width:35vw;'}))


class EnterPartWeight(forms.Form):#needs to be tested
	
	value = forms.IntegerField(label='Weight', widget=forms.TextInput(attrs={'placeholder':'Enter weight', 'style':'width:35vw;'}))

class AddMaterialForm(ModelForm):#needs to be tested
	
	class Meta:
		model = Material
		fields = ['name']
		widgets = {
				'name': forms.Select(attrs={
				'placeholder':'Material'
				})	
		}


class SubMasterForm(forms.Form):
	def __init__(self, name, *args, **kwargs): #passing subprocess name to access specific fields for each sub process
		super(SubMasterForm, self).__init__(*args, **kwargs)
		if name == "Material and Tool Inside Press":
			self.fields['choice'] = forms.ChoiceField(choices=SubProcess.MATERIAL_IN_PRESS_CHOICES, label = 'Choice', widget=forms.Select(), required=True)
			self.fields['value'] = forms.DecimalField(label='value', widget=forms.TextInput(attrs={'placeholder':'Enter value', 'style':'width:5.5vw;'}))
		elif name == "Material Pressed":
			self.fields['choice'] = forms.ChoiceField(choices=SubProcess.MATERIAL_PRESSED_CHOICES, label = 'Choice', widget=forms.Select(), required=True)
			self.fields['value'] = forms.DecimalField(label='value', widget=forms.TextInput(attrs={'placeholder':'Enter value', 'style':'width:5.5vw;'}))
		elif name == "Removal End effector actuated":
			self.fields['choice'] = forms.ChoiceField(choices=SubProcess.REMOVAL_EFFECTOR_CHOICES, label = 'Choice', widget=forms.Select(), required=True)
			self.fields['value'] = forms.DecimalField(label='value', widget=forms.TextInput(attrs={'placeholder':'Enter value', 'style':'width:5.5vw;'}))
		elif name == "Final Inspection":
			self.fields['choice'] = forms.ChoiceField(choices=SubProcess.TRIMMING_CHOICES, label = 'Choice', widget=forms.Select(), required=True)
			self.fields['value'] = forms.DecimalField(label='value', widget=forms.TextInput(attrs={'placeholder':'Enter value', 'style':'width:5.5vw;'}))
			
class ProcessWindowForm(forms.Form):
	
	value = forms.BooleanField(required = False)


