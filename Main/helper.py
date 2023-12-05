
from datetime import datetime,date,time,timedelta
from django.db.models import Case, When, Value
from django.contrib.auth.models import User

#HELPER FUNCTIONS
"""
def updateIntervals(process):
	Function to update a process's cycle,interface and process times
	#setup
	totalInterface = timedelta()
	totalProcess = timedelta()
	totalCycle = timedelta()
	totalTechLabour = timedelta()
	totalSuperLabour = timedelta()
	#cycle sub process's to find total interface and process times
	for subPro in process.subprocess_set.all():
		totalInterface += subPro.interfaceTime
		totalProcess += subPro.processTime
		totalTechLabour += subPro.technicianLabour
		totalSuperLabour += subPro.supervisorLabour
	
	#calc total cycle
	totalCycle = totalInterface + totalProcess	
	
	#assign to model and save
	process.interfaceTime = totalInterface
	process.processTime = totalProcess
	process.cycle = totalCycle
	process.technicianLabour = totalTechLabour
	process.supervisorLabour = totalSuperLabour
	process.save()
	
	
def updateSubIntervals(sub_pro):
	Function to update the sub process's interface or process times
	user = User.objects.get(username=sub_pro.operator)
		  
	if (sub_pro.jobStart is not None) and (sub_pro.jobEnd is not None):
		#the tz replace was originally executed when input read in but did not work
		interval = sub_pro.jobEnd.replace(tzinfo=None) - sub_pro.jobStart.replace(tzinfo=None)
		
		if sub_pro.processCheck:
			sub_pro.processTime = interval
		else:
			sub_pro.interfaceTime = interval

		if user.groups.filter(name='Supervisor').exists():
			interval = timedelta(seconds=int((int(sub_pro.labourInput)/100) * float(interval.total_seconds())))		
			sub_pro.supervisorLabour = interval
			sub_pro.technicianLabour = timedelta()	
		else:
			interval = timedelta(seconds=int((int(sub_pro.labourInput)/100) * float(interval.total_seconds())))
			sub_pro.technicianLabour = interval
			sub_pro.supervisorLabour = timedelta()
		
		sub_pro.save()
		updateIntervals(sub_pro.process)
	
	
		
def temp(pro):
	Function to update the sub process's interface or process times FOR SHELL USE ONLY
	for sub_pro in pro.subprocess_set.all(): 
		if sub_pro.processCheck:
			if (sub_pro.jobStart is not None) and (sub_pro.jobEnd is not None):
				#the tz replace was originally executed when input read in but did not work
				sub_pro.processTime = sub_pro.jobEnd.replace(tzinfo=None) - sub_pro.jobStart.replace(tzinfo=None)
				sub_pro.save()
				updateIntervals(sub_pro.process)
		else:
			if (sub_pro.jobStart is not None) and (sub_pro.jobEnd is not None):
				#the tz replace was originally executed when input read in but did not work
				sub_pro.interfaceTime = sub_pro.jobEnd.replace(tzinfo=None) - sub_pro.jobStart.replace(tzinfo=None)
				sub_pro.save()
				updateIntervals(sub_pro.process)


	
def updateProcessStartEnd(process):
	Function to update a process's start and end times
	#setup	
	endList = []
	startList = []

	for subPro in process.subprocess_set.all():
		if subPro.jobStart is not None:
			startList.append(subPro.jobStart)
		if subPro.jobEnd is not None:
			endList.append(subPro.jobEnd)
	
	#find min time in start list and assign 
	if len(startList) != 0: 	
		process.jobStart = min(startList)
	#find max time in end list and assign
	if len(endList) != 0:	
		process.jobEnd = max(endList)
	#save
	process.save()
	
def updateBatchSize(process):
	Function to update a process batch range
	#setup	
	batchList = []
	
	#get list of all batch sizes
	for subPro in process.subprocess_set.all():
		batchList.append(subPro.batchSize)
	
	#assign to model and save
	process.minBatchSize = min(batchList)
	process.maxBatchSize = max(batchList)
	process.save()
	
def updateScrapRate(process):
	Function to update a process scrap value
	#setup	
	scrapList = []
	#create list of all scrap rates
	for subPro in process.subprocess_set.all():
		scrapList.append(subPro.scrapRate)
	
	#find average scrap assign and save
	process.scrapRate = sum(scrapList)/len(scrapList)
	process.save()
	
def updateLabourInput(process):
	Function to update a process labour input
	#setups
	labourList = []
	#create list of all labour inputs
	for subPro in process.subprocess_set.all():
		if subPro.labourInput is not None:
			labourList.append(subPro.labourInput)
	
	#calc average labour assign and save
	process.labourInput = sum(labourList)/len(labourList)
	process.save()


def updatePowerCon(process):
	Function To update the power value of a given process by summing
	 all related sub-process power values
	#setup
	powerList = []
	#get all power values
	for subPro in process.subprocess_set.all():
		if subPro.power is not None:
			powerList.append(subPro.power)
	
	#calc average and assign
	process.power = sum(powerList)
	process.save()

def updateSubCosts(subPro):
	Function to update costs associated with sub process's
	subPro.technicianLabourCost = subPro.technicianLabour.total_seconds()/(60*60) * float(subPro.process.project.techRate)
	subPro.supervisorLabourCost = subPro.supervisorLabour.total_seconds()/(60*60) * float(subPro.process.project.superRate)
	subPro.labourSumCost = subPro.technicianLabourCost + subPro.supervisorLabourCost
	subPro.save()
		
	
def updateProcessCosts(process):
	Function to update costs associated with process's
	totalTechLabour = timedelta()
	totalSuperLabour = timedelta()
	totalTechLabourCost = 0
	totalSuperLabourCost = 0
	totalLabourCost = 0
	
	for subProcess in process.subprocess_set.all():
		totalTechLabour += subProcess.technicianLabour
		totalSuperLabour += subProcess.supervisorLabour
		totalTechLabourCost += subProcess.technicianLabourCost
		totalSuperLabourCost += subProcess.supervisorLabourCost
		totalLabourCost += subProcess.labourSumCost
		
	process.technicainLabour = totalTechLabour
	process.supervisorLabour = totalSuperLabour
	process.technicainLabourCost = totalTechLabourCost
	process.supervisorLabourCost = totalSuperLabourCost
	process.labourSumCost = totalLabourCost
	process.save()
	
	
def updateMaterialCosts(process):
	Update project costs
	totalMaterialWastage = 0
	totalMaterialScrap = 0	
	
	for subPro in process:
		totalMaterialWastage += subPro.materialWastage
		totalMaterialScrap += subPro.materialScrap
		
	process.materialWastage = totalMaterialWastage
	process.materialScrap = totalMaterialScrap
	process.save()  
		
	
def updateProjectMaterialCosts(project):
	
	totalMaterialWastage = 0
	totalMaterialScrap = 0	
	
	for process in project:
		totalMaterialWastage += process.materialWastage
		totalMaterialScrap += process.materialScrap
		
	project.materialWastage = totalMaterialWastage
	project.materialScrap = totalMaterialScrap
	project.save()  

def updateCosts(process):
	process.totalCost = 0
	process.labourSumCost = 0
	process.materialSumCost = 0
	process.materialWastage = 0
	process.materialScrap = 0
	process.materialPart = 0
	process.technicianLabour = 0
	process.supervisorLabour = 0
	process.powerCost = 0 
	process.CO2 = 0

	project = process.project 

	project.labourCost = 0
	project.materialCost = 0
	project.powerCost = 0
	project.totalCost = 0

	
	for subprocess in process.subprocess_set.all():
		subprocess.totalCost = subprocess.technicianLabour + subprocess.supervisorLabour + subprocess.materialWastage + subprocess.materialScrap + subprocess.materialPart + subprocess.powerCost
		subprocess.save()
		#main process 
		process.materialWastage = process.materialWastage + subprocess.materialWastage
		process.materialScrap = process.materialScrap + subprocess.materialScrap
		process.materialPart = process.materialPart + subprocess.materialPart

		process.technicianLabour = process.technicianLabour + subprocess.technicianLabour
		process.supervisorLabour = process.supervisorLabour + subprocess.supervisorLabour

		process.powerCost = process.powerCost + subprocess.powerCost
		process.CO2 = process.CO2 + subprocess.CO2

	process.materialSumCost = process.materialWastage + process.materialScrap + process.materialPart 
	process.labourSumCost = process.technicianLabour + process.supervisorLabour 

	process.totalCost = process.materialSumCost + process.labourSumCost + process.powerCost
	process.save()

	#add all process costs to project
	for pro in project.process_set.all():
		project.labourCost = project.labourCost + pro.labourSumCost
		project.materialCost = project.materialCost + pro.materialSumCost
		project.powerCost = project.powerCost + pro.powerCost
		project.save()

	project.totalCost = project.labourCost + project.materialCost + project.powerCost
	project.save()

def order_process(project):
	processSet = project.process_set.all()
	return processSet.order_by( Case( 
							When ( name ="Incoming Goods", then=Value(0) ),
							When ( name ="Store Material", then=Value(1)  ),
							When ( name ="Move Material to Ply Cutting", then=Value(2) ),
							When ( name ="Cut Plies", then=Value(3) ),
							When ( name ="Inspect Plies", then=Value(4) ),
							When ( name ="Sort Plies", then=Value(5) ),
							When ( name ="Create Stabilised Blanks", then=Value(6) ),
							When ( name ="Form Preform", then=Value(7) ),
							default = Value(0)
								)
							)
						

def order_subprocess(process):
	
	subprocessSet = process.subprocess_set.all()	
	return subprocessSet.order_by( Case( 
							When ( name ="Initialisation", then=Value(0) ),
							When ( name ="Material loaded in machine", then=Value(1)  ),
							When ( name ="Platten at initial location", then=Value(2) ),
							When ( name ="Material and Tool Inside Press", then=Value(3) ),
							When ( name ="Material Pressed", then=Value(4) ),
							When ( name ="Material Released from Tool", then=Value(5) ),
							When ( name ="Machine Returns To Initial Locations", then=Value(6) ),
							When ( name ="Removal End effector actuated", then=Value(7) ),
							When ( name ="Preform leaves Tool", then=Value(8) ),
							When ( name ="Final Inspection", then=Value(9) ),
							default = Value(0)
								)
							)
			
#CUSTOM ERRORS

class Error(Exception):
	Base error class
	pass
class TimeAttributeIsNone(Error):
	Error for if submitted part is missing attributes
	pass

"""