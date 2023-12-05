from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, date, timedelta
from Main.models import * 
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import *

class Part(models.Model):
	averageList = ['labourInput', 'scrapRate']
	"""Model to store info about each complete part"""
	#standard info
	part_id = models.AutoField(primary_key=True)	
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	date = models.DateField(null=True)
	partInstance = models.ForeignKey(PartInstance, on_delete=models.SET_NULL, null = True)
	
	#VSM values
	submitted = models.BooleanField(default = False)
	operator = models.CharField(max_length=50, null=True)
	labourInput = models.DecimalField(max_digits=5, decimal_places=2, default=0.500)
	jobStart = models.DateTimeField(null=True)
	jobEnd = models.DateTimeField(null=True)

	#project values
	priceKG = models.IntegerField(default=0)
	priceM2 = models.IntegerField(default=0) 
	CO2PerPower = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	materialDensity = models.IntegerField(default=0)
	techRate = models.IntegerField(default=0)
	superRate = models.IntegerField(default=0)
	powerRate = models.IntegerField(default=0)
	setUpCost = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)

	badPart = models.BooleanField(default=False)

	superLabourHours = models.DurationField(null=True,default=timedelta())
	techLabourHours = models.DurationField(null=True,default=timedelta())

	#Data remapping
	powerUsage = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	labourTotal = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	partAreaRatio = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	partPerimeter = models.DecimalField(max_digits=10, decimal_places=3, default=1)
	totalSurfaceArea = models.DecimalField(max_digits=10, decimal_places=3, default=1)
	totalSumOfPerimeters = models.DecimalField(max_digits=10, decimal_places=3, default=1)
	partPerimeterRatio = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	partSurfaceArea = models.DecimalField(max_digits=10, decimal_places=3, default=1)
	totalOffcutArea = models.DecimalField(max_digits=10, decimal_places=3, default=1)

	processTimePerPart = models.DurationField(null=True, default=timedelta())
	interfaceTimePerPart = models.DurationField(null=True, default=timedelta())
	cycleTimePerPart = models.DurationField(null=True, default=timedelta())

	
	#----#
	materialWastagePerPart = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialWastageCostPerPart = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialScrapPerPart = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialScrapCostPerPart = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	partScrapRate = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialCostPerPart = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	materialRateArea = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialRateWeight = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialDensity = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	powerConsumptionCostPerPart = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	CO2EmissionsPerPart = models.DecimalField(max_digits=50, decimal_places=3, default=0)


	#--Labour--#
	technicianLabourCostPerPart = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	supervisorLabourCostPerPart = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
		
	#--Totals--#
	labourCost = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)
	labourTotal = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)
	totalCost = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)

	def initialiseValues(self):
		self.labourTotal = self.labourInput #leaving at a default of 50 as this is currently undefined. Should be (LabourHours/FullTimeHours)*CycleTimePerPart in the future
		self.partAreaRatio = self.partSurfaceArea / self.totalSurfaceArea
		self.partPerimeterRatio = self.partPerimeter / self.totalSumOfPerimeters
		self.materialWastagePerPart = (self.totalOffcutArea/self.totalSurfaceArea)*self.partAreaRatio*100
		self.materialWastageCostPerPart = (self.materialRateArea * self.totalOffcutArea * self.partAreaRatio) + (self.materialRateWeight * self.totalOffcutArea * self.materialDensity * self.partAreaRatio)
		self.materialScrapCostPerPart = (self.partScrapRate * self.materialRateArea * self.partSurfaceArea) + (self.partScrapRate * self.materialRateWeight * self.partSurfaceArea * self.materialDensity)
		self.materialCostPerPart = (self.materialRateArea * self.partSurfaceArea * self.partAreaRatio) + (self.materialRateWeight * self.partSurfaceArea * self.materialDensity * self.partAreaRatio)
		self.technicianLabourCostPerPart = self.techRate * self.labourTotal * self.partAreaRatio
		self.supervisorLabourCostPerPart = self.superRate * self.labourTotal * self.partAreaRatio

		self.powerConsumptionCostPerPart = self.powerRate * self.powerUsage * self.partAreaRatio
		self.CO2EmissionsPerPart = self.project.CO2PerPower * self.powerUsage * self.partAreaRatio

		self.totalCost = self.powerConsumptionCostPerPart + self.technicianLabourCostPerPart + self.supervisorLabourCostPerPart + self.materialCostPerPart 

		self.save()

	def updateLabour(self):

		#for every process part in part process part set
		for processPart in self.processpart_set.all():			
			#cumulatively add all process costs to total part costs
			
			if processPart.supervisorLabour is not None:
				self.superLabourHours += processPart.supervisorLabour 
			if processPart.technicianLabour is not None:
				self.techLabourHours += processPart.technicianLabour 
			
		self.save()

	#--methods--#
	def updateIntervals(self):
		"""Function to update a process's cycle,interface and process times"""
		#setup
		totalInterface = timedelta()
		totalProcess = timedelta()
		totalCycle = timedelta()
		#cycle sub process's to find total interface and process times
		for process in self.processpart_set.all():
			totalProcess += process.processTime * float(self.partPerimeterRatio)
			totalInterface += process.interfaceTime * float(self.partPerimeterRatio)
        
		#calc total cycle
		totalCycle = totalInterface + totalProcess  
        
		#assign to model and save
		self.interfaceTimePerPart = totalInterface
		self.processTimePerPart = totalProcess
		self.cycleTimePerPart = totalCycle
		self.save()

	def updateProcessStartEnd(self):
		"""Function to update a process's start and end times"""
		#setup  
		endList = []
		startList = []

		for process in self.processpart_set.all():
			if process.jobStart is not None:
				startList.append(process.jobStart)
				if process.jobEnd is not None:
					endList.append(process.jobEnd)
        
		#find min time in start list and assign 
		if len(startList) != 0:     
			self.jobStart = min(startList)
		#find max time in end list and assign
		if len(endList) != 0:   
			self.jobEnd = max(endList)
		#save
		self.save()


	def updateWholePart(self):
		
		self.updateIntervals()
		self.updateProcessStartEnd()
		self.updateLabour()	
		self.initialiseValues()

	def consolidate_process_parts(self, processName):
		consolidatedProcessPart = ProcessPart.objects.create(processName=processName, part=self, date = date.today(), jobStart = datetime.now().replace(microsecond=0))
		dct = {}
		for blank in self.blank_set.all():
			if blank.processpart_set.filter(processName=processName).exists():
				processPart = blank.processpart_set.get(processName=processName)
				for attr in processPart._meta.fields:
					if hasattr(consolidatedProcessPart,attr.name):
						blankValue = getattr(processPart, attr.name)
						consolValue = getattr(consolidatedProcessPart, attr.name)
						if (isinstance(blankValue, int) or isinstance(blankValue, timedelta) or isinstance(blankValue, Decimal)) and attr.name != 'blank_id' and attr.name != 'id' and consolValue != None:
							if attr.name in self.averageList:
								dct[f"lst_{blank.blank_id}_{attr.name}"] = blankValue
							else:
								setattr(consolidatedProcessPart, attr.name, blankValue+consolValue)
				jobS = self.blank_set.first().processpart_set.get(processName=processName).jobStart
				jobE = self.blank_set.last().processpart_set.get(processName=processName).jobEnd
				consolidatedProcessPart.jobEnd = jobE 
				consolidatedProcessPart.jobStart = jobS
		for attr in self.averageList:
			tempList = []
			tempIndex = 0
			for key in dct:
				if attr in key:
					tempList.append(dct[key])
					tempIndex += 1
			if tempIndex == 0:
				setattr(consolidatedProcessPart, attr, 0)
			else:
				setattr(consolidatedProcessPart, attr, sum(tempList)/tempIndex)
		consolidatedProcessPart.save()
		return consolidatedProcessPart

	def consolidate_sub_process_parts(self, subProcessName, processName):
		blankProcessPart = ProcessPart.objects.get(processName=processName, part = self)
		consolidatedSubProcessPart = SubProcessPart.objects.create(subProcessName=subProcessName, processPart = blankProcessPart, part=self, date = date.today())
		dct = {}
		
		for blank in self.blank_set.all():
			processPart = blank.processpart_set.get(processName=processName)
			if processPart.subprocesspart_set.filter(subProcessName=subProcessName).exists():
				subProcessPart = processPart.subprocesspart_set.get(subProcessName=subProcessName)
				for attr in subProcessPart._meta.fields:
					if hasattr(consolidatedSubProcessPart,attr.name):
						subValue = getattr(subProcessPart, attr.name)
						consolValue = getattr(consolidatedSubProcessPart, attr.name)
						if (type(subValue) == int or isinstance(subValue, timedelta) or isinstance(subValue, Decimal)) and attr.name != 'ply_id' and attr.name != 'id' and consolValue != None:
							if attr.name in self.averageList:
								dct[f"lst_{blank.blank_id}_{attr.name}"] = subValue
							else:
								setattr(consolidatedSubProcessPart, attr.name, subValue+consolValue)
				jobS = self.blank_set.first().processpart_set.get(processName=processName).subprocesspart_set.filter(subProcessName=subProcessName).first().jobStart
				jobE = self.blank_set.last().processpart_set.get(processName=processName).subprocesspart_set.filter(subProcessName=subProcessName).last().jobEnd
				consolidatedSubProcessPart.jobEnd = jobE 
				consolidatedSubProcessPart.jobStart = jobS
		for attr in self.averageList:
			tempList = []
			tempIndex = 0
			for key in dct:
				if attr in key:
					tempList.append(dct[key])
					tempIndex += 1
			if tempIndex == 0:
				setattr(consolidatedSubProcessPart, attr, 0)
			else:
				setattr(consolidatedSubProcessPart, attr, sum(tempList)/tempIndex)
		consolidatedSubProcessPart.save()
		return consolidatedSubProcessPart

	def updatePrimaryValues(self, project):
		for attr in project._meta.fields: #loop through project attributes and assign to part
			if "Cost" in attr.name or attr.name == "part" or attr.name == "date" or attr.name == "plyCutter" or attr.name == "sortPickAndPlace" or attr.name == "blanksPickAndPlace" or attr.name == "preformCell" or attr.name == "id":
				pass
			else:
				value = getattr(project, attr.name)
				setattr(self, attr.name, value)
        
