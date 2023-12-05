from django.contrib import admin
from .models import Profile, Company, Project, Process, SubProcess, Sensor, SensorTime, Machine

# Register your models here.

@admin.register(Profile)
class Profile(admin.ModelAdmin):
  list_display = [field.name for field in
Profile._meta.get_fields()]

@admin.register(Company)
class Company(admin.ModelAdmin):
  list_display = ['company_name']

@admin.register(Machine)
class Machine(admin.ModelAdmin):
  list_display = ['name']

@admin.register(Project)
class Project(admin.ModelAdmin):
  list_display = ['project_name']

@admin.register(SubProcess)
class SubProcess(admin.ModelAdmin):
  list_display = ['name','manualName']

@admin.register(Process)
class Process(admin.ModelAdmin):
  list_display = ['name', 'manualName']

@admin.register(Sensor)
class Sensor(admin.ModelAdmin):
  list_display=['name','proName']

@admin.register(SensorTime)
class SensorTime(admin.ModelAdmin):
  list_display = [field.name for field in
SensorTime._meta.get_fields()]

