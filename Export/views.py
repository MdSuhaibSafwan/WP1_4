from django.shortcuts import render
from django.contrib import messages

#Django
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.db.models.fields import NOT_PROVIDED

#Importing local .py files
from Main.forms import *
from Main.models import *
from MainData.models import *

#Importing DateTime
from datetime import datetime,date,time,timedelta

#import json
import json, csv, io

#Importing reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch, A4, A3, landscape
from reportlab.lib.units import cm, mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet 
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER 
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Flowable, FrameBreak, KeepTogether, PageBreak, Spacer
from reportlab.platypus import Frame, PageTemplate, KeepInFrame
from reportlab.lib.units import cm
from reportlab.platypus import (Table, TableStyle, BaseDocTemplate)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch


def exportCSV(response, id, partID):

	ProcessName, SubProcessName, SensorName ="", "", ""
	management, supervisor = False,False

	part = Part.objects.get(part_id=partID)
	Proc= ProcessPart.objects.get(part=part)
	sensors = Proc.sensordata_set.all()
	Manual = Proc.part.project.manual

	if Manual:
		ProcessName = Proc.processName
	else:
		ProcessName = Proc.processName

	if response.user.groups.filter(name='Management').exists():
		management = True
	if response.user.groups.filter(name='Supervisor').exists():
		supervisor = True
	#if user is in company
	if response.user.is_authenticated:
		if Proc.part.project in response.user.profile.user_company.project_set.all():

			#if user is in the Manager Group
			if management:			
				#Preliminary CSV assignments
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment;filename=Management-SubProcessData.csv'
				writer = csv.writer(response)

				#Writing the Main process and correlating attributes to CSV
				writer.writerow(['Main Process: '])
				writer.writerow(['Name', 'Cycle Time', 'Process Time', 'Interface Time', 'Scrap Rate'])
				writer.writerow([ProcessName, Proc.cycleTime, Proc.processTime, Proc.interfaceTime, Proc.scrapRate])
				#Writing the associated machines to CSV
				writer.writerow([' '])
				writer.writerow(['Sub Processes: '])
				#Writing Sub-process attributes to CSV
				writer.writerow(['Name', 'Date', 'Cycle Time', 'Process Time', 'Scrap Rate', 'Material Wastage', 'Cost Of Material Waste', 'Cost of Scrap', 'Cost of Part', 'Technician Labour Cost', 'Supervisor Labour Cost', 'Power Consumption cost', 'CO2 Emissions from power'])
				for each in Proc.order_subprocesspart():
			
					SubProcessName = each.subProcessName
					writer.writerow([SubProcessName, date.today(), each.proIntTime,each.processTime, each.scrapRate, each.materialWastage, each.materialWastageCost, each.materialScrapCost, each.materialPartCost, each.technicianLabourCost, each.supervisorLabourCost,each.powerCost,each.CO2])
				#Writing Sub-process sensor attributes to CSV
				writer.writerow([' '])


			elif supervisor:
				#Preliminary CSV assignments
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment;filename=Supervisor-SubProcessData.csv'
				writer = csv.writer(response)

				
				ProcessName = Proc.processName

				writer.writerow(['Main Process: ', ProcessName])
				#for every sub-process, write these attributes
				for each in Proc.order_subprocesspart():
					SubProcessName= each.subProcessName
					if SubProcessName == "Material and Tool Inside Press":
						writer.writerow(['Name', 'Date', 'Process Pass?', 'Quality Pass?', 'Centre position error at tension frame', 'Centre position error at male tool'])
						writer.writerow([SubProcessName, date.today(), each.processCheck, each.qualityCheck, '1.0%', '2.3%'])
					elif SubProcessName == "Material Pressed":
						writer.writerow(['Name', 'Date', 'Process Pass?', 'Quality Pass?', 'Time if Passed', 'Time criteria when passed'])
						writer.writerow([SubProcessName, date.today(), each.processCheck, each.qualityCheck, '23', '21'])
					elif SubProcessName == "Removal End effector actuated":
						writer.writerow(['Name', 'Date', 'Process Pass?', 'Quality Pass?', 'Vertical position error of end effector'])
						writer.writerow([SubProcessName, date.today(), each.processCheck, each.qualityCheck, '1.0%'])
					elif SubProcessName == "Final Inspection":
						writer.writerow(['Name', 'Date', 'Process Pass?', 'Quality Pass?', 'Geometry Quality Pass?', 'Weight Quality Pass?', 'Wrinkle/Bridging Quality Pass?', 'Width Error', 'Length Error', 'Depth Error', 'Weight error', 'Number of wrinkle(s)/bridging'])
						writer.writerow([SubProcessName, date.today(), each.processCheck, each.qualityCheck, True, False, True, '1.0%', '2.0%', '1.5%', '2%', '5'])
					else:
						writer.writerow(['Name', 'Date', 'Process Pass?', 'Quality Pass?'])
						writer.writerow([SubProcessName, date.today(), each.processCheck, each.qualityCheck])
					writer.writerow([' '])
				#for every sub-process sensor set, write attributes to CSV
				writer.writerow(['Sub Process Sensors: '])
				for instance in Proc.order_subprocesspart():
					sensors = instance.sensordata_set.all()
					for sensorinstance in sensors:
						SensorName = sensorinstance.sensorName 
						SubProcessName = instance.subProcessName
						writer.writerow([' '])
						writer.writerow(['Sub-Process Name',  'Sensor Name', 'Position X (mm)', 'Position Y (mm)', 'Position Z (mm)', 'Thickness Error'])
						writer.writerow([SubProcessName, SensorName, '72', '0.05', '30', '2%'])
			else:
				return redirect('/') 
			#return CSV file
			return response
		else:
			return redirect('/')
	else:
		return redirect('/')