class Blank(models.Model):
	averageList = ['labourInput', 'scrapRate']
	"""Model to hold information about a blanks history in the process"""
	#standard info
	part = models.ForeignKey(Part, on_delete=models.CASCADE, null=True)
	blankInstance = models.ForeignKey(BlankInstance, on_delete=models.SET_NULL, null=True)
	blank_id = models.BigAutoField(primary_key=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	date = models.DateField(null=True)
	
	#VSM values
	submitted = models.BooleanField(default = False)
	operator = models.CharField(max_length=50, null=True)
	labourInput = models.DecimalField(max_digits=5, decimal_places=2, default=0.500)
	jobStart = models.DateTimeField(null=True)
	jobEnd = models.DateTimeField(null=True)

	#project values
	priceKG = models.IntegerField(default=0)
	priceM2 = models.IntegerField(default=0) 
	CO2PerPower = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	materialDensity = models.IntegerField(default=0)
	techRate = models.IntegerField(default=0)
	superRate = models.IntegerField(default=0)
	powerRate = models.IntegerField(default=0)
	setUpCost = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)

	badPart = models.BooleanField(default=False)

	superLabourHours = models.DurationField(null=True,default=timedelta())
	techLabourHours = models.DurationField(null=True,default=timedelta())

	#Data remapping
	powerUsage = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	labourTotal = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	blankAreaRatio = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	blankPerimeter = models.DecimalField(max_digits=10, decimal_places=3, default=0.5)
	totalSurfaceArea = models.DecimalField(max_digits=10, decimal_places=3, default=1)
	totalSumOfPerimeters = models.DecimalField(max_digits=10, decimal_places=3, default=1)
	blankPerimeterRatio = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	blankSurfaceArea = models.DecimalField(max_digits=10, decimal_places=3, default=0.5)
	totalOffcutArea = models.DecimalField(max_digits=10, decimal_places=3, default=1)

	processTimePerBlank = models.DurationField(null=True, default=timedelta())
	interfaceTimePerBlank = models.DurationField(null=True, default=timedelta())
	cycleTimePerBlank = models.DurationField(null=True, default=timedelta())

	
	#----#
	materialWastagePerBlank = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialWastageCostPerBlank = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialScrapPerBlank = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialScrapCostPerBlank = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	blankScrapRate = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialCostPerBlank = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	materialRateArea = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialRateWeight = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialDensity = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	powerConsumptionCostPerBlank = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	CO2EmissionsPerBlank = models.DecimalField(max_digits=50, decimal_places=3, default=0)


	#--Labour--#
	technicianLabourCostPerBlank = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	supervisorLabourCostPerBlank = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
		
	#--Totals--#
	labourCost = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)
	labourTotal = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)
	totalCost = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)

	def initialiseValues(self):
		self.labourTotal = self.labourInput #leaving at a default of 50 as this is currently undefined. Should be (LabourHours/FullTimeHours)*CycleTimePerBlank in the future
		self.blankAreaRatio = self.blankSurfaceArea / self.totalSurfaceArea
		self.blankPerimeterRatio = self.blankPerimeter / self.totalSumOfPerimeters
		self.materialWastagePerBlank = (self.totalOffcutArea/self.totalSurfaceArea)*self.blankAreaRatio*100
		self.materialWastageCostPerBlank = (self.materialRateArea * self.totalOffcutArea * self.blankAreaRatio) + (self.materialRateWeight * self.totalOffcutArea * self.materialDensity * self.blankAreaRatio)
		self.materialScrapCostPerBlank = (self.blankScrapRate * self.materialRateArea * self.blankSurfaceArea) + (self.blankScrapRate * self.materialRateWeight * self.blankSurfaceArea * self.materialDensity)
		self.materialCostPerBlank = (self.materialRateArea * self.blankSurfaceArea * self.blankAreaRatio) + (self.materialRateWeight * self.blankSurfaceArea * self.materialDensity * self.blankAreaRatio)
		self.technicianLabourCostPerBlank = self.techRate * self.labourTotal * self.blankAreaRatio
		self.supervisorLabourCostPerBlank = self.superRate * self.labourTotal * self.blankAreaRatio

		self.powerConsumptionCostPerBlank = self.powerRate * self.powerUsage * self.blankAreaRatio
		self.CO2EmissionsPerBlank = self.project.CO2PerPower * self.powerUsage * self.blankAreaRatio

		self.totalCost = self.powerConsumptionCostPerBlank + self.technicianLabourCostPerBlank + self.supervisorLabourCostPerBlank + self.materialCostPerBlank 

		self.save()

	def updateLabour(self):

		#for every process part in part process part set
		for processPart in self.processpart_set.all():			
			#cumulatively add all process costs to total part costs
			
			if processPart.supervisorLabour is not None:
				self.superLabourHours += processPart.supervisorLabour 
			if processPart.technicianLabour is not None:
				self.techLabourHours += processPart.technicianLabour 
			
		self.save()

	#--methods--#
	def updateIntervals(self):
		"""Function to update a process's cycle,interface and process times"""
		#setup
		totalInterface = timedelta()
		totalProcess = timedelta()
		totalCycle = timedelta()
		#cycle sub process's to find total interface and process times
		for process in self.processpart_set.all():
			totalProcess += process.processTime * float(self.blankPerimeterRatio)
			totalInterface += process.interfaceTime * float(self.blankPerimeterRatio)
        
		#calc total cycle
		totalCycle = totalInterface + totalProcess  
        
		#assign to model and save
		self.interfaceTimePerBlank = totalInterface
		self.processTimePerBlank = totalProcess
		self.cycleTimePerBlank = totalCycle
		self.save()

	def updateProcessStartEnd(self):
		"""Function to update a process's start and end times"""
		#setup  
		endList = []
		startList = []

		for process in self.processpart_set.all():
			if process.jobStart is not None:
				startList.append(process.jobStart)
				if process.jobEnd is not None:
					endList.append(process.jobEnd)
        
		#find min time in start list and assign 
		if len(startList) != 0:     
			self.jobStart = min(startList)
		#find max time in end list and assign
		if len(endList) != 0:   
			self.jobEnd = max(endList)
		#save
		self.save()


	def updateWholePart(self):
		
		self.updateIntervals()
		self.updateProcessStartEnd()
		self.updateLabour()	
		self.initialiseValues()

	def consolidate_process_parts(self, processName):
		dct = {}
		consolidatedProcessPart = ProcessPart.objects.create(processName=processName, blank=self, date = date.today())
		for ply in self.ply_set.all():
			if ply.processpart_set.filter(processName=processName).exists():
				processPart = ply.processpart_set.get(processName=processName)
				for attr in processPart._meta.fields:
					if hasattr(consolidatedProcessPart,attr.name):
						plyValue = getattr(processPart, attr.name)
						consolValue = getattr(consolidatedProcessPart, attr.name)
						if (type(plyValue) == int or isinstance(plyValue, timedelta) or isinstance(plyValue, Decimal)) and attr.name != 'ply_id' and attr.name != 'id':
							if attr.name in self.averageList:
								dct[f"lst_{ply.ply_id}_{attr.name}"] = plyValue
							else:
								setattr(consolidatedProcessPart, attr.name, plyValue+consolValue)
				jobS = self.ply_set.first().processpart_set.get(processName=processName).jobStart
				jobE = self.ply_set.last().processpart_set.get(processName=processName).jobEnd
				consolidatedProcessPart.jobEnd = jobE 
				consolidatedProcessPart.jobStart = jobS
		for attr in self.averageList:
			tempList = []
			tempIndex = 0
			for key in dct:
				if attr in key:
					tempList.append(dct[key])
					tempIndex += 1
			if tempIndex == 0:
				setattr(consolidatedProcessPart, attr, 0)
			else:
				setattr(consolidatedProcessPart, attr, sum(tempList)/tempIndex)

		consolidatedProcessPart.save()
		return consolidatedProcessPart

	def consolidate_sub_process_parts(self, subProcessName, processName):
		blankProcessPart = ProcessPart.objects.get(processName=processName, blank = self)
		consolidatedSubProcessPart = SubProcessPart.objects.create(subProcessName=subProcessName, processPart = blankProcessPart, blank=self, date = date.today())
		dct = {}
		for ply in self.ply_set.all():
			processPart = ply.processpart_set.get(processName=processName)
			if processPart.subprocesspart_set.filter(subProcessName=subProcessName).exists():
				subProcessPart = processPart.subprocesspart_set.get(subProcessName=subProcessName)
				for attr in subProcessPart._meta.fields:
					if hasattr(consolidatedSubProcessPart,attr.name):
						subValue = getattr(subProcessPart, attr.name)
						consolValue = getattr(consolidatedSubProcessPart, attr.name)

						if (type(subValue) == int or isinstance(subValue, timedelta) or isinstance(subValue, Decimal)) and attr.name != 'ply_id' and attr.name != 'id' and consolValue != None:
							if attr.name in self.averageList:
								dct[f"lst_{ply.ply_id}_{attr.name}"] = subValue
							else:
								setattr(consolidatedSubProcessPart, attr.name, subValue+consolValue)
				jobS = self.ply_set.first().processpart_set.get(processName=processName).subprocesspart_set.filter(subProcessName=subProcessName).first().jobStart
				jobE = self.ply_set.last().processpart_set.get(processName=processName).subprocesspart_set.filter(subProcessName=subProcessName).last().jobEnd
				consolidatedSubProcessPart.jobEnd = jobE 
				consolidatedSubProcessPart.jobStart = jobS
		for attr in self.averageList:
			tempList = []
			tempIndex = 0
			for key in dct:
				if attr in key:
					tempList.append(dct[key])
					tempIndex += 1
			if tempIndex == 0:
				setattr(consolidatedSubProcessPart, attr, 0)
			else:
				setattr(consolidatedSubProcessPart, attr, sum(tempList)/tempIndex)
		consolidatedSubProcessPart.save()
		return consolidatedSubProcessPart

	def updatePrimaryValues(self, project):
		for attr in project._meta.fields: #loop through project attributes and assign to part
			if "Cost" in attr.name or attr.name == "part" or attr.name == "date" or attr.name == "plyCutter" or attr.name == "sortPickAndPlace" or attr.name == "blanksPickAndPlace" or attr.name == "preformCell" or attr.name == "id":
				pass
			else:
				value = getattr(project, attr.name)
				setattr(self, attr.name, value)

