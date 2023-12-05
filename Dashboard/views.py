from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from json import dumps
from datetime import datetime,date,time,timedelta
from Main.models import *
from MainData.models import *
from .forms import *
from .models import *
import math
from itertools import chain

from decimal import Decimal


def project_dash(response):
	'''View to allow section of the project for which the dashboard should be shown'''
	#setup
	if response.user.is_authenticated:
		management = False
		supervisor = False

		if response.user.groups.filter(name='Management').exists():
			management = True

		try:
			if management:
				return render(response, 'Dashboard/selectProjectDash.html')
			else:
				return redirect('/')
		except AttributeError:
			return redirect('/')
	else:
		return redirect('/mylogout/')



def dashboard(response, id):
	'''view to calculate basic metrics and return the main dashboard page '''
	#setup
	if response.user.is_authenticated:
		company, project, manualProject = response.user.profile.user_company, Project.objects.get(id=id), Project.objects.filter(manual=True).first()
		management, supervisor = False, False
		totalBlanks, totalBlankCost, totalBlankCycle, totalPlies, totalPlyCost,totalCost, totalParts, mID, partCost, OEE = 0,0,0,0,0,0,0,0,0,0
		interfaceTime, processTime, totalLabourHours, totalProcessTime, totalCycle, totalPlyCycle, totalBlankCycle, startDate, endDate, OEEstartDate, OEEendDate, plyInterfaceTime, plyProcessTime, blankProcessTime, blankInterfaceTime=  timedelta(), timedelta(),timedelta(),timedelta(),timedelta(), timedelta(), timedelta(), timedelta(), timedelta(), timedelta(), timedelta(), timedelta(), timedelta(), timedelta(), timedelta()
		scrapList = []
		metricChoice = 'CYT'
		error = " "

		form = MetricForm()
		assumedform = AssumedCostForm()
		manualprojectform = ManualProjectComparisonForm(response.user)
		learningrateform = LearningRateForm()
		timeform = TimesForm()
		oee_form = OEEForm()
		oee_time_form =  OEETimesForm()

		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True

		if project in response.user.profile.user_company.project_set.all():
			if management or supervisor:
				if project.startDate != None and project.endDate != None:
					startDate = project.startDate
					endDate = project.endDate
				else:
					startDate = date.today() - timedelta(days=7)
					endDate = date.today()

				if project.OEEstartDate != None and project.OEEendDate != None:
					OEEstartDate = project.OEEstartDate
					OEEendDate = project.OEEendDate
				else:
					project.OEEstartDate = date.today() - timedelta(days=7)
					project.OEEendDate = date.today()
					OEEstartDate = project.OEEstartDate
					OEEendDate = project.OEEendDate
					project.save()


				if response.method == 'POST':
					if response.POST.get('selectMetric'):
						#if user changes metric for sub chart
						form = MetricForm(response.POST)
						if form.is_valid():
							#new metric choice = user choice
							metricChoice = form.cleaned_data['choice']
					if response.POST.get('AssumedC'):
						#If user changes assumed cost in cost model chart
						assumedform = AssumedCostForm(response.POST)
						if assumedform.is_valid():
							project.assumedCost = assumedform.cleaned_data['value']
							#if the assumed cost is higher than the length of the current part set
							if project.assumedCost > len(project.part_set.all()):
								messages.error(response, "You have less parts than the assumed cost!")
							else:
								messages.success(response, "Success!")
							project.save()

					if response.POST.get('manualProjectChoice'):
						#if user chooses a manual project to compare an automated project with on cost model chart
						manualprojectform = ManualProjectComparisonForm(response.user, response.POST)
						if manualprojectform.is_valid():
							manualProject = manualprojectform.cleaned_data['choice']
							manualProject.assumedCost = manualprojectform.cleaned_data['value']
							mID = manualProject.id #save manual ID and pass it into render response so it can be used in template
							manualProject.save()

					if response.POST.get("learningRate"):
						learningrateform = LearningRateForm(response.POST)

						if learningrateform.is_valid():
							manualProject.learningRate = learningrateform.cleaned_data['value']
							manualProject.save()

					if response.POST.get("selectTime"):
						timeform = TimesForm(response.POST)
						if timeform.is_valid():
							project.startDate = timeform.cleaned_data['start_date_field']
							project.endDate = timeform.cleaned_data['end_date_field']
							project.save()

					if response.POST.get("selectOEEtime"):

						oee_time_form = OEETimesForm(response.POST)
						n = response.POST['start_date']
						e = response.POST['end_date']

						project.OEEstartDate =datetime.strptime(n, "%Y-%m-%d").date()
						project.OEEendDate = datetime.strptime(e, "%Y-%m-%d").date()

						project.save()

						if timeform.is_valid():
							project.OEEstartDate = timeform.cleaned_data['start_date']
							project.OEEendDate = timeform.cleaned_data['end_date']
							project.save()

					if response.POST.get("OEE"):
						oee_form = OEEForm(response.POST)

						if oee_form.is_valid():
							inputValue = oee_form.cleaned_data['value']
							reqDirty = oee_form.cleaned_data['choice']
							reqClean = oee_choices_dict[reqDirty]
							setattr(project, reqClean, inputValue)
							project.save()

				for part in project.part_set.all():
					totalParts +=1
					totalCycle += part.cycleTimePerPart
					#find percent of labour input
					totalLabourHours += part.superLabourHours + part.techLabourHours
					totalCost += part.totalCost
					interfaceTime += part.interfaceTimePerPart
					processTime += part.processTimePerPart
					scrapList.append(part.partScrapRate)

				for blank in project.blank_set.all():
					if blank.part is None:
						totalBlanks +=1
						totalCycle += blank.cycleTimePerBlank
						#find percent of labour input
						totalCost += blank.totalCost
						totalLabourHours += blank.superLabourHours + blank.techLabourHours
						interfaceTime += blank.interfaceTimePerBlank
						processTime += blank.processTimePerBlank
						scrapList.append(blank.blankScrapRate)

				for ply in project.ply_set.all():
					if ply.blank is None:
						totalPlies +=1
						totalCycle += ply.cycleTimePerPly
						#find percent of labour input
						totalCost += ply.totalCost
						totalLabourHours += ply.superLabourHours + ply.techLabourHours
						interfaceTime += ply.interfaceTimePerPly
						processTime += ply.processTimePerPly
						scrapList.append(ply.plyScrapRate)

				#find average scrap
				if len(scrapList) != 0:
					scrapRate = format(sum(scrapList)/len(scrapList),'.2f')
				else:
					scrapRate = 0
				#used for conversion of datetime.deltatime into int
				secsPerDay = 24*60*60
				#formatting from datetime.deltatime to int. int represents number of days
				totalLabourCost = format((totalLabourHours.total_seconds()/secsPerDay) * (24*float(project.superRate)), '.2f')
				interfaceTimeFrac = format((interfaceTime.total_seconds()/secsPerDay), '.2f')
				processTimeFrac = format(processTime.total_seconds()/secsPerDay, '.2f')
				totalLabourTimeFrac = format(totalLabourHours.total_seconds()/secsPerDay, '.2f')

				#--OEE CALCULATION--#
				try:
					totalCycleOEE, OEEprocessTime  = timedelta(), timedelta()
					averageCycle, goodPartCounter, badPartCounter,= 0,0,0
					temp = project.OEEendDate - project.OEEstartDate
					avgList = []
					project.totalShiftTime = temp.total_seconds() / 60
					project.save()

					for part in project.part_set.all().filter(date__range=[OEEstartDate, OEEendDate], submitted=True):
						avgList.append(part.cycleTimePerPart.total_seconds()/60)
						OEEprocessTime += part.processTimePerPart
						totalCycleOEE += part.cycleTimePerPart
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

				#return response page and relevant vars
				return render(response, 'Dashboard/dashboard.html', { 'availability':availability, 'performance':performance, 'quality':quality, 'oee_time_form':oee_time_form,  'oee_form':oee_form,   'timeform':timeform ,   'OEE':OEE,  'learningrateform':learningrateform,'error':error, 'mID':mID, 'manualProject':manualProject, 'manualprojectform': manualprojectform,
																						'totalParts' : totalParts, 'totalCycle' : totalCycle,
																						'totalLabourHours' : totalLabourHours, 'totalLabourCost' : totalLabourCost,
																						'project':project, 'interfaceTime':interfaceTime, 'processTime':processTime,
																						'scrapRate': scrapRate, 'interfaceTimeFrac':interfaceTimeFrac,
																						'processTimeFrac':processTimeFrac, 'totalLabourTimeFrac':totalLabourTimeFrac,
																						'project':project, 'form':form, 'metricChoice':metricChoice, 'assumedform':assumedform, 'totalCost':totalCost})
		return redirect('/')
	else:
		return redirect('/')