def exportPDF(response, id, partID):
	management, supervisor, manualProject = False, False, False
	#assigning Main Process objects and corresponding Sub-processes, sensors and machines
	#process_ID = response.session.get('id')
	part = Part.objects.get(part_id=partID)
	Proc = ProcessPart.objects.get(part=part)
	sensors = Proc.sensordata_set.all()
	Manual = Proc.part.project.manual

	buffer, AirborneIMG, distance =  io.BytesIO(), "static/Main/logo.png", 0

	today = date.today()
	timestamp = today.strftime("%d/%m/%Y")
	#Airborne image grabbed from their website

	ProcessName = Proc.processName
	subProName = ""
	sensorName=""

	if response.user.groups.filter(name='Management').exists():
		management = True
	if response.user.groups.filter(name='Supervisor').exists():
		supervisor = True


	if response.user.is_authenticated:
		if Proc.part.project in response.user.profile.user_company.project_set.all():
			PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
			Title = "Process Data"
			pageinfo = "Airborne LTD."

			def myFirstPage(canvas, doc):
				canvas.saveState()
				canvas.setFont('Times-Bold',16)
				canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
				canvas.setFont('Times-Roman',9)
				canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
				canvas.restoreState()
			def myLaterPages(canvas, doc):
				canvas.saveState()
				canvas.setFont('Times-Roman',9)
				canvas.drawString(inch,0.75 * inch, "Page %d / %s" % (doc.page, pageinfo)) 
				canvas.restoreState()

			buffer=io.BytesIO()
			response = HttpResponse(content_type='application/pdf')

			if management:
				#assigning preliminary PDF attributes
				
				response['Content-Disposition'] = 'attachment; filename = "Management-ProcessData.pdf"'

				styles = getSampleStyleSheet()
				AirborneIMG = "static/Main/logo.png"

				doc = SimpleDocTemplate(buffer)
				Story = [Image(AirborneIMG, width=200, height=100)]
				style = styles["Normal"]
				#Table Data
				data = [['Process Name', 'Cycle time', 'Process Time', 'Interface Time', 'Scrap Rate'],
				[ProcessName, Proc.cycleTime, Proc.processTime, Proc.interfaceTime, Proc.scrapRate]]

				table = Table(data)
				table.setStyle([("VAlIGN", (0,0), (-1,-1), "MIDDLE"),
					("ALIGN", (0,0), (-1,-1), "CENTRE"),
					("GRID", (0,0), (-1,-1),0.25, colors.black)
					])
				Story.append(table)
				Story.append(Spacer(1,0.2*inch))
				data = [['Sub Process', 'Cycle Time', 'Process Time', 'Scrap Rate', 'Material Wastage', 'Material Waste Cost', 'Cost of Scrap', 'Cost of Part', 'Technician Cost', 'Supervisor Cost', 'Power Consumption', 'CO2 Consumption']]
				for each in Proc.order_subprocesspart():
					subProName = each.subProcessName
					data.append(
						   [subProName, each.proIntTime,each.processTime, each.scrapRate, each.materialWastage, each.materialWastageCost, each.materialScrapCost, each.materialPartCost, each.technicianLabourCost, each.supervisorLabourCost,each.powerCost,each.CO2])

				temptable = Table(data)
				temptable.setStyle([("VAlIGN", (0,0), (-1,-1), "MIDDLE"),
				("ALIGN", (0,0), (-1,-1), "CENTRE"),
				("GRID", (0,0), (-1,-1),0.25, colors.black),
				("FONTSIZE", (0,0), (-1,-1), 4.6),
				])
				Story.append(temptable)

				doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

				response.write(buffer.getvalue())
				buffer.close() 

				return response
			elif supervisor:
				#preliminary PDF assignments
				response['Content-Disposition'] = 'attachment; filename = "Supervisor-ProcessData.pdf"'

				styles = getSampleStyleSheet()
				AirborneIMG = "static/Main/logo.png"

				doc = SimpleDocTemplate(buffer)
				Story = [Image(AirborneIMG, width=200, height=100)]
				style = styles["Normal"]

				for each in Proc.order_subprocesspart():
					subProName = each.subProcessName
					#for every sub-process, draw this table
					#dependent cases
					if subProName =="Material Pressed":
						data = [['Sub Process',  'Date', 'Process Pass?', 'Quality Pass?', 'Time if passed?', 'Time Criteria'],
								[subProName, date.today(), 'False', 'True', '21', '23']]
						temptable = Table(data)
						temptable.setStyle([("VAlIGN", (0,0), (-1,-1), "MIDDLE"),
											("ALIGN", (0,0), (-1,-1), "CENTRE"),
											("GRID", (0,0), (-1,-1),0.25, colors.black),
											("FONTSIZE", (0,0), (-1,1), 8),
											])
						
					elif subProName =="Material and Tool Inside Press":
						data = [['Sub Process','Date', 'Process Pass?', 'Quality Pass?', 'Centre error at tension frame', 'Centre error at male tool'],
								[subProName, date.today(), 'False', 'True', '1.0%', '0.5%']]
						temptable = Table(data)
						temptable.setStyle([("VAlIGN", (0,0), (-1,-1), "MIDDLE"),
											("ALIGN", (0,0), (-1,-1), "CENTRE"),
											("GRID", (0,0), (-1,-1),0.25, colors.black),
											("FONTSIZE", (0,0), (-1,1), 8),
											])
						
					elif subProName == "Removal End effector actuated":
						data = [['Sub Process','Date', 'Process Pass?', 'Quality Pass?', 'Vertical position error of end effector'],
								[subProName, date.today(), 'False', 'True', '1.2%']]
						temptable = Table(data)
						temptable.setStyle([("VAlIGN", (0,0), (-1,-1), "MIDDLE"),
											("ALIGN", (0,0), (-1,-1), "CENTRE"),
											("GRID", (0,0), (-1,-1),0.25, colors.black),
											("FONTSIZE", (0,0), (-1,1), 8),
											])
						
					elif subProName == "Final Inspection":
						data = [['Sub Process','Date', 'Process Pass?', 'Quality Pass?', 'Geometry Quality?', 'Weight Quality?', 'Wrinkle Quality?', 'Width Error', 'Length Error', 'Depth error', 'Weight error', 'NO. wrinkle(s)'],
								[subProName, date.today(), 'False', 'True', 'False', 'True', 'False', '1.2%', '1.0%', '2.0%', '1.5%', '5']]
						temptable = Table(data)
						temptable.setStyle([("VAlIGN", (0,0), (-1,-1), "MIDDLE"),
											("ALIGN", (0,0), (-1,-1), "CENTRE"),
											("GRID", (0,0), (-1,-1),0.25, colors.black),
											("FONTSIZE", (0,0), (-1,1), 6.5),
											])
					
					else:
						#default case
						data = [['Sub Process','Date', 'Process Pass?', 'Quality Pass?'],
								[subProName, date.today(), 'False', 'True']]
						temptable = Table(data)
						temptable.setStyle([("VAlIGN", (0,0), (-1,-1), "MIDDLE"),
											("ALIGN", (0,0), (-1,-1), "CENTRE"),
											("GRID", (0,0), (-1,-1),0.25, colors.black),
											("FONTSIZE", (0,0), (-1,1), 8),
											])
					Story.append(temptable)
					Story.append(Spacer(1,0.2*inch))

				for each in Proc.order_subprocesspart():
					subProName = each.subProcessName
				
					data = [['Sub Process', 'Sensor Name', 'Position X', 'Position Y', 'Position Z', 'Thickness Error']]
	
					for instance in each.sensordata_set.all():
						sensorName = instance.sensorName
						#for every sub-process sensor set, draw this table with corresponding value	
						data.append([subProName, sensorName, '72', '0.05', '7', '2%'])

				temptable = Table(data)
				temptable.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
									("ALIGN", (0,0), (-1,-1), "CENTRE"),
									("GRID", (0,0), (-1,-1),0.25, colors.black),
									("FONTSIZE", (0,0), (-1,-1), 8),
									("SPAN", (0,0), (0,len(each.sensordata_set.all())))
									])
				Story.append(temptable)
				doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

				response.write(buffer.getvalue())
				buffer.close() 

				return response
		else:
			return redirect('/')
	else:
		return redirect('/')


