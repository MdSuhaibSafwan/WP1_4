#Django
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from .forms import *

def file_upload_view(response, sub_pro):
	if response.user.is_authenticated:
		if response.method == 'POST':
			form = FileUploadForm(response.POST, response.FILES)
			if form.is_valid():
				file = form.cleaned_data['file']
				sub_pro.file = file
				print('made it')
				sub_pro.save()
		else:
			form = FileUploadForm()
	else:
		redirect('/')

def image_upload_view(response, sub_pro):
	if response.user.is_authenticated:
		if response.method == 'POST':
			form = ImageUploadForm(response.POST, response.FILES)
			if form.is_valid():
				image = form.cleaned_data['image']
				sub_pro.image = image
				sub_pro.save()
		else:
			form = ImageUploadForm()
	else:
		redirect('/')

def run_edge_detection(response):
	if response.user.is_authenticated:
		if response.method == 'POST':
			# run edge detection
			print("this is here so I don't break")
	else:
		redirect('/')