class Ply(models.Model):
	"""Model to hold inofrmation about a plys history in the process"""
	#standard info
	blank = models.ForeignKey(Blank, on_delete=models.CASCADE, null=True)
	plyInst = models.ForeignKey(PlyInstance, on_delete=models.SET_NULL, null=True)
	ply_id = models.IntegerField(primary_key=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	date = models.DateField(null=True)
	
	#VSM values
	submitted = models.BooleanField(default = False)
	operator = models.CharField(max_length=50, null=True)
	labourInput = models.DecimalField(max_digits=5, decimal_places=2, default=0.500)
	jobStart = models.DateTimeField(null=True)
	jobEnd = models.DateTimeField(null=True)

	#project values
	priceKG = models.IntegerField(default=0)
	priceM2 = models.IntegerField(default=0) 
	CO2PerPower = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	materialDensity = models.IntegerField(default=0)
	techRate = models.IntegerField(default=0)
	superRate = models.IntegerField(default=0)
	powerRate = models.IntegerField(default=0)
	setUpCost = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)

	badPart = models.BooleanField(default=False)

	superLabourHours = models.DurationField(null=True,default=timedelta())
	techLabourHours = models.DurationField(null=True,default=timedelta())

	#Data remapping
	powerUsage = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	labourTotal = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	plyAreaRatio = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	plyPerimeter = models.DecimalField(max_digits=10, decimal_places=3, default=0.33)
	totalSurfaceArea = models.DecimalField(max_digits=10, decimal_places=3, default=1)
	totalSumOfPerimeters = models.DecimalField(max_digits=10, decimal_places=3, default=1)
	plyPerimeterRatio = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	plySurfaceArea = models.DecimalField(max_digits=10, decimal_places=3, default=0.33)
	totalOffcutArea = models.DecimalField(max_digits=10, decimal_places=3, default=1)

	processTimePerPly = models.DurationField(null=True, default=timedelta())
	interfaceTimePerPly = models.DurationField(null=True, default=timedelta())
	cycleTimePerPly = models.DurationField(null=True, default=timedelta())

	
	#----#
	materialWastagePerPly = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialWastageCostPerPly = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialScrapPerPly = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialScrapCostPerPly = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	plyScrapRate = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialCostPerPly = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	materialRateArea = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialRateWeight = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialDensity = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	powerConsumptionCostPerPly = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	CO2EmissionsPerPly = models.DecimalField(max_digits=50, decimal_places=3, default=0)


	#--Labour--#
	technicianLabourCostPerPly = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	supervisorLabourCostPerPly = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
		
	#--Totals--#
	labourCost = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)
	labourTotal = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)
	totalCost = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)

	def initialiseValues(self):
		self.labourTotal = self.labourInput #leaving at a default of 50 as this is currently undefined. Should be (LabourHours/FullTimeHours)*CycleTimePerPly in the future
		self.plyAreaRatio = self.plySurfaceArea / self.totalSurfaceArea
		self.plyPerimeterRatio = self.plyPerimeter / self.totalSumOfPerimeters
		self.materialWastagePerPly = (self.totalOffcutArea/self.totalSurfaceArea)*self.plyAreaRatio*100
		self.materialWastageCostPerPly = (self.materialRateArea * self.totalOffcutArea * self.plyAreaRatio) + (self.materialRateWeight * self.totalOffcutArea * self.materialDensity * self.plyAreaRatio)
		self.materialScrapCostPerPly = (self.plyScrapRate * self.materialRateArea * self.plySurfaceArea) + (self.plyScrapRate * self.materialRateWeight * self.plySurfaceArea * self.materialDensity)
		self.materialCostPerPly = (self.materialRateArea * self.plySurfaceArea * self.plyAreaRatio) + (self.materialRateWeight * self.plySurfaceArea * self.materialDensity * self.plyAreaRatio)
		self.technicianLabourCostPerPly = self.techRate * self.labourTotal * self.plyAreaRatio
		self.supervisorLabourCostPerPly = self.superRate * self.labourTotal * self.plyAreaRatio

		self.powerConsumptionCostPerPly = self.powerRate * self.powerUsage * self.plyAreaRatio
		self.CO2EmissionsPerPly = self.project.CO2PerPower * self.powerUsage * self.plyAreaRatio

		self.totalCost = self.powerConsumptionCostPerPly + self.technicianLabourCostPerPly + self.supervisorLabourCostPerPly + self.materialCostPerPly 

		self.save()


	def updateLabourValues(self):
		
		#for every process part in part process part set
		for processPart in self.processpart_set.all():			
			if processPart.supervisorLabour is not None:
				self.superLabourHours += processPart.supervisorLabour 
			if processPart.technicianLabour is not None:
				self.techLabourHours += processPart.technicianLabour 
			
		self.save()

	#--methods--#
	def updateIntervals(self):
		"""Function to update a process's cycle,interface and process times"""
		#setup
		totalInterface = timedelta()
		totalProcess = timedelta()
		totalCycle = timedelta()
		#cycle sub process's to find total interface and process times
		for process in self.processpart_set.all():
			totalProcess += process.processTime * float(self.plyPerimeterRatio)
			totalInterface += process.interfaceTime * float(self.plyPerimeterRatio)
        
		#calc total cycle
		totalCycle = totalInterface + totalProcess  
        
		#assign to model and save
		self.interfaceTimePerPly = totalInterface
		self.processTimePerPly = totalProcess
		self.cycleTimePerPly = totalCycle
		self.save()

	def updateProcessStartEnd(self):
		"""Function to update a process's start and end times"""
		#setup  
		endList = []
		startList = []

		for process in self.processpart_set.all():
			if process.jobStart is not None:
				startList.append(process.jobStart)
				if process.jobEnd is not None:
					endList.append(process.jobEnd)
        
		#find min time in start list and assign 
		if len(startList) != 0:     
			self.jobStart = min(startList)
		#find max time in end list and assign
		if len(endList) != 0:   
			self.jobEnd = max(endList)
		#save
		self.save()


	def updateWholePart(self):
		
		self.updateIntervals()
		self.updateProcessStartEnd()
		self.updateLabourValues()
		self.initialiseValues()	

	def updatePrimaryValues(self, project):
		for attr in project._meta.fields: #loop through project attributes and assign to part
			if "Cost" in attr.name or attr.name == "part" or attr.name == "date" or attr.name == "plyCutter" or attr.name == "sortPickAndPlace" or attr.name == "blanksPickAndPlace" or attr.name == "preformCell" or attr.name == "id":
				pass
			else:
				value = getattr(project, attr.name)
				setattr(self, attr.name, value)