def exportSysArchitectureCSV(response, id): 
	management, supervisor = False, False
	#receiving the Process of ID
	#process_ID = response.session.get('id')
	#Assign Process objects and corresponding sub-process, sensor and machine sets
	project = Project.objects.get(id=id)
	processes = project.process_set.all()
	Manual = project.manual

	ProcessName, SubProcessName, SensorName = "", "", ""

	if response.user.groups.filter(name='Management').exists():
		management = True
	if response.user.groups.filter(name='Supervisor').exists():
		supervisor = True


	if response.user.is_authenticated:
		if project in response.user.profile.user_company.project_set.all():
			if management or supervisor:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment;filename=SystemArchitecture.csv'
				writer = csv.writer(response)

				#Writing the Main process and correlating attributes to CSV
				writer.writerow(['Project Name: ', project.project_name])
				writer.writerow([''])
				writer.writerow(['Process steps', 'Machines', 'Status', 'Sensors', 'Status'])
				for pro in processes:
					machines, machineStatus, sensors, sensorStatus = [], [], [] ,[]
					if Manual:
						ProcessName = pro.manualName
					else:
						ProcessName = pro.name

					#writing all machine data to CSV, providing it is not = to None
					try:
						machines.append(pro.plyCutter.name+ "\n")
						machineStatus.append(str(pro.plyCutter.status)+ "\n")
					except:
						pass

					try:
						machines.append(pro.sortPickAndPlace.name+ "\n")
						machineStatus.append(str(pro.sortPickAndPlace.status)+ "\n")
					except:
						pass

					try:
						machines.append(pro.blanksPickAndPlace.name+ "\n")
						machineStatus.append(str(pro.blanksPickAndPlace.status)+ "\n")
					except:
						pass

					try:
						machines.append(pro.preformCell.name+ "\n")
						machineStatus.append(str(pro.preformCell.status)+ "\n")
					except:
						pass

					for sensor in pro.sensor_set.all():
						sensors.append(sensor.name+ "\n")
						sensorStatus.append(str(sensor.status)+ "\n")

					#allowing all machine and sensor statuses to be written within the same cells
					machines = (','.join(machines))
					machineStatus = (','.join(machineStatus))

					machines = machines.replace(',',"")
					machineStatus = machineStatus.replace(',',"")
					sensors = (','.join(sensors))
					sensorStatus = (','.join(sensorStatus))
					sensors = sensors.replace(',',"")
					sensorStatus = sensorStatus.replace(',',"")

					writer.writerow([ProcessName, machines, machineStatus, sensors, sensorStatus])

				#same process as before but for sub process machines and sensors
				for pro in processes:
					if Manual:
						ProcessName = pro.manualName
					else:
						ProcessName = pro.name
					for subpro in pro.order_subprocess():
						machines, machineStatus, sensors, sensorStatus = [], [], [] ,[]
						if Manual:
							subProcessName = subpro.manualName
						else:
							subProcessName = subpro.name

						try:
							machines.append(subpro.plyCutter.name+ "\n")
							machineStatus.append(str(subpro.plyCutter.status)+ "\n")
						except:
							pass

						try:
							machines.append(subpro.sortPickAndPlace.name+ "\n")
							machineStatus.append(str(subpro.sortPickAndPlace.status) + "\n")
						except:
							pass

						try:
							machines.append(subpro.blanksPickAndPlace.name+ "\n")
							machineStatus.append(str(subpro.blanksPickAndPlace.status)+ "\n")
						except:
							pass

						try:
							machines.append(subpro.preformCell.name+ "\n")
							machineStatus.append(str(subpro.preformCell.status)+ "\n")
						except:
							pass

						for sensor in subpro.sensor_set.all():
							sensors.append(sensor.name+ "\n")
							sensorStatus.append(str(sensor.status)+ "\n")


						machines = (','.join(machines))
						machineStatus = (','.join(machineStatus))

						machines = machines.replace(',',"")
						machineStatus = machineStatus.replace(',',"")
						sensors = (','.join(sensors))
						sensorStatus = (','.join(sensorStatus))
						sensors = sensors.replace(',',"")
						sensorStatus = sensorStatus.replace(',',"")

						writer.writerow([ProcessName + "-" +subProcessName, machines, machineStatus, sensors, sensorStatus])

		return response
	else:
		return redirect('/')

