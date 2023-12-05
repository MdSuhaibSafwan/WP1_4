from django.db import models

METRIC_CHOICES = [
	('','Choose a Metric'),
	('CYT','Cycle Time'),
	('PRT','Process Time'),
	('INT','Interface Time'),
	('SCR','Scrap Rate'),
	('TLR','Technician Labour'),
	('SLR','Supervisor Labour'),
	('PWC','Power consumption'),
]

metric_dict = {
	'':'Choose a Metric',
	'CYT':'cycleTime',
	'PRT':'processTime',
	'INT':'interfaceTime',
	'SCR':'scrapRate',
	'TLR':'technicianLabour',
	'SLR':'supervisorLabour',
	'PWC':'power',
}

OEE_CHOICES = [
	    ("PDT",	'Planned Down Time'),
	    ("TCT",	'Theoretical Cycle Time'),

]

oee_choices_dict = {
	    'TCT':'theoreticalCycleTime',
	    'PDT':'plannedDownTime',
	
}