class ProcessPart(models.Model):
	"""Model to store info about each complete process"""
	#standard info
	part = models.ForeignKey(Part, on_delete=models.CASCADE, null=True)
	blank = models.ForeignKey(Blank, on_delete=models.CASCADE, null=True)
	ply = models.ForeignKey(Ply, on_delete=models.CASCADE, null=True)
	processName = models.CharField(max_length = 30, null = True)
	date = models.DateField(null=True)

	plyCutter = models.ForeignKey(Machine,  related_name='plyCutter', on_delete=models.CASCADE, null=True)
	sortPickAndPlace = models.ForeignKey(Machine, related_name='sortPickAndPlace',on_delete=models.CASCADE, null=True)
	blanksPickAndPlace = models.ForeignKey(Machine,related_name='blanksPickAndPlace', on_delete=models.CASCADE, null=True)
	preformCell = models.ForeignKey(Machine,related_name='preformCell', on_delete=models.CASCADE, null=True)
	#VSM values
	operator = models.CharField(max_length=50, null=True)
	labourInput = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
	jobStart = models.DateTimeField(null=True)
	jobEnd = models.DateTimeField(null=True)
	processStart = models.DateTimeField(null=True)
	processEnd = models.DateTimeField(null=True)
	processTime = models.DurationField(null=True, default=timedelta())
	cycleTime = models.DurationField(null=True, default=timedelta())
	interfaceTime = models.DurationField(null=True, default=timedelta())
	popUpStart = models.DateTimeField(null=True)
	popUpEnd = models.DateTimeField(null=True)
	scrapRate = models.DecimalField(max_digits=3, decimal_places=0, default = 0)
	minBatchSize = models.DecimalField(max_digits=50, decimal_places=0, default=50)
	maxBatchSize = models.DecimalField(max_digits=50, decimal_places=0, default=350)
	wastedTime = models.DurationField(null=True, default=timedelta())
	#non-time dependant data
	power = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)
	status = models.IntegerField(default=0)
	processCheck = models.BooleanField(default=False, null=True)	
	qualityCheck = models.BooleanField(default=False, null=True)
	cycleCostRatio = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	postTrimWeight = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	preTrimWeight = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	wastedTime = models.DurationField(null=True, default=timedelta())	

	CO2 = models.DecimalField(max_digits=50, decimal_places=3, default=0)

	#Cost Breakdown

	#--Material--#
	materialWastage = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialScrap = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialPart = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialWastageCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialScrapCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialPartCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialSumCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	#--Labour--#
	technicianLabour = models.DurationField(default=timedelta())
	supervisorLabour = models.DurationField(default=timedelta())
	technicianLabourCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	supervisorLabourCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	labourSumCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	#--Utility--#
	powerCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	powerRate = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	#--TotalCost--#
	totalCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	#--methods--#
	def __str__(self):
		return self.processName
		

	def updateIntervals(self):
		"""Function to update a process's cycle,interface and process times"""
		#setup
		totalInterface = timedelta()
		totalProcess = timedelta()
		totalCycle = timedelta()
		#cycle sub process's to find total interface and process times
		for process in self.subprocesspart_set.all():
			if process.processCheck:
				totalProcess += process.processTime
			else:
				totalInterface += process.interfaceTime
        
		#calc total cycle
		totalCycle = totalInterface + totalProcess  
        
		#assign to model and save
		self.interfaceTime = totalInterface
		self.processTime = totalProcess
		self.cycleTime = totalCycle
		self.save()

	def updateBatchSize(self):
		"""Function to update a process batch range"""
		#setup  
		batchList = []
        
		#get list of all batch sizes
		for process in self.subprocesspart_set.all():
			batchList.append(process.batchSize)
        
		#assign to model and save
		self.minBatchSize = min(batchList)
		self.maxBatchSize = max(batchList)
		self.save()

	def updateProcessStartEnd(self):
		"""Function to update a process's start and end times"""
		#setup  
		endList = []
		startList = []

		for process in self.subprocesspart_set.all():
			if process.jobStart is not None:
				startList.append(process.jobStart)
				if process.jobEnd is not None:
					endList.append(process.jobEnd)
        
		#find min time in start list and assign 
		if len(startList) != 0:     
			self.jobStart = min(startList)
		#find max time in end list and assign
		if len(endList) != 0:   
			self.jobEnd = max(endList)
		#save
		self.save()

	def updateScrapRate(self):
		"""Function to update a process scrap value"""
		#setup  
		scrapList = []
		#create list of all scrap rates
		for process in self.subprocesspart_set.all():
			scrapList.append(process.scrapRate)
        
		#find average scrap assign and save
		self.scrapRate = sum(scrapList)/len(scrapList)
		self.save()

	def updateLabourInput(self):
		"""Function to update a process labour input"""
		#setups
		labourList = []
		#create list of all labour inputs
		for process in self.subprocesspart_set.all():
			if process.labourInput is not None:
				labourList.append(process.labourInput)
        
		#calc average labour assign and save
		self.labourInput = sum(labourList)/len(labourList)
		self.save()

	def updatePowerCon(self):
		"""Function To update the power value of a given process by summing all related sub-process power values"""
		#setup
		powerList = []
		CO2List = []
		#get all power values
		for process in self.subprocesspart_set.all():
			if process.power is not None:
				powerList.append(process.power)
			if process.CO2 is not None:
				CO2List.append(process.CO2)
        
		#calc average and assign
		self.power = sum(powerList)
		self.CO2 = sum(CO2List)
		self.save()
        
		
	def updateProcessCosts(self):
		"""Function to update costs associated with process's"""
		#Initialisation
		totalTechLabour = timedelta()
		totalSuperLabour = timedelta()
		totalTechLabourCost = 0
		totalSuperLabourCost = 0
		totalLabourCost = 0
		totalPowerCost = 0
		totalProcessCost = 0
		totalWastageCost = 0
		totalScrapCost = 0
		totalPartCost = 0
		
		#for each subprocess in process subprocess set
		for subProcess in self.subprocesspart_set.all():
			#cumulatively adding all subprocess cost data
			totalTechLabour += subProcess.technicianLabour
			totalSuperLabour += subProcess.supervisorLabour
			totalTechLabourCost += subProcess.technicianLabourCost
			totalSuperLabourCost += subProcess.supervisorLabourCost
			totalLabourCost += subProcess.labourSumCost
			totalPowerCost += subProcess.powerCost
			totalWastageCost += subProcess.materialWastageCost
			totalScrapCost += subProcess.materialScrapCost
			totalPartCost += subProcess.materialPartCost
			
			if subProcess.processCheck:
				totalProcessCost += subProcess.totalCost
		
			#if final inspection exists run this
			if subProcess.weighPoint:

				SubProcessPartWeights.objects.create(subProPart=subProcess, weight= subProcess.preTrimWeight)

			if subProcess.finalWeighPoint:

				finalInspection = self.subprocesspart_set.get(subProcessName=subProcess.subProcessName)
				SubSet = self.order_subprocesspart_custom()
				for value in SubSet.order_by('-position'):
					if value.weighPoint:
						finalInspection.preTrimWeight = value.preTrimWeight
						break

				#if post trim weight and pre trim weight have been defined
				if (finalInspection.postTrimWeight is not None) and (finalInspection.preTrimWeight is not None):
					self.postTrimWeight = finalInspection.postTrimWeight
					self.preTrimWeight = finalInspection.preTrimWeight
					self.materialPart = finalInspection.materialPart
					self.materialWastage = finalInspection.materialWastage
					self.materialScrap = finalInspection.materialScrap
				
		#process costs defined here from subprocess costs
		self.technicianLabour = totalTechLabour
		self.supervisorLabour = totalSuperLabour
		self.technicianLabourCost = totalTechLabourCost
		self.supervisorLabourCost = totalSuperLabourCost
		self.labourSumCost = totalLabourCost
		self.powerCost = totalPowerCost
		self.processCost = totalProcessCost
		self.materialWastageCost = totalWastageCost
		self.materialPartCost = totalPartCost
		self.materialScrapCost = totalScrapCost
		self.materialSumCost = float(self.materialPartCost) + float(self.materialWastageCost) + float(self.materialScrapCost)
		self.totalCost = float(self.powerCost) + float(self.labourSumCost) + float(self.materialSumCost)

		if self.totalCost == 0 or self.cycleTime.total_seconds() == 0:
			self.cycleCostRatio = 0
		else:
			self.cycleCostRatio = float(self.totalCost)/float(self.cycleTime.total_seconds()/24*60*60)

		self.save()

	def updateProcessPartMachines(self, process):

		#self.plyCutter = process.plyCutter
		#self.sortPickAndPlace = process.sortPickAndPlace
		#self.blanksPickAndPlace = process.blanksPickAndPlace
		#self.preformCell = process.preformCell
		self.save()

	def calcWastedTime(self):
		"""Function to calulate the whole wasted time of a process"""
		wastedTime = timedelta()
		for subProcessPart in self.subprocesspart_set.all():
			wastedTime += subProcessPart.wastedTime
		self.wastedTime = wastedTime
		self.save()


	def updateWholeProcessPart(self):
		
		self.updateIntervals()
		self.updateBatchSize()
		self.updateProcessStartEnd()
		self.updateScrapRate()
		self.updateLabourInput()
		self.updatePowerCon()
		self.updateProcessCosts()	
		#self.calcWastedTime()

	def order_subprocesspart(self): #order all subprocesses in this sequential order
		subprocessPartSet = self.subprocesspart_set.all()    
		
		return subprocessPartSet.order_by( Case( 
                                When ( subProcessName ="Initialisation", then=Value(0) ),
                                When ( subProcessName ="Material loaded in machine", then=Value(1)  ),
                                When ( subProcessName ="Platten at initial location", then=Value(2) ),
                                When ( subProcessName ="Material and Tool Inside Press", then=Value(3) ),
                                When ( subProcessName ="Material Pressed", then=Value(4) ),
                                When ( subProcessName ="Material Released from Tool", then=Value(5) ),
                                When ( subProcessName ="Machine Returns To Initial Locations", then=Value(6) ),
                                When ( subProcessName ="Removal End effector actuated", then=Value(7) ),
                                When ( subProcessName ="Preform leaves Tool", then=Value(8) ),
                                When ( subProcessName ="Final Inspection", then=Value(9) ),
                                default = Value(0)
                                    )
                                )
	

	def order_subprocesspart_custom(self):
		subprocessPartSet = self.subprocesspart_set.all() 
		return subprocessPartSet.order_by( Case( 
                                When ( position = 0, then=Value(0) ),
                                When ( position = 1, then=Value(1)  ),
                                When ( position = 2,then=Value(2)  ),
                                When ( position = 3, then=Value(3) ),
                                When ( position = 4, then=Value(4) ),
                                When ( position = 5, then=Value(5) ),
                                When ( position = 6, then=Value(6) ),
                                When ( position = 7, then=Value(7) ),
                                When ( position = 8, then=Value(8) ),
                                When ( position = 9, then=Value(9) ),
                                )
		)
	
	