def exportSysArchitecturePDF(response, id):
	management, supervisor, manualProject, AirborneIMG = False, False, False, None
	#assigning Main Process objects and corresponding Sub-processes, sensors and machines
	#process_ID = response.session.get('id')
	project = Project.objects.get(id=id)
	processes = project.process_set.all()


	today = date.today()
	timestamp = today.strftime("%d/%m/%Y")
	buffer=io.BytesIO()
	#Airborne image grabbed from their website
	AirborneImg = "static/Main/logo.png"
	#AirborneIMG = Image.open(path)
	
	ProcessName, subProName, sensorName = "", "", ""

	if project.manual == True:
		manualProject = True
	subData = [['Main/Sub-Process', 'Machines', 'Status', 'Sensors', 'Status']]
	data = [['Process', 'Machines', 'Status']]
	proSensorData = [['Process', 'Sensor', 'Status']]
	if response.user.groups.filter(name='Management').exists():
		management = True
	if response.user.groups.filter(name='Supervisor').exists():
		supervisor = True

	if response.user.is_authenticated:
		if project in response.user.profile.user_company.project_set.all():
			if management or supervisor:
				PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
				Title = "SystemArchitecture Data"
				pageinfo = "Airborne LTD."

				def myFirstPage(canvas, doc):
					canvas.saveState()
					canvas.setFont('Times-Bold',16)
					canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
					canvas.setFont('Times-Roman',9)
					canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
					canvas.restoreState()
				def myLaterPages(canvas, doc):
					canvas.saveState()
					canvas.setFont('Times-Roman',9)
					canvas.drawString(inch,0.75 * inch, "Page %d / %s" % (doc.page, pageinfo)) 
					canvas.restoreState()

				buffer=io.BytesIO()
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename = "SystemArchitectureData.pdf"'

				styles = getSampleStyleSheet()
				AirborneIMG = "static/Main/logo.png"

				doc = SimpleDocTemplate(buffer)
				Story = [Image(AirborneIMG, width=200, height=100)]
				style = styles["Normal"]

				for pro in processes:
				
					if manualProject:
						ProcessName = pro.manualName
					else:
						ProcessName = pro.name
	
					#paragraphs used for spacing and aesthetic purposes
					for machine in pro.machine.all():
						data.append([ProcessName,machine.name, machine.status])		

				table = Table(data)
				table.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
					("ALIGN", (0,0), (-1,-1), "CENTRE"),
					("GRID", (0,0), (-1,-1),0.25, colors.black),
					])

				Story.append(table)
				Story.append(Spacer(1,0.2*inch))

				for pro in processes:
					length = 0
					for sensor in pro.sensor_set.all():
						length+=1
						proSensorData.append([pro.name,sensor.name, sensor.status])
										
				table = Table(proSensorData)
				table.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
					("ALIGN", (0,0), (-1,-1), "CENTRE"),
					("GRID", (0,0), (-1,-1),0.25, colors.black),
					("SPAN", (0,1), (0, length))
					])

				Story.append(table)
				Story.append(Spacer(1,0.2*inch))

				for pro in processes:
					for subpro in pro.order_subprocess():
						#if too many sensors and machines are written within the table, then create a new page and tabl
						if manualProject:
							ProcessName = pro.manualName
							subProcessName = subpro.manualName
						else:
							ProcessName = pro.name
							subProcessName = subpro.name

						machineData = []
						machineStatus = []
						sensorData = []
						sensorStatus = []

						for machine in subpro.process.machine.all():
							machineData.append(Paragraph(machine.name + "<br/>",style = style))
							machineStatus.append(Paragraph(str(machine.status) + "<br/>",style = style))	

						for sensor in subpro.sensor_set.all():
							sensorData.append(Paragraph(sensor.name + "<br/>",style = style))
							sensorStatus.append(Paragraph(str(sensor.status) + "<br/>",style = style))

		

						subData.append([Paragraph(ProcessName + "-" + subProcessName, style=style), machineData, machineStatus, sensorData, sensorStatus])
	
				table = Table(subData,colWidths=[1.4*inch])
				table.setStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
				("ALIGN", (0,0), (-1,-1), "CENTRE"),
				("GRID", (0,0), (-1,-1),0.25, colors.black)
				])
				Story.append(table)
				doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

				response.write(buffer.getvalue())
				buffer.close() 
				return response
	else:
		return redirect('/')