def part_graph(response):
	'''View to control project part graph'''
	#setup
	company = response.user.profile.user_company
	data, labels=[],[]
	totalProjectParts = 0

	if response.user.groups.filter(name='Management').exists():
		management = True
	elif response.user.groups.filter(name='Supervisor').exists():
		supervisor = True
	if response.user.is_authenticated:

		#loop through all projects to find how many parts have been made in each
		for project in company.project_set.all():
			for part in project.part_set.all():
				totalProjectParts +=1
			#add name of project
			labels.append(project.project_name)
			#add num of parts
			data.append(totalProjectParts)
			#reset num of parts
			totalProjectParts = 0

		#return json file with data and labels for chart
		return JsonResponse(data={'labels':labels,'data':data})
	else:
		return redirect('mylogout/')

def blank_graph(response):
	#setup
	company = response.user.profile.user_company
	data, labels=[],[]
	totalProjectBlanks = 0

	if response.user.groups.filter(name='Management').exists():
		management = True
	elif response.user.groups.filter(name='Supervisor').exists():
		supervisor = True
	if response.user.is_authenticated:

		#loop through all projects to find how many parts have been made in each
		for project in company.project_set.all():
			for blank in project.blank_set.all():
				totalProjectBlanks +=1
			#add name of project
			labels.append(project.project_name)
			#add num of parts
			data.append(totalProjectBlanks)
			#reset num of parts
			totalProjectBlanks = 0

		#return json file with data and labels for chart
		return JsonResponse(data={'labels':labels,'data':data})
	else:
		return redirect('mylogout/')

