from django import forms
from django.forms import TextInput, ModelForm
from Main.models import *

class ImageUploadForm(ModelForm):
	class Meta:
		model = SubProcess
		fields = ['image']

class FileUploadForm(ModelForm):
	class Meta:
		model = SubProcess
		fields = ['file']