def exportPartPDF(response, id):
	management, supervisor, manualProject = False, False, False
	#part_ID = response.session.get('id')
	#assigning Main Process objects and corresponding Sub-processes, sensors and machines
	
	part = Part.objects.get(part_id=id)
	Processes = part.processpart_set.all()


	if response.user.groups.filter(name='Management').exists():
		management = True
	if response.user.groups.filter(name='Supervisor').exists():
		supervisor = True

	if response.user.is_authenticated:
		if part.project in response.user.profile.user_company.project_set.all():

			PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
			Title = "Part Data"
			pageinfo = "Airborne LTD."

			def myFirstPage(canvas, doc):
				canvas.saveState()
				canvas.setFont('Times-Bold',16)
				canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
				canvas.setFont('Times-Roman',9)
				canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
				canvas.restoreState()
			def myLaterPages(canvas, doc):
				canvas.saveState()
				canvas.setFont('Times-Roman',9)
				canvas.drawString(inch,0.75 * inch, "Page %d / %s" % (doc.page, pageinfo)) 
				canvas.restoreState()

			if management:
				#assigning preliminary PDF attributes
				#PDF Creation
				
				buffer=io.BytesIO()
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename = "Management-PartData.pdf"'

				styles = getSampleStyleSheet()
				AirborneIMG = "static/Main/logo.png"

				doc = SimpleDocTemplate(buffer)
				Story = [Image(AirborneIMG, width=200, height=100)]
				style = styles["Normal"]

				#Table Data
				data = [['Part ID','Price Per KG', 'Price Per Metre Squared', 'Material Density', 'Technician Rate', 'Supervisor Rate', 'Power Rate'],
				[part.part_id,part.priceKG, part.priceM2, part.materialDensity, part.techRate, part.superRate, part.powerRate]]
				table = Table(data)
				table.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
						("ALIGN", (0,0), (-1,-1), "CENTRE"),
						("GRID", (0,0), (-1,-1),0.25, colors.black),
						("FONTSIZE", (0,0), (-1,1), 6.5),
						])
				
				Story.append(table)
				Story.append(Spacer(1,0.2*inch))

				data = [['Nominal Weight', 'Nominal Length', 'Nominal Width', 'Nominal Thickness', 'Weight Tolerance', 'Length Tolerance', 'Width Tolerance', 'Thickness Tolerance', 'Set Up Cost'],
				[part.nominalPartWeight, part.nominalPartLength, part.nominalPartWidth, part.nominalPartThickness, part.weightTolerance, part.lengthTolerance, part.widthTolerance, part.depthTolerance, part.setUpCost]]
				table = Table(data)
				table.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
						("ALIGN", (0,0), (-1,-1), "CENTRE"),
						("GRID", (0,0), (-1,-1),0.25, colors.black),
						("FONTSIZE", (0,0), (-1,1), 6.5),
						])
				
				Story.append(table)
				Story.append(Spacer(1,0.2*inch))

				text = "Process Data: "
				p = Paragraph(text, style)
				Story.append(p)

				Story.append(Spacer(1,0.2*inch))

				for process in Processes:
					data = [['Process Name', 'Cycle time', 'Process Time', 'Interface Time', 'Scrap Rate', 'Power Rate', 'CO2 Consumption', 'Cost of Material Waste', 'Cost of Scrap', 'Cost of Part', 'Technician Labour Cost', 'Supervisor Labour Cost', 'Power Consumption Cost', 'Total Cost'],
					[process.processName, process.cycleTime, process.processTime, process.interfaceTime, process.scrapRate, process.powerRate, process.CO2, process.materialWastageCost, process.materialScrapCost, process.materialPartCost, process.technicianLabourCost, process.supervisorLabourCost, process.powerCost, process.totalCost]]
					table = Table(data)
					table.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
						("ALIGN", (0,0), (-1,-1), "CENTRE"),
						("GRID", (0,0), (-1,-1),0.25, colors.black),
						("FONTSIZE", (0,0), (-1,1), 4),
						])
					Story.append(table)

					data = [['Sub Process', 'Cycle Time', 'Process Time', 'Scrap Rate', 'Material Waste Cost', 'Cost of Scrap', 'Cost of Part', 'Technician Cost', 'Supervisor Cost', 'Power Consumption Cost', 'CO2 Consumption']]
					Story.append(Spacer(1,0.2*inch))
					for subprocess in process.order_subprocesspart():
						#for every Sub-process, draw a table with these attri
						data.append([subprocess.subProcessName, subprocess.proIntTime, subprocess.processTime, subprocess.scrapRate, subprocess.materialWastageCost, subprocess.materialScrapCost, subprocess.materialPartCost, subprocess.technicianLabourCost, subprocess.supervisorLabourCost, subprocess.powerCost, subprocess.CO2])

					table = Table(data)
					table.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
					("ALIGN", (0,0), (-1,-1), "CENTRE"),
					("GRID", (0,0), (-1,-1),0.25, colors.black),
					("FONTSIZE", (0,0), (-1,-1), 5.2),
					])
					Story.append(table)

				doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

				response.write(buffer.getvalue())
				buffer.close() 

				return response
			elif supervisor:
				#preliminary PDF assignments
				buffer=io.BytesIO()
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename = "Supervisor-PartData.pdf"'

				styles = getSampleStyleSheet()
				AirborneIMG = "static/Main/logo.png"

				doc = SimpleDocTemplate(buffer)
				Story = [Image(AirborneIMG, width=200, height=100)]
				style = styles["Normal"]

				#Table Data
				data = [['Part ID','Price Per KG', 'Price Per Metre Squared', 'Material Density', 'Technician Rate', 'Supervisor Rate', 'Power Rate'],
				[part.part_id, part.priceKG, part.priceM2, part.materialDensity, part.techRate, part.superRate, part.powerRate]]
				table = Table(data)
				table.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
						("ALIGN", (0,0), (-1,-1), "CENTRE"),
						("GRID", (0,0), (-1,-1),0.25, colors.black),
						("FONTSIZE", (0,0), (-1,1), 6.5),
						])
				
				Story.append(table)
				Story.append(Spacer(1,0.2*inch))

				data = [['Nominal Weight', 'Nominal Length', 'Nominal Width', 'Nominal Thickness', 'Weight Tolerance', 'Length Tolerance', 'Width Tolerance', 'Thickness Tolerance', 'Set Up Cost'],
				[part.nominalPartWeight, part.nominalPartLength, part.nominalPartWidth, part.nominalPartThickness, part.weightTolerance, part.lengthTolerance, part.widthTolerance, part.depthTolerance, part.setUpCost]]
				table = Table(data)
				table.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
						("ALIGN", (0,0), (-1,-1), "CENTRE"),
						("GRID", (0,0), (-1,-1),0.25, colors.black),
						("FONTSIZE", (0,0), (-1,1), 6.5),
						])
				
				Story.append(table)
				Story.append(Spacer(1,0.2*inch))

				for process in Processes:
					#same process as bove but for all sub processes 
					data = [['Process','Sub Process','Date', 'Process Pass?', 'Quality Pass?','Time if passed?', 'Time Criteria', 'Centre error at tension frame', 'Centre error at male tool', 'Vertical position error of end effector' ,'Geometry Quality?', 'Weight Quality?', 'Wrinkle Quality?', 'Width Error', 'Length Error', 'Depth error', 'Weight error', 'NO. wrinkle(s)']]
					for subprocess in process.order_subprocesspart():

						if subprocess.subProcessName == "Material Pressed":
							data.append(
									[process.processName, subprocess.subProcessName,date.today(), 'False', 'True', '21', '23'])

						elif subprocess.subProcessName=="Material and Tool Inside Press":
							data.append(
								[process.processName, subprocess.subProcessName,date.today(), 'False', 'True', '','','1.0%', '0.5%'])

						elif subprocess.subProcessName=="Removal End effector actuated":
							data.append(
								[process.processName, subprocess.subProcessName,date.today(), 'False', 'True', '','','','','1.2%'])
				
						elif subprocess.subProcessName=="Final Inspection":
							data.append(
								[process.processName, subprocess.subProcessName,date.today(), 'False', 'True','','','','','', 'False', 'True', 'False', '1.2%', '1.0%', '2.0%', '1.5%', '5'])
		
						else:
							#default case
							data.append(
									[process.processName, subprocess.subProcessName,date.today(), 'False', 'True'])
			
					temptable = Table(data)
					temptable.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
						("ALIGN", (0,0), (-1,-1), "CENTRE"),
						("GRID", (0,0), (-1,-1),0.25, colors.black),
						("FONTSIZE", (0,0), (-1,-1), 2.4),
						("SPAN", (0,1), (0,len(process.subprocesspart_set.all()))),
						])
					Story.append(temptable)
					Story.append(Spacer(1,0.2*inch))

				
				#writeData determines if a new page with a new table is created when too many instances are found within the table
				data= [['Process Name','Sensor Name', 'Position X', 'Position Y', 'Position Z', 'Thickness Error']]

				for process in Processes:
					for sensor in process.sensordata_set.all():
						data.append([process.processName, sensor.sensorName, '72', '0.05', '7', '2%'])	

					temptable = Table(data)
					temptable.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
										("ALIGN", (0,0), (-1,-1), "CENTRE"),
										("GRID", (0,0), (-1,-1),0.25, colors.black),
										("FONTSIZE", (0,0), (-1,-1), 8),
										("SPAN", (0,1), (0,len(process.sensordata_set.all()))),
										])
					Story.append(temptable)
				Story.append(Spacer(1,0.2*inch))

				#sub process sensors
				
				data = [['Process', 'Sub Process','Sensor Name', 'Position X', 'Position Y', 'Position Z', 'Thickness Error']]
				overallLength = 0 
				length =0 
				for process in Processes:
					overallLength = length
					length = 0
					for subpro in process.order_subprocesspart():
						for each in subpro.sensordata_set.all():
							#for every sub-process sensor set, draw this table with corresponding value	
							data.append([process.processName,subpro.subProcessName, each.sensorName, '72', '0.05', '7', '2%'])
							length +=1

				temptable = Table(data)
				temptable.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
									("ALIGN", (0,0), (-1,-1), "CENTRE"),
									("GRID", (0,0), (-1,-1),0.25, colors.black),
									("FONTSIZE", (0,0), (-1,-1), 8),
									])
				Story.append(temptable)

				doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

				response.write(buffer.getvalue())
				buffer.close() 
				return response
		else:
			return redirect('/')
	else:
		return redirect('/')