class SubProcessPart(models.Model):
	"""Model to store info about each complete sub process"""
	#standard info
	processPart = models.ForeignKey(ProcessPart,on_delete=models.CASCADE)
	blank = models.ForeignKey(Blank, on_delete=models.CASCADE, null=True)
	ply = models.ForeignKey(Ply, on_delete=models.CASCADE, null=True)
	part = models.ForeignKey(Part, on_delete=models.CASCADE, null = True)
	subProcessName = models.CharField(max_length = 50, null = True)
	date = models.DateField(null=True)
	#VSM values
	operator = models.CharField(max_length=50, null=True)
	labourInput = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
	jobStart = models.DateTimeField(null=True)
	jobEnd = models.DateTimeField(null=True)
	proIntTime = models.DurationField(null=True, default=timedelta(0))
	processTime = models.DurationField(null=True, default=timedelta(0))
	interfaceTime = models.DurationField(null=True, default=timedelta(0))
	cycleTime = models.DurationField(null=True, default=timedelta(0))
	popUpStart = models.DateTimeField(null=True)
	popUpEnd = models.DateTimeField(null=True)
	scrapRate = models.DecimalField(max_digits=3, decimal_places=0, default = 0)
	batchSize = models.DecimalField(max_digits=50, decimal_places=0, default=5)
	wastedTime = models.DurationField(null=True)
	#non-time dependant data 
	power = models.DecimalField(max_digits = 10, decimal_places=3, default = 0)
	status = models.IntegerField(default=0)
	processCheck = models.BooleanField(default=False, null=True)	
	qualityCheck = models.BooleanField(default=False, null=True)
	preTrimWeight = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	postTrimWeight = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	wastedTime = models.DurationField(null=True)	

	CO2 = models.DecimalField(max_digits=50, decimal_places=3, default=0)

	weighPoint = models.BooleanField(default=False)
	finalWeighPoint = models.BooleanField(default=False)

	#Edge detection fields
	image = models.ImageField(upload_to='', null=True)
	file = models.FileField(upload_to='', null=True)
	
	position = models.IntegerField(null=True)
	#Cost Breakdown

	#--Material--#
	materialWastage = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialScrap = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialPart = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialWastageCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialScrapCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialPartCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialSumCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	

	#--Labour--#
	technicianLabour = models.DurationField(null=True, default=timedelta())
	supervisorLabour = models.DurationField(null=True, default=timedelta())
	technicianLabourCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	supervisorLabourCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	labourSumCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	

	#--Utility--#
	powerCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	powerRate = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	#--TotalCost--#
	totalCost = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	partInstance = models.IntegerField(default=None, null = True)
	blankInstance = models.IntegerField(default=None, null= True)
	plyInstance = models.IntegerField(default=None, null= True)

	partTask = models.BooleanField(default=False)
	blankTask = models.BooleanField(default=False)
	plyTask = models.BooleanField(default=False)

	consolidationCheck = models.BooleanField(default=False)

	cycleTimeRatio = models.DecimalField(max_digits=10, decimal_places=3, default = 0)

	materialDensity = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	plySurfaceArea = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	totalSurfaceArea = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	plyPerimeter = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	totalSumOfPerimeter = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	totalSurfaceArea = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	totalOffcutArea = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	powerUsage = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialRateArea = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialRateWeight = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	materialDensity = models.DecimalField(max_digits=10, decimal_places=3, default = 0)
	blankArea = models.DecimalField(max_digits=10, decimal_places=3, default = 0)


	#--methods--#	
	def __str__(self):
		return self.subProcessName

	def updateSubCO2(self):
		#sub process CO2 calculation
		self.CO2 = float(self.power)*float(self.processPart.part.CO2PerPower)
		self.save()
	
	def updateSubCosts(self):
		"""Function to update costs associated with sub process's"""

		#error handling for float divison by zero
		#finding labour costs
		if self.technicianLabour.total_seconds() == 0 or self.processPart.part.techRate == 0:
			self.technicianLabourCost = 0
		else:
			self.technicianLabourCost = self.technicianLabour.total_seconds()/(60*60) * float(self.processPart.part.techRate)
			
		if self.supervisorLabour.total_seconds() == 0 or self.processPart.part.superRate == 0:
			self.supervisorLabourCost = 0
		else:
			self.supervisorLabourCost = self.supervisorLabour.total_seconds()/(60*60) * float(self.processPart.part.superRate)

		#total cost calculations
		self.materialSumCost = float(self.materialWastageCost) + float(self.materialScrapCost) + float(self.materialPartCost)
		self.labourSumCost = self.technicianLabourCost + self.supervisorLabourCost
		self.powerCost = float(self.power) * float(self.processPart.part.powerRate)
		self.totalCost = float(self.powerCost) + float(self.labourSumCost) + float(self.materialSumCost)
		
		if self.processCheck:
			interval = self.processTime.total_seconds()/24*60*60
		else:
			interval = self.interfaceTime.total_seconds()/24*60*60
		

		if float(self.totalCost) == 0 or float(interval) == 0:
			self.cycleCostRatio = 0
		else:
			self.cycleCostRatio = float(self.totalCost)/float(interval)
      
		self.save()

	def updateIntervals(self):
		"""Function to update a process's cycle,interface and process times"""

		#calc total cycle
		totalCycle = self.interfaceTime + self.processTime 
		#assign to model and save
		self.cycleTime = totalCycle
		self.save()

	def mirrorAttributes(self, sub_pro):
		for attr in sub_pro._meta.fields: #iterate through all fields in sub process and mirror them to sub process part
			if attr.name == "processTime" or attr.name == "interfaceTime" or attr.name == "cycleTime" or attr.name == "date" or attr.name == 'process' or attr.name == 'name' or attr.name == 'manualName' or attr.name == 'id'  or attr.name == "startPoint" or attr.name == "repeat":
				pass
			else:
				value = getattr(sub_pro, attr.name)
				setattr(self, attr.name, value)
		self.save()






