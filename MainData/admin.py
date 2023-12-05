from django.contrib import admin

from .models import  Part, ProcessPart, SubProcessPart, SensorData, SensorTimeData


@admin.register(Part)
class Part(admin.ModelAdmin):
  list_display = ['part_id']

@admin.register(ProcessPart)
class ProcessPart(admin.ModelAdmin):
  list_display = ['processName']

@admin.register(SubProcessPart)
class SubProcessPart(admin.ModelAdmin):
  list_display = ['subProcessName']

@admin.register(SensorData)
class SensorData(admin.ModelAdmin):
  list_display=['sensorName']

@admin.register(SensorTimeData)
class SensorTimeData(admin.ModelAdmin):
  list_display = [field.name for field in
SensorTimeData._meta.get_fields()]