def exportPartCSV(response, id):
	management, supervisor = False, False
	#receiving the Process of ID
	#part_id = response.session.get('id')

	#Assign Process objects and corresponding sub-process, sensor and machine sets
	part = Part.objects.get(part_id=id)
	Processes = part.processpart_set.all()

	if response.user.groups.filter(name='Management').exists():
		management = True
	if response.user.groups.filter(name='Supervisor').exists():
		supervisor = True
	#if user is in company
	if response.user.profile != None:
		if part.project in response.user.profile.user_company.project_set.all():
			#if user is in the Manager Group
			if management:			
				#Preliminary CSV assignments
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment;filename=Management-PartData.csv'
				writer = csv.writer(response)

				writer.writerow(['Project Part Values: '])
				writer.writerow(['Part ID','Price Per KG', 'Price Per Metre Squared', 'Material Density', 'Technician Rate', 'Supervisor Rate', 'Power Rate', 'Nominal Weight', 'Nominal Length', 'Nominal Width', 'Nominal Thickness', 'Weight Tolerance', 'Length Tolerance', 'Width Tolerance', 'Thickness Tolerance', 'Set Up Cost'])
				writer.writerow([part.part_id, part.priceKG, part.priceM2, part.materialDensity, part.techRate, part.superRate, part.project.powerRate, part.nominalPartWeight, part.nominalPartLength, part.nominalPartWidth, part.nominalPartThickness, part.weightTolerance, part.lengthTolerance, part.widthTolerance, part.depthTolerance, part.setUpCost])

				writer.writerow([''])
				for process in Processes:
					writer.writerow(['Process: '])
					writer.writerow(['Process Name', 'Cycle time', 'Process Time', 'Interface Time', 'Scrap Rate', 'Power Rate', 'Cost of Material Waste', 'Cost of Scrap', 'Cost of Part', 'Technician Labour Cost', 'Supervisor Labour Cost', 'Power Consumption Cost', 'Total Cost', 'CO2 Consumption'])
					writer.writerow([process.processName, process.cycleTime, process.processTime, process.interfaceTime, process.scrapRate, process.part.project.powerRate, process.materialWastageCost, process.materialScrapCost, process.materialPartCost, process.technicianLabourCost, process.supervisorLabourCost, process.powerCost, process.totalCost, process.CO2])

					writer.writerow([' '])
					writer.writerow(['Sub-Processes: '])
					writer.writerow(['Sub Process Name',  'Interface Time', 'Scrap Rate', 'Power Rate', 'Cost of Material Waste', 'Cost of Scrap', 'Cost of Part', 'Technician Labour Cost', 'Supervisor Labour Cost', 'Power Consumption Cost', 'Total Cost', 'CO2 Consumption'])
					for subprocess in process.order_subprocesspart():
						writer.writerow([subprocess.subProcessName, subprocess.proIntTime, subprocess.scrapRate, subprocess.processPart.part.project.powerRate, subprocess.materialWastageCost, subprocess.materialScrapCost, process.materialPartCost, subprocess.technicianLabourCost, subprocess.supervisorLabourCost, subprocess.powerCost, subprocess.totalCost, subprocess.CO2])

			elif supervisor:
				#Preliminary CSV assignments
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment;filename=Supervisor-PartData.csv'
				writer = csv.writer(response)

				writer.writerow(['Project Part Values: '])
				writer.writerow(['Part ID','Price Per KG', 'Price Per Metre Squared', 'Material Density', 'Technician Rate', 'Supervisor Rate', 'Power Rate', 'Nominal Weight', 'Nominal Length', 'Nominal Width', 'Nominal Thickness', 'Weight Tolerance', 'Length Tolerance', 'Width Tolerance', 'Thickness Tolerance', 'Set Up Cost'])
				writer.writerow([part.part_id, part.priceKG, part.priceM2, part.materialDensity, part.techRate, part.superRate, part.project.powerRate, part.nominalPartWeight, part.nominalPartLength, part.nominalPartWidth, part.nominalPartThickness, part.weightTolerance, part.lengthTolerance, part.widthTolerance, part.depthTolerance, part.setUpCost])
				writer.writerow([''])

				for process in Processes:

					writer.writerow(['Process: ', process.processName])
					#for every sub-process, write these attributes
					for each in process.order_subprocesspart():
						if each.subProcessName == "Material and Tool Inside Press":
							writer.writerow(['Sub-Process Name', 'Date', 'Process Pass?', 'Quality Pass?', 'Centre position error at tension frame', 'Centre position error at male tool'])
							writer.writerow([each.subProcessName, date.today(), each.processCheck, each.qualityCheck, '1.0%', '2.3%'])
						elif each.subProcessName == "Material Pressed":
							writer.writerow(['Sub-Process Name', 'Date', 'Process Pass?', 'Quality Pass?', 'Time if Passed', 'Time criteria when passed'])
							writer.writerow([each.subProcessName, date.today(), each.processCheck, each.qualityCheck, '23', '21'])
						elif each.subProcessName == "Removal End effector actuated":
							writer.writerow(['Sub-Process Name', 'Date', 'Process Pass?', 'Quality Pass?', 'Vertical position error of end effector'])
							writer.writerow([each.subProcessName, date.today(), each.processCheck, each.qualityCheck, '1.0%'])
						elif each.subProcessName== "Final Inspection":
							writer.writerow(['Sub-Process Name', 'Date', 'Process Pass?', 'Quality Pass?', 'Geometry Quality Pass?', 'Weight Quality Pass?', 'Wrinkle/Bridging Quality Pass?', 'Width Error', 'Length Error', 'Depth Error', 'Weight error', 'Number of wrinkle(s)/bridging'])
							writer.writerow([each.subProcessName, date.today(), each.processCheck, each.qualityCheck, True, False, True, '1.0%', '2.0%', '1.5%', '2%', '5'])
						else:
							writer.writerow(['Sub-Process Name', 'Date', 'Process Pass?', 'Quality Pass?'])
							writer.writerow([each.subProcessName, date.today(), each.processCheck, each.qualityCheck])
						writer.writerow([' '])

					writer.writerow([process.processName + ' Sensors: '])
					for sensor in process.sensordata_set.all():
						writer.writerow(['Sensor Name', 'Position X', 'Position Y', 'Position Z', 'Thickness Error'])
						writer.writerow([sensor.sensorName, '72', '0.05', '7', '2%'])
					writer.writerow([''])

					for subprocess in process.order_subprocesspart():
						writer.writerow([''])
						writer.writerow(['Sub Process Name: '+ subprocess.subProcessName])

						for sensor in subprocess.sensordata_set.all():
							writer.writerow(['Sensor Name', 'Position X', 'Position Y', 'Position Z', 'Thickness Error'])
							writer.writerow([sensor.sensorName, '72', '0.05', '7', '2%'])

			else:
				return redirect('/') 
			#return CSV file
			return response
		else:
			return redirect('/')	
	else:
		return redirect('/')