class SubProcessPartWeights(models.Model):
	"""Model to store weights associated with SubProcessParts"""
	subProPart = models.ForeignKey(SubProcessPart, on_delete=models.CASCADE)
	weight = models.DecimalField(default=0, null=True, decimal_places=4, max_digits=10)
		
	
class SensorData(models.Model):
	"""Model to hold non-time data from sensors"""	
	#standard info
	sensorName = models.CharField(max_length = 30, null = True)
	processPart = models.ForeignKey(ProcessPart, on_delete=models.CASCADE, null=True)
	subProcessPart = models.ForeignKey(SubProcessPart, on_delete=models.CASCADE, null=True)
	status = models.IntegerField(default=0)
	#bounds
	maxTemp = models.IntegerField(default=0, null=True)
	minTemp = models.IntegerField(default=0, null=True)
	maxPressure = models.IntegerField(default=0, null=True)
	minPressure = models.IntegerField(default=0, null=True)
	#non-time dependent data
	distance = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	posCheck = models.BooleanField(default=False, null=True)
	actualWeight = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	thickness = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	partPresent = models.BooleanField(default=False, null=True)
	partDimX = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	partDimY = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	encoderPos = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	timerCheck = models.BooleanField(default=False, null=True)
	serviceDate = models.DateTimeField(null=True)
	contactNum = PhoneNumberField(null=True, unique=True)
	dateInstalled = models.DateTimeField(null=True)
	modelID = models.CharField(max_length=50, null=True)
	warrentExp = models.DateTimeField(null=True)
	

	def mirrorSensorAttributes(self, sensor):
		for attr in sensor._meta.fields: #iterate through all sensor fields and mirror them to sensordata fields
			if attr.name == "id" or attr.name == "sensorName" or attr.name == "subProcessPart" or attr.name == "processPart" or attr.name == "status":
				pass
			else:
				value = getattr(sensor, attr.name)
				setattr(self, attr.name, value)
		self.save()

		for sensortime in sensor.sensortime_set.all():
			sensorTimeData= self.sensortimedata_set.create()
			for attr in sensortime._meta.fields: #iterate through all sensortime fields and mirror to sensortimedata fields
				if attr.name == "sensorData" or attr.name == "id":
					pass
				else:
					value = getattr(sensortime, attr.name)
					setattr(sensorTimeData, attr.name, value)

		sensor.sensortime_set.all().delete()
		sensor.save()
	
class SensorTimeData(models.Model):
	"""Model to hold time data from sensors"""
	#standard info
	sensorData = models.ForeignKey(SensorData, on_delete=models.CASCADE, null = True)
	time = models.DateTimeField(null=True)
	#time dependant data
	temp = models.DecimalField(max_digits=10,decimal_places=3,null=True)
	pressure = models.DecimalField(max_digits=10,decimal_places=3,null=True)
	noise = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	energy = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	VOC = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	dust = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	torque = models.DecimalField(max_digits = 10, decimal_places=3, null=True)
	acceleration = models.DecimalField(max_digits = 10, decimal_places=3, null=True) 
	