def ply_graph(response):
	#setup
	company = response.user.profile.user_company
	data, labels=[],[]
	totalProjectPlies = 0

	if response.user.groups.filter(name='Management').exists():
		management = True
	elif response.user.groups.filter(name='Supervisor').exists():
		supervisor = True
	if response.user.is_authenticated:

		#loop through all projects to find how many parts have been made in each
		for project in company.project_set.all():
			for ply in project.ply_set.all():
				totalProjectPlies +=1
			#add name of project
			labels.append(project.project_name)
			#add num of parts
			data.append(totalProjectPlies)
			#reset num of parts
			totalProjectPlies = 0
			print(data)

		#return json file with data and labels for chart
		return JsonResponse(data={'labels':labels,'data':data})
	else:
		return redirect('mylogout/')


def pie_chart(response, id):
	#setup
	if response.user.is_authenticated:
		project = Project.objects.get(id=id)
		timedata=[timedelta(0).total_seconds(), timedelta(0).total_seconds()]
		data = []
		'''View to provide info for the pie chart'''
		for part in project.part_set.all():
			#set process time and interface time to timedata indices

			timedata[0] += part.processTimePerPart.total_seconds()
			timedata[1] += part.interfaceTimePerPart.total_seconds()

		for blank in project.blank_set.all():
			if blank.part is None:
				timedata[0] += blank.processTimePerBlank.total_seconds()
				timedata[1] += blank.interfaceTimePerBlank.total_seconds()

		for ply in project.ply_set.all():
			if ply.blank is None:
				timedata[0] += ply.processTimePerPly.total_seconds()
				timedata[1] += ply.interfaceTimePerPly.total_seconds()

		#sum of both is cycle time
		sumData = sum(timedata)

		try:
			processTime = (timedata[0]/sumData) * 100 # process time as a percentage
		except ZeroDivisionError:
			processTime = 10
		try:
			interfaceTime = (timedata[1]/sumData) * 100 # interface time as a percentage
		except ZeroDivisionError:
			interfaceTime = 10

		data.append("{:.2f}".format(processTime)) #display with 2 decimal places
		data.append("{:.2f}".format(interfaceTime))
		labels = ['Process Time', 'Interface Time']

		return JsonResponse(data={'labels':labels,'data':data})
	else:
		return redirect('/')