def exportDashboard(response, pID, id, type):
	project = Project.objects.get(id=id)
	management, supervisor = False, False
	totalCost, totalParts, mID, partCost, OEE = 0,0,0,0,0
	interfaceTime, processTime, totalLabourHours, totalProcessTime, totalCycle=  timedelta(),timedelta(),timedelta(),timedelta(), timedelta()
	scrapList = []
	costData=[0,0,0]
	metricChoice = 'CYT'
	error = " "
	secsPerDay = 24 * 60 * 60
	if response.user.groups.filter(name='Management').exists():
		management = True
	if response.user.groups.filter(name='Supervisor').exists():
		supervisor = True

	if response.user.is_authenticated:
		if project in response.user.profile.user_company.project_set.all():
			#data gathering#
			for part in project.part_set.all():
				totalParts +=1
				totalCycle += part.cycleTime 
				totalLabourHours += ((int(part.labourInput)/100) * part.cycleTime)
				totalCost += part.totalCost
				interfaceTime += part.interfaceTime
				processTime += part.processTime
				costData[0] += float(part.materialSumCost)
				costData[1] += float(part.labourCost)
				costData[2] += float(part.powerCost)


			totalLabourCost = format((totalLabourHours.total_seconds()/secsPerDay) * (24*float(project.superRate)), '.2f')
			sumData = sum(costData) #total cost
			materialCost = (costData[0]/sumData) * 100 # material cost as a percentage
			labourCost = (costData[1]/sumData) * 100 #labour cost as a percentage
			powerCost = (costData[2]/sumData) * 100 # power cost as a percentage

			#--OEE CALCULATION--#
			try:
				totalCycleOEE, OEEprocessTime  = timedelta(), timedelta()
				averageCycle, goodPartCounter, badPartCounter,= 0,0,0
				temp = project.OEEendDate - project.OEEstartDate
				avgList = []
				project.totalShiftTime = temp.total_seconds() / 60
				project.save()

				for part in project.part_set.all().filter(date__range=[project.OEEstartDate, project.OEEendDate], submitted=True):
					avgList.append(part.cycleTime.total_seconds()/60)
					OEEprocessTime += part.processTime
					totalCycleOEE += part.cycleTime
					if part.badPart == False:
						goodPartCounter +=1
					else:
						badPartCounter+=1

				asum = sum(avgList)

				averageCycle = asum/len(avgList)

				loadingTime = float(project.totalShiftTime) - float(project.plannedDownTime)
				operatingTime = totalCycleOEE.total_seconds() / 60
				availability = float(operatingTime) / float(loadingTime)
				performance = float(project.theoreticalCycleTime) / (operatingTime / len(project.part_set.all().filter(submitted=True)))
				quality = float(goodPartCounter) / len(project.part_set.all().filter(submitted=True))
				OEE = (float(availability) * float(performance) * float(quality))

				print("availability: " + str(availability) + "\nPerformance: " + str(performance) + "\nQuality: "+ str(quality))

				availability = availability*100
				quality = quality*100
				performance = performance * 100
				OEE = OEE * 100
			except:
				OEE = 0
				availability = 0
				quality = 0
				performance = 0
			OEE = "{:.2f}".format(OEE)

			if type == "CSV":
				
				#CSV#
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment;filename=DashboardData.csv'
				writer = csv.writer(response)

				writer.writerow(['Project', 'Number of Parts', 'Total Cycle Time', 'Total Labour Hours', 'Total Labour Costs', 'Total Cost', 'Interface Time', 'Process Time', 'OEE', 'Material Cost', 'Labour Cost', 'Power Cost'])
				writer.writerow([project.project_name, totalParts, totalCycle, totalLabourHours, totalLabourCost, totalCost, interfaceTime, processTime, OEE, materialCost, labourCost, powerCost])

				

				for part in project.part_set.all():
					writer.writerow('')
					writer.writerow(['Part: ', str(part), str(part.date)])
					for process in part.processpart_set.all():
						writer.writerow(['Process: ', str(process.processName)])
						writer.writerow('')
						writer.writerow(['Sub Process', 'Cycle Time', 'Process Time', 'Interface Time', 'Technician Labour', 'Supervisor Labour', 'Power Consumption'])
						for subpro in process.subprocesspart_set.all():
							writer.writerow([subpro.subProcessName, subpro.cycleTime, subpro.processTime, subpro.interfaceTime, subpro.technicianLabour, subpro.supervisorLabour, subpro.power])



				return response
			elif type == "PDF":

				#PDF Creation
				PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
				Title = "Dashboard Data"
				pageinfo = "Airborne LTD."
				buffer=io.BytesIO()
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename = "DashboardData.pdf"'
				
				def myFirstPage(canvas, doc):
					canvas.saveState()
					canvas.setFont('Times-Bold',16)
					canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
					canvas.setFont('Times-Roman',9)
					canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
					canvas.restoreState()
				def myLaterPages(canvas, doc):
					canvas.saveState()
					canvas.setFont('Times-Roman',9)
					canvas.drawString(inch,0.75 * inch, "Page %d / %s" % (doc.page, pageinfo)) 
					canvas.restoreState()

				styles = getSampleStyleSheet()
				AirborneIMG = "static/Main/logo.png"
				doc = SimpleDocTemplate(buffer)
				Story = [Image(AirborneIMG, width=200, height=100)]
				style = styles["Normal"]

				#Standard Information
				data = [['Project Name', 'Number of Parts','Total Cycle Time', 'Total Labour Hours', 'Total Labour Costs', 'Process Time', 'Interface Time', 'Total Cost', 'OEE'],
				[project.project_name, totalParts, totalCycle, totalLabourHours, totalLabourCost, processTime,interfaceTime, totalCost, OEE]]
				
				table = Table(data)
				table.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
						("ALIGN", (0,0), (-1,-1), "CENTRE"),
						("GRID", (0,0), (-1,-1),0.25, colors.black),
						("FONTSIZE", (0,0), (-1,1), 7.5),
						])
				Story.append(table)

				for part in project.part_set.all():
					Story.append(Spacer(1,0.2*inch))
					partID = "Part ID: " + str(part.part_id) + " - " + str(part.date)
					p = Paragraph(partID, style)
					Story.append(p)
					for process in part.processpart_set.all():
						Story.append(Spacer(1,0.2*inch))
						data = [['Process', 'Sub Process', 'Cycle Time', 'Process Time', 'Interface Time', 'Technician Labour', 'Supervisor Labour', 'Power Consumption']]
						for subpro in process.subprocesspart_set.all():
							data.append([process.processName, subpro.subProcessName, subpro.cycleTime, subpro.processTime, subpro.interfaceTime, subpro.technicianLabour, subpro.supervisorLabour, subpro.power])
						table = Table(data)
						table.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
							("ALIGN", (0,0), (-1,-1), "CENTRE"),
							("GRID", (0,0), (-1,-1),0.25, colors.black),
							("FONTSIZE", (0,0), (-1,-1), 6.5),
							("SPAN", (0,1), (0,len(process.subprocesspart_set.all()))),
							])
						Story.append(table)
								
					
				doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

				response.write(buffer.getvalue())
				buffer.close() 
				return response


		else:
			return redirect('/')
	else:
		return redirect('/')