def pie_cost_chart(response,id):
	if response.user.is_authenticated:
		project = Project.objects.get(id=id)
		costData=[0,0,0]
		data = []
		'''View to provide info for the pie chart'''
		for part in project.part_set.all():
			#for all cost data in part set
			costData[0] += float(part.materialCostPerPart)
			costData[1] += float(part.technicianLabourCostPerPart + part.supervisorLabourCostPerPart)
			costData[2] += float(part.powerConsumptionCostPerPart)

		for blank in project.blank_set.all():
			if blank.part is None:
				#for all cost data in part set
				costData[0] += float(blank.materialCostPerBlank)
				costData[1] += float(blank.technicianLabourCostPerBlank + blank.supervisorLabourCostPerBlank)
				costData[2] += float(blank.powerConsumptionCostPerBlank)

		for ply in project.ply_set.all():
			if ply.blank is None:
				#for all cost data in part set
				costData[0] += float(ply.materialCostPerPly)
				costData[1] += float(ply.technicianLabourCostPerPly + supervisorLabourCostPerPly)
				costData[2] += float(ply.powerConsumptionCostPerPly)

		print(costData)


		sumData = sum(costData) #total cost
		try:
			materialCost = (costData[0]/sumData) * 100 # material cost as a percentage
		except ZeroDivisionError:
			materialCost = 10
		try:
			labourCost = (costData[1]/sumData) * 100 #labour cost as a percentage
		except ZeroDivisionError:
			labourCost = 10

		try:
			powerCost = (costData[2]/sumData) * 100 # power cost as a percentage
		except ZeroDivisionError:
			powerCost = 10

		data.append("{:.2f}".format(materialCost)) #display costs to 2 decimal places (as a percentage)
		data.append("{:.2f}".format(labourCost))
		data.append("{:.2f}".format(powerCost))
		labels = ['Material Cost', 'Labour Cost', 'Power Cost']

		return JsonResponse(data={'labels':labels,'data':data})
	else:
		return redirect('/')

def sub_chart(response, id, choice):
	'''View to provide info for the sub process cycle graph'''
	#setup
	project = Project.objects.get(id=id)
	management = False
	supervisor = False
	if response.user.groups.filter(name='Management').exists():
		management = True
	elif response.user.groups.filter(name='Supervisor').exists():
		supervisor = True

	if response.user.is_authenticated:
		if project in response.user.profile.user_company.project_set.all():
			if management or supervisor:
				#setup
				data, avg, labels, avgList, iterations, totalProjectParts, count, secsPerDay=[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ,0,0,24*60*60
				productSet = list(chain(project.part_set.all(), project.blank_set.all(), project.ply_set.all()))
				metric = metric_dict[choice]
				subSet = SubProcessPart.objects.none()
				print(metric)

				for product in productSet:
					for processPart in product.processpart_set.all():
						for subProPart in processPart.order_subprocesspart_custom():
							if not subSet.filter(subProcessName=subProPart.subProcessName).exists():
								subSet |= SubProcessPart.objects.filter(id=subProPart.id)

				startDate = project.startDate
				endDate = project.endDate
				print(subSet)
				for subProPart in subSet.filter(date__range=[startDate, endDate]):
						print(subProPart)
						if subProPart.subProcessName in labels: #if subprocesspart has been iterated over in a previous part
							index = labels.index(subProPart.subProcessName) #get label index
							iterations[index]=iterations[index]  + 1  #increase iterations by 1. This will be used for the average calculation later
						else:
							#add sub process name to chart labels
							labels.append(subProPart.subProcessName)
							index = labels.index(subProPart.subProcessName)
							iterations[index]=iterations[index]  + 1  #increase iteration by 1

						attr = getattr(subProPart, metric) #metric is the choice chosen by the user for sub chart viewing

						if choice in ['CYT','PRT','INT', 'TLR', 'SLR']:  #if choice is Cycletime, Process Time, Interface Time, Technician labour hours or Supervisor labour hours
							temp = attr.total_seconds()

							if choice == 'PRT': #if choice is process time
								if not subProPart.processCheck:
									temp = 0

							elif choice == 'INT': #if choice is interface time
								if subProPart.processCheck:
									temp = 0
						else:
							temp = attr
						if attr is not None:
							avgList[index] = avgList[index] + temp #index for iterations and avgList are the same (for continuity)

				for each in avgList:
					if iterations[count] != 0: #if iterations is above one (check has been passed above)
						avg.append(each/iterations[count]) #average = every subprocesspart attribute / the number of times they appear in parts
						count=count+1

				data = avg #return data in json response for graphs

				#return json file with data and labels for chart
				return JsonResponse(data={'labels':labels,'data':data})
	else:
		return redirect('/mylogout/')


def cost_model_chart(response, id, error, mID):

	if response.user.is_authenticated:
		#setup
		project = Project.objects.get(id=id)
		manualComparison, management, supervisor= False, False, False
		manualLabel = "Select a Manual Project to see me!"
		label = ""


		if mID != 0: #if user has chosen a manual project
			manualProject = Project.objects.get(id=mID)
			manualComparison = True #manual line will be drawn below
		else:
			if len(Project.objects.filter(manual=True))>0:
				manualComparison = True
				manualProject = Project.objects.filter(manual=True).first()
			else:
				manualComparison = False
				manualProject=  None
		if response.user.groups.filter(name='Management').exists():
			management = True
		elif response.user.groups.filter(name='Supervisor').exists():
			supervisor = True

		#setup vars
		if len(project.part_set.all()) == 0:
			cont = False
		else:
			cont = True

		data, labels, manualData = [], [], []

		dataCheck, cont = False, False
		labourinput, totalPower, totalCycleTime, learningRate, partNumber, i, value, secsPerDay = 0, 0, 0, 0.88, 0, 1, 0, 24 * 60 * 60
		label = project.project_name
		try:
			formPreform = project.process_set.get(name='Form Preform')
			cont = True
		except:
			cont = False


		setUpCost = project.setUpCost
		superRate = project.superRate
		techRate = project.techRate
		assumedCostPart = project.assumedCost

		if cont:

			##check base number of parts met
			if len(project.part_set.all()) >= assumedCostPart: #if length of project part set is above or equal to assumed cost (attribute defined in project model)
				#part Set = all parts within project that have been fully submitted (bad part and final inspection has been submitted)
				partSet = project.part_set.all().filter(submitted=True).order_by('-part_id')[:assumedCostPart]
				lastPart = partSet[:1]

				for item in lastPart:
					part = item

				#get total cost of part
				totalCost = float(part.totalCost)

				#calc cost of first 100 parts
				while i < 100:
					#calc initial cost including start up
					if i == 1:
						totalInitialCost = totalCost + float(project.setUpCost)
						value = totalInitialCost
						#add to data to be sent in response
						data.append(totalInitialCost)
					#calc the cost of the rest of the parts
					else:
						 value = value + totalCost
						 data.append(value)
					#add part number to labels
					labels.append(i)
					i+=1

			if manualComparison == True: #if manual project has been selected
				#setup vars
				manualData = []
				manualLabel = manualProject.project_name
				formPreform = manualProject.process_set.get(manualName='Form Preform')
				setUpCost = manualProject.setUpCost
				superRate = manualProject.superRate
				techRate = manualProject.techRate
				assumedCostPartManual = manualProject.assumedCost

				labourinput, totalPower, totalCycleTime, partNumber, i, value, secsPerDay = 0,0,0,0,1,0,24*60*60

				if len(manualProject.part_set.all()) >= assumedCostPartManual:

					partSet = manualProject.part_set.all().filter(submitted=True).order_by('-part_id')[:assumedCostPartManual]
					lastPart = partSet[:1]

					for item in lastPart:
						part = item

					superCost = (part.superLabourHours.total_seconds()/secsPerDay) * (24*float(superRate)) # supervisor labour cost
					techCost = (part.techLabourHours.total_seconds()/secsPerDay) * (24*float(techRate)) #technician labour cost
					labourCost = superCost + techCost #(float(superRate)*part.superLabourHours) + (float(techRate) * part.techLabourHours)
					initialLabourCost = labourCost/pow(assumedCostPartManual, math.log(learningRate, 2)) #manual cost is calculated differently
					materialCost = float(part.materialSumCost)

					while i < 100:
						if i == 1:
							totalInitialCost = initialLabourCost + materialCost#cumulative addition
							manualData.append(totalInitialCost)
						elif i == 2:
							value = totalInitialCost + initialLabourCost*(pow(i, math.log(learningRate,2))) + materialCost
							manualData.append(value)
						else:
							 value = value + initialLabourCost*(pow(i, math.log(learningRate, 2))) + materialCost
							 manualData.append(value)
						i+=1





		return JsonResponse(data={ 'data':data, 'manualData':manualData , 'manualLabel': manualLabel, 'label':label,'error': error, 'labels':labels, 'dataCheck':dataCheck, 'setUpCost':setUpCost})
	else:
		return redirect('/mylogout